#!/bin/bash
set -eu

VAULT="${OPENCLAW_VAULT:-$(pwd)}"
STATE_DIR="${COMPILE_STATE_DIR:-$VAULT/.openclaw/state}"
RUN_ROOT="${COMPILE_TASK_RUN_ROOT:-$STATE_DIR/compile/runs}"
MAX_RUN_FILES="${COMPILE_RUN_MAX_FILES:-500}"
RETENTION_DAYS="${COMPILE_RUN_RETENTION_DAYS:-14}"
TASK_ID=""
TARGET_DOC=""
FINAL_STATUS=""
ERRORS="[]"
QUERY_HISTORY_CALLS="[]"
STEPS="[]"

cleanup_runs() {
  [ -d "$RUN_ROOT" ] || return 0

  find "$RUN_ROOT" -type f -name '*.log' -mtime +"$RETENTION_DAYS" -delete 2>/dev/null || true

  local count extra
  count="$(find "$RUN_ROOT" -type f -name '*.log' 2>/dev/null | wc -l | tr -d ' ')"
  [ "$count" -le "$MAX_RUN_FILES" ] && return 0

  extra=$((count - MAX_RUN_FILES))
  find "$RUN_ROOT" -type f -name '*.log' -exec stat -f '%m %N' {} \; 2>/dev/null \
    | sort -n \
    | head -n "$extra" \
    | cut -d' ' -f2- \
    | while IFS= read -r old_file; do
        rm -f "$old_file"
      done
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --task-id)
      TASK_ID="$2"; shift 2 ;;
    --target-doc)
      TARGET_DOC="$2"; shift 2 ;;
    --final-status)
      FINAL_STATUS="$2"; shift 2 ;;
    --errors)
      ERRORS="$2"; shift 2 ;;
    --query-history-calls)
      QUERY_HISTORY_CALLS="$2"; shift 2 ;;
    --steps)
      STEPS="$2"; shift 2 ;;
    *)
      echo "未知参数: $1"
      exit 1 ;;
  esac
done

[ -z "$TASK_ID" ] && TASK_ID="$(date +%Y%m%d-%H%M%S)-compile"
DAY_DIR="$RUN_ROOT/$(date +%Y-%m-%d)"
mkdir -p "$DAY_DIR"
OUT="$DAY_DIR/${TASK_ID}.log"

cat > "$OUT" <<EOF
{
  "task_id": "$TASK_ID",
  "time": "$(date '+%Y-%m-%d %H:%M:%S')",
  "target_doc": "$TARGET_DOC",
  "steps": $STEPS,
  "errors": $ERRORS,
  "query_history_calls": $QUERY_HISTORY_CALLS,
  "final_status": "$FINAL_STATUS"
}
EOF

cleanup_runs

echo "✅ task log written: $OUT"
exit 0
