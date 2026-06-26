#!/bin/bash
# Environment check for metabot-basic
# Verifies Node.js >= 18, npm; installs dependencies if missing (TypeScript/ts-node via npm install)

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🔍 Checking environment prerequisites..."

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装"
    echo "   请安装 Node.js >= 18: https://nodejs.org/"
    echo "   或使用 nvm: nvm install 18 && nvm use 18"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ 需要 Node.js >= 18，当前: $(node -v)"
    echo "   请升级: https://nodejs.org/ 或 nvm install 18"
    exit 1
fi

echo "✅ Node.js: $(node -v)"

# Check npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm 未安装"
    exit 1
fi

echo "✅ npm: $(npm -v)"

# Auto-install dependencies if node_modules missing (installs TypeScript / ts-node)
if [ ! -d "$SKILL_ROOT/node_modules" ]; then
    echo "📦 未检测到依赖，正在执行 npm install..."
    (cd "$SKILL_ROOT" && npm install)
    echo "✅ 依赖安装完成"
fi

# Verify ts-node available (global or via npx)
if ! command -v ts-node &> /dev/null; then
    if [ -f "$SKILL_ROOT/node_modules/.bin/ts-node" ]; then
        echo "✅ ts-node 已通过 npm 安装，请使用: npx ts-node scripts/..."
    else
        echo "⚠️  未找到 ts-node，正在安装依赖..."
        (cd "$SKILL_ROOT" && npm install)
        echo "✅ 请使用: npx ts-node scripts/main.ts \"<用户提示词>\""
    fi
else
    echo "✅ ts-node 可用"
fi

echo ""
echo "✅ 环境检查通过。运行示例:"
echo "   npm run start -- \"创建 metabot，名字叫'小橙'\""
echo "   npm run start -- \"创建 metabot，名字叫'小橙'，并发送一条 buzz 叫'hello'\""
echo "   npm run send-buzz -- \"小橙\" \"你好世界\""
echo "   npm run check-env   # 再次检查环境"
exit 0
