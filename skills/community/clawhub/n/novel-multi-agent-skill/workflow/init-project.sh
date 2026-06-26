#!/bin/bash
# ==============================================
# 多智能体小说创作系统 - 项目初始化脚本
# ==============================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
TEMPLATES_DIR="$SKILL_DIR/templates"

if [ $# -lt 1 ]; then
    echo "用法: $0 <项目目录> [小说名]"
    echo "示例: $0 ../my-novel \"深夜便利店\""
    exit 1
fi

PROJECT_DIR="$1"
NOVEL_NAME="${2:-未命名小说}"
PROJECT_ID="NDP-$(date +%Y%m%d-%H%M%S)"

echo "=============================================="
echo "📚 多智能体小说创作系统 - 项目初始化"
echo "=============================================="
echo ""
echo "📁 项目目录: $PROJECT_DIR"
echo "📖 小说名: $NOVEL_NAME"
echo "🆔 项目编号: $PROJECT_ID"
echo ""

# 创建目录结构
echo "📂 创建目录结构..."
mkdir -p "$PROJECT_DIR"
mkdir -p "$PROJECT_DIR/03-分章大纲"
mkdir -p "$PROJECT_DIR/04-正文初稿"
mkdir -p "$PROJECT_DIR/05-评审报告"
mkdir -p "$PROJECT_DIR/06-最终定稿"
mkdir -p "$PROJECT_DIR/99-完整小说"
mkdir -p "$PROJECT_DIR/_temp_"
echo "✅ 目录结构创建完成"

# 复制总纲模板
echo "📋 生成项目总纲..."
TODAY=$(date +%Y-%m-%d)
sed -e "s/{{小说名}}/$NOVEL_NAME/g" \
    -e "s/{{项目编号}}/$PROJECT_ID/g" \
    -e "s/{{日期}}/$TODAY/g" \
    "$TEMPLATES_DIR/00-总纲模板.md" > "$PROJECT_DIR/00-总纲.md"
echo "✅ 项目总纲已生成"

# 创建README
cat > "$PROJECT_DIR/README.md" << EOF
# 📚 $NOVEL_NAME 创作项目

## 项目信息
- **项目编号**: $PROJECT_ID
- **创建时间**: $TODAY
- **创作系统**: 多智能体小说创作系统 v1.0

## 目录说明

\`\`\`
00-总纲.md              # 项目总纲（用户确认后启动）
01-世界观设定.md        # 世界观设定（完成后不变）
02-角色档案.md          # 角色设定（完成后不变）
03-分章大纲/           # 大纲分批次存放
04-正文初稿/           # 正文初稿存放
05-评审报告/           # 评审意见存放
06-最终定稿/           # 最终定稿存放
99-完整小说/           # 合并后的完整文件
_temp_/                # 临时文件（自动清理）
\`\`\`

## 创作流程

1. ✅ 编辑并确认 00-总纲.md
2. 🌍 运行 step1-world.sh 生成世界观
3. 👥 运行 step2-character.sh 生成角色
4. 📑 运行 step3-plot.sh 生成大纲
5. ✍️ 运行 step4-write.sh 创作正文
6. 🔍 运行 step5-review.sh 质量评审
7. 🔄 重复4-6步，直到完成

## 快速开始

编辑 \`00-总纲.md\` 确认需求后，执行：
\`\`\`bash
cd $(dirname "$SCRIPT_DIR")/workflow
./step1-world.sh $PROJECT_DIR
\`\`\`

---
**祝您创作愉快！** 🎉
EOF

echo ""
echo "=============================================="
echo "✅ 项目初始化完成！"
echo "=============================================="
echo ""
echo "📝 下一步操作："
echo "1. 编辑 $PROJECT_DIR/00-总纲.md，确认创作需求"
echo "2. 确认无误后，运行：$SCRIPT_DIR/step1-world.sh $PROJECT_DIR"
echo ""
