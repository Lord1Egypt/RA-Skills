#!/usr/bin/env bash
set -euo pipefail
source "$(cd "$(dirname "$0")" && pwd)/lib.sh"

case "${1:-}" in
  snapshot)
    path=$(snapshot_now)
    echo "Saved snapshot: $path"
    ;;
  list)
    snapshots=$(list_snapshots || true)
    if [[ -z "$snapshots" ]]; then
      echo "No snapshots yet. Run: bash ./scripts/track-changes.sh snapshot"
      exit 1
    fi
    while IFS= read -r file; do
      full="$CACHE_DIR/snapshots/$file"
      echo "$file  $(wc -l < "$full" | tr -d ' ') pages"
    done <<< "$snapshots"
    ;;
  since)
    if [[ -z "${2:-}" ]]; then
      echo "Usage: bash ./scripts/track-changes.sh since <snapshot-prefix|YYYY-MM-DD>"
      exit 1
    fi
    latest=$(find "$CACHE_DIR/snapshots" -maxdepth 1 -type f -name '*.tsv' | sort | tail -n1 || true)
    if [[ -z "$latest" ]]; then
      echo "No snapshots yet. Run: bash ./scripts/track-changes.sh snapshot"
      exit 1
    fi
    ref="${2:-}"
    older=""
    if older=$(resolve_snapshot "$ref" 2>/dev/null); then
      :
    else
      cutoff=$(date -u -d "$ref" +%s 2>/dev/null || true)
      if [[ -n "$cutoff" ]]; then
        older=$(find "$CACHE_DIR/snapshots" -maxdepth 1 -type f -name '*.tsv' -printf '%T@ %p\n' | sort -n | awk -v t="$cutoff" '$1 >= t {print substr($0, index($0,$2)); exit}')
      fi
    fi
    if [[ -z "$older" ]]; then
      echo "Could not resolve snapshot or date: $ref"
      exit 1
    fi
    if [[ "$older" == "$latest" ]]; then
      echo "Only one matching snapshot is available, nothing to compare yet."
      echo "Run another snapshot later: bash ./scripts/track-changes.sh snapshot"
      exit 1
    fi
    compare_snapshots "$older" "$latest"
    ;;
  *)
    echo "Usage: bash ./scripts/track-changes.sh {snapshot|list|since <snapshot-prefix|YYYY-MM-DD>}"
    exit 1
    ;;
esac
