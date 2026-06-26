#!/usr/bin/env bash
set -euo pipefail
source "$(cd "$(dirname "$0")" && pwd)/lib.sh"

DAYS="${1:-7}"
ensure_cache_dirs
latest=$(find "$CACHE_DIR/snapshots" -maxdepth 1 -type f -name '*.tsv' -printf '%T@ %p\n' | sort -n | tail -n1 | cut -d' ' -f2- || true)
if [[ -z "$latest" ]]; then
  echo "No snapshots yet. Run: bash ./scripts/track-changes.sh snapshot"
  exit 1
fi

threshold=$(date -u -d "$DAYS days ago" +%s)
base=$(find "$CACHE_DIR/snapshots" -maxdepth 1 -type f -name '*.tsv' -printf '%T@ %p\n' | sort -n | awk -v t="$threshold" '$1 >= t {print substr($0, index($0,$2)); exit}')
if [[ -z "$base" || "$base" == "$latest" ]]; then
  echo "Not enough snapshots within the last $DAYS days to compare."
  echo "Run another snapshot later: bash ./scripts/track-changes.sh snapshot"
  exit 1
fi

compare_snapshots "$base" "$latest"
