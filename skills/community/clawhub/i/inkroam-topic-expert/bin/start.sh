#!/bin/bash
# 选题专家 - 启动守护进程

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PID_FILE="$PROJECT_ROOT/data/topic_expert.pid"
LOG_FILE="$PROJECT_ROOT/logs/daemon.log"

mkdir -p "$PROJECT_ROOT/data" "$PROJECT_ROOT/logs"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null 2>&1; then
        echo "❌ 选题专家已在运行 (PID: $PID)"
        exit 1
    fi
fi

echo "🚀 启动选题专家守护进程..."
cd "$PROJECT_ROOT"
nohup python3 -u main.py --daemon >> "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"
echo "✅ 已启动 (PID: $(cat $PID_FILE))"
echo "📋 日志文件: $LOG_FILE"
