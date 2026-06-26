#!/bin/bash
# 控制面板启动脚本
# 用法: bash panel_start.sh

WORK_DIR="${POLYMARKET_BOT_DIR:-$HOME/.openclaw/workspace/polymarket_bot}"
SKILL_DIR="$HOME/.openclaw/workspace/skills/polymarket-bot"

mkdir -p "$WORK_DIR/.runtime"
mkdir -p "$WORK_DIR/public"

# 同步面板文件
cp "$SKILL_DIR/scripts/status_server.py"  "$WORK_DIR/status_server.py"
cp -r "$SKILL_DIR/assets/public/"*        "$WORK_DIR/public/"

cd "$WORK_DIR"

# 杀掉旧面板进程（找所有 status_server.py 相关的）
pkill -f "status_server.py" 2>/dev/null && echo "🛑 已停止旧面板"

echo "🚀 启动控制面板..."
nohup .venv/bin/python3 -u status_server.py >> .runtime/status_panel.log 2>&1 &
PANEL_PID=$!
echo $PANEL_PID > .runtime/status_panel.pid

sleep 2
if ps -p $PANEL_PID > /dev/null 2>&1; then
    echo "✅ 面板已启动 (PID $PANEL_PID)"
    echo "   访问: http://localhost:18095"
else
    echo "❌ 面板启动失败，查看日志:"
    tail -20 .runtime/status_panel.log
fi
