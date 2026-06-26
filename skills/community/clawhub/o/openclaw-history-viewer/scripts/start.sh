#!/bin/bash
# OpenClaw History Viewer - 快速启动脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${1:-8765}"

echo "🚀 启动 OpenClaw History Viewer..."
echo "📍 服务地址：http://localhost:${PORT}"
echo "📁 数据目录：~/.openclaw/agents/main/sessions/"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

python3 "${SCRIPT_DIR}/history_server.py" "${PORT}"
