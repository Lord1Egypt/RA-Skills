---
name: j
description: Short alias skill for joining, merging, or combining files, data, or strings. Use when you need to concatenate or merge content from multiple sources.
---

# j（Join 简写）

这是一个快速"合并" Skill，用字母 **j** 触发。用于拼接文件、合并数据、连接字符串，让分散的内容重新组合。

---

## 适用场景

当你说：
- "合并这两个文件"
- "把多行合并成一行"
- "join these csv files"
- "concatenate files"
- "combine strings"
- "merge JSON files"

---

## 文件合并

**cat（拼接）**
```bash
cat file1.txt file2.txt > combined.txt  # 合并两个文件
cat *.log > all.log                     # 合并所有log
cat part* > full.txt                    # 合并part开头的文件
```

**paste（列合并）**
```bash
paste file1.txt file2.txt              # 按列合并
paste -d ',' file1.txt file2.txt      # 指定分隔符
paste -s file.txt                      # 行转列（单行输出）
```

**awk高级合并**
```bash
awk 'FNR==NR{a[$1]=$2;next}{print $0,a[$1]}' file1 file2  # 基于字段合并
join file1 file2                       # 基于共同字段连接（需排序）
join -t $'\t' -1 1 -2 1 file1 file2  # 指定分隔符和字段
```

---

## 文本合并

**行转列**
```bash
# 多行变单行（空格分隔）
cat file.txt | tr '\n' ' '

# 逗号分隔
paste -sd ',' file.txt

# 不同分隔符
sed ':a;N;$!ba;s/\n/ /g' file.txt
```

**去重合并**
```bash
cat file1.txt file2.txt | sort | uniq > merged.txt
cat file*.txt | sort -u > unique.txt
```

---

## JSON合并

**jq工具**
```bash
# 合并两个JSON数组
jq -s 'add' file1.json file2.json

# 合并对象（深合并）
jq -s 'reduce .[] as $item ({}; . * $item)' file1.json file2.json

# 合并数组到对象（按key）
jq -s 'from_entries' file1.json file2.json
```

**Node.js脚本**
```javascript
// merge.js
const fs = require('fs');
const files = process.argv.slice(2);
const result = files.map(f => JSON.parse(fs.readFileSync(f, 'utf8')));
console.log(JSON.stringify(result, null, 2));
```
```bash
node merge.js file1.json file2.json
```

---

## CSV/TSV处理

```bash
# 合并CSV（跳过header）
tail -q -n +2 file1.csv file2.csv > combined.csv

# 垂直合并（相同列结构）
csvstack file1.csv file2.csv > merged.csv

# 水平合并（相同行数）
csvjoin -c id file1.csv file2.csv > merged.csv
```

---

## 代码文件合并

```bash
# 合并多个JS文件（加注释分隔）
for f in *.js; do echo "// === $f ===" >> bundle.js; cat "$f" >> bundle.js; done

# 压缩合并（去除空行和注释）
cat *.js | sed '/^\s*\/\//d' | sed '/^\s*$/d' > bundle.min.js

# 按字母顺序
ls *.js | sort | xargs cat > bundle.js
```

---

## URL/参数合并

**bash参数处理**
```bash
# 合并数组
array=($(cat list.txt))
merged="${array[@]}"

# 合并多行参数
params=$(cat params.txt | tr '\n' '&')
```

**构建请求体**
```bash
# 合并JSON参数
jq -n --arg a "$(cat a.json)" --arg b "$(cat b.json)" '{a:$a, b:$b}'
```

---

## 技巧与陷阱

**保持顺序**
```bash
# 按文件名顺序合并
ls -1v *.txt | xargs cat > merged.txt  # -v: 自然排序
```

**大文件处理**
```bash
# 流式合并（内存友好）
cat large1.txt large2.txt | gzip > merged.gz
```

**编码问题**
```bash
# 统一编码为UTF-8
iconv -f GBK -t UTF-8 file.txt > file_utf8.txt
cat *.txt | iconv -f GBK -t UTF-8 > merged.txt
```

---

## 实用单行

```bash
# 合并所有Markdown为PDF（需pandoc）
pandoc *.md -o combined.md

# 合并日志并按时间排序（按文件名）
ls -t *.log | xargs cat > chrono.log

# 合并并统计总行数
cat *.txt | wc -l
```

---

> j 技能帮你无缝衔接碎片化的内容。记住：合并前先备份，合并后做验证！
