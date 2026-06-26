#!/bin/bash
# 每周总结脚本

if [ -z "$1" ]; then
  echo "用法: $0 <project-name>"
  exit 1
fi

PROJECT_NAME="$1"
PROJECT_DIR="/root/.openclaw/projects/$PROJECT_NAME"
TEMPLATE_DIR="/root/.openclaw/skills/multi-agent-memory/templates"
WEEK=$(date +'%Y-W%V')
YEAR=$(date +'%Y')
WEEK_NUM=$(date +'%V')
START_DATE=$(date -d "monday this week" +'%Y-%m-%d')
END_DATE=$(date -d "sunday this week" +'%Y-%m-%d')
DATE_TIME=$(date +'%Y-%m-%d %H:%M')

echo "=== 生成周报: $PROJECT_NAME - $WEEK ==="

# 1. 创建周报文件
WEEKLY_FILE="$PROJECT_DIR/weekly/$WEEK.md"
sed "s/{YEAR}/$YEAR/g; s/{WEEK}/$WEEK_NUM/g; s/{START_DATE}/$START_DATE/g; s/{END_DATE}/$END_DATE/g; s/{PROJECT_NAME}/$PROJECT_NAME/g; s/{DATE} {TIME}/$DATE_TIME/g" \
  "$TEMPLATE_DIR/weekly.md.template" > "$WEEKLY_FILE"

echo "✅ 周报已创建: $WEEKLY_FILE"
echo ""
echo "下一步："
echo "1. 编辑 $WEEKLY_FILE 填写本周工作"
echo "2. 更新 $PROJECT_DIR/milestones/milestones.md"
echo "3. 归档本周数据: tar -czf /root/.openclaw/archive/$PROJECT_NAME/$WEEK/status-snapshot.tar.gz $PROJECT_DIR/status/"
