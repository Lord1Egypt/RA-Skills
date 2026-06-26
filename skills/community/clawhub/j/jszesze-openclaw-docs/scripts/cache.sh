#!/usr/bin/env bash
set -euo pipefail
source "$(cd "$(dirname "$0")" && pwd)/lib.sh"

case "${1:-}" in
  status)
    ensure_cache_dirs
    idx=$(index_file)
    if [[ -s "$idx" ]]; then
      age=$(file_age_seconds "$idx")
      docs_count=$(extract_doc_tsv | wc -l | tr -d ' ')
      echo "Index cache: $idx"
      echo "Age seconds: $age"
      echo "Docs listed: $docs_count"
      echo "Docs cache dir: $CACHE_DIR/docs"
      echo "Snapshots dir: $CACHE_DIR/snapshots"
    else
      echo "Index cache missing. Run: bash ./scripts/cache.sh refresh"
    fi
    ;;
  refresh)
    dest=$(refresh_index)
    count=$(extract_doc_tsv | wc -l | tr -d ' ')
    echo "Refreshed docs index: $dest"
    echo "Docs listed: $count"
    ;;
  *)
    echo "Usage: bash ./scripts/cache.sh {status|refresh}"
    exit 1
    ;;
esac
