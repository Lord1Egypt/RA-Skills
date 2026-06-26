#!/bin/bash
# ClawHub 发布脚本 v4.1
# 用法：./scripts/publish.sh [版本号] [changelog] [详细说明]
# 自动更新所有文件的版本号和版本历史，然后发布
#
# 示例：
#   ./scripts/publish.sh                    # 使用 version.js 中的版本同步后发布
#   ./scripts/publish.sh 4.2.0 "新功能"     # 更新版本后发布

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# 查找 clawhub 命令
if command -v clawhub &> /dev/null; then
    CLAWHUB_CMD="clawhub"
elif [ -f "$HOME/.nvm/versions/node/v22.22.0/bin/clawhub" ]; then
    CLAWHUB_CMD="$HOME/.nvm/versions/node/v22.22.0/bin/clawhub"
else
    echo "❌ clawhub 命令未找到"
    echo "💡 请确保已安装 clawhub"
    exit 1
fi

# 从 version.js 读取当前版本
CURRENT_VERSION=$(grep "version:" "$PROJECT_DIR/workflows/version.js" | head -1 | sed "s/.*'\([^']*\)'.*/\1/")

VERSION="${1:-$CURRENT_VERSION}"
CHANGELOG="${2:-更新}"
DETAIL="${3:-$CHANGELOG}"

echo "════════════════════════════════════════════════════════"
echo "  PRD Workflow 发布脚本 v4.1"
echo "════════════════════════════════════════════════════════"
echo ""
echo "📦 版本：${VERSION}"
echo "📝 Changelog: ${CHANGELOG}"
echo "📄 详情：${DETAIL}"
echo "📁 目录：${PROJECT_DIR}"
echo ""

# 确认发布
read -p "继续发布？(y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 已取消"
    exit 1
fi

echo ""

# 调用 Python 脚本更新所有文件
echo "🔧 更新版本号和版本历史..."
if [ "$VERSION" != "$CURRENT_VERSION" ]; then
    python3 "${SCRIPT_DIR}/update_version.py" "${VERSION}" "${CHANGELOG}" "${DETAIL}"
else
    python3 "${SCRIPT_DIR}/update_version.py"
fi

echo ""

# 运行测试
echo "🧪 运行测试..."
cd "${PROJECT_DIR}"
node tests/test.js
echo ""

# 发布
echo "📦 发布到 ClawHub..."
$CLAWHUB_CMD publish . --version "${VERSION}" --changelog "v${VERSION}: ${CHANGELOG}" 2>&1

# 等待服务器处理
echo ""
echo "⏳ 等待服务器处理..."
sleep 3

# 验证远程状态
echo "🔍 验证发布状态..."
RESULT=$($CLAWHUB_CMD inspect prd-workflow --json 2>/dev/null | grep -o '"latest": "[^"]*"')

if echo "$RESULT" | grep -q "${VERSION}"; then
    echo ""
    echo "════════════════════════════════════════════════════════"
    echo "  ✅ 发布成功！"
    echo "════════════════════════════════════════════════════════"
    echo ""
    echo "   版本：${VERSION}"
    echo "   验证：$RESULT"
    echo ""
    echo "🔗 安装命令：clawhub install prd-workflow"
    echo ""
else
    echo ""
    echo "⚠️ 无法确认发布状态"
    echo "   期望版本：${VERSION}"
    echo "   远程状态：$RESULT"
    echo ""
    echo "💡 建议：稍后手动验证"
    echo "   $CLAWHUB_CMD inspect prd-workflow --json | grep latest"
fi
