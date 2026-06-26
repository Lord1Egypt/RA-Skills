#!/bin/bash
# lint.sh — wiki 自愈体检
# LLM 扫描 wiki/ 检查一致性、缺失、矛盾，主动修复

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
KB_ROOT="$(dirname "$SCRIPT_DIR")"
WIKI_DIR="$KB_ROOT/wiki"
CACHE_DIR="$KB_ROOT/cache"

AGGRESSIVE=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --aggressive)
      AGGRESSIVE=true
      shift
      ;;
    --help)
      echo "用法: lint.sh [--aggressive]"
      echo "  --aggressive  深度检查，包括过时内容标记"
      exit 0
      ;;
    *)
      shift
      ;;
  esac
done

echo "🔍 知识库体检中..."

# 检查 wiki 目录
if [ ! -d "$WIKI_DIR" ] || [ -z "$(ls -A "$WIKI_DIR" 2>/dev/null | grep -v '^_')" ]; then
  echo "⚠️  wiki/ 目录为空或不存在，请先编译: ./scripts/compile.sh"
  exit 1
fi

# 收集所有 wiki 条目
echo "📂 扫描 wiki/ 条目..."
ENTRIES=$(find "$WIKI_DIR" -maxdepth 1 -name "*.md" ! -name "index.md" | sort)
ENTRY_COUNT=$(echo "$ENTRIES" | wc -l | tr -d ' ')

if [ -z "$ENTRIES" ]; then
  echo "⚠️  未找到任何 wiki 条目"
  exit 1
fi

echo "  找到 $ENTRY_COUNT 个条目"

# 构建体检 prompt
cat > "$CACHE_DIR/lint_prompt.md" << 'LINT_EOF'
# 知识库体检任务

你是一个 AI 研究图书馆员，负责检查和维护百科全书的健康状态。

## 任务

扫描以下所有 wiki 条目，检查并修复：

### 基础检查
- [ ] 文件格式是否 valid Markdown
- [ ] 每个条目是否有 `type`、`title`、`concepts` 元信息
- [ ] 摘要是否简洁（50字内）

### 链接检查
- [ ] `[[条目名]]` 链接是否都有对应条目
- [ ] 是否有 orphaned 条目（没有被任何条目链接）
- [ ] 反向链接是否完整

### 内容检查
- [ ] 内容是否与元信息一致
- [ ] 关键概念是否准确
- [ ] 是否有矛盾信息

LINT_EOF

if [ "$AGGRESSIVE" = true ]; then
  cat >> "$CACHE_DIR/lint_prompt.md" << 'DEEP_EOF'

### 深度检查（--aggressive）
- [ ] 标记超过 30 天未更新的条目为"可能过时"
- [ ] 检查是否有重复内容
- [ ] 建议可以合并的相似条目
- [ ] 识别知识缺口（相关主题缺失）
DEEP_EOF
fi

cat >> "$CACHE_DIR/lint_prompt.md" << 'LINT_EOF'

## 输出要求

1. 生成 `wiki/_index/health.md` 体检报告
2. 对于可修复的问题，直接修改对应文件
3. 对需要人工确认的问题，在报告中标记 `[NEED_REVIEW]`

## 开始体检

请扫描以下 wiki 条目：
LINT_EOF

while IFS= read -r entry; do
  echo "### $entry" >> "$CACHE_DIR/lint_prompt.md"
  echo '```' >> "$CACHE_DIR/lint_prompt.md"
  cat "$entry" >> "$CACHE_DIR/lint_prompt.md"
  echo '```' >> "$CACHE_DIR/lint_prompt.md"
  echo "" >> "$CACHE_DIR/lint_prompt.md"
done <<< "$ENTRIES"

echo "📋 体检任务已生成: $CACHE_DIR/lint_prompt.md"
echo ""
echo "⚠️  提示：体检需要 LLM 介入，请通过 OpenClaw 进行下一步"
echo ""
echo "  openclaw run 'run knowledge base health check' --context-file $CACHE_DIR/lint_prompt.md"
