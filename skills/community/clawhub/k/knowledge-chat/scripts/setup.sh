#!/bin/bash

# Knowledge Chat Skill 安装脚本 v1.1

echo "🚀 开始安装 Knowledge Chat v1.1..."

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 请先安装 Node.js 18+"
    exit 1
fi

echo "✅ Node.js 版本: $(node -v)"

# 安装依赖
echo "📦 安装依赖..."
npm install react-markdown remark-gfm --save

# 检查环境变量
if [ -z "$DASHSCOPE_API_KEY" ]; then
    echo "⚠️  请配置 DASHSCOPE_API_KEY 环境变量"
fi

echo "✅ Knowledge Chat v1.1 安装完成！"