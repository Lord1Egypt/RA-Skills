#!/bin/bash
# Polymarket Bot 启动脚本
# 用法: bash bot_start.sh

WORK_DIR="${POLYMARKET_BOT_DIR:-$HOME/.openclaw/workspace/polymarket_bot}"
SKILL_DIR="$HOME/.openclaw/workspace/skills/polymarket-btc-bot"

mkdir -p "$WORK_DIR/.runtime"
mkdir -p "$WORK_DIR/public"
mkdir -p "$WORK_DIR/config"

# 同步核心文件（取 skill 中的最新版本）
cp "$SKILL_DIR/bot.py"                "$WORK_DIR/bot.py"
cp "$SKILL_DIR/status_server.py"         "$WORK_DIR/status_server.py"
cp -r "$SKILL_DIR/assets/public/"*        "$WORK_DIR/public/"

# 如果 .env 不存在，从 example 创建
if [ ! -f "$WORK_DIR/.env" ]; then
    cp "$SKILL_DIR/references/.env.example" "$WORK_DIR/.env"
    echo "⚠️  已创建 .env，请编辑 $WORK_DIR/.env 填入 API Key！"
fi

cd "$WORK_DIR"

# 检查 .env 是否有真实配置
if grep -q "your_polymarket_api_key\|your_minimax" "$WORK_DIR/.env" 2>/dev/null; then
    echo "⚠️  .env 中仍有占位符，请先填入真实 API Key！"
    echo "   文件: $WORK_DIR/.env"
fi

# 杀掉旧进程
if [ -f "$WORK_DIR/.runtime/paper_bot.pid" ]; then
    OLD_PID=$(cat "$WORK_DIR/.runtime/paper_bot.pid")
    kill "$OLD_PID" 2>/dev/null && echo "🛑 已停止旧 Bot (PID $OLD_PID)"
fi

echo "🚀 启动 Polymarket Bot..."
nohup .venv/bin/python3 -u bot.py >> .runtime/paper_bot.log 2>&1 &
BOT_PID=$!
echo $BOT_PID > .runtime/paper_bot.pid

sleep 2
if ps -p $BOT_PID > /dev/null 2>&1; then
    echo "✅ Bot 已启动 (PID $BOT_PID)"
    echo "   日志: $WORK_DIR/.runtime/paper_bot.log"
    echo "   tail -f .runtime/paper_bot.log  # 实时查看"
else
    echo "❌ Bot 启动失败，查看日志:"
    tail -20 .runtime/paper_bot.log
fi
