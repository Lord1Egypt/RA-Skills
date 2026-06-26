#!/bin/bash

# Harness Engineering - 代码质量扫描脚本
# 功能：执行完整的代码质量检查，包括类型、lint、依赖、构建

set -e

echo "====================================="
echo "  Harness Engineering - 质量扫描"
echo "====================================="
echo ""

# 检查是否在项目目录中
if [ ! -f "package.json" ]; then
    echo "❌ 错误：未找到 package.json，请在项目根目录运行此脚本"
    exit 1
fi

# 初始化结果
FAILED=0
PASSED=0

# 1. TypeScript 类型检查
echo "🔍 1/5 - TypeScript 类型检查..."
if [ -f "tsconfig.json" ]; then
    if npx tsc --noEmit 2>&1; then
        echo "✅ TypeScript 类型检查通过"
        PASSED=$((PASSED + 1))
    else
        echo "❌ TypeScript 类型检查失败"
        FAILED=$((FAILED + 1))
    fi
else
    echo "⚠️  未找到 tsconfig.json，跳过 TypeScript 检查"
fi
echo ""

# 2. ESLint 检查
echo "🔍 2/5 - ESLint 代码规范检查..."
if [ -f ".eslintrc.js" ] || [ -f ".eslintrc.json" ] || [ -f ".eslintrc" ] || grep -q '"eslint"' package.json; then
    if npx eslint . --ext .ts,.tsx,.js,.jsx --quiet 2>&1; then
        echo "✅ ESLint 检查通过"
        PASSED=$((PASSED + 1))
    else
        echo "❌ ESLint 检查失败"
        FAILED=$((FAILED + 1))
    fi
else
    echo "⚠️  未配置 ESLint，跳过检查"
fi
echo ""

# 3. 依赖检查
echo "🔍 3/5 - 依赖检查..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if "$SCRIPT_DIR/depcheck.sh 2>&1; then
    echo "✅ 依赖检查通过"
    PASSED=$((PASSED + 1))
else
    echo "❌ 依赖检查发现问题"
    FAILED=$((FAILED + 1))
fi
echo ""

# 4. 环境配置检查
echo "🔍 4/5 - 环境配置检查..."
if [ -f ".env.example" ]; then
    echo "✅ 找到 .env.example"
    # 检查 .env.example 中是否有注释
    COMMENT_COUNT=$(grep -c "^#" .env.example 2>/dev/null || echo 0)
    if [ "$COMMENT_COUNT" -gt 0 ]; then
        echo "✅ .env.example 包含配置说明"
        PASSED=$((PASSED + 1))
    else
        echo "⚠️  .env.example 建议添加配置说明注释"
        PASSED=$((PASSED + 1))
    fi
else
    echo "❌ 未找到 .env.example，建议创建"
    FAILED=$((FAILED + 1))
fi
echo ""

# 5. 构建检查
echo "🔍 5/5 - 构建检查..."
if grep -q '"build"' package.json; then
    if npm run build 2>&1; then
        echo "✅ 构建检查通过"
        PASSED=$((PASSED + 1))
    else
        echo "❌ 构建检查失败"
        FAILED=$((FAILED + 1))
    fi
else
    echo "⚠️  package.json 中未找到 build 脚本，跳过构建检查"
fi
echo ""

# 总结
echo "====================================="
echo "  质量扫描结果"
echo "====================================="
echo ""
echo "✅ 通过: $PASSED"
echo "❌ 失败: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "🎉 所有检查通过！代码质量优秀！"
    echo ""
    echo "📋 交付前建议："
    echo "   - 阅读 README 确保文档完整"
    echo "   - 手动运行主要功能流程验证"
    echo "   - 检查是否有未处理的 TODO 注释"
    exit 0
else
    echo "⚠️  发现 $FAILED 个问题需要修复"
    echo ""
    echo "📋 建议："
    echo "   - 逐一修复上述问题"
    echo "   - 修复后重新运行此脚本"
    echo "   - 如果无法修复的问题，添加注释说明原因"
    exit 1
fi
