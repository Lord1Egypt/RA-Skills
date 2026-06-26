#!/bin/bash
set -u

VAULT="${OPENCLAW_VAULT:-$(pwd)}"
RUN_ROOT="${WIKI_ENTRY_TASK_RUN_ROOT:-$VAULT/Openclaw/Ops/wiki-entry/runs}"
TASK_ID=""
TARGET_DOC=""
TARGET_WIKI=""
PATH_TYPE=""
FINAL_STATUS=""
ERROR_MSG=""

while [ "$#" -gt 0 ]; do
  case "$1" in
    --task-id)
      TASK_ID="$2"; shift 2 ;;
    --target-doc)
      TARGET_DOC="$2"; shift 2 ;;
    --target-wiki)
      TARGET_WIKI="$2"; shift 2 ;;
    --path)
      PATH_TYPE="$2"; shift 2 ;;
    --final-status)
      FINAL_STATUS="$2"; shift 2 ;;
    --error)
      ERROR_MSG="$2"; shift 2 ;;
    *)
      echo "未知参数: $1"
      exit 1 ;;
  esac
done

if [ -z "$TASK_ID" ]; then
  TASK_ID="$(date +%Y%m%d-%H%M%S)-wiki-entry"
fi

DAY_DIR="$RUN_ROOT/$(date +%Y-%m-%d)"
mkdir -p "$DAY_DIR"
OUT="$DAY_DIR/${TASK_ID}.log"

cat > "$OUT" <<EOF
{
  "task_id": "$TASK_ID",
  "time": "$(date '+%Y-%m-%d %H:%M:%S')",
  "target_doc": "$TARGET_DOC",
  "target_wiki": "$TARGET_WIKI",
  "path": "$PATH_TYPE",
  "final_status": "$FINAL_STATUS",
  "error": "$ERROR_MSG"
}
EOF

echo "✅ task log written: $OUT"
exit 0
