#!/usr/bin/env bash

# Health Assistant 安装脚本

set -e

echo "🦞 开始安装 Health Assistant 依赖..."

# 获取脚本所在目录
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# 1. 检查 Python 虚拟环境，如果没有则创建
if [ ! -d "venv" ]; then
    echo "📦 创建 Python 虚拟环境..."
    python3 -m venv venv
fi

# 2. 激活虚拟环境并安装项目依赖
source venv/bin/activate
echo "🔧 安装 Python 依赖..."
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    # 至少安装 garth
    pip install garth
fi

# 3. 检查并安装 notebooklm-py 及其依赖
echo "📦 安装 notebooklm-py 及浏览器驱动..."
pip install "notebooklm-py[browser]"

# 4. 自动下载 Playwright 所需的 Chromium 浏览器
echo "🌐 正在下载 Chromium 浏览器内核 (用于 AI 登录)..."
python3 -m playwright install chromium

echo "✅ 环境依赖已全部就绪！"

echo "✅ 安装完成！"
echo "👉 请回到 OpenClaw 聊天窗口发送 '生成健康报告' 体验功能。"
