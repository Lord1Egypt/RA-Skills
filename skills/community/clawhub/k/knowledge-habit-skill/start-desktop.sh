#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/tracker"
echo "💻 启动知识习惯追踪器 (Electron桌面版)..."
echo "   主窗口: 完整习惯记录器"
echo "   悬浮窗: 全局置顶计时窗"
echo "   快捷键:"
echo "     - Ctrl+Shift+T: 显示/隐藏悬浮窗"
echo "     - Ctrl+Shift+H: 唤起主窗口"
npm run desktop