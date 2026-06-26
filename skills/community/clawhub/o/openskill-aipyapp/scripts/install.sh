#!/bin/bash
# AIPyApp 一键安装脚本

set -e

echo "🚀 开始安装 AIPyApp..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi
echo "✅ Python3: $(python3 --version)"

# 检查并安装 pip
if ! python3 -m pip --version &> /dev/null; then
    echo "📦 安装 python3-pip..."
    apt update && apt install -y python3-full python3-pip
fi

echo "✅ pip 已就绪"

# 安装 aipyapp
echo "📦 安装 aipyapp..."
python3 -m pip install aipyapp --break-system-packages

echo ""
echo "🎉 安装完成!"
echo ""
echo "使用方式:"
echo "  aipy run '你的任务描述'"
