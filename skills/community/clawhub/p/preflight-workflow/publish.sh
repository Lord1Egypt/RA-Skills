#!/usr/bin/env bash
# Preflight Workflow — 一键上架脚本
# 用法：老板输完设备码后，我执行这个

set -e

PRODUCT_DIR="/Users/apple/Desktop/隅舍/跨境电商/技能产品"
cd "$PRODUCT_DIR"

echo "🛡️ 准备上架 Preflight Workflow..."
echo ""

# 确保已登录
if ! clawhub whoami &>/dev/null; then
    echo "❌ 未登录，请先执行 device login"
    exit 1
fi

# 本地验证
echo "📋 验证产品文件..."
for f in SKILL.md preflight.sh install.sh LEARNINGS.md README.md; do
    if [ -f "$f" ]; then
        echo "  ✅ $f"
    else
        echo "  ❌ $f 缺失"
        exit 1
    fi
done

# Dry-run 预览
echo ""
echo "🔍 Dry-run 预览..."
clawhub skill publish . --slug preflight-workflow --name "Preflight Workflow" --dry-run --owner @yushe

# 实际发布
echo ""
echo "🚀 发布中..."
clawhub skill publish . --slug preflight-workflow --name "Preflight Workflow" --owner @yushe

echo ""
echo "✅ 上架完成！"
echo "   https://clawhub.ai/@yushe/preflight-workflow"
