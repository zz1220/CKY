import nltk
from nltk.tokenize import TweetTokenizer
from math import log
import copy
import sys

# file = 'documentcky.txt'
# sentence = "The flights include a meal"

file = sys.argv[1]
sentence = sys.argv[2]

tknzr = TweetTokenizer()
t = tknzr.tokenize(sentence)
mystc = []
for i in range(0,len(t)):
    s = t[i]
    s = s.lower()
    mystc.append(str(s))

with open(file) as f:
    getgrammer = f.readlines()

grammer = {}
temp = []
word = {}
s = ""
binary = 1
for i in range(0,len(getgrammer)):
    n = getgrammer[i]
    line = n.rstrip('\n').split(' ')
    temp = line
    for k in range(0,len(temp)):
        temp[k] = temp[k].replace('-','')
    a = str.isalpha(temp[0])
    if not a:
        text = temp[0][1:-1]
        s = ""
        count = 0
        for m in range(1,len(temp)):
            if temp[m] != '->' and temp[m] != '>':
                if count == 0:
                    s = s + temp[m]
                    count+=1
                else:
                    s = " ".join((s,temp[m]))
                    count+=1

        if count == 4:                           #binarization
            n = s.rstrip('\n').split(' ')
            subname = " ".join((n[2],n[3]))
            sub = "".join(("x",str(binary)))
            subname = " ".join((sub,subname))
            name = " ".join((n[0],n[1]))
            nameneed = " ".join((n[1], name))
            binary+=1
            grammer[nameneed] = text
            grammer[subname] = 1
        else:
            grammer[s] = text
    else:                                      #the second part is in another dict
        for j in range(1,len(temp)):
            b = str.isalpha(temp[j])
            if temp[j] != '->' and temp[j] != '|' and b:
                com = " ".join((temp[0], temp[j]))
                num = temp[j+1]
                num = num[1:-1]
                word[com] = num

print grammer
print word
print mystc
for i in word:
    grammer[i] = word[i]

#cky
store_table = {}
callback = {}
count1 = 0
path  = {}
probability_table = {}
for i in probability_table:
    probability_table[i] = {}
    for j in probability_table[i]:
        probability_table[i][j] = {}

def count_initial(grammer,store_table,s,word,theword):
    for search_the_word_ingrammer in grammer:
        s2 = search_the_word_ingrammer.rstrip('').split(' ')
        if len(s2) == 2 and s[0] == s2[1]:
            ss = " ".join((s2[0], search))
            ss2 = ss.rstrip('').split(' ')
            store_table[i][i].append(ss)
            if ss not in word.keys():
                word[ss] = float(grammer[search_the_word_ingrammer]) * float(grammer[theword])
            count_initial(grammer,store_table,ss2,word,search_the_word_ingrammer)
    return store_table

def comparision(index_for_left1,index_for_left2,index_for_down1,index_for_down2,mytable,grammer,level,outlevel, callback):
    left = mytable[index_for_left1][index_for_left2]
    down = mytable[index_for_down1][index_for_down2]

    try:
        if down != 'None' and left != 'None':
            setting = False
            for word_index1 in range(len(left)):
                grammer_word = left[word_index1]
                grammer_word_split = grammer_word.rstrip('').split(' ')
                for word_index2 in range(len(down)):
                    grammer_word2 = down[word_index2]
                    grammer_word_split2 = grammer_word2.rstrip('').split(' ')
                    the_first_element_add = " ".join((grammer_word_split[0], grammer_word_split2[0]))
                    for search_grammer in grammer.keys():
                        temp_search = search_grammer.rstrip('').split(' ')
                        if len(temp_search) == 3:
                            search_grammer_add = " ".join((temp_search[1], temp_search[2]))
                            if the_first_element_add == search_grammer_add:
                                if mytable[index_for_left1][index_for_left2 + level] == 'None':
                                   mytable[index_for_left1][index_for_left2 + level] = []
                                callback[index_for_left1][index_for_left2 + level].append((index_for_left1,index_for_left2,index_for_down1,index_for_down2))
                                mytable[index_for_left1][index_for_left2 + level].append(search_grammer)
                                setting = True
                    if not setting and len(mytable[index_for_left1][index_for_left2 + level]) == 0:
                        mytable[index_for_left1][index_for_left2 + level] = "None"
        else:
            if len(mytable[index_for_left1][index_for_left2 + level]) == 0:
                mytable[index_for_left1][index_for_left2 + level] = "None"
    except TypeError:
        pass
    return mytable,callback

for i in range(0,len(mystc)):
    store_table[i] = {}
    callback[i] = {}
    for j in range(count1,len(mystc)):
        store_table[i][j] = []
        callback[i][j] = []
    count1 += 1

for i in range(0,len(store_table)):
    search = mystc[i]
    s = []
    word_len = len(word.keys())
    for word_idx in range(word_len):
        search_the_word = word.keys()[word_idx]
        s = search_the_word.rstrip('').split(' ')
        for wordneed in range(len(s)):
            if search == s[wordneed]:
                store_table[i][i].append(search_the_word)
                store_table = count_initial(grammer,store_table,s,word,search_the_word)

for level in range(1,len(mystc)):
    for i in range(0, len(mystc) - level):
        j = i + level
        cc = 0
        for split in range(i, j):
            number  = level - cc
            store_table, callback = comparision(i, split, 1 + split, j, store_table, grammer, number, level, callback)
            cc += 1

# parse


applied_rules = []
applied_cur_rule = set()
checker = set()

def parse(i, j, tag):
    if i == j:
        for ind in range(len(store_table[i][j])):
            labels = store_table[i][j][ind].split()
            if labels[0] == tag:
                applied_cur_rule.add(store_table[i][j][ind])
                if j == len(mystc) - 1:
                    result = copy.deepcopy(sorted(applied_cur_rule))
                    if "_".join(result) not in checker:
                        applied_rules.append(result)
                        checker.add("_".join(result))
                return True
            else:
                continue
    callback_start_quads = callback[i][j]
    for ind in range(len(callback_start_quads)):
        callback_start_quad = callback_start_quads[ind]
        applied_cur_rule.add(store_table[i][j][ind])
        labels = store_table[i][j][ind].split()
        if labels[0] != tag:
            applied_cur_rule.remove(store_table[i][j][ind])
            continue
        flag_left = parse(callback_start_quad[0], callback_start_quad[1], labels[1])
        if not flag_left:
            applied_cur_rule.remove(store_table[i][j][ind])
            continue
        flag_right = parse(callback_start_quad[2], callback_start_quad[3], labels[2])
        if not flag_right:
            applied_cur_rule.remove(store_table[i][j][ind])
            continue
        applied_cur_rule.remove(store_table[i][j][ind])

    return True


parse(0, len(mystc) - 1, "S")

print(applied_rules)

#calculate the probability
score = 1.0
for applied_rule in applied_rules:
    for rule in applied_rule:
        type = len(rule.split())
        if type == 2:
            score *= float(word[rule])
        elif type == 3:
            score *= float(grammer[rule])
    print("probability is [",sentence,"] is ", str(score))
