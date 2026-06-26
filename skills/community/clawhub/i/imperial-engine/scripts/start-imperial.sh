#!/bin/bash
# 帝王引擎启动脚本
# 使用前请确保已配置预算限制！

set -e

echo "⚔️ 帝王引擎启动检查 ⚔️"
echo "========================"

# 检查是否在测试环境
if [[ "$ENVIRONMENT" != "test" && "$ENVIRONMENT" != "development" ]]; then
    echo "❌ 错误：当前环境不是测试环境！"
    echo "请设置 ENVIRONMENT=test 或 development"
    exit 1
fi

# 检查预算配置
if ! grep -q "max_usd" config.yml 2>/dev/null; then
    echo "⚠️ 警告：未检测到预算限制配置！"
    echo "建议在 config.yml 中添加："
    echo "openclaw:"
    echo "  budget:"
    echo "    max_usd: 50"
    read -p "是否继续？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 检查技能是否已安装
if ! openclaw skill list | grep -q "imperial-engine"; then
    echo "📦 安装帝王引擎 Skill..."
    openclaw skill add . --skill imperial-engine
fi

# 启用技能
echo "🔧 启用帝王引擎..."
openclaw skill enable imperial-engine

echo ""
echo "✅ 帝王引擎已启用！"
echo ""
echo "触发方式："
echo "1. 发送消息: '/imperial 开始帝王模式'"
echo "2. 发送消息: '帝王引擎'"
echo "3. 发送消息: '开启帝王模式'"
echo ""
echo "📊 监控命令："
echo "- openclaw status --usage"
echo "- openclaw logs --follow"
echo ""
echo "🛑 紧急停止："
echo "- openclaw skill disable imperial-engine"
echo "- openclaw skill uninstall imperial-engine"
echo ""
echo "⚠️ 注意：请保持实时监控！"