#!/usr/bin/env bash
# session-health-watchdog.sh — Detect bloated sessions, stale locks, and stuck crons
# Patterns: Exception Handling (12), Goal Monitoring (11), Evaluation & Monitoring (19)
# Run via cron every 30 min. Alerts on Telegram when thresholds are breached.
set -uo pipefail

SESSIONS_DIR="$HOME/.openclaw/agents/main/sessions"
SESSIONS_JSON="$SESSIONS_DIR/sessions.json"
CRON_FILE="$HOME/.openclaw/cron/jobs.json"
AGENTS_MD="$HOME/.openclaw/workspace/AGENTS.md"
BOOTSTRAP_LIMIT=20000
BOOTSTRAP_WARN_PCT=80
SESSION_SIZE_WARN_MB=5
LOCK_AGE_WARN_SEC=600  # 10 minutes
CRON_STUCK_SEC=300      # 5 minutes

ALERTS=()
WARN_COUNT=0
CRIT_COUNT=0

add_alert() {
  local severity="$1" msg="$2"
  ALERTS+=("[$severity] $msg")
  case "$severity" in
    CRIT) ((CRIT_COUNT++)) ;;
    WARN) ((WARN_COUNT++)) ;;
  esac
}

# ── 1. Session file sizes ────────────────────────────────────────────
while IFS= read -r f; do
  SIZE_BYTES=$(stat -f%z "$f" 2>/dev/null || echo 0)
  SIZE_MB=$(( SIZE_BYTES / 1048576 ))
  if [[ "$SIZE_MB" -ge "$SESSION_SIZE_WARN_MB" ]]; then
    BASENAME=$(basename "$f" .jsonl)
    SESSION_KEY=$(python3 -c "
import json, sys
with open('$SESSIONS_JSON') as f:
    d = json.load(f)
for k, v in d.items():
    if v.get('sessionId','') == '$BASENAME':
        print(k); break
" 2>/dev/null || echo "unknown")
    if [[ "$SIZE_MB" -ge 10 ]]; then
      add_alert "CRIT" "Session ${SIZE_MB}MB: $SESSION_KEY ($BASENAME) — compaction will timeout"
    else
      add_alert "WARN" "Session ${SIZE_MB}MB: $SESSION_KEY ($BASENAME)"
    fi
  fi
done < <(find "$SESSIONS_DIR" -name "*.jsonl" -not -name "*.lock" 2>/dev/null)

# ── 2. Stale locks ──────────────────────────────────────────────────
NOW=$(date +%s)
while IFS= read -r lockfile; do
  LOCK_CREATED=$(python3 -c "
import json
with open('$lockfile') as f:
    d = json.load(f)
import datetime
ts = d.get('createdAt','')
if ts:
    from datetime import datetime as dt, timezone
    t = dt.fromisoformat(ts.replace('Z','+00:00'))
    print(int(t.timestamp()))
else:
    print(0)
" 2>/dev/null || echo 0)
  if [[ "$LOCK_CREATED" -gt 0 ]]; then
    AGE=$(( NOW - LOCK_CREATED ))
    if [[ "$AGE" -ge "$LOCK_AGE_WARN_SEC" ]]; then
      LOCK_PID=$(python3 -c "import json; print(json.load(open('$lockfile')).get('pid','?'))" 2>/dev/null || echo "?")
      BASENAME=$(basename "$lockfile" .jsonl.lock)
      AGE_MIN=$(( AGE / 60 ))
      if [[ "$AGE" -ge 1800 ]]; then
        add_alert "CRIT" "Lock held ${AGE_MIN}m on $BASENAME (PID $LOCK_PID) — session likely stuck"
      else
        add_alert "WARN" "Lock held ${AGE_MIN}m on $BASENAME (PID $LOCK_PID)"
      fi
    fi
  fi
done < <(find "$SESSIONS_DIR" -name "*.lock" 2>/dev/null)

# ── 3. Cron jobs stuck on main lane ─────────────────────────────────
if [[ -f "$CRON_FILE" ]]; then
  MAIN_LANE_CRONS=$(python3 -c "
import json
with open('$CRON_FILE') as f:
    data = json.load(f)
for job in data.get('jobs', []):
    if not job.get('enabled', True):
        continue
    sk = job.get('sessionKey', '')
    if sk == 'agent:main:main':
        running = job.get('state', {}).get('runningAtMs', 0)
        print(f\"{job.get('name','unnamed')}|{sk}|{running}\")
" 2>/dev/null)
  while IFS='|' read -r name sk running_ms; do
    [[ -z "$name" ]] && continue
    add_alert "CRIT" "Cron '$name' uses session agent:main:main — BLOCKS interactive messages. Must use isolated session."
    if [[ "$running_ms" -gt 0 ]]; then
      RUNNING_SEC=$(( ($(date +%s) * 1000 - running_ms) / 1000 ))
      if [[ "$RUNNING_SEC" -gt "$CRON_STUCK_SEC" ]]; then
        add_alert "CRIT" "Cron '$name' has been running for ${RUNNING_SEC}s — stuck"
      fi
    fi
  done <<< "$MAIN_LANE_CRONS"
fi

# ── 4. Bootstrap budget ─────────────────────────────────────────────
if [[ -f "$AGENTS_MD" ]]; then
  AGENTS_SIZE=$(wc -c < "$AGENTS_MD" | tr -d ' ')
  AGENTS_PCT=$(( AGENTS_SIZE * 100 / BOOTSTRAP_LIMIT ))
  if [[ "$AGENTS_PCT" -ge 95 ]]; then
    add_alert "CRIT" "AGENTS.md at ${AGENTS_PCT}% of bootstrap limit (${AGENTS_SIZE}/${BOOTSTRAP_LIMIT} chars) — will truncate"
  elif [[ "$AGENTS_PCT" -ge "$BOOTSTRAP_WARN_PCT" ]]; then
    add_alert "WARN" "AGENTS.md at ${AGENTS_PCT}% of bootstrap limit (${AGENTS_SIZE}/${BOOTSTRAP_LIMIT} chars)"
  fi
fi

# ── 5. Recent gateway errors (last 15 min) ──────────────────────────
ERR_LOG="$HOME/.openclaw/logs/gateway.err.log"
if [[ -f "$ERR_LOG" ]]; then
  RECENT_STUCK=$(grep "stuck session" "$ERR_LOG" 2>/dev/null | tail -20 | while read -r line; do
    TS=$(echo "$line" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}' | head -1)
    if [[ -n "$TS" ]]; then
      LOG_EPOCH=$(date -j -f "%Y-%m-%dT%H:%M" "$TS" +%s 2>/dev/null || echo 0)
      if [[ $(( NOW - LOG_EPOCH )) -lt 900 ]]; then
        echo "$line"
      fi
    fi
  done)
  STUCK_COUNT=$(echo "$RECENT_STUCK" | grep -c "stuck session" 2>/dev/null || true)
  STUCK_COUNT=${STUCK_COUNT##*$'\n'}
  STUCK_COUNT=${STUCK_COUNT:-0}
  if [[ "$STUCK_COUNT" -gt 3 ]]; then
    add_alert "WARN" "${STUCK_COUNT} stuck session warnings in last 15 min"
  fi
fi

# ── Output ──────────────────────────────────────────────────────────
if [[ ${#ALERTS[@]} -eq 0 ]]; then
  echo "Session health: all clear"
  echo "Sessions checked: $(find "$SESSIONS_DIR" -name "*.jsonl" -not -name "*.lock" 2>/dev/null | wc -l | tr -d ' ')"
  [[ -f "$AGENTS_MD" ]] && echo "AGENTS.md: ${AGENTS_PCT}% of limit"
  exit 0
fi

echo "SESSION HEALTH WATCHDOG — ${CRIT_COUNT} critical, ${WARN_COUNT} warnings"
echo ""
for alert in "${ALERTS[@]}"; do
  echo "  $alert"
done
echo ""
echo "Run 'openclaw doctor' for full diagnostics."
exit 1
