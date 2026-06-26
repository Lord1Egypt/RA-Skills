#!/usr/bin/env bash
# extract.sh – 提取 RSS/XML 中的标题（前 10 条）
FILE="$1"
if [[ -z "$FILE" ]]; then
  echo "Usage: $0 <rss-file>"
  exit 1
fi
if [[ ! -f "$FILE" ]]; then
  echo "File not found: $FILE"
  exit 1
fi
# 提取 <title> 内容，去掉标签，限制前 10 行
grep -o '<title>[^<]*' "$FILE" | sed 's/<title>//' | head -n 10
