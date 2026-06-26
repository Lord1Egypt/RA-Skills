#!/bin/bash
# MCP Hello World 快速启动脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🦞 MCP Hello World 服务器"
echo "========================"
echo ""

# 检查依赖
if ! command -v node &> /dev/null; then
    echo "❌ 错误：需要安装 Node.js"
    exit 1
fi

if [ ! -d "node_modules" ]; then
    echo "📦 首次运行，安装依赖..."
    npm install
fi

echo "✅ 依赖已就绪"
echo ""
echo "🚀 启动服务器..."
echo "   传输方式：stdio"
echo "   可用工具：add, hello_world"
echo ""
echo "💡 使用示例："
echo "   mcporter call --stdio \"node src/server.js\" add a:10 b:20"
echo "   mcporter call --stdio \"node src/server.js\" hello_world name:\"朋友\""
echo ""
echo "------------------------"

# 启动服务器
node src/server.js
