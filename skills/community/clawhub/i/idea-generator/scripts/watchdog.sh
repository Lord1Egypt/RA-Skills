#!/bin/bash
# watchdog.sh - 守护 idea-generator 服务器
SCRIPT_DIR="$(dirname "$0")"
PORT=50000

# 检查服务器是否响应
if ! curl -s --max-time 2 "http://localhost:$PORT/state.json" > /dev/null 2>&1; then
    echo "[$(date)] idea-generator server not responding, restarting..."
    # 杀掉旧进程
    kill $(lsof -t -i:$PORT) 2>/dev/null
    sleep 1
    # 重启
    cd "$SCRIPT_DIR" && nohup python3 server.py >> /tmp/idea-server.log 2>&1 &
    echo "[$(date)] Server restarted on port $PORT"
fi
