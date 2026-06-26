#!/bin/bash
# count-chinese-words.sh
# 统计中文字数（排除Markdown标记）

FILE="$1"

if [ -z "$FILE" ]; then
  echo "用法: bash count-chinese-words.sh <文件路径>"
  exit 1
fi

if [ ! -f "$FILE" ]; then
  echo "错误: 文件不存在: $FILE"
  exit 1
fi

# 方法1: 使用grep统计非ASCII字符（中文）
# 排除markdown标记符号
TOTAL_CHARS=$(cat "$FILE" | grep -oP '[\x{4e00}-\x{9fff}]' | wc -l)

# 排除Markdown标题标记
MARKDOWN_LINES=$(cat "$FILE" | grep -E '^(#{1,6}\s|[*\-+]\s|\d+\.\s|> )' | grep -oP '[\x{4e00}-\x{9fff}]' | wc -l)

FINAL_COUNT=$((TOTAL_CHARS - MARKDOWN_LINES))

echo "文件: $FILE"
echo "中文字数: $FINAL_COUNT"

# 输出字数（供脚本调用）
echo "$FINAL_COUNT"
