#!/bin/bash
# index.sh — 生成 wiki 索引

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
KB_ROOT="$(dirname "$SCRIPT_DIR")"
WIKI_DIR="$KB_ROOT/wiki"

echo "📋 生成知识库索引..."

# 按类型分类
echo "📂 扫描 wiki 条目..."

# 创建类型索引目录
mkdir -p "$WIKI_DIR/_index"

# 收集所有条目
ALL_ENTRIES=$(find "$WIKI_DIR" -maxdepth 1 -name "*.md" ! -name "index.md" | sort)

if [ -z "$ALL_ENTRIES" ]; then
  echo "⚠️  未找到任何 wiki 条目"
  exit 1
fi

# 生成 papers 索引
> "$WIKI_DIR/_index/papers.md"
echo "# 论文索引" >> "$WIKI_DIR/_index/papers.md"
echo "" >> "$WIKI_DIR/_index/papers.md"
while IFS= read -r entry; do
  if grep -q "type: paper" "$entry" 2>/dev/null; then
    title=$(grep -m1 "^# " "$entry" | sed 's/^# //')
    echo "- [[$(basename "$entry" .md)|$title]]" >> "$WIKI_DIR/_index/papers.md"
  fi
done <<< "$ALL_ENTRIES"

# 生成 articles 索引
> "$WIKI_DIR/_index/articles.md"
echo "# 文章索引" >> "$WIKI_DIR/_index/articles.md"
echo "" >> "$WIKI_DIR/_index/articles.md"
while IFS= read -r entry; do
  if grep -q "type: article" "$entry" 2>/dev/null; then
    title=$(grep -m1 "^# " "$entry" | sed 's/^# //')
    echo "- [[$(basename "$entry" .md)|$title]]" >> "$WIKI_DIR/_index/articles.md"
  fi
done <<< "$ALL_ENTRIES"

# 生成 notes 索引
> "$WIKI_DIR/_index/notes.md"
echo "# 笔记索引" >> "$WIKI_DIR/_index/notes.md"
echo "" >> "$WIKI_DIR/_index/notes.md"
while IFS= read -r entry; do
  if grep -q "type: note" "$entry" 2>/dev/null; then
    title=$(grep -m1 "^# " "$entry" | sed 's/^# //')
    echo "- [[$(basename "$entry" .md)|$title]]" >> "$WIKI_DIR/_index/notes.md"
  fi
done <<< "$ALL_ENTRIES"

# 更新主索引
cat > "$WIKI_DIR/index.md" << INDEX_EOF
---
title: 知识库索引
last_indexed: DATE_PLACEHOLDER
---

# 知识库

> LLM 编译的结构化百科全书

## 最近更新

- $(date '+%Y-%m-%d') — 索引更新

## 按类型浏览

- [论文](_index/papers.md) — $(grep -c "^-" "$WIKI_DIR/_index/papers.md" 2>/dev/null || echo 0) 篇
- [文章](_index/articles.md) — $(grep -c "^-" "$WIKI_DIR/_index/articles.md" 2>/dev/null || echo 0) 篇
- [笔记](_index/notes.md) — $(grep -c "^-" "$WIKI_DIR/_index/notes.md" 2>/dev/null || echo 0) 条

## 全部条目

INDEX_EOF

while IFS= read -r entry; do
  title=$(grep -m1 "^# " "$entry" | sed 's/^# //')
  basename=$(basename "$entry" .md)
  echo "- [[$basename|$title]]" >> "$WIKI_DIR/index.md"
done <<< "$ALL_ENTRIES"

sed -i '' "s/DATE_PLACEHOLDER/$(date '+%Y-%m-%d %H:%M')/" "$WIKI_DIR/index.md"

echo "✅ 索引生成完成！"
echo ""
echo "生成的文件："
echo "  wiki/index.md           — 主索引"
echo "  wiki/_index/papers.md   — 论文索引"
echo "  wiki/_index/articles.md — 文章索引"
echo "  wiki/_index/notes.md    — 笔记索引"
