#!/bin/bash
# install-all-agents.sh — 为所有 Agent 激活知识库
# 管理员用：一次性为所有企微 Agent 初始化知识库

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"
AGENTS_DIR="$HOME/.openclaw/agents"

echo "🚀 批量激活 huo15-knowledge-base"
echo ""

# 收集所有 agent
AGENTS=$(find "$AGENTS_DIR" -mindepth 1 -maxdepth 1 -type d | grep -v ".git" | sort)

AGENT_COUNT=$(echo "$AGENTS" | wc -l | tr -d ' ')
echo "找到 $AGENT_COUNT 个 Agent"

echo ""
for agent_path in $AGENTS; do
  agent_name=$(basename "$agent_path")
  agent_work_dir="$agent_path/agent"
  
  # 确保 agent 工作目录存在
  mkdir -p "$agent_work_dir"
  
  # 设置 KB 目录
  KB_DATA_DIR="$agent_work_dir/kb"
  
  if [ -d "$KB_DATA_DIR" ]; then
    echo "⏭️  [$agent_name] 已激活，跳过"
    continue
  fi
  
  echo "📦 [$agent_name] 激活中..."
  
  # 创建目录
  mkdir -p "$KB_DATA_DIR/raw"
  mkdir -p "$KB_DATA_DIR/wiki"
  mkdir -p "$KB_DATA_DIR/wiki/_index"
  mkdir -p "$KB_DATA_DIR/cache"
  
  # 创建配置
  cat > "$KB_DATA_DIR/config.json" << CONFIG_EOF
{
  "version": "0.1.0",
  "agent_id": "$agent_name",
  "agent_context": "$agent_work_dir",
  "paths": {
    "raw": "$KB_DATA_DIR/raw",
    "wiki": "$KB_DATA_DIR/wiki",
    "cache": "$KB_DATA_DIR/cache"
  }
}
CONFIG_EOF
  
  # 创建初始索引
  cat > "$KB_DATA_DIR/wiki/index.md" << 'WIKI_INDEX'
---
title: 知识库索引
last_compiled: never
---

# 知识库

> Agent 专属知识库

尚未编译任何文档。
WIKI_INDEX
  
  echo "   ✅ [$agent_name] 激活完成"
done

echo ""
echo "✅ 批量激活完成！"
echo ""
echo "各 Agent 数据目录："
find "$AGENTS_DIR" -path "*/agent/kb/config.json" -exec dirname {} \; 2>/dev/null | while read -r kb_dir; do
  agent=$(echo "$kb_dir" | sed "s|$AGENTS_DIR/||" | sed 's|/agent/kb||')
  echo "  - $agent: $kb_dir"
done
