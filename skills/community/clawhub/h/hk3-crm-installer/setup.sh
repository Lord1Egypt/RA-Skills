#!/bin/bash
# HK3 CRM Installer — 给 OpenClaw 代理自动执行
# 用法: bash setup.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="${SCRIPT_DIR}/../.." # relative to workspace/skills/hk3-crm-installer/
CRM_DIR="$WORKSPACE/hk3-crm"
REPO_URL="https://github.com/jiangyisheng9-bot/hk3-crm.git"

echo "🔧 正在安装 HK3 CRM..."

# 1. Clone
if [ -d "$CRM_DIR" ]; then
    echo "📂 目录已存在，git pull 更新..."
    cd "$CRM_DIR" && git pull
else
    echo "📥 从 GitHub 克隆..."
    cd "$WORKSPACE" && git clone "$REPO_URL"
fi

# 2. 装依赖
echo "📦 安装 Python 依赖..."
cd "$CRM_DIR"
pip3 install -r requirements.txt -q 2>/dev/null || pip install -r requirements.txt -q

# 3. 启动（后台）
echo "🚀 启动 CRM..."
nohup python3 app.py > /tmp/hk3-crm.log 2>&1 &
CRM_PID=$!
echo $CRM_PID > "$CRM_DIR/.pid"

# 4. 等启动
sleep 3
if curl -s -o /dev/null -w "" http://127.0.0.1:5001 2>/dev/null; then
    echo "✅ HK3 CRM 已启动！"
    echo "📊 浏览器打开: http://127.0.0.1:5001"
    echo "🎮 体验演示数据: cd $CRM_DIR && python3 seed_demo.py"
else
    echo "⚠️ 启动中，请稍后刷新 http://127.0.0.1:5001"
    echo "   日志: cat /tmp/hk3-crm.log"
fi
