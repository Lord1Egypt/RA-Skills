#!/bin/bash
# 快速启动脚本 - 一键安装并启用

set -e

echo "🦐 记忆优化工具包 - 快速启动"
echo "=================================================="

# 运行安装
bash install.sh

echo ""
echo "🚀 启动监听器..."
cd "$HOME/.openclaw/workspace"
python3 scripts/memory-watcher.py ./memory/ &

echo ""
echo "✅ 全部完成！监听器已在后台运行。"
echo "   查看进程：ps aux | grep memory-watcher"
echo "   停止监听：pkill -f memory-watcher"
echo ""
