#!/bin/bash
set -u

VAULT="${OPENCLAW_VAULT:-$(pwd)}"
STATE_DIR="${COMPILE_STATE_DIR:-$VAULT/.openclaw/state}"
SESSION_FILE="$STATE_DIR/compile_session.json"
STEP=""
STATUS=""
AUDIT_CMD=""
NOTE=""
SESSION_ID=""

ORDER=("0" "0.0" "0.1" "0.1.5" "0.3" "1" "1.5" "2" "3" "3.5" "4" "5" "6")

while [ "$#" -gt 0 ]; do
  case "$1" in
    --step)
      STEP="$2"; shift 2 ;;
    --status)
      STATUS="$2"; shift 2 ;;
    --audit-cmd)
      AUDIT_CMD="$2"; shift 2 ;;
    --note)
      NOTE="$2"; shift 2 ;;
    --session-id)
      SESSION_ID="$2"; shift 2 ;;
    --vault)
      VAULT="$2"
      STATE_DIR="${COMPILE_STATE_DIR:-$VAULT/.openclaw/state}"
      SESSION_FILE="$STATE_DIR/compile_session.json"
      shift 2 ;;
    *)
      echo "未知参数: $1"
      exit 1 ;;
  esac
done

if [ -z "$STEP" ] || [ -z "$STATUS" ]; then
  echo "用法: compile_step_checkpoint.sh --step <label> --status <pending|done|blocked|awaiting_user> [--audit-cmd <cmd>] [--note <text>]"
  exit 1
fi

case "$STATUS" in
  pending|done|blocked|awaiting_user) ;;
  *)
    echo "status 非法: $STATUS"
    exit 1 ;;
esac

is_valid_step() {
  local candidate="$1"
  local item
  for item in "${ORDER[@]}"; do
    [ "$item" = "$candidate" ] && return 0
  done
  return 1
}

if ! is_valid_step "$STEP"; then
  echo "非法 step: $STEP"
  exit 1
fi

mkdir -p "$STATE_DIR"

if [ -z "$SESSION_ID" ] && [ -f "$SESSION_FILE" ]; then
  SESSION_ID=$(grep -m1 '"session_id"' "$SESSION_FILE" | sed -E 's/.*"session_id"[[:space:]]*:[[:space:]]*"([^"]+)".*/\1/')
fi
[ -z "$SESSION_ID" ] && SESSION_ID="$(date +%Y%m%d-%H%M%S)-$$"
STATE_FILE="$STATE_DIR/compile_${SESSION_ID}.tsv"

get_status() {
  local target="$1"
  if [ ! -f "$STATE_FILE" ]; then
    echo "pending"
    return
  fi
  local line
  line=$(grep -E "^${target}[[:space:]]" "$STATE_FILE" | tail -n 1 || true)
  if [ -z "$line" ]; then
    echo "pending"
  else
    echo "$line" | cut -f2
  fi
}

if [ "$STATUS" = "done" ]; then
  local_index=-1
  idx=0
  for item in "${ORDER[@]}"; do
    if [ "$item" = "$STEP" ]; then
      local_index=$idx
      break
    fi
    idx=$((idx + 1))
  done

  idx=0
  while [ "$idx" -lt "$local_index" ]; do
    prev="${ORDER[$idx]}"
    prev_status="$(get_status "$prev")"
    if [ "$prev_status" != "done" ]; then
      echo "❌ 防跳步: Step $STEP 不能标记 done，因为 Step $prev 当前是 $prev_status"
      exit 1
    fi
    idx=$((idx + 1))
  done

  if [ -z "$AUDIT_CMD" ]; then
    echo "❌ Step $STEP 标记 done 时必须提供 --audit-cmd"
    exit 1
  fi

  echo "[micro-audit] $AUDIT_CMD"
  bash -lc "$AUDIT_CMD"
  rc=$?
  if [ "$rc" -ne 0 ]; then
    echo "❌ micro-audit 失败，Step $STEP 不能标记 done"
    exit 2
  fi
fi

TS="$(date '+%Y-%m-%d %H:%M:%S')"
SAFE_NOTE=$(printf '%s' "$NOTE" | tr '\t\n' '  ')
printf '%s\t%s\t%s\t%s\n' "$STEP" "$STATUS" "$TS" "$SAFE_NOTE" >> "$STATE_FILE"

echo "✅ 已记录: session=$SESSION_ID step=$STEP status=$STATUS"
echo "State file: $STATE_FILE"
echo ""
echo "=== 进度图 ==="
for item in "${ORDER[@]}"; do
  s="$(get_status "$item")"
  mark=" "
  [ "$s" = "done" ] && mark="✓"
  [ "$s" = "blocked" ] && mark="!"
  [ "$s" = "awaiting_user" ] && mark="?"
  printf '[%s] Step %s: %s\n' "$mark" "$item" "$s"
done

exit 0
