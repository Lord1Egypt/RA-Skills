#!/bin/bash

# Human-Like Memory Skill 发布脚本
# 用法：./publish-skill.sh

set -e

SKILL_DIR="/home/admin/openclaw/workspace/skills/human-like-memory"
SKILL_SLUG="human-like-memory"
SKILL_NAME="Human-Like Memory"
VERSION="1.0.0"

echo "🚀 开始发布技能：$SKILL_NAME v$VERSION"
echo ""

# 检查登录状态
echo "📋 检查登录状态..."
if ! clawhub whoami > /dev/null 2>&1; then
    echo "❌ 未登录 ClawHub"
    echo ""
    echo "请选择登录方式："
    echo "  1. 浏览器登录：clawhub login"
    echo "  2. Token 登录：clawhub login --token <你的 Token>"
    echo ""
    read -p "按回车键打开浏览器登录..."
    clawhub login
fi

echo "✅ 登录成功：$(clawhub whoami)"
echo ""

# 检查技能目录
echo "📁 检查技能文件..."
if [ ! -d "$SKILL_DIR" ]; then
    echo "❌ 技能目录不存在：$SKILL_DIR"
    exit 1
fi

echo "✅ 技能目录存在"
echo ""

# 显示技能信息
echo "📊 技能信息："
echo "  名称：$SKILL_NAME"
echo "  Slug: $SKILL_SLUG"
echo "  版本：$VERSION"
echo "  目录：$SKILL_DIR"
echo ""

# 确认发布
read -p "确认发布？(y/n): " confirm
if [ "$confirm" != "y" ]; then
    echo "❌ 取消发布"
    exit 0
fi

# 发布技能
echo ""
echo "📦 发布技能到 ClawHub..."
cd "$SKILL_DIR"

clawhub publish . \
  --slug "$SKILL_SLUG" \
  --name "$SKILL_NAME" \
  --version "$VERSION" \
  --changelog "Initial release: Human-like memory simulation with 3-tier storage (HOT/WARM/COLD), 5-dimension importance scoring, auto-compaction, review mechanism, and forgetting curve"

echo ""
echo "✅ 发布成功！"
echo ""
echo "🌐 查看技能：https://clawhub.com/skills/$SKILL_SLUG"
echo ""
echo "📥 安装命令：clawhub install $SKILL_SLUG"
echo ""

# 验证发布
echo "🔍 验证发布..."
clawhub search "$SKILL_SLUG" | head -5

echo ""
echo "🎉 发布完成！"
