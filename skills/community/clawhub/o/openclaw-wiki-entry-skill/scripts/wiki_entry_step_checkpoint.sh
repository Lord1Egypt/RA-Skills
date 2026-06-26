#!/bin/bash
set -u

VAULT="${OPENCLAW_VAULT:-$(pwd)}"
STATE_DIR="${WIKI_ENTRY_STATE_DIR:-$VAULT/.openclaw/state}"
SESSION_FILE="$STATE_DIR/wiki_entry_session.json"

STEP=""
STATUS=""
AUDIT_CMD=""
NOTE=""
SESSION_ID=""

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
      STATE_DIR="${WIKI_ENTRY_STATE_DIR:-$VAULT/.openclaw/state}"
      SESSION_FILE="$STATE_DIR/wiki_entry_session.json"
      shift 2 ;;
    *)
      echo "未知参数: $1"
      exit 1 ;;
  esac
done

if [ -z "$STEP" ] || [ -z "$STATUS" ]; then
  echo "用法: wiki_entry_step_checkpoint.sh --step <1-12> --status <pending|done|blocked|awaiting_user> [--audit-cmd <cmd>] [--note <text>]"
  exit 1
fi

case "$STATUS" in
  pending|done|blocked|awaiting_user) ;;
  *)
    echo "status 非法: $STATUS"
    exit 1 ;;
esac

if ! [[ "$STEP" =~ ^[0-9]+$ ]] || [ "$STEP" -lt 1 ] || [ "$STEP" -gt 12 ]; then
  echo "step 必须是 1-12 的整数"
  exit 1
fi

mkdir -p "$STATE_DIR"

if [ -z "$SESSION_ID" ]; then
  if [ -f "$SESSION_FILE" ]; then
    SESSION_ID=$(grep -m1 '"session_id"' "$SESSION_FILE" | sed -E 's/.*"session_id"[[:space:]]*:[[:space:]]*"([^"]+)".*/\1/')
  fi
fi

if [ -z "$SESSION_ID" ]; then
  SESSION_ID="$(date +%Y%m%d-%H%M%S)-$$"
fi

STATE_FILE="$STATE_DIR/wiki_entry_${SESSION_ID}.tsv"

get_status() {
  local step_no="$1"
  if [ ! -f "$STATE_FILE" ]; then
    echo "pending"
    return
  fi
  local line
  line=$(grep -E "^${step_no}[[:space:]]" "$STATE_FILE" | tail -n1 || true)
  if [ -z "$line" ]; then
    echo "pending"
  else
    echo "$line" | cut -f2
  fi
}

if [ "$STATUS" = "done" ]; then
  prev=1
  while [ "$prev" -lt "$STEP" ]; do
    s=$(get_status "$prev")
    if [ "$s" != "done" ]; then
      echo "❌ 防跳步: Step $STEP 不能标记 done，因为 Step $prev 当前是 $s"
      exit 1
    fi
    prev=$((prev + 1))
  done

  if [ -n "$AUDIT_CMD" ]; then
    echo "[micro-audit] $AUDIT_CMD"
    bash -lc "$AUDIT_CMD"
    rc=$?
    if [ "$rc" -ne 0 ]; then
      echo "❌ micro-audit 失败，Step $STEP 不能标记 done"
      exit 2
    fi
  else
    echo "⚠️  Step $STEP 标记 done 但未提供 --audit-cmd"
  fi
fi

TS="$(date '+%Y-%m-%d %H:%M:%S')"
SAFE_NOTE=$(printf '%s' "$NOTE" | tr '\t\n' '  ')

echo -e "${STEP}\t${STATUS}\t${TS}\t${SAFE_NOTE}" >> "$STATE_FILE"

echo "✅ 已记录: session=$SESSION_ID step=$STEP status=$STATUS"
echo "State file: $STATE_FILE"
echo ""
echo "=== 进度图 ==="
for i in $(seq 1 12); do
  s=$(get_status "$i")
  mark=" "
  [ "$s" = "done" ] && mark="✓"
  [ "$s" = "blocked" ] && mark="!"
  [ "$s" = "awaiting_user" ] && mark="?"
  printf "[%s] Step %02d: %s\n" "$mark" "$i" "$s"
done

exit 0
