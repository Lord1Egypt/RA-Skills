#!/bin/bash
# next-id.sh - Get next available TASK ID
# Scans active/ and archived/ for maximum ID, returns next
#
# Usage: next-id.sh [TASK_DIR]
#   TASK_DIR defaults to ~/.openclaw/workspace/kinema-tasks

TASK_DIR="${1:-$HOME/.openclaw/workspace/kinema-tasks}"
max_id=0

for dir in "$TASK_DIR/active" "$TASK_DIR/archived"; do
  [ -d "$dir" ] || continue
  for f in "$dir"/TASK-*.md; do
    [ -f "$f" ] || continue
    basename_f=$(basename "$f" .md)
    id="${basename_f#TASK-}"
    # Validate numeric
    if [[ "$id" =~ ^[0-9]+$ ]]; then
      [ "$id" -gt "$max_id" ] 2>/dev/null && max_id=$id
    fi
  done
done

printf "TASK-%05d\n" $((max_id + 1))
