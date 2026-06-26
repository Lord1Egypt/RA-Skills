#!/bin/bash
# ==============================================
# 多智能体小说创作系统 - 第5步：质量评审
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
echo "🔍 第5步：质量评审（第${START_CHAPTER}-${END_CHAPTER}章）"
echo "=============================================="
echo ""
echo "📁 项目目录: $PROJECT_DIR"
echo "📖 章节范围: 第${START_CHAPTER}-${END_CHAPTER}章"
echo ""

# 检查前置文件
for ((i=START_CHAPTER; i<=END_CHAPTER; i++)); do
    DRAFT_FILE="$PROJECT_DIR/04-正文初稿/第${i}章-初稿.md"
    if [ ! -f "$DRAFT_FILE" ]; then
        echo "❌ 错误: 找不到第 $i 章初稿"
        echo "   请先运行 step4-write.sh $PROJECT_DIR $CHAPTER_RANGE"
        exit 1
    fi
done

echo "📋 前置检查通过"
for ((i=START_CHAPTER; i<=END_CHAPTER; i++)); do
    echo "   ✅ 第${i}章-初稿.md"
done
echo ""

TODAY=$(date +%Y-%m-%d)
NOVEL_NAME=$(grep "小说名称" "$PROJECT_DIR/00-总纲.md" | head -1 | sed 's/.*：//' | sed 's/.*- //')

echo "🤖 调用质量评审智能体..."
echo ""

# ==============================================
# 调用智能体的命令（根据你的实际配置调整）
# ==============================================
# openclaw agent --agent novel-quality-reviewer --message "
# 请对《$NOVEL_NAME》第${START_CHAPTER}-${END_CHAPTER}章进行质量评审。
# 
# 要求：
# 1. 按五维度评分标准评分（文笔/人物/情节/逻辑/创意）
# 2. 指出优点、问题、给出具体修改建议
# 3. 检查红线内容和字数
# 4. 输出文件：$PROJECT_DIR/05-评审报告/第${START_CHAPTER}-${END_CHAPTER}章-评审报告.md
# 5. 完成后通知写作智能体按建议优化
# "

echo "⚠️  提示：当前使用模板生成模式"
echo "   配置好 novel-quality-reviewer 智能体后，可以自动完成"
echo ""

OUTPUT_FILE="$PROJECT_DIR/05-评审报告/第${START_CHAPTER}-${END_CHAPTER}章-评审报告.md"

sed -e "s/{{小说名}}/$NOVEL_NAME/g" \
    -e "s/{{起始章}}/$START_CHAPTER/g" \
    -e "s/{{结束章}}/$END_CHAPTER/g" \
    -e "s/{{日期}}/$TODAY/g" \
    -e "s/{{总分}}/待评审/g" \
    "$TEMPLATES_DIR/05-评审模板.md" > "$OUTPUT_FILE"

echo "✅ 评审报告模板已生成"
echo ""
echo "📄 文件: $OUTPUT_FILE"
echo ""
echo "=============================================="
echo "📝 下一步操作："
echo "1. 完成质量评审，填写 $OUTPUT_FILE"
echo "2. 根据评审意见，优化正文，保存到 06-最终定稿/"
echo "3. 完成后，可以开始下一批章节的创作"
echo ""
