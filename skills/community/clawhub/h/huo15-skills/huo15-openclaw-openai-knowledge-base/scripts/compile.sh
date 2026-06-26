#!/bin/bash
# compile.sh — 编译 raw/ → wiki/
# LLM 读取原始文档，生成结构化百科

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
KB_ROOT="$(dirname "$SCRIPT_DIR")"
RAW_DIR="$KB_ROOT/raw"
WIKI_DIR="$KB_ROOT/wiki"
CACHE_DIR="$KB_ROOT/cache"

INCREMENTAL=false

# 解析参数
while [[ $# -gt 0 ]]; do
  case $1 in
    --incremental)
      INCREMENTAL=true
      shift
      ;;
    --help)
      echo "用法: compile.sh [--incremental]"
      echo "  --incremental  仅编译新文档（跳过已编译的）"
      exit 0
      ;;
    *)
      shift
      ;;
  esac
done

echo "📚 知识库编译中..."

# 检查 raw 目录
if [ ! -d "$RAW_DIR" ] || [ -z "$(ls -A "$RAW_DIR" 2>/dev/null)" ]; then
  echo "⚠️  raw/ 目录为空，请先入库文档: ./scripts/ingest.sh"
  exit 1
fi

# 收集所有待编译文档
echo "📂 扫描 raw/ 目录..."
DOCS=$(find "$RAW_DIR" -name "*.md" -o -name "*.txt" | sort)

if [ -z "$DOCS" ]; then
  echo "⚠️  未找到任何文档"
  exit 1
fi

DOC_COUNT=$(echo "$DOCS" | wc -l | tr -d ' ')
echo "  找到 $DOC_COUNT 个文档"

# 构建 LLM prompt
cat > "$CACHE_DIR/compile_prompt.md" << 'PROMPT_EOF'
# 编译任务

你是一个研究图书馆员，负责把收集的原始文档编译成结构化百科。

## 任务

1. 读取以下所有原始文档
2. 为每个文档生成：
   - **摘要**（50字内）
   - **关键概念**（3-5个标签）
   - **百科正文**（整理成 Markdown 格式）
3. 创建**反向链接**（相关条目间互联）
4. 更新 `wiki/index.md` 索引

## 输出格式

为每个文档，在 `wiki/` 下生成一个 `.md` 文件：

```markdown
---
type: paper|article|note
title: 标题
source: 来源
date: 日期
concepts: [概念1, 概念2]
---

# 标题

## 摘要
...

## 核心内容
...

## 相关概念
<!-- links: [[相关条目1]], [[相关条目2]] -->

## 原始出处
[链接](url)
```

## 重要规则

- 所有输出必须是有效的 Markdown
- 使用中文撰写摘要和正文
- 关键概念用 `concepts:` 标签列出
- 相关条目用 `[[条目名]]` 格式创建反向链接
- 不要臆造信息，只基于原文整理

## 开始编译

请读取以下文档并开始编译：
PROMPT_EOF

# 追加文档列表
echo "" >> "$CACHE_DIR/compile_prompt.md"
echo "## 待编译文档" >> "$CACHE_DIR/compile_prompt.md"
echo "" >> "$CACHE_DIR/compile_prompt.md"

while IFS= read -r doc; do
  echo "### $doc" >> "$CACHE_DIR/compile_prompt.md"
  echo '```' >> "$CACHE_DIR/compile_prompt.md"
  cat "$doc" >> "$CACHE_DIR/compile_prompt.md"
  echo '```' >> "$CACHE_DIR/compile_prompt.md"
  echo "" >> "$CACHE_DIR/compile_prompt.md"
done <<< "$DOCS"

# 生成 wiki/index.md 模板
cat > "$WIKI_DIR/index.md" << 'INDEX_EOF'
---
title: 知识库索引
last_compiled: DATE_PLACEHOLDER
---

# 知识库

> LLM 编译的结构化百科全书

## 最近更新


## 概念索引


## 按类型浏览

- [论文](_index/papers.md)
- [文章](_index/articles.md)
- [笔记](_index/notes.md)
INDEX_EOF

sed -i '' "s/DATE_PLACEHOLDER/$(date '+%Y-%m-%d %H:%M')/" "$WIKI_DIR/index.md"

echo ""
echo "📋 编译任务已生成: $CACHE_DIR/compile_prompt.md"
echo ""
echo "⚠️  提示：编译需要 LLM 介入，请通过 OpenClaw 进行下一步："
echo ""
echo "  方案1（推荐）："
echo "    openclaw run 'compile the knowledge base' --context-file $CACHE_DIR/compile_prompt.md"
echo ""
echo "  方案2（手动）："
echo "    阅读 wiki/ 目录结构，手动创建百科条目"
echo ""
echo "✅ 目录结构初始化完成！"
