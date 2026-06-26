#!/bin/bash

# ClawHub 一键发布脚本
# 用法: bash publish-to-clawhub.sh

SKILL_NAME="mbti-master"
VERSION="1.0.0"

echo "═══════════════════════════════════════════════════════════════"
echo "              MBTI Master - ClawHub发布助手"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# 检查 clawhub CLI
if ! command -v clawhub &> /dev/null; then
    echo "⚠️  未安装 ClawHub CLI"
    echo ""
    echo "请先安装:"
    echo "  npm i -g clawhub"
    echo ""
    echo "或访问: https://clawhub.com"
    exit 1
fi

echo "✓ ClawHub CLI 已安装"
echo ""

# 检查登录状态
echo "检查登录状态..."
if ! clawhub whoami &> /dev/null; then
    echo "⚠️  未登录 ClawHub"
    echo ""
    echo "请先登录:"
    echo "  clawhub login"
    echo ""
    exit 1
fi

echo "✓ 已登录 ClawHub"
echo ""

# 检查SKILL.md
echo "检查 skill 格式..."
if [ ! -f "SKILL.md" ]; then
    echo "❌ 未找到 SKILL.md"
    exit 1
fi

echo "✓ SKILL.md 存在"
echo ""

# 验证 skill
echo "验证 skill 格式..."
if clawhub validate &> /dev/null; then
    echo "✓ Skill 格式验证通过"
else
    echo "⚠️  格式验证警告（继续发布）"
fi
echo ""

# 确认发布
echo "准备发布:"
echo "  Skill名称: $SKILL_NAME"
echo "  版本: $VERSION"
echo "  作者: ShenJian"
echo ""
read -p "确认发布到 ClawHub? [y/N]: " confirm

if [[ $confirm != [yY] && $confirm != [yY][eE][sS] ]]; then
    echo "已取消"
    exit 0
fi

echo ""
echo "开始发布..."
echo ""

# 发布
if clawhub publish; then
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "✅ 发布成功！"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "其他用户现在可以:"
    echo "  clawhub search mbti"
    echo "  clawhub install $SKILL_NAME"
    echo ""
    echo "或访问: https://clawhub.com/s/$SKILL_NAME"
    echo "═══════════════════════════════════════════════════════════════"
else
    echo ""
    echo "❌ 发布失败"
    echo ""
    echo "请检查:"
    echo "  1. 网络连接"
    echo "  2. 是否已登录: clawhub whoami"
    echo "  3. SKILL.md 格式是否正确"
    echo ""
    echo "查看详细错误:"
    echo "  clawhub publish --verbose"
fi