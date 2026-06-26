#!/bin/bash
# Hermes Agent 更新并重启网关脚本 (Linux/macOS)
# 用法: bash update-restart.sh

set -e

HERMES_DIR="$HOME/.hermes/hermes-agent"

echo "=== Hermes Agent 更新并重启 ==="
echo ""

# 检查目录是否存在
if [ ! -d "$HERMES_DIR" ]; then
    echo "❌ 错误: Hermes Agent 未安装在 $HERMES_DIR"
    exit 1
fi

cd "$HERMES_DIR"

# 激活虚拟环境
echo "📦 激活虚拟环境..."
source venv/bin/activate

# 停止网关
echo "🛑 停止网关..."
hermes gateway stop 2>/dev/null || true

# 检查更新
echo "🔍 检查更新..."
hermes update

# 启动网关
echo "🚀 启动网关..."
hermes gateway run &

# 等待启动
sleep 3

# 检查状态
echo ""
echo "📊 网关状态:"
hermes gateway status

echo ""
echo "✅ 更新并重启完成！"
