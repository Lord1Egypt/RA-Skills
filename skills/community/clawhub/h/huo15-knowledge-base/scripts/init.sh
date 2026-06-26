#!/bin/bash
# init.sh — 初始化 huo15-knowledge-base 目录结构

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
KB_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🔧 初始化知识库: $KB_ROOT"

# 创建目录结构
mkdir -p "$KB_ROOT/raw"
mkdir -p "$KB_ROOT/wiki"
mkdir -p "$KB_ROOT/wiki/_index"
mkdir -p "$KB_ROOT/wiki/_concepts"
mkdir -p "$KB_ROOT/wiki/_papers"
mkdir -p "$KB_ROOT/wiki/_notes"
mkdir -p "$KB_ROOT/cache"

# 创建 .gitkeep 保证空目录可提交
touch "$KB_ROOT/raw/.gitkeep"
touch "$KB_ROOT/wiki/.gitkeep"
touch "$KB_ROOT/cache/.gitkeep"

# 创建初始 index.md
if [ ! -f "$KB_ROOT/wiki/index.md" ]; then
  cat > "$KB_ROOT/wiki/index.md" << 'EOF'
# 知识库索引

> 最后更新: 2026-04-05

## 概念 (Concepts)

## 论文 (Papers)

## 笔记 (Notes)

## 最近更新


EOF
fi

# 创建 config.json（如果不存在）
if [ ! -f "$KB_ROOT/config.json" ]; then
  cp "$KB_ROOT/config.example.json" "$KB_ROOT/config.json" 2>/dev/null || true
fi

echo "✅ 初始化完成！"
echo ""
echo "目录结构："
echo "  raw/       — 原始文档"
echo "  wiki/      — 编译后的百科"
echo "  cache/     — 临时缓存"
echo ""
echo "下一步："
echo "  ./scripts/ingest.sh --url 'https://...'  # 入库文档"
echo "  ./scripts/compile.sh                     # 编译 wiki"
