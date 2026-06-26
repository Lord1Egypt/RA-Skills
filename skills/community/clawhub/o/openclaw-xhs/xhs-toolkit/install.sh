#!/bin/bash

echo "🌺 小红书MCP工具包 v1.2.0 - 快速安装脚本"
echo "============================================"

# 检查操作系统
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "✅ 检测到 macOS 系统"
    CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    CHROMEDRIVER_PATH="/opt/homebrew/bin/chromedriver"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "✅ 检测到 Linux 系统"
    CHROME_PATH="/usr/bin/google-chrome"
    CHROMEDRIVER_PATH="/usr/bin/chromedriver"
else
    echo "❌ 不支持的操作系统: $OSTYPE"
    exit 1
fi

# 检查Chrome浏览器
echo "🔍 检查Chrome浏览器..."
if [ -f "$CHROME_PATH" ]; then
    echo "✅ Chrome浏览器已安装"
else
    echo "❌ Chrome浏览器未找到"
    echo "💡 请先安装 Google Chrome 浏览器"
    exit 1
fi

# 检查ChromeDriver
echo "🔍 检查ChromeDriver..."
if [ -f "$CHROMEDRIVER_PATH" ]; then
    echo "✅ ChromeDriver已安装"
else
    echo "❌ ChromeDriver未找到，正在安装..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install chromedriver
    else
        sudo apt-get update
        sudo apt-get install -y chromium-chromedriver
    fi
fi

# 创建.env文件
echo "📝 创建配置文件..."
if [ ! -f ".env" ]; then
    cp env_example .env
    
    # 替换默认路径
    sed -i.bak "s|CHROME_PATH=.*|CHROME_PATH=\"$CHROME_PATH\"|g" .env
    sed -i.bak "s|WEBDRIVER_CHROME_DRIVER=.*|WEBDRIVER_CHROME_DRIVER=\"$CHROMEDRIVER_PATH\"|g" .env
    rm .env.bak 2>/dev/null || true
    
    echo "✅ 配置文件已创建"
else
    echo "✅ 配置文件已存在"
fi

# 创建数据目录
echo "📁 创建数据目录..."
mkdir -p data/creator_db
echo "✅ 数据目录已创建: data/creator_db/"

# 安装Python依赖（如果是源码方式）
if [ -f "requirements.txt" ] && command -v pip &> /dev/null; then
    echo "📦 安装Python依赖..."
    pip install -r requirements.txt
    echo "✅ 依赖安装完成"
fi

echo ""
echo "🎉 安装完成！"
echo ""
echo "📋 下一步："
echo "1. 运行: ./xhs-toolkit cookie save"
echo "2. 运行: ./xhs-toolkit server start"
echo ""
echo "🆕 v1.2.0 新功能："
echo "📊 数据采集与AI分析功能已启用"
echo "📁 数据将保存在 data/creator_db/ 目录"
echo "🤖 AI可通过 get_creator_data_analysis 工具分析您的账号数据"
echo ""
echo "💡 更多帮助: ./xhs-toolkit --help" 