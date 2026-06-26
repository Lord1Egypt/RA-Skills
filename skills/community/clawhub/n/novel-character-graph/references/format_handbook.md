# 小说格式处理手册

## 编码问题终极解决方案

### 中文小说编码问题诊断

99%的中文TXT小说编码问题：
- 老小说：GBK / GB18030 编码（起点/纵横等老站）
- 新小说：UTF-8 编码
- 台湾小说：BIG5 编码

### 批量编码转换脚本

```bash
# 批量转换GBK→UTF-8
for f in *.txt; do
    iconv -f GBK -t UTF-8 "$f" -o "${f%.txt}_utf8.txt" 2>/dev/null && mv "${f%.txt}_utf8.txt" "$f" && echo "OK: $f" || echo "FAIL: $f"
done
```

---

## 各格式转换工具安装

### EPUB/MOBI 处理

```bash
# Debian/Ubuntu
sudo apt install calibre-bin poppler-utils pandoc

# 转换命令
ebook-convert novel.epub novel.txt
ebook-convert novel.mobi novel.txt
```

### PDF 处理

```bash
# 最佳文本提取工具
pdftotext -layout novel.pdf output.txt
pdftotext -f 10 -l 100 novel.pdf output.txt  # 指定页码范围
```

### DOCX 处理

```bash
pandoc -s novel.docx -o output.txt
```

---

## 大文件分段Shell脚本

```bash
#!/bin/bash
# split_novel.sh - 智能分段脚本

FILE=$1
LINES_PER_CHUNK=500
TOTAL_LINES=$(wc -l < "$FILE")
CHUNKS=$(( (TOTAL_LINES + LINES_PER_CHUNK - 1) / LINES_PER_CHUNK ))

echo "Total: $TOTAL_LINES lines, split into $CHUNKS chunks"

for i in $(seq 1 $CHUNKS); do
    START=$(( (i-1) * LINES_PER_CHUNK + 1 ))
    echo "=== Chunk $i / $CHUNKS (lines $START - $((START + LINES_PER_CHUNK - 1))) ==="
    cat "$FILE" | tail -n +$START | head -n $LINES_PER_CHUNK
done
```
