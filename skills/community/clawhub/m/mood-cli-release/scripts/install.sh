#!/bin/bash

# Mood CLI Skill 安装脚本
# 用于 ClawHub 技能市场安装
# 作者：万万粥 <wanwan_app@163.com>
# 版本：v1.0.0

set -e

echo "🌤️  正在安装 Mood CLI Skill..."

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误：未找到 Node.js，请先安装 Node.js"
    exit 1
fi

# 检查 npm
if ! command -v npm &> /dev/null; then
    echo "❌ 错误：未找到 npm，请先安装 npm"
    exit 1
fi

# 安装 CLI 工具
echo "📦 安装 mood-weather-cli..."
npm install -g mood-weather-cli

# 验证安装
if command -v mood &> /dev/null; then
    echo "✅ CLI 工具安装成功"
else
    echo "❌ CLI 工具安装失败"
    exit 1
fi

# 检查配置文件
ENV_FILE="$HOME/.mood-weather-cli.env"
if [ ! -f "$ENV_FILE" ]; then
    echo "⚠️  配置文件不存在，创建示例配置..."
    echo "# 请替换为你的 DeepSeek API 密钥" > "$ENV_FILE"
    echo "DEEPSEEK_API_KEY=sk-your-api-key-here" >> "$ENV_FILE"
    echo "📝 配置文件已创建：$ENV_FILE"
    echo "⚠️  请编辑该文件，填入你的 DeepSeek API 密钥"
fi

# 运行健康检查
echo ""
echo "🏥 运行健康检查..."
mood --healthcheck || {
    echo ""
    echo "⚠️  健康检查未通过，请检查配置"
    echo "💡 提示：编辑 $ENV_FILE 填入正确的 API 密钥"
}

echo ""
echo "🎉 Mood CLI Skill 安装完成！"
echo ""
echo "使用方法："
echo "  mood 今天心情好          # 分析情绪"
echo "  mood --healthcheck       # 健康检查"
echo "  mood --help              # 查看帮助"
echo ""
