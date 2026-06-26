#!/bin/bash
# archive-task.sh - Move a task from active/ to archived/
#
# Usage: archive-task.sh <task_id> <new_status> [reason]
#   task_id:   TASK-XXXXX
#   new_status: Done | Cancelled
#   reason:    Changelog reason (optional)
#
# Updates status, appends changelog, moves file to archived/

TASK_DIR="${TASK_DIR:-$HOME/.openclaw/workspace/kinema-tasks}"
ACTIVE_DIR="$TASK_DIR/active"
ARCHIVE_DIR="$TASK_DIR/archived"

TASK_ID="$1"
NEW_STATUS="$2"
REASON="${3:-状态变更: $NEW_STATUS → 移入 archived}"
TODAY=$(date +%Y-%m-%d)

if [ -z "$TASK_ID" ] || [ -z "$NEW_STATUS" ]; then
  echo "Usage: archive-task.sh <task_id> <new_status> [reason]" >&2
  echo "  new_status: Done | Cancelled" >&2
  exit 1
fi

if [[ "$NEW_STATUS" != "Done" && "$NEW_STATUS" != "Cancelled" ]]; then
  echo "Error: new_status must be Done or Cancelled" >&2
  exit 1
fi

SRC="$ACTIVE_DIR/${TASK_ID}.md"

if [ ! -f "$SRC" ]; then
  echo "Error: $SRC not found" >&2
  exit 1
fi

# Ensure archive directory exists
mkdir -p "$ARCHIVE_DIR"

# Update status in Metadata
sed -i "s/^| 状态 | .* |$/| 状态 | ${NEW_STATUS} |/" "$SRC"

# Update 最后更新
sed -i "s/^| 最后更新 | .* |$/| 最后更新 | ${TODAY} |/" "$SRC"

# Append changelog entry (before the last line or at end)
echo "| ${TODAY} | ${REASON} |" >> "$SRC"

# Move to archived
DST="$ARCHIVE_DIR/${TASK_ID}.md"
mv "$SRC" "$DST"

echo "Archived: $DST (status: $NEW_STATUS)"
