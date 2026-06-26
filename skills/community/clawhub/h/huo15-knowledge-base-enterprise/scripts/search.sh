#!/bin/bash
# search.sh — 搜索知识库
# 用法: ./search.sh "query" [--format json|markdown]

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
KB_ROOT="$(dirname "$SCRIPT_DIR")"
WIKI_DIR="$KB_ROOT/wiki"

FORMAT="markdown"
QUERY=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --format)
      FORMAT="$2"
      shift 2
      ;;
    -q)
      QUERY="$2"
      shift 2
      ;;
    *)
      if [ -z "$QUERY" ]; then
        QUERY="$1"
      fi
      shift
      ;;
  esac
done

if [ -z "$QUERY" ]; then
  echo "用法: search.sh '搜索关键词' [--format json|markdown]"
  exit 1
fi

echo "🔍 搜索: $QUERY"

# 检查 wiki 目录
if [ ! -d "$WIKI_DIR" ]; then
  echo "⚠️  wiki/ 目录不存在，请先初始化和编译"
  exit 1
fi

# 简单 grep 搜索
echo ""
echo "📂 在 wiki/ 中搜索..."

RESULTS=$(grep -l -i "$QUERY" "$WIKI_DIR"/*.md "$WIKI_DIR"/**/*.md 2>/dev/null || true)

if [ -z "$RESULTS" ]; then
  echo "未找到相关内容"
  exit 0
fi

RESULT_COUNT=$(echo "$RESULTS" | wc -l | tr -d ' ')
echo "找到 $RESULT_COUNT 个相关条目:"
echo ""

# 显示结果
if [ "$FORMAT" = "json" ]; then
  echo "{"
  echo "  \"query\": \"$QUERY\","
  echo "  \"results\": ["
  first=true
  while IFS= read -r file; do
    if [ "$first" = true ]; then
      first=false
    else
      echo ","
    fi
    title=$(grep -m1 "^# " "$file" | sed 's/^# //' || basename "$file")
    echo "    {\"path\": \"$file\", \"title\": \"$title\"}"
  done <<< "$RESULTS"
  echo ""
  echo "  ]"
  echo "}"
else
  while IFS= read -r file; do
    title=$(grep -m1 "^# " "$file" | sed 's/^# //' || basename "$file")
    echo "📄 $title"
    echo "   $file"
    
    # 显示匹配片段
    snippet=$(grep -i -m1 "$QUERY" "$file" | head -c 200)
    if [ -n "$snippet" ]; then
      echo "   → $snippet..."
    fi
    echo ""
  done <<< "$RESULTS"
fi
