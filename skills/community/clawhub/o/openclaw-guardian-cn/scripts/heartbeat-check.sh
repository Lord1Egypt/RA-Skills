#!/bin/bash
# OpenClaw Guardian - Heartbeat 轻量检查

PID=$(pgrep -f "openclaw gateway" | head -1)

if [ -n "$PID" ]; then
    # 进程存活，轻量检查通过
    exit 0
else
    # 进程不在，尝试启动
    openclaw gateway start
    sleep 2
    if pgrep -f "openclaw gateway" > /dev/null; then
        echo "🛡️ Gateway 已自动恢复"
        exit 0
    else
        echo "🛡️ Gateway 自救失败，需要手动处理"
        exit 1
    fi
fi
