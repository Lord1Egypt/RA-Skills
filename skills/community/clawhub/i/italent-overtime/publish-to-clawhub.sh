#!/bin/bash
# 北森 iTalent 加班管理 Skill - ClawHub 快速发布脚本

set -e

SKILL_NAME="italent-overtime"
SKILL_DIR="$HOME/.openclaw/skills/$SKILL_NAME"
VERSION="1.1.0"

echo "======================================"
echo " 北森 iTalent 加班管理 Skill"
echo " ClawHub 发布工具"
echo "======================================"
echo ""

# 检查 Skill 目录
if [ ! -d "$SKILL_DIR" ]; then
    echo "❌ 错误：Skill 目录不存在：$SKILL_DIR"
    exit 1
fi

cd "$SKILL_DIR"

# 检查必要文件
echo "📋 检查必要文件..."
required_files=("SKILL.md" "skill.json" "scripts/italent-overtime-simple.py")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (缺失)"
        exit 1
    fi
done
echo ""

# 检查 clawhub 登录状态
echo "🔐 检查 ClawHub 登录状态..."
if ! npx clawhub whoami > /dev/null 2>&1; then
    echo "⚠️  未登录 ClawHub"
    echo ""
    echo "请先登录："
    echo "  npx clawhub login"
    echo ""
    echo "或者使用 Token 登录："
    echo "  npx clawhub auth --token YOUR_TOKEN"
    echo ""
    read -p "是否现在登录？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        npx clawhub login
    else
        echo "❌ 发布已取消"
        exit 1
    fi
fi

echo "  ✅ 已登录"
echo ""

# 显示 Skill 信息
echo "📊 Skill 信息："
echo "  名称：$SKILL_NAME"
echo "  版本：v$VERSION"
echo "  目录：$SKILL_DIR"
echo ""

# 确认发布
read -p "是否确认发布？(y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 发布已取消"
    exit 1
fi

# 发布
echo ""
echo "🚀 正在发布到 ClawHub..."
npx clawhub publish .

echo ""
echo "======================================"
echo "  ✅ 发布成功！"
echo "======================================"
echo ""
echo "📦 Skill 信息："
echo "  名称：$SKILL_NAME"
echo "  版本：v$VERSION"
echo ""
echo "🔗 安装命令："
echo "  npx clawhub install $SKILL_NAME"
echo ""
echo "📊 查看 Skill："
echo "  npx clawhub inspect $SKILL_NAME"
echo "  npx clawhub search $SKILL_NAME"
echo ""
echo "🔄 用户更新："
echo "  npx clawhub update $SKILL_NAME"
echo ""
echo "======================================"
echo ""
echo "🎉 发布完成！用户现在可以通过以下命令安装："
echo ""
echo "   npx clawhub install $SKILL_NAME"
echo ""
echo "======================================"
