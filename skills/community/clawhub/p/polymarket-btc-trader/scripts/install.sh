#!/bin/bash
# Polymarket Bot 安装脚本
# 用法: bash install.sh

set -e

BOT_DIR="${POLYMARKET_BOT_DIR:-$HOME/.openclaw/workspace/polymarket_bot}"
mkdir -p "$BOT_DIR"

echo "📦 安装 Polymarket Bot 依赖..."
echo "   Python 版本需求: 3.10+"
echo "   安装目录: $BOT_DIR"

# 创建虚拟环境
if [ ! -d "$BOT_DIR/.venv" ]; then
    python3 -m venv "$BOT_DIR/.venv"
    echo "✅ 虚拟环境创建完成"
else
    echo "✅ 虚拟环境已存在，跳过"
fi

# 安装依赖
"$BOT_DIR/.venv/bin/pip" install --upgrade pip
"$BOT_DIR/.venv/bin/pip" install aiohttp requests python-dotenv uvicorn

echo ""
echo "✅ 安装完成！"
echo ""
echo "下一步："
echo "  1. cp references/.env.example .env  # 填入你的 API Key"
echo "  2. bash scripts/bot_start.sh         # 启动 Bot"
echo "  3. bash scripts/panel_start.sh        # 启动控制面板"
