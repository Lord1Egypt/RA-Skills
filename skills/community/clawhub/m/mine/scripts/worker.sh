#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# Benchmark Worker — background polling & submission loop
# Part of: s1-benchmark-skill
#
# This script runs in the background on OpenClaw. It handles:
#   • Polling the Benchmark API every 15s
#   • Writing received questions to /tmp/awp_q_pending.json
#   • Watching for agent answers at /tmp/awp_answer.json
#   • Submitting answers (or fallback "unknown" before deadline)
#   • Submitting questions written to /tmp/awp_question.json
#   • Refreshing wallet session every 30 minutes
#   • Logging to /tmp/awp_worker.log
#
# The LLM agent handles thinking — this script handles timing.
# ─────────────────────────────────────────────────────────────

set -euo pipefail

# ── paths ───────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASEDIR="$(dirname "$SCRIPT_DIR")"
LOGFILE="/tmp/awp_worker.log"

# 自动检测 awp-wallet 路径（OpenClaw 的 npm link 可能装在不同位置）
if [ -z "${AWP_WALLET:-}" ]; then
  _AWP_BIN="awp-wallet"
  for candidate in \
    "/usr/bin/$_AWP_BIN" \
    "/usr/local/bin/$_AWP_BIN" \
    "$HOME/.local/bin/$_AWP_BIN" \
    "$HOME/.awp/bin/$_AWP_BIN" \
    "$(command -v "$_AWP_BIN" 2>/dev/null)"; do
    if [ -n "$candidate" ] && [ -x "$candidate" ]; then
      AWP_WALLET="$candidate"
      break
    fi
  done
fi
# 最后尝试 node 直接运行
if [ -z "${AWP_WALLET:-}" ]; then
  _NODE_ENTRY="/usr/lib/node_modules/awp-wallet/scripts/wallet-cli.js"
  if [ -f "$_NODE_ENTRY" ]; then
    AWP_WALLET="node $_NODE_ENTRY"
  fi
fi
if [ -z "${AWP_WALLET:-}" ]; then
  echo "[!] awp-wallet not found. Install it or set AWP_WALLET env var." >&2
  exit 1
fi
export AWP_WALLET  # 导出给 benchmark-sign.sh 使用

PENDING_Q="/tmp/awp_q_pending.json"
ANSWER_FILE="/tmp/awp_answer.json"
QUESTION_FILE="/tmp/awp_question.json"

# ── config ──────────────────────────────────────────────────
export BENCHMARK_API_URL="${BENCHMARK_API_URL:-https://tapis1.awp.sh}"
POLL_INTERVAL=15          # seconds between idle polls
TOKEN_REFRESH=1800        # refresh wallet every 30 min (in seconds)
FALLBACK_BUFFER=20        # submit fallback N seconds before deadline
SCORE_CHECK_INTERVAL=300  # check scores every 5 min

# ── state ───────────────────────────────────────────────────
COUNTER=0
LAST_TOKEN_REFRESH=0
LAST_SCORE_CHECK=0

# ── helpers ─────────────────────────────────────────────────

log() {
  echo "[$(date -u '+%H:%M:%S')] $*" | tee -a "$LOGFILE"
}

sign() {
  bash "$BASEDIR/scripts/benchmark-sign.sh" "$@" 2>/dev/null
}

refresh_token() {
  # unlock 需要 WALLET_PASSWORD（由 OpenClaw secret store 注入到环境变量）
  UNLOCK_OUT=$($AWP_WALLET unlock --duration 3600 2>/dev/null) || UNLOCK_OUT=""

  # 解析 sessionToken（awp-wallet 输出 JSON: {"sessionToken":"wlt_xxx", ...}）
  local token
  token=$(echo "$UNLOCK_OUT" | jq -r '.sessionToken // empty' 2>/dev/null)
  if [ -z "$token" ]; then
    # 兼容旧版输出格式
    token=$(echo "$UNLOCK_OUT" | grep -o '"sessionToken":"[^"]*"' | head -1 | cut -d'"' -f4)
  fi
  if [ -n "$token" ]; then
    export AWP_SESSION_TOKEN="$token"
  fi

  # 解析钱包地址（receive 输出 JSON: {"address":"0x...", ...}）
  RECV_OUT=$($AWP_WALLET receive 2>/dev/null) || RECV_OUT=""
  local addr
  addr=$(echo "$RECV_OUT" | jq -r '.address // empty' 2>/dev/null)
  if [ -z "$addr" ]; then
    addr=$(echo "$RECV_OUT" | grep -oi '0x[0-9a-fA-F]\{40\}' | head -1)
  fi
  if [ -n "$addr" ]; then
    export WALLET_ADDRESS="$addr"
  fi

  LAST_TOKEN_REFRESH=$(date +%s)
  log "[TOKEN] wallet session refreshed (addr=${WALLET_ADDRESS:-unknown})"
}

# Parse ISO 8601 / RFC 3339 timestamp to epoch seconds
# Handles both GNU date and Python fallback
parse_timestamp() {
  local ts="$1"
  # Try GNU date first
  date -d "$ts" +%s 2>/dev/null && return
  # Fallback to Python
  python3 -c "
from datetime import datetime, timezone
import sys
ts = sys.argv[1].replace('Z', '+00:00')
dt = datetime.fromisoformat(ts)
print(int(dt.timestamp()))
" "$ts" 2>/dev/null && return
  # Last resort: return 0 (will trigger immediate fallback)
  echo "0"
}

cleanup() {
  log "[WORKER] shutting down..."
  rm -f "$PENDING_Q" "$ANSWER_FILE" "$QUESTION_FILE"
  exit 0
}

trap cleanup SIGTERM SIGINT

# ── init ────────────────────────────────────────────────────

rm -f "$PENDING_Q" "$ANSWER_FILE" "$QUESTION_FILE"
: > "$LOGFILE"

refresh_token
log "=== Benchmark Worker started ==="
log "    BASEDIR=$BASEDIR"
log "    API=$BENCHMARK_API_URL"
log "    WALLET=$WALLET_ADDRESS"
log "    AWP_WALLET=$AWP_WALLET"

# ── main loop ───────────────────────────────────────────────

while true; do
  NOW=$(date +%s)

  # ── token refresh ─────────────────────────────────────────
  if [ $((NOW - LAST_TOKEN_REFRESH)) -ge $TOKEN_REFRESH ]; then
    refresh_token
  fi

  # ── poll ──────────────────────────────────────────────────
  RESULT=$(sign GET /api/v1/poll 2>/dev/null) || RESULT=""

  if [ -z "$RESULT" ]; then
    log "[POLL] no response, retrying in 10s..."
    sleep 10
    continue
  fi

  # ── error handling ────────────────────────────────────────
  ERR=$(echo "$RESULT" | jq -r '.error // empty' 2>/dev/null)

  if [ -n "$ERR" ]; then
    if echo "$ERR" | grep -qi "not registered\|registration denied"; then
      log "[!] wallet not registered on AWP RootNet. exiting."
      exit 1
    fi

    if echo "$ERR" | grep -qi "suspended"; then
      UNSUSPEND=$(echo "$RESULT" | jq -r '.data.unsuspend_at // empty' 2>/dev/null)
      if [ -n "$UNSUSPEND" ]; then
        UNSUSPEND_TS=$(parse_timestamp "$UNSUSPEND")
        WAIT_SECS=$((UNSUSPEND_TS - NOW))
        [ "$WAIT_SECS" -lt 10 ] && WAIT_SECS=60
        log "[POLL] suspended until $UNSUSPEND UTC. waiting ${WAIT_SECS}s..."
        sleep "$WAIT_SECS"
      else
        log "[POLL] suspended. waiting 60s..."
        sleep 60
      fi
      continue
    fi

    log "[!] error: $ERR"
    sleep 10
    continue
  fi

  # ── check for assignment ──────────────────────────────────
  ASSIGNED=$(echo "$RESULT" | jq -r '.data.assigned // empty' 2>/dev/null)

  HAS_ASSIGNMENT=false
  if [ "$ASSIGNED" != "null" ] && [ "$ASSIGNED" != "" ]; then
    QID=$(echo "$RESULT" | jq -r '.data.assigned.question_id // empty' 2>/dev/null)
    if [ -n "$QID" ] && [ "$QID" != "null" ]; then
      HAS_ASSIGNMENT=true
    fi
  fi

  if [ "$HAS_ASSIGNMENT" = true ]; then
    # ── ANSWER MODE ─────────────────────────────────────────
    QUESTION=$(echo "$RESULT" | jq -r '.data.assigned.question // empty' 2>/dev/null)
    DDL=$(echo "$RESULT" | jq -r '.data.assigned.reply_ddl // empty' 2>/dev/null)
    ANSWER_MAXLEN=$(echo "$RESULT" | jq -r '.data.assigned.answer_maxlen // 200' 2>/dev/null)
    Q_REQS=$(echo "$RESULT" | jq -r '.data.assigned.question_requirements // empty' 2>/dev/null)
    A_REQS=$(echo "$RESULT" | jq -r '.data.assigned.answer_requirements // empty' 2>/dev/null)

    log "[POLL] assignment received: Q#$QID"
    log "[SOLVE] \"${QUESTION:0:100}\""

    # Write pending question for the agent to pick up
    jq -n \
      --arg qid "$QID" \
      --arg q "$QUESTION" \
      --arg ddl "$DDL" \
      --arg maxlen "$ANSWER_MAXLEN" \
      --arg qreqs "$Q_REQS" \
      --arg areqs "$A_REQS" \
      '{question_id: $qid, question: $q, reply_ddl: $ddl, answer_maxlen: $maxlen, question_requirements: $qreqs, answer_requirements: $areqs}' \
      > "$PENDING_Q"

    # Wait for the agent to write an answer, or hit the deadline
    DEADLINE_TS=$(parse_timestamp "$DDL")
    FALLBACK_TS=$((DEADLINE_TS - FALLBACK_BUFFER))

    while [ ! -f "$ANSWER_FILE" ]; do
      NOW_INNER=$(date +%s)
      if [ "$NOW_INNER" -ge "$FALLBACK_TS" ]; then
        log "[!] deadline approaching, submitting fallback answer"
        break
      fi
      sleep 2
    done

    # Build and submit the answer
    if [ -f "$ANSWER_FILE" ]; then
      ANS_BODY=$(cat "$ANSWER_FILE")
      rm -f "$ANSWER_FILE"
      log "[SUBMIT] using agent answer"
    else
      # Fallback: submit "unknown" — score 3 is better than timeout score 0
      ANS_BODY=$(jq -n --arg qid "$QID" '{question_id: ($qid | tonumber), valid: true, answer: "unknown"}')
      log "[SUBMIT] fallback answer: \"unknown\""
    fi

    SUBMIT_RESULT=$(sign POST /api/v1/answers "$ANS_BODY" 2>/dev/null) || SUBMIT_RESULT=""
    ACCEPTED=$(echo "$SUBMIT_RESULT" | jq -r '.data.accepted // .accepted // "unknown"' 2>/dev/null)
    log "[SUBMIT] Q#$QID → accepted=$ACCEPTED"

    # Clean up pending question
    rm -f "$PENDING_Q"

    # After answering, loop immediately (no sleep)
    COUNTER=$((COUNTER + 1))
    continue
  fi

  # ── IDLE MODE ─────────────────────────────────────────────
  log "[POLL] idle"

  # Check if agent wrote a question to submit
  if [ -f "$QUESTION_FILE" ]; then
    Q_BODY=$(cat "$QUESTION_FILE")
    rm -f "$QUESTION_FILE"
    log "[ASK] submitting agent question..."
    ASK_RESULT=$(sign POST /api/v1/questions "$Q_BODY" 2>/dev/null) || ASK_RESULT=""
    ASK_QID=$(echo "$ASK_RESULT" | jq -r '.data.question_id // .question_id // empty' 2>/dev/null)
    ASK_ERR=$(echo "$ASK_RESULT" | jq -r '.error // empty' 2>/dev/null)

    if [ -n "$ASK_QID" ] && [ "$ASK_QID" != "null" ]; then
      log "[ASK] Q#$ASK_QID submitted ✓"
    elif [ -n "$ASK_ERR" ]; then
      log "[ASK] error: $ASK_ERR"
    else
      log "[ASK] submission result: $ASK_RESULT"
    fi
  fi

  # ── score check ───────────────────────────────────────────
  NOW=$(date +%s)
  if [ $((NOW - LAST_SCORE_CHECK)) -ge $SCORE_CHECK_INTERVAL ]; then
    log "[SCORES] checking..."
    MY_Q=$(sign GET /api/v1/my/questions 2>/dev/null) || MY_Q=""
    MY_A=$(sign GET /api/v1/my/assignments 2>/dev/null) || MY_A=""

    if [ -n "$MY_Q" ]; then
      echo "$MY_Q" > /tmp/awp_my_questions.json
    fi
    if [ -n "$MY_A" ]; then
      echo "$MY_A" > /tmp/awp_my_assignments.json
    fi

    LAST_SCORE_CHECK=$NOW
    log "[SCORES] updated → /tmp/awp_my_questions.json, /tmp/awp_my_assignments.json"
  fi

  COUNTER=$((COUNTER + 1))
  sleep "$POLL_INTERVAL"
done
