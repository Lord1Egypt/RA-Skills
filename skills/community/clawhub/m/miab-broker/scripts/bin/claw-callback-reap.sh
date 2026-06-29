#!/usr/bin/env bash
# Automatic orphan reaper for the callback registry.
# Marks `pending` callbacks older than CALLBACK_TTL_MIN as failed, cleans them up,
# and logs to logs/callback-reaper.log. Driven by a launchd LaunchAgent (see
# com.openclaw.callback-reaper.plist) or any scheduler. Deterministic — no LLM.
set -euo pipefail

export CLAW_HOME="${CLAW_HOME:-$HOME/.openclaw}"
TTL_MIN="${CALLBACK_TTL_MIN:-120}"
LOG_DIR="$CLAW_HOME/logs"
LOG="$LOG_DIR/callback-reaper.log"
mkdir -p "$LOG_DIR"

ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
if out="$(python3 "$CLAW_HOME/workspace/Skills/miab-broker/scripts/bin/claw-callback.py" sweep --older-than "$TTL_MIN" --fail 2>&1)"; then
  # Compact single-line log entry; only note when something was actually reaped.
  reaped="$(printf '%s' "$out" | python3 -c 'import sys,json;
try:
  d=json.load(sys.stdin); print(d.get("stale_count",0))
except Exception:
  print("?")' 2>/dev/null || echo "?")"
  if [ "$reaped" != "0" ]; then
    echo "[$ts] reaped=$reaped ttl=${TTL_MIN}m :: $(printf '%s' "$out" | tr '\n' ' ')" >> "$LOG"
  else
    echo "[$ts] ok reaped=0 ttl=${TTL_MIN}m" >> "$LOG"
  fi
else
  echo "[$ts] ERROR :: $out" >> "$LOG"
  exit 1
fi
