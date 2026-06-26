#!/bin/bash
# snapshot.sh - Generate and write daily snapshot
#
# Usage: snapshot.sh [TASK_DIR] [date]
#   TASK_DIR: defaults to ~/.openclaw/workspace/kinema-tasks
#   date:     YYYY-MM-DD, defaults to today (Beijing time, UTC+8)
#
# Scans active/ directory and writes snapshot to snapshots/YYYY-MM-DD.md

TASK_DIR="${1:-$HOME/.openclaw/workspace/kinema-tasks}"
ACTIVE_DIR="$TASK_DIR/active"
SNAP_DIR="$TASK_DIR/snapshots"

# Default to Beijing time (UTC+8)
DATE="${2:-$(TZ=Asia/Shanghai date +%Y-%m-%d)}"

mkdir -p "$SNAP_DIR"

SNAP_FILE="$SNAP_DIR/${DATE}.md"

# Collect task data
tasks=""
in_progress=0
pending=0
snoozed=0
total=0

if [ -d "$ACTIVE_DIR" ]; then
  for f in "$ACTIVE_DIR"/TASK-*.md; do
    [ -f "$f" ] || continue
    
    task_id=$(basename "$f" .md)
    
    # Parse metadata fields
    title=$(grep "^# ${task_id}: " "$f" | sed "s/^# ${task_id}: //")
    status=$(grep "^| 状态 | " "$f" | sed 's/^| 状态 | \(.*\) |$/\1/')
    priority=$(grep "^| 优先级 | " "$f" | sed 's/^| 优先级 | \(.*\) |$/\1/')
    domain=$(grep "^| 领域 | " "$f" | sed 's/^| 领域 | \(.*\) |$/\1/')
    due=$(grep "^| 截止日期 | " "$f" | sed 's/^| 截止日期 | \(.*\) |$/\1/')
    
    [ -z "$title" ] && title="(无标题)"
    [ -z "$status" ] && status="Unknown"
    [ -z "$priority" ] && priority="normal"
    [ -z "$domain" ] && domain="—"
    [ -z "$due" ] && due="—"
    
    tasks="${tasks}| ${task_id} | ${title} | ${status} | ${priority} | ${domain} | ${due} |\n"
    
    total=$((total + 1))
    case "$status" in
      "In Progress") in_progress=$((in_progress + 1)) ;;
      "Pending") pending=$((pending + 1)) ;;
      "Snoozed") snoozed=$((snoozed + 1)) ;;
    esac
  done
fi

summary="共 ${total} 个活跃任务 | ${in_progress} In Progress · ${pending} Pending · ${snoozed} Snoozed"

# Write snapshot
cat > "$SNAP_FILE" << EOF
# Snapshot — ${DATE}

> 生成时间：${DATE} 09:00 BJT

## 任务列表

| 任务 | 标题 | 状态 | 优先级 | 领域 | 截止日期 |
|------|------|------|--------|------|---------|
$(echo -e "$tasks")
## 摘要

${summary}
EOF

echo "Snapshot written: $SNAP_FILE"
echo "$summary"
