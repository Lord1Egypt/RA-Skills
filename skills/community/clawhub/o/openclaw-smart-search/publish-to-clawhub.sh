#!/bin/bash

# Smart Search ClawHub 发布脚本

set -e

echo "🚀 Smart Search ClawHub 发布脚本"
echo "=================================="
echo ""

cd ~/.agents/skills/smart-search

# 步骤 1：检查登录状态
echo "📋 步骤 1: 检查登录状态..."
if clawhub whoami &>/dev/null; then
    echo "✅ 已登录"
else
    echo "⚠️  未登录，需要登录 ClawHub"
    echo ""
    echo "请运行以下命令登录："
    echo "  clawhub login"
    echo ""
    echo "或者在浏览器中打开："
    echo "  https://clawhub.ai/cli/auth"
    echo ""
    read -p "按回车键继续..."
fi

# 步骤 2：验证登录
echo ""
echo "📋 步骤 2: 验证登录..."
clawhub whoami
echo ""

# 步骤 3：发布
echo "📋 步骤 3: 发布技能..."
echo "准备发布以下文件:"
echo "  - dist/ (构建输出)"
echo "  - scripts/ (配置脚本)"
echo "  - src/ (TypeScript 源码)"
echo "  - SKILL.md (技能说明)"
echo "  - README.md (使用文档)"
echo "  - package.json (依赖配置)"
echo ""

read -p "是否继续发布？(y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 发布已取消"
    exit 1
fi

echo ""
echo "🚀 发布到 ClawHub..."
clawhub publish .

# 步骤 4：验证发布
echo ""
echo "📋 步骤 4: 验证发布..."
echo "搜索技能..."
clawhub search smart-search

echo ""
echo "✅ 发布完成！"
echo ""
echo "📊 技能信息:"
clawhub info smart-search

echo ""
echo "🎉 恭喜！Smart Search 已成功发布到 ClawHub！"
echo ""
echo "技能页面："
echo "  https://clawhub.com/skills/smart-search"
echo ""
echo "安装命令："
echo "  clawhub install smart-search"
echo ""
