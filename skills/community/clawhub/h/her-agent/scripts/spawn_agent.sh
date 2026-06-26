#!/bin/bash
# Her-Agent 子 Agent 召唤脚本
# 用于召唤 Code Agent、Research Agent 等

WORKSPACE="/Users/wenvis/.openclaw/workspace"
HER_AGENT_DIR="$WORKSPACE/skills/her-agent/memory/her-agent"

AGENT_TYPE="${1:-codex}"
TASK="${2:-分析当前项目结构}"

echo "[Her-Agent] Spawning sub-agent: $AGENT_TYPE"
echo "[Her-Agent] Task: $TASK"

case "$AGENT_TYPE" in
    codex)
        echo "[Her-Agent] Would spawn Code Agent for: $TASK"
        echo "[Note] Use sessions_spawn with runtime=acp in OpenClaw"
        ;;
    research)
        echo "[Her-Agent] Would spawn Research Agent for: $TASK"
        ;;
    coding)
        echo "[Her-Agent] Would spawn Coding Agent for: $TASK"
        ;;
    *)
        echo "[Her-Agent] Unknown agent type: $AGENT_TYPE"
        ;;
esac

echo "[Her-Agent] Sub-agent spawn configuration ready"
