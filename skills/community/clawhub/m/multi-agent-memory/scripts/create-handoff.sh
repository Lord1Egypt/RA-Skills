#!/bin/bash
# 创建交接文档脚本

if [ -z "$1" ] || [ -z "$2" ]; then
  echo "用法: $0 <project-name> <phase>"
  echo "示例: $0 content-factory Phase1"
  exit 1
fi

PROJECT_NAME="$1"
PHASE="$2"
PROJECT_DIR="/root/.openclaw/projects/$PROJECT_NAME"
TEMPLATE_DIR="/root/.openclaw/skills/multi-agent-memory/templates"
DATE=$(date +'%Y-%m-%d')

echo "=== 创建交接文档: $PROJECT_NAME - $PHASE ==="

# 1. 创建交接文档
HANDOFF_FILE="$PROJECT_DIR/handoffs/$DATE-$PHASE-交接.md"
sed "s/{PROJECT_NAME}/$PROJECT_NAME/g; s/{PHASE}/$PHASE/g; s/{DATE}/$DATE/g" \
  "$TEMPLATE_DIR/handoff.md.template" > "$HANDOFF_FILE"

# 2. 更新 latest.md 符号链接
cd "$PROJECT_DIR/handoffs/"
ln -sf "$DATE-$PHASE-交接.md" latest.md

echo "✅ 交接文档已创建: $HANDOFF_FILE"
echo "✅ latest.md 已更新"
echo ""
echo "下一步："
echo "1. 编辑 $HANDOFF_FILE 填写交接内容"
echo "2. 归档到 archive: cp $HANDOFF_FILE /root/.openclaw/archive/$PROJECT_NAME/$PHASE/handoff.md"
