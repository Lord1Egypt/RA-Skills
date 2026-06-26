#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/tracker"
echo "🌐 启动知识习惯追踪器 (Web版)..."
echo "   访问: http://127.0.0.1:3000"
echo "   按 Ctrl+C 停止服务"
npm start