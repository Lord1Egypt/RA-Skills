#!/bin/bash
# ==============================================
# 多智能体小说创作系统 - 第4步：正文创作
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
echo "✍️  第4步：正文创作（第${START_CHAPTER}-${END_CHAPTER}章）"
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
    exit 1
fi

# 检查大纲文件
OUTLINE_FILE="$PROJECT_DIR/03-分章大纲/第${START_CHAPTER}-${END_CHAPTER}章大纲.md"
if [ ! -f "$OUTLINE_FILE" ]; then
    echo "❌ 错误: 找不到大纲文件"
    echo "   请先运行 step3-plot.sh $PROJECT_DIR $CHAPTER_RANGE"
    exit 1
fi

echo "📋 前置检查通过"
echo "   ✅ 00-总纲.md"
echo "   ✅ 01-世界观设定.md"
echo "   ✅ 02-角色档案.md"
echo "   ✅ $OUTLINE_FILE"
echo ""

TODAY=$(date +%Y-%m-%d)
NOVEL_NAME=$(grep "小说名称" "$PROJECT_DIR/00-总纲.md" | head -1 | sed 's/.*：//' | sed 's/.*- //')

echo "🤖 调用章节写作智能体..."
echo ""

# ==============================================
# 调用智能体的命令（根据你的实际配置调整）
# ==============================================
# 可以循环每一章调用
# for ((i=START_CHAPTER; i<=END_CHAPTER; i++)); do
#     echo "   正在创作第 $i 章..."
#     openclaw agent --agent novel-chapter-writer --message "
#     请为《$NOVEL_NAME》创作第 $i 章正文。
#     
#     要求：
#     1. 严格 1800-2200 字
#     2. 严格遵循大纲、世界观、角色设定
#     3. 每章必须有爽点和结尾钩子
#     4. 输出文件：$PROJECT_DIR/04-正文初稿/第${i}章-初稿.md
#     5. 完成后通知总策划
#     "
# done

echo "⚠️  提示：当前使用模板生成模式"
echo "   配置好 novel-chapter-writer 智能体后，可以自动完成"
echo ""

# 生成每章的模板
for ((i=START_CHAPTER; i<=END_CHAPTER; i++)); do
    OUTPUT_FILE="$PROJECT_DIR/04-正文初稿/第${i}章-初稿.md"
    sed -e "s/{{章节号}}/$i/g" \
        -e "s/{{章节标题}}/第${i}章标题/g" \
        -e "s/{{日期}}/$TODAY/g" \
        "$TEMPLATES_DIR/04-正文模板.md" > "$OUTPUT_FILE"
    echo "   ✅ 第 $i 章模板已生成: $OUTPUT_FILE"
done

echo ""
echo "✅ 所有章节模板生成完成"
echo ""
echo "=============================================="
echo "📝 下一步操作："
echo "1. 编辑 $PROJECT_DIR/04-正文初稿/ 下的文件，完成正文创作"
echo "2. 全部完成后，运行：$SCRIPT_DIR/step5-review.sh $PROJECT_DIR $CHAPTER_RANGE"
echo ""
