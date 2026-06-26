#!/bin/bash
# InvestmentTracker技能发布脚本
# 使用方法: ./publish_script.sh YOUR_CLAWHUB_TOKEN

set -e

TOKEN="$1"
SKILL_DIR="InvestmentTracker-platform"
SKILL_PATH="/home/node/.openclaw/workspace/skills/$SKILL_DIR"

echo "🔧 InvestmentTracker技能发布脚本"
echo "========================================"

# 检查参数
if [ -z "$TOKEN" ]; then
    echo "❌ 错误: 请提供ClawHub token作为参数"
    echo "使用方法: ./publish_script.sh YOUR_CLAWHUB_TOKEN"
    exit 1
fi

# 检查技能目录
if [ ! -d "$SKILL_PATH" ]; then
    echo "❌ 错误: 技能目录不存在: $SKILL_PATH"
    exit 1
fi

echo "✅ 技能目录存在: $SKILL_PATH"
echo "📁 技能大小: $(du -sh "$SKILL_PATH" | cut -f1)"
echo "📄 文件数量: $(find "$SKILL_PATH" -type f | wc -l)"

# 设置环境变量
echo "🔑 设置ClawHub token..."
export CLAWHUB_TOKEN="$TOKEN"

# 验证登录
echo "🔐 验证ClawHub登录..."
if ! clawhub whoami > /dev/null 2>&1; then
    echo "❌ ClawHub登录失败，请检查token"
    exit 1
fi

echo "✅ ClawHub登录成功"

# 进入技能目录
cd /home/node/.openclaw/workspace/skills

# 发布技能
echo "🚀 开始发布技能..."
clawhub publish "$SKILL_DIR" \
  --slug investmenttracker-platform \
  --name "InvestmentTracker Platform" \
  --version v1.0.0 \
  --tags "investment,finance,mcp,api,tracking" \
  --changelog "初始版本发布：完整的InvestmentTracker MCP API集成，支持用户信息查询、持仓管理、投资方法论和统计分析功能。包含多模式支持（API/模拟/混合）、SSE流式响应处理、优雅降级机制。"

echo "========================================"
echo "🎉 技能发布完成！"
echo ""
echo "📋 发布信息:"
echo "   Slug: investmenttracker-platform"
echo "   名称: InvestmentTracker Platform"
echo "   版本: v1.0.0"
echo "   标签: investment, finance, mcp, api, tracking"
echo ""
echo "🔍 验证发布:"
echo "   查看技能: clawhub list"
echo "   搜索技能: clawhub search investmenttracker"
echo "   安装测试: clawhub install investmenttracker-platform"
echo ""
echo "💡 后续步骤:"
echo "   1. 在ClawHub网站查看技能页面"
echo "   2. 测试技能安装和功能"
echo "   3. 收集用户反馈"
echo "   4. 准备下一个版本更新"