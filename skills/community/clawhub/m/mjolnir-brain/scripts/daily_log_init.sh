#!/bin/bash
# daily_log_init.sh — Initialize today's daily log with a template
# Can be called at session start or via cron

WORKSPACE="${MJOLNIR_BRAIN_WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE/memory"
TODAY=$(date '+%Y-%m-%d')
LOG_FILE="$MEMORY_DIR/${TODAY}.md"

mkdir -p "$MEMORY_DIR"

if [ -f "$LOG_FILE" ]; then
    exit 0  # Already exists
fi

cat > "$LOG_FILE" << EOF
# $TODAY $(date '+%A')

## Summary
*(auto-filled at end of day)*

---

EOF

echo "📝 Created: $LOG_FILE"
