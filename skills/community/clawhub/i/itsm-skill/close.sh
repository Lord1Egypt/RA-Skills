#!/bin/bash

# ITSM 工单技能 - 关闭浏览器

DEBUG_PORT=9222

echo "🔒 关闭 Chrome 浏览器..."

if pgrep -f "chromium.*remote-debugging-port=$DEBUG_PORT" > /dev/null; then
    pkill -f "chromium.*--remote-debugging-port=$DEBUG_PORT"
    echo "✅ 浏览器已关闭"
else
    echo "⚠️  浏览器未运行"
fi
