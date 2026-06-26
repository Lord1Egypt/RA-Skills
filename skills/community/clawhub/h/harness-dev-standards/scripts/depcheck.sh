#!/bin/bash

# Harness Engineering - 依赖检查脚本
# 功能：检查项目中未使用的依赖和缺失的依赖

set -e

echo "====================================="
echo "  Harness Engineering - 依赖检查"
echo "====================================="
echo ""

# 检查是否在项目目录中
if [ ! -f "package.json" ]; then
    echo "❌ 错误：未找到 package.json，请在项目根目录运行此脚本"
    exit 1
fi

# 检查 depcheck 是否安装
if ! command -v depcheck &> /dev/null; then
    echo "📦 安装 depcheck..."
    npm install -g depcheck
fi

echo "🔍 开始检查依赖..."
echo ""

# 运行 depcheck
DEPCHECK_OUTPUT=$(depcheck --json)

# 解析结果
UNUSED_DEPS=$(echo "$DEPCHECK_OUTPUT" | node -e "console.log(JSON.parse(require('fs').readFileSync(0, 'utf-8')).dependencies.join('\n'))")
UNUSED_DEV_DEPS=$(echo "$DEPCHECK_OUTPUT" | node -e "console.log(JSON.parse(require('fs').readFileSync(0, 'utf-8')).devDependencies.join('\n'))")
MISSING_DEPS=$(echo "$DEPCHECK_OUTPUT" | node -e "console.log(JSON.parse(require('fs').readFileSync(0, 'utf-8')).missing.join('\n'))")

echo "📊 检查结果："
echo ""

# 未使用的依赖
if [ -n "$UNUSED_DEPS" ] && [ "$UNUSED_DEPS" != "" ]; then
    echo "⚠️  发现未使用的依赖（dependencies）："
    echo "$UNUSED_DEPS" | while read -r dep; do
        if [ -n "$dep" ]; then
            echo "   - $dep"
        fi
    done
    echo ""
else
    echo "✅ 未发现未使用的 dependencies"
fi

# 未使用的 devDependencies
if [ -n "$UNUSED_DEV_DEPS" ] && [ "$UNUSED_DEV_DEPS" != "" ]; then
    echo "⚠️  发现未使用的 devDependencies："
    echo "$UNUSED_DEV_DEPS" | while read -r dep; do
        if [ -n "$dep" ]; then
            echo "   - $dep"
        fi
    done
    echo ""
else
    echo "✅ 未发现未使用的 devDependencies"
fi

# 缺失的依赖
if [ -n "$MISSING_DEPS" ] && [ "$MISSING_DEPS" != "" ]; then
    echo "❌ 发现缺失的依赖（代码中引用但未在 package.json 声明）："
    echo "$MISSING_DEPS" | while read -r dep; do
        if [ -n "$dep" ]; then
            echo "   - $dep"
        fi
    done
    echo ""
else
    echo "✅ 未发现缺失的依赖"
fi

# 安全漏洞检查
echo ""
echo "🔐 安全漏洞检查..."
echo ""

AUDIT_OUTPUT=$(npm audit --json 2>/dev/null || true)
HIGH_VULNS=$(echo "$AUDIT_OUTPUT" | node -e "
try {
  const data = JSON.parse(require('fs').readFileSync(0, 'utf-8'));
  console.log(data.metadata.vulnerabilities.high || 0);
} catch(e) {
  console.log(0);
}")
CRITICAL_VULNS=$(echo "$AUDIT_OUTPUT" | node -e "
try {
  const data = JSON.parse(require('fs').readFileSync(0, 'utf-8'));
  console.log(data.metadata.vulnerabilities.critical || 0);
} catch(e) {
  console.log(0);
}")

if [ "$CRITICAL_VULNS" != "0" ] || [ "$HIGH_VULNS" != "0" ]; then
    echo "⚠️  发现安全漏洞："
    echo "   - Critical: $CRITICAL_VULNS"
    echo "   - High: $HIGH_VULNS"
    echo ""
    echo "   建议运行：npm audit fix"
else
    echo "✅ 未发现高危安全漏洞"
fi

echo ""
echo "====================================="
echo "  依赖检查完成！"
echo "====================================="

# 返回非零状态码表示有问题需要处理
if [ -n "$UNUSED_DEPS" ] && [ "$UNUSED_DEPS" != "" ] || \
   [ -n "$MISSING_DEPS" ] && [ "$MISSING_DEPS" != "" ] || \
   [ "$CRITICAL_VULNS" != "0" ]; then
    exit 1
fi

exit 0
