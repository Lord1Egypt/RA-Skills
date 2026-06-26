#!/bin/bash
# Kindle Monitor hook forwarder
# Usage in settings.json:
#   "command": "~/.claude/kindle-monitor/notify.sh PreToolUse"
#
# Reads hook JSON from stdin, adds event name, POSTs to local monitor.
# Pass-through: writes stdin to stdout so it doesn't break other hooks.

EVENT="${1:-Unknown}"
PORT="${KINDLE_MONITOR_PORT:-8787}"

# Read all stdin
INPUT=$(cat)

# Pass-through stdin to stdout so chained hooks/Claude get the original payload
printf '%s' "$INPUT"

# Best-effort POST in background; never block Claude Code, never error out
(
  if [ -z "$INPUT" ]; then
    INPUT="{}"
  fi
  # Inject event name into JSON (override any existing "event" key)
  PAYLOAD=$(printf '%s' "$INPUT" | python3 -c "
import json,sys
try:
    d = json.loads(sys.stdin.read() or '{}')
except Exception:
    d = {}
d['event'] = '$EVENT'
print(json.dumps(d, ensure_ascii=False))
" 2>/dev/null)

  if [ -n "$PAYLOAD" ]; then
    curl -s -m 1 -X POST -H "Content-Type: application/json" \
      --data "$PAYLOAD" "http://localhost:$PORT/event" > /dev/null 2>&1 || true
  fi
) &

exit 0
