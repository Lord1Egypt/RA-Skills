#!/bin/bash
# env.sh — 加载知识库环境变量
# 用法: source env.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"

# 检测 Agent 上下文
# AGENT_DIR 应该在 OpenClaw 运行时设置
# 如果没有设置，尝试从路径推断
if [ -z "$AGENT_DIR" ]; then
  # 尝试从当前路径推断
  if [[ "$PWD" =~ agents/([^/]+)/ ]]; then
    AGENT_DIR="$HOME/.openclaw/agents/${BASH_REMATCH[1]}/agent"
  else
    AGENT_DIR="$HOME/.openclaw/agents/main/agent"
  fi
fi

export KB_ROOT="$SKILL_ROOT"
export KB_DATA_DIR="${AGENT_DIR}/kb"
export KB_RAW_DIR="${KB_DATA_DIR}/raw"
export KB_WIKI_DIR="${KB_DATA_DIR}/wiki"
export KB_CACHE_DIR="${KB_DATA_DIR}/cache"

# 添加 skill scripts 到 PATH
export PATH="$SCRIPT_DIR:$PATH"

echo "✅ 知识库环境已加载"
echo "   KB_DATA_DIR: $KB_DATA_DIR"
echo "   KB_RAW_DIR: $KB_RAW_DIR"
echo "   KB_WIKI_DIR: $KB_WIKI_DIR"
