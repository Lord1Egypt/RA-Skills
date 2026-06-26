#!/bin/bash
# 配置向导脚本

echo "========================================"
echo "🦞 长桥智能投资助手 - 配置向导"
echo "========================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3"
    echo "请先安装 Python3"
    exit 1
fi

# 检查长桥 SDK
if ! python3 -c "import longbridge" 2>/dev/null; then
    echo "📦 安装长桥 Python SDK..."
    pip3 install longbridge
fi

# 检查 matplotlib
if ! python3 -c "import matplotlib" 2>/dev/null; then
    echo "📦 安装 matplotlib..."
    pip3 install matplotlib
fi

# 检查配置文件
ENV_FILE="$HOME/.longbridge/env"
if [ -f "$ENV_FILE" ]; then
    echo "✅ 找到配置文件: $ENV_FILE"
    echo ""
    echo "当前配置:"
    grep "LONGBRIDGE_APP_KEY" "$ENV_FILE" | cut -d'=' -f1
    grep "LONGBRIDGE_APP_SECRET" "$ENV_FILE" | cut -d'=' -f1
    grep "LONGBRIDGE_ACCESS_TOKEN" "$ENV_FILE" | cut -d'=' -f1
else
    echo "⚠️  未找到配置文件"
    echo ""
    echo "请创建文件: $ENV_FILE"
    echo "内容格式:"
    echo "export LONGBRIDGE_APP_KEY=你的AppKey"
    echo "export LONGBRIDGE_APP_SECRET=你的AppSecret"
    echo "export LONGBRIDGE_ACCESS_TOKEN=你的AccessToken"
    echo ""
    echo "获取方式:"
    echo "1. 登录长桥官网: https://open.longportapp.com"
    echo "2. 申请开发者权限"
    echo "3. 创建应用获取 Token"
fi

echo ""
echo "========================================"
echo "配置完成！运行 ./run.sh 开始使用"
echo "========================================"
