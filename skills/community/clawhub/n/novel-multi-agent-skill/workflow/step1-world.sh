#!/bin/bash
# ==============================================
# 多智能体小说创作系统 - 第1步：世界观构建
# ==============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
TEMPLATES_DIR="$SKILL_DIR/templates"
RULES_DIR="$SKILL_DIR/rules"

if [ $# -lt 1 ]; then
    echo "用法: $0 <项目目录>"
    echo "示例: $0 ../my-novel"
    exit 1
fi

PROJECT_DIR="$1"

echo "=============================================="
echo "🌍 第1步：世界观构建"
echo "=============================================="
echo ""
echo "📁 项目目录: $PROJECT_DIR"
echo ""

# 检查总纲是否存在
if [ ! -f "$PROJECT_DIR/00-总纲.md" ]; then
    echo "❌ 错误: 找不到项目总纲文件"
    echo "   请先运行 init-project.sh 初始化项目"
    exit 1
fi

echo "📋 读取项目总纲..."
cat "$PROJECT_DIR/00-总纲.md"
echo ""
echo "=============================================="
echo ""

# 复制世界观模板作为参考
TODAY=$(date +%Y-%m-%d)
NOVEL_NAME=$(grep "小说名称" "$PROJECT_DIR/00-总纲.md" | head -1 | sed 's/.*：//' | sed 's/.*- //')

echo "🤖 调用世界观构建智能体..."
echo ""

# ==============================================
# 调用智能体的命令（根据你的实际配置调整）
# ==============================================
# 方法1：使用 openclaw agent 命令（推荐）
# openclaw agent --agent novel-world-builder --message "
# 请为《$NOVEL_NAME》创作完整的世界观设定。
# 
# 要求：
# 1. 严格遵循 00-总纲.md 中的需求
# 2. 输出格式参考 templates/01-世界观模板.md
# 3. 输出文件：$PROJECT_DIR/01-世界观设定.md
# 4. 完成后立即通知总策划验收
# 
# 总纲内容：
# $(cat "$PROJECT_DIR/00-总纲.md")
# "

# 方法2：如果智能体未配置，先生成模板文件让用户编辑
echo "⚠️  提示：当前使用模板生成模式"
echo "   配置好 novel-world-builder 智能体后，可以自动完成"
echo ""

sed -e "s/{{小说名}}/$NOVEL_NAME/g" \
    -e "s/{{日期}}/$TODAY/g" \
    "$TEMPLATES_DIR/01-世界观模板.md" > "$PROJECT_DIR/01-世界观设定.md"

echo "✅ 世界观模板已生成"
echo ""
echo "📄 文件: $PROJECT_DIR/01-世界观设定.md"
echo ""
echo "=============================================="
echo "📝 下一步操作："
echo "1. 编辑 $PROJECT_DIR/01-世界观设定.md，完成世界观设定"
echo "2. 确认无误后，运行：$SCRIPT_DIR/step2-character.sh $PROJECT_DIR"
echo ""
