#!/bin/bash
# OpenClaw History Viewer - 备份当前会话并启动服务

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "📦 备份当前会话..."
python3 "$SCRIPT_DIR/backup_session.py"

echo ""
echo "🚀 启动 History Viewer..."
python3 "$SCRIPT_DIR/history_server.py" "$@"
