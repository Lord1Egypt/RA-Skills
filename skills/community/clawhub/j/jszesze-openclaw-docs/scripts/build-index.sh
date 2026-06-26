#!/usr/bin/env bash
set -euo pipefail
source "$(cd "$(dirname "$0")" && pwd)/lib.sh"

case "${1:-}" in
  fetch)
    count=$(fetch_all_docs)
    echo "Fetched $count docs into $CACHE_DIR/docs"
    ;;
  build)
    ensure_cache_dirs
    manifest="$CACHE_DIR/local-index.tsv"
    : > "$manifest"
    while IFS=$'\t' read -r title url; do
      [[ -n "$url" ]] || continue
      path=$(download_doc "$url")
      printf '%s\t%s\t%s\n' "$title" "$url" "$path" >> "$manifest"
    done < <(extract_doc_tsv)
    echo "Built local manifest: $manifest"
    echo "Docs indexed: $(wc -l < "$manifest" | tr -d ' ')"
    ;;
  search)
    shift
    if [[ $# -lt 1 ]]; then
      echo "Usage: bash ./scripts/build-index.sh search <query>"
      exit 1
    fi
    search_cached_docs "$*"
    ;;
  *)
    echo "Usage: bash ./scripts/build-index.sh {fetch|build|search <query>}"
    exit 1
    ;;
esac
