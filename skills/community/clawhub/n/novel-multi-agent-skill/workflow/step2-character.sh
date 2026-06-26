#!/bin/bash
# ==============================================
# 多智能体小说创作系统 - 第2步：角色设计
# ==============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
TEMPLATES_DIR="$SKILL_DIR/templates"

if [ $# -lt 1 ]; then
    echo "用法: $0 <项目目录>"
    echo "示例: $0 ../my-novel"
    exit 1
fi

PROJECT_DIR="$1"

echo "=============================================="
echo "👥 第2步：角色设计"
echo "=============================================="
echo ""
echo "📁 项目目录: $PROJECT_DIR"
echo ""

# 检查前置文件
if [ ! -f "$PROJECT_DIR/00-总纲.md" ]; then
    echo "❌ 错误: 找不到项目总纲文件"
    exit 1
fi
if [ ! -f "$PROJECT_DIR/01-世界观设定.md" ]; then
    echo "❌ 错误: 找不到世界观设定文件"
    echo "   请先运行 step1-world.sh 完成世界观设定"
    exit 1
fi

echo "📋 前置检查通过"
echo "   ✅ 00-总纲.md"
echo "   ✅ 01-世界观设定.md"
echo ""

TODAY=$(date +%Y-%m-%d)
NOVEL_NAME=$(grep "小说名称" "$PROJECT_DIR/00-总纲.md" | head -1 | sed 's/.*：//' | sed 's/.*- //')

echo "🤖 调用角色设计智能体..."
echo ""

# ==============================================
# 调用智能体的命令（根据你的实际配置调整）
# ==============================================
# openclaw agent --agent novel-character-designer --message "
# 请为《$NOVEL_NAME》设计完整的角色档案。
# 
# 要求：
# 1. 严格遵循 00-总纲.md 和 01-世界观设定.md
# 2. 输出格式参考 templates/02-角色模板.md
# 3. 输出文件：$PROJECT_DIR/02-角色档案.md
# 4. 人物要立体、有辨识度、有完整的动机
# 5. 完成后立即通知总策划验收
# 
# 总纲：
# $(cat "$PROJECT_DIR/00-总纲.md")
# 
# 世界观：
# $(cat "$PROJECT_DIR/01-世界观设定.md")
# "

echo "⚠️  提示：当前使用模板生成模式"
echo "   配置好 novel-character-designer 智能体后，可以自动完成"
echo ""

sed -e "s/{{小说名}}/$NOVEL_NAME/g" \
    -e "s/{{日期}}/$TODAY/g" \
    "$TEMPLATES_DIR/02-角色模板.md" > "$PROJECT_DIR/02-角色档案.md"

echo "✅ 角色模板已生成"
echo ""
echo "📄 文件: $PROJECT_DIR/02-角色档案.md"
echo ""
echo "=============================================="
echo "📝 下一步操作："
echo "1. 编辑 $PROJECT_DIR/02-角色档案.md，完成角色设计"
echo "2. 确认无误后，运行：$SCRIPT_DIR/step3-plot.sh $PROJECT_DIR 1-10"
echo ""
