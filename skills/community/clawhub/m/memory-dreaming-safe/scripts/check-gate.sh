#!/bin/bash
# check-gate.sh — Check if dream conditions are met
#
# Reads the last dream timestamp from dreaming-log.md and compares
# against the configured minimum hours. Exits 0 if gate passes, 1 if not.
#
# Usage: bash scripts/check-gate.sh [--min-hours 6] [--log path/to/dreaming-log.md]

set -euo pipefail

MIN_HOURS="${1:-6}"
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
LOG_FILE="${2:-$WORKSPACE/memory/dreaming-log.md}"

if [ ! -f "$LOG_FILE" ]; then
  echo "PASS: No dreaming log found — first dream"
  exit 0
fi

# Extract the most recent timestamp from the log (format: ## YYYY-MM-DD HH:MM)
LAST_DREAM=$(grep -oP '^## \K\d{4}-\d{2}-\d{2} \d{2}:\d{2}' "$LOG_FILE" | tail -1)

if [ -z "$LAST_DREAM" ]; then
  echo "PASS: No previous dream timestamp found"
  exit 0
fi

# Calculate hours since last dream
LAST_EPOCH=$(date -j -f "%Y-%m-%d %H:%M" "$LAST_DREAM" "+%s" 2>/dev/null || date -d "$LAST_DREAM" "+%s" 2>/dev/null)
NOW_EPOCH=$(date "+%s")
HOURS_SINCE=$(( (NOW_EPOCH - LAST_EPOCH) / 3600 ))

if [ "$HOURS_SINCE" -ge "$MIN_HOURS" ]; then
  echo "PASS: ${HOURS_SINCE}h since last dream (gate: ${MIN_HOURS}h)"
  exit 0
else
  echo "SKIP: Only ${HOURS_SINCE}h since last dream (gate: ${MIN_HOURS}h)"
  exit 1
fi
