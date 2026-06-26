#!/bin/bash
# 记忆优化工具包 - 安装脚本

set -e

echo "🦐 安装记忆优化工具包..."

# 检查工作目录
if [ -z "$OPENCLAW_WORKSPACE" ]; then
    OPENCLAW_WORKSPACE="$HOME/.openclaw/workspace"
fi

echo "📁 工作目录：$OPENCLAW_WORKSPACE"

# 复制脚本
echo "📋 复制脚本文件..."
mkdir -p "$OPENCLAW_WORKSPACE/scripts"
cp scripts/*.py "$OPENCLAW_WORKSPACE/scripts/"
cp scripts/*.sh "$OPENCLAW_WORKSPACE/scripts/" 2>/dev/null || true

# 安装依赖
echo "📦 安装 Python 依赖..."
pip3 install watchdog

# 设置权限
chmod +x "$OPENCLAW_WORKSPACE/scripts/"*.py
chmod +x "$OPENCLAW_WORKSPACE/scripts/"*.sh

echo ""
echo "✅ 安装完成！"
echo ""
echo "📖 使用指南："
echo "  1. 手动索引：python3 scripts/memory-dedup.py ./memory/"
echo "  2. 启动监听：python3 scripts/memory-watcher.py ./memory/ &"
echo "  3. 查看详情：cat docs/README.md"
echo ""
