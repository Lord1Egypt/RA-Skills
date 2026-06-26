#!/bin/bash

# Human-Like Memory v1.1.0 一键安装脚本

set -e

SKILL_DIR="/home/admin/openclaw/workspace/skills/human-like-memory"

echo "🚀 安装 Human-Like Memory v1.1.0"
echo ""

# 检查 Node.js 版本
echo "📋 检查 Node.js 版本..."
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js 版本过低，需要 >=18.0.0"
    echo "当前版本：$(node -v)"
    exit 1
fi
echo "✅ Node.js 版本：$(node -v)"
echo ""

# 进入技能目录
cd "$SKILL_DIR"

# 安装依赖
echo "📦 安装依赖..."
echo "   包：@xenova/transformers"
echo "   大小：~50MB"
echo ""

npm install @xenova/transformers --save

echo ""
echo "✅ 依赖安装完成"
echo ""

# 测试向量化引擎
echo "🧪 测试向量化引擎..."
node test-vector-engine.js

echo ""
echo "✅ 安装完成！"
echo ""
echo "📚 下一步:"
echo "   1. 运行测试：/memory test vector-search"
echo "   2. 查看统计：/memory stats"
echo "   3. 开始使用：/remember [内容]"
echo ""
echo "⚠️  首次使用会下载模型（约 200MB，仅需一次）"
echo ""
