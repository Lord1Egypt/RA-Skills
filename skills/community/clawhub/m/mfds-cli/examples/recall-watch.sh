#!/usr/bin/env bash
# Daily delta of MFDS recalls. Saves today's snapshot under recall-snapshots/
# and prints rows that weren't in yesterday's snapshot.
#
# Usage: examples/recall-watch.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CLI="$ROOT/bin/mfds-cli"
SNAP_DIR="${MFDS_SNAP_DIR:-$ROOT/recall-snapshots}"
mkdir -p "$SNAP_DIR"

today="$(date +%F)"
yesterday="$(date -v-1d +%F 2>/dev/null || date -d "yesterday" +%F)"
year="$(date +%Y)"

today_file="$SNAP_DIR/$today.jsonl"
yest_file="$SNAP_DIR/$yesterday.jsonl"

$CLI recall --year "$year" --rows 100 --format jsonl > "$today_file"

if [[ -f "$yest_file" ]]; then
  comm -23 <(sort "$today_file") <(sort "$yest_file")
else
  echo "(no yesterday snapshot — printing today's first 5 rows)" >&2
  head -n 5 "$today_file"
fi
