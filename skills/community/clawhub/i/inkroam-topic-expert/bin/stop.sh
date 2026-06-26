#!/bin/bash
# 选题专家 - 停止守护进程

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PID_FILE="$PROJECT_ROOT/data/topic_expert.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "⚠️  选题专家未运行"
    exit 1
fi

PID=$(cat "$PID_FILE")
echo "🛑 停止选题专家 (PID: $PID)..."
kill $PID 2>/dev/null
rm -f "$PID_FILE"
echo "✅ 已停止"
