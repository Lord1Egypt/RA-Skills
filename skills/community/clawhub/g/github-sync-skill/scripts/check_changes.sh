#!/bin/bash

# Check Changes - 检测技能变更
# 用法：check_changes.sh

SKILLS_DIR="$HOME/.claude/skills"

cd "$SKILLS_DIR" || exit 1

echo "============================================================"
echo "  技能变更检测"
echo "============================================================"
echo ""

# 检查 Git 仓库是否存在
if [ ! -d ".git" ]; then
    echo "⚠️  Git 仓库未初始化"
    echo ""
    echo "请先运行初始化命令："
    echo "  git init"
    echo "  git add ."
    echo "  git commit -m 'Initial commit'"
    exit 1
fi

# 获取状态
echo "📊 Git 状态："
echo ""
git status --short

echo ""
echo "------------------------------------------------------------"

# 统计变更
added=$(git status --short | grep "^??" | wc -l | tr -d ' ')
modified=$(git status --short | grep "^ M" | wc -l | tr -d ' ')

echo ""
echo "📈 变更统计："
echo "   新增文件：$added"
echo "   修改文件：$modified"
echo "   总计变更：$((added + modified))"

if [ $((added + modified)) -eq 0 ]; then
    echo ""
    echo "✅ 没有检测到变更，所有技能已同步"
else
    echo ""
    echo "⚠️  有未同步的变更，建议运行："
    echo "   ~/.claude/skills/github-sync-skill/scripts/sync_to_github.sh"
fi

echo ""
echo "============================================================"
