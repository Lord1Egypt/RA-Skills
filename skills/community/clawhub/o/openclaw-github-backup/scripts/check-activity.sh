#!/bin/bash
# 检查 OpenClaw 活跃对话状态
# 返回: active 或 inactive

OPENCLAW_DIR="$HOME/.openclaw"
ACTIVE_THRESHOLD=3600  # 1小时（秒）

# 检查 agents 目录下的会话文件
if [[ -d "$OPENCLAW_DIR/agents" ]]; then
    recent_files=$(find "$OPENCLAW_DIR/agents" -name "*.jsonl" -type f -mmin -$((ACTIVE_THRESHOLD/60)) 2>/dev/null | wc -l)
    
    if [[ $recent_files -gt 0 ]]; then
        echo "active"
        exit 0
    fi
fi

# 检查 workspace 目录下的文件变更
if [[ -d "$OPENCLAW_DIR/workspace" ]]; then
    recent_files=$(find "$OPENCLAW_DIR/workspace" -type f -mmin -$((ACTIVE_THRESHOLD/60)) 2>/dev/null | wc -l)
    
    if [[ $recent_files -gt 0 ]]; then
        echo "active"
        exit 0
    fi
fi

echo "inactive"