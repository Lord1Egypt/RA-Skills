#!/bin/bash
# activate.sh — 为当前 Agent 激活知识库
# 会在 Agent 自己的工作目录下创建 kb/ 子目录，实现数据隔离

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"

# 检测当前 Agent 上下文
# OpenClaw 通过环境变量或 symlink 标识 agent
AGENT_DIR="${AGENT_DIR:-$HOME/.openclaw/agents/main/agent}"
KB_DATA_DIR="${AGENT_DIR}/kb"

echo "🔧 激活 huo15-knowledge-base"
echo "  Agent 目录: $AGENT_DIR"
echo "  知识库目录: $KB_DATA_DIR"

# 创建 Agent 专属数据目录
mkdir -p "$KB_DATA_DIR/raw"
mkdir -p "$KB_DATA_DIR/wiki"
mkdir -p "$KB_DATA_DIR/wiki/_index"
mkdir -p "$KB_DATA_DIR/cache"

# 创建 .gitkeep
touch "$KB_DATA_DIR/raw/.gitkeep"
touch "$KB_DATA_DIR/wiki/.gitkeep"
touch "$KB_DATA_DIR/cache/.gitkeep"

# 生成 Agent 专属配置
cat > "$KB_DATA_DIR/config.json" << CONFIG_EOF
{
  "version": "0.1.0",
  "agent_context": "$AGENT_DIR",
  "paths": {
    "raw": "$KB_DATA_DIR/raw",
    "wiki": "$KB_DATA_DIR/wiki",
    "cache": "$KB_DATA_DIR/cache"
  },
  "llm": {
    "model": "minimax/MiniMax-M2.7",
    "provider": "openclaw"
  }
}
CONFIG_EOF

# 创建索引文件
if [ ! -f "$KB_DATA_DIR/wiki/index.md" ]; then
  cat > "$KB_DATA_DIR/wiki/index.md" << 'WIKI_INDEX'
---
title: 知识库索引
last_compiled: never
---

# 知识库

> Agent 专属知识库 — LLM 编译的结构化百科全书

## 状态

尚未编译任何文档。请先入库：
```bash
kb-ingest --url "https://..."
```

## 最近更新

暂无
WIKI_INDEX
fi

echo ""
echo "✅ 激活完成！"
echo ""
echo "Agent 专属目录："
echo "  $KB_DATA_DIR/raw/       — 原始文档"
echo "  $KB_DATA_DIR/wiki/      — 编译后的百科"
echo "  $KB_DATA_DIR/cache/     — 临时缓存"
echo "  $KB_DATA_DIR/config.json — 配置"
echo ""
echo "下一步："
echo "  kb-ingest --url 'https://...'  # 入库文档"
echo "  kb-compile                      # 编译"
echo ""
echo "快捷命令（需要在 Shell 中 source）："
echo "  source $SKILL_ROOT/scripts/env.sh  # 加载环境变量"
