#!/usr/bin/env bash
# WAL hook (prototype)
# Usage: echo "Human message" | ./wal_hook.sh --source=cli

set -euo pipefail

SOURCE="unknown"
while [ $# -gt 0 ]; do
  case "$1" in
    --source=*) SOURCE="${1#--source=}"; shift;;
    *) shift;;
  esac
done

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
IN=$(cat -)

# Simple trigger detection (expand as needed)
if echo "$IN" | grep -Ei "actually|no,|not|use .* instead|change to|it's|it's not" >/dev/null; then
  echo "[${TIMESTAMP}] Human (source:${SOURCE}]" >> ../../memory/working-buffer.md
  echo "$IN" >> ../../memory/working-buffer.md
  echo "" >> ../../memory/working-buffer.md
  # Also write to SESSION-STATE.md as minimal WAL entry
  echo "- ${TIMESTAMP} | WAL: ${IN}" >> ../../SESSION-STATE.md
else
  # For non-trigger messages still append to working buffer when called from danger zone
  echo "[${TIMESTAMP}] Human (source:${SOURCE}]" >> ../../memory/working-buffer.md
  echo "$IN" >> ../../memory/working-buffer.md
  echo "" >> ../../memory/working-buffer.md
fi

# Exit success
exit 0
