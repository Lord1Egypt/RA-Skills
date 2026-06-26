#!/bin/sh
set -e

echo "🚀 启动 OpenClaw..."

# 检查配置
if [ ! -f /home/node/.openclaw/openclaw.json ]; then
    echo "⚠️  未找到配置文件，请先配置 OpenClaw"
    echo "   运行: openclaw configure"
fi

# 启动服务
echo "📡 启动 Gateway..."
openclaw gateway start &

# 等待一下
sleep 3

# 检查是否启动成功
if openclaw status > /dev/null 2>&1; then
    echo "✅ OpenClaw 已启动！"
    echo "   访问 http://localhost:2026"
else
    echo "❌ 启动失败，请检查配置"
fi

# 保持容器运行
tail -f /dev/null
