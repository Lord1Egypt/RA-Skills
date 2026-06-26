#!/usr/bin/env bash
# dream-check.sh — Pre-flight check: should we run a dream?
# Exit 0 = should dream, Exit 1 = skip
# Usage: bash scripts/dream-check.sh [workspace_dir] [min_hours]

set -euo pipefail

WORKSPACE="${1:-$HOME/.openclaw/workspace}"
MIN_HOURS="${2:-24}"
LAST_DREAM_FILE="$WORKSPACE/memory/.last_dream"

# Check 1: Does memory/ directory exist?
if [ ! -d "$WORKSPACE/memory" ]; then
  echo "SKIP: no memory/ directory"
  exit 1
fi

# Check 2: How long since last dream?
if [ -f "$LAST_DREAM_FILE" ]; then
  LAST_DREAM=$(cat "$LAST_DREAM_FILE" | tr -d '[:space:]')
  LAST_EPOCH=$(date -d "$LAST_DREAM" +%s 2>/dev/null || echo 0)
  NOW_EPOCH=$(date +%s)
  HOURS_SINCE=$(( (NOW_EPOCH - LAST_EPOCH) / 3600 ))
  
  if [ "$HOURS_SINCE" -lt "$MIN_HOURS" ]; then
    echo "SKIP: last dream was ${HOURS_SINCE}h ago (min: ${MIN_HOURS}h)"
    exit 1
  fi
  echo "CHECK: last dream was ${HOURS_SINCE}h ago — OK"
else
  echo "CHECK: no previous dream — first run"
fi

# Check 3: Are there new daily notes since last dream?
if [ -f "$LAST_DREAM_FILE" ]; then
  NEW_FILES=$(find "$WORKSPACE/memory" -name "202*.md" -newer "$LAST_DREAM_FILE" | wc -l)
else
  NEW_FILES=$(find "$WORKSPACE/memory" -name "202*.md" | wc -l)
fi

if [ "$NEW_FILES" -eq 0 ]; then
  echo "SKIP: no new daily notes since last dream"
  exit 1
fi

echo "CHECK: $NEW_FILES new daily note(s) — OK"

# Check 4: Lock file (prevent concurrent dreams)
LOCK_FILE="$WORKSPACE/memory/.dream_lock"
if [ -f "$LOCK_FILE" ]; then
  LOCK_AGE=$(( ($(date +%s) - $(stat -c %Y "$LOCK_FILE")) / 60 ))
  if [ "$LOCK_AGE" -lt 30 ]; then
    echo "SKIP: dream already running (lock age: ${LOCK_AGE}m)"
    exit 1
  else
    echo "WARN: stale lock file (${LOCK_AGE}m old) — removing"
    rm -f "$LOCK_FILE"
  fi
fi

# All checks passed
echo "READY: dream should run"

# Show stats
MEMORY_LINES=$(wc -l < "$WORKSPACE/MEMORY.md" 2>/dev/null || echo 0)
DAILY_FILES=$(find "$WORKSPACE/memory" -name "202*.md" | wc -l)
JSONL_ENTRIES=$(cat "$WORKSPACE"/memory/self-improving/*.jsonl 2>/dev/null | wc -l || echo 0)

echo ""
echo "Stats:"
echo "  MEMORY.md lines: $MEMORY_LINES"
echo "  Daily note files: $DAILY_FILES"
echo "  Self-improving JSONL entries: $JSONL_ENTRIES"
echo "  New files since last dream: $NEW_FILES"

exit 0
