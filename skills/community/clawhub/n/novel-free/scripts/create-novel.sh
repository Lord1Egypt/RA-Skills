#!/usr/bin/env bash
#
# novel-free 项目创建包装脚本
# 将项目创建在用户指定的外部目录，避免污染技能目录
#

set -e

SKILL_DIR="/root/.openclaw/workspace/skills/novel-free"
DEFAULT_EXTERNAL_DIR="/root/.openclaw/workspace/novels"

echo "🎬 novel-free 项目创建脚本"
echo "📁 默认项目目录: $DEFAULT_EXTERNAL_DIR"
echo ""

if [ $# -eq 0 ]; then
    echo "用法: $0 <项目名称> [自定义项目路径]"
    echo ""
    echo "示例:"
    echo "  $0 my-novel                          # 使用默认目录"
    echo "  $0 my-novel ~/Documents/novels       # 使用自定义目录"
    echo ""
    echo "项目命名规则: 只允许英文字母、数字、下划线、连字符"
    echo "例如: '修仙传' → 'xiu-xian-zhuan'"
    exit 1
fi

PROJECT_NAME="$1"
CUSTOM_DIR="${2:-$DEFAULT_EXTERNAL_DIR}"

# 检查项目名称合法性
if [[ ! "$PROJECT_NAME" =~ ^[a-zA-Z0-9_-]+$ ]]; then
    echo "❌ 错误: 项目名称只能包含英文字母、数字、下划线、连字符"
    echo "💡 提示: 中文名请转为拼音，例如 '修仙传' → 'xiu-xian-zhuan'"
    exit 1
fi

# 确保外部目录存在
mkdir -p "$CUSTOM_DIR"

echo "📦 准备创建项目: $PROJECT_NAME"
echo "📍 项目将存放在: $CUSTOM_DIR/$PROJECT_NAME"

# 调用原始脚本
"$SKILL_DIR/scripts/init-project.sh" "$PROJECT_NAME" "$CUSTOM_DIR"

echo ""
echo "✅ 项目创建完成！"
echo "📋 下一步:"
echo "   1. 编辑 $CUSTOM_DIR/$PROJECT_NAME/meta/project.md"
echo "   2. 开始 Phase 1 创作流程"