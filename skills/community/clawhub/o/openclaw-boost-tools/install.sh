#!/bin/bash
# bw-openclaw-boost 安装脚本

INSTALL_DIR="$HOME/.openclaw/bw-openclaw-boost"
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "正在安装 bw-openclaw-boost..."

# 创建目录
mkdir -p "$INSTALL_DIR/tools"

# 复制文件
cp -r "$SKILL_DIR"/* "$INSTALL_DIR/"

# 设置执行权限
chmod +x "$INSTALL_DIR/launch.sh"
chmod +x "$INSTALL_DIR/tools/"*.sh 2>/dev/null
chmod +x "$INSTALL_DIR/tools/"*.py 2>/dev/null

echo ""
echo "✅ 安装完成！"
echo ""
echo "安装路径: $INSTALL_DIR"
echo ""
echo "使用方式:"
echo "  bash $INSTALL_DIR/launch.sh all-status"
echo ""
echo "或单独运行工具:"
echo "  python3 $INSTALL_DIR/tools/cost_tracker.py"
echo "  python3 $INSTALL_DIR/tools/memory_relevance.py scan"
echo ""
