#!/bin/bash
# ==============================================
# 多智能体小说创作系统 - 第3步：情节规划
# ==============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
TEMPLATES_DIR="$SKILL_DIR/templates"

if [ $# -lt 2 ]; then
    echo "用法: $0 <项目目录> <章节范围>"
    echo "示例: $0 ../my-novel 1-10"
    exit 1
fi

PROJECT_DIR="$1"
CHAPTER_RANGE="$2"
START_CHAPTER=$(echo $CHAPTER_RANGE | cut -d'-' -f1)
END_CHAPTER=$(echo $CHAPTER_RANGE | cut -d'-' -f2)

echo "=============================================="
echo "📑 第3步：情节规划（第${START_CHAPTER}-${END_CHAPTER}章）"
echo "=============================================="
echo ""
echo "📁 项目目录: $PROJECT_DIR"
echo "📖 章节范围: 第${START_CHAPTER}-${END_CHAPTER}章"
echo ""

# 检查前置文件
if [ ! -f "$PROJECT_DIR/00-总纲.md" ]; then
    echo "❌ 错误: 找不到项目总纲文件"
    exit 1
fi
if [ ! -f "$PROJECT_DIR/01-世界观设定.md" ]; then
    echo "❌ 错误: 找不到世界观设定文件"
    exit 1
fi
if [ ! -f "$PROJECT_DIR/02-角色档案.md" ]; then
    echo "❌ 错误: 找不到角色档案文件"
    echo "   请先运行 step2-character.sh 完成角色设计"
    exit 1
fi

echo "📋 前置检查通过"
echo "   ✅ 00-总纲.md"
echo "   ✅ 01-世界观设定.md"
echo "   ✅ 02-角色档案.md"
echo ""

TODAY=$(date +%Y-%m-%d)
NOVEL_NAME=$(grep "小说名称" "$PROJECT_DIR/00-总纲.md" | head -1 | sed 's/.*：//' | sed 's/.*- //')

echo "🤖 调用情节策划智能体..."
echo ""

# ==============================================
# 调用智能体的命令（根据你的实际配置调整）
# ==============================================
# openclaw agent --agent novel-plot-planner --message "
# 请为《$NOVEL_NAME》设计第${START_CHAPTER}-${END_CHAPTER}章的详细大纲。
# 
# 要求：
# 1. 严格遵循总纲、世界观、角色设定
# 2. 输出格式参考 templates/03-大纲模板.md
# 3. 输出文件：$PROJECT_DIR/03-分章大纲/第${START_CHAPTER}-${END_CHAPTER}章大纲.md
# 4. 每章必须有明确的爽点和结尾钩子
# 5. 完成后立即通知总策划验收
# "

echo "⚠️  提示：当前使用模板生成模式"
echo "   配置好 novel-plot-planner 智能体后，可以自动完成"
echo ""

OUTPUT_FILE="$PROJECT_DIR/03-分章大纲/第${START_CHAPTER}-${END_CHAPTER}章大纲.md"

sed -e "s/{{小说名}}/$NOVEL_NAME/g" \
    -e "s/{{起始章}}/$START_CHAPTER/g" \
    -e "s/{{结束章}}/$END_CHAPTER/g" \
    -e "s/{{日期}}/$TODAY/g" \
    "$TEMPLATES_DIR/03-大纲模板.md" > "$OUTPUT_FILE"

echo "✅ 大纲模板已生成"
echo ""
echo "📄 文件: $OUTPUT_FILE"
echo ""
echo "=============================================="
echo "📝 下一步操作："
echo "1. 编辑 $OUTPUT_FILE，完成详细大纲"
echo "2. 确认无误后，运行：$SCRIPT_DIR/step4-write.sh $PROJECT_DIR $CHAPTER_RANGE"
echo ""
