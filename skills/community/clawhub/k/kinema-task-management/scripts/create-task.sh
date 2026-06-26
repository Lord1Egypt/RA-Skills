#!/bin/bash
# create-task.sh - Create a new task file with template
#
# Usage: create-task.sh <task_id> <title> <priority> <domain> [due_date] [description]
#   task_id:   TASK-XXXXX (from next-id.sh)
#   title:     Task title
#   priority:  urgent | normal | low
#   domain:    e.g. OpenClaw生态, 其他项目, 生活
#   due_date:  YYYY-MM-DD or — (optional, default —)
#   description: Task description (optional, default empty)
#
# Creates file in TASK_DIR/active/

TASK_DIR="${TASK_DIR:-$HOME/.openclaw/workspace/kinema-tasks}"
ACTIVE_DIR="$TASK_DIR/active"

TASK_ID="$1"
TITLE="$2"
PRIORITY="$3"
DOMAIN="$4"
DUE_DATE="${5:-—}"
DESCRIPTION="${6:-}"
TODAY=$(date +%Y-%m-%d)

if [ -z "$TASK_ID" ] || [ -z "$TITLE" ] || [ -z "$PRIORITY" ] || [ -z "$DOMAIN" ]; then
  echo "Usage: create-task.sh <task_id> <title> <priority> <domain> [due_date] [description]" >&2
  exit 1
fi

# Ensure active directory exists
mkdir -p "$ACTIVE_DIR"

FILE="$ACTIVE_DIR/${TASK_ID}.md"

if [ -f "$FILE" ]; then
  echo "Error: $FILE already exists" >&2
  exit 1
fi

cat > "$FILE" << EOF
# ${TASK_ID}: ${TITLE}

## Metadata

| 字段 | 值 |
|------|-----|
| 状态 | Pending |
| 优先级 | ${PRIORITY} |
| 领域 | ${DOMAIN} |
| 截止日期 | ${DUE_DATE} |
| 创建时间 | ${TODAY} |
| 最后更新 | ${TODAY} |

## 描述

${DESCRIPTION}

## Changelog

| 时间 | 变更 |
|------|------|
| ${TODAY} | 创建任务，状态: Pending |
EOF

echo "Created: $FILE"
