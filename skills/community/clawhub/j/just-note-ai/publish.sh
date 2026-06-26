#!/bin/bash
# just-note 发布脚本

set -e

echo "🦞 发布 just-note 到 ClawHub"
echo ""

# 检查 clawhub 是否安装
if ! command -v clawhub &> /dev/null; then
    echo "❌ clawhub CLI 未安装"
    echo "请运行：npm install -g clawhub"
    exit 1
fi

# 检查登录状态
echo "📝 检查登录状态..."
if ! clawhub whoami &> /dev/null; then
    echo "❌ 未登录"
    echo ""
    echo "请登录："
    echo "  clawhub login"
    echo ""
    echo "或者手动输入 token："
    echo "  clawhub login --token <your-token>"
    echo ""
    exit 1
fi

echo "✅ 已登录"
echo ""

# 发布信息
SLUG="just-note"
NAME="记一下"
VERSION="0.2.0"
DESCRIPTION="像发消息一样记录一切，AI 自动分类整理"
TAGS="note,ai,knowledge,productivity"
CHANGELOG="MVP 完成：记录/查询/统计/导出功能，AI 自动分类"

# 检查文件
echo "📁 检查文件..."
if [ ! -f "SKILL.md" ]; then
    echo "❌ 找不到 SKILL.md"
    exit 1
fi

if [ ! -f "README.md" ]; then
    echo "❌ 找不到 README.md"
    exit 1
fi

if [ ! -x "bin/just-note" ]; then
    echo "❌ bin/just-note 不可执行"
    exit 1
fi

echo "✅ 文件检查通过"
echo ""

# 发布
echo "🚀 开始发布..."
echo ""
echo "Slug: $SLUG"
echo "Name: $NAME"
echo "Version: $VERSION"
echo "Tags: $TAGS"
echo "Changelog: $CHANGELOG"
echo ""

clawhub publish . \
    --slug "$SLUG" \
    --name "$NAME" \
    --version "$VERSION" \
    --changelog "$CHANGELOG" \
    --tags "$TAGS"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 发布成功！"
    echo ""
    echo "访问：https://clawhub.ai/skills/$SLUG"
    echo ""
    echo "安装命令："
    echo "  npx clawhub install $SLUG"
    echo ""
else
    echo ""
    echo "❌ 发布失败"
    exit 1
fi
