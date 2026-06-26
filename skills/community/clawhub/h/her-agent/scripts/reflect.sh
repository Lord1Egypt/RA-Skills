#!/bin/bash
# Her-Agent 自我反思脚本
# 生成周期性自我复盘

WORKSPACE="/Users/wenvis/.openclaw/workspace"
HER_AGENT_DIR="$WORKSPACE/skills/her-agent/memory/her-agent"
DATE=$(date "+%Y-%m-%d %H:%M:%S")

echo "[Her-Agent] Starting self-reflection..."

# 读取当前配置
CONFIG="$HER_AGENT_DIR/config.json"
LEVEL=$(cat "$CONFIG" | grep -o '"level":[^,}]*' | cut -d':' -f2 | tr -d ' "')
XP=$(cat "$CONFIG" | grep -o '"xp":[^,}]*' | cut -d':' -f2 | tr -d ' "')

# 生成反思记录
REFLECTION_FILE="$HER_AGENT_DIR/reflections.jsonl"

echo "{\"timestamp\":\"$DATE\",\"level\":$LEVEL,\"xp\":$XP,\"reflection\":\"自我反思：持续进化中\",\"insights\":[\"保持学习\",\"保持进化\"]}" >> "$REFLECTION_FILE"

echo "[Her-Agent] Reflection recorded at $DATE"
echo "[Her-Agent] Current Level: $LEVEL, XP: $XP"
