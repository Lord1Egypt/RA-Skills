#!/usr/bin/env bash
set -euo pipefail

SKILL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
LOG_DIR="$WORKSPACE/logs"
LOG_FILE="$LOG_DIR/last30days-watchlist.log"

mkdir -p "$LOG_DIR"

{
  echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] Running last30days watchlist run-all"
  cd "$SKILL_ROOT"
  python3 "$SKILL_ROOT/scripts/watchlist.py" run-all
  echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] Done"
} >> "$LOG_FILE" 2>&1
