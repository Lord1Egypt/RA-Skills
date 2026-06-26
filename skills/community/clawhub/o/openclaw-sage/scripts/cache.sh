#!/bin/bash
# Cache management for OpenClaw docs
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/lib.sh"

parse_version_flag "$@"
set -- "${REMAINING_ARGS[@]}"

case "$1" in
  status)
    echo "Cache location: $CACHE_DIR"
    echo ""
    echo "Cached versions:"
    found=0
    for d in "$CACHE_DIR"/*/; do
      [ -d "$d" ] || continue
      ver=$(basename "$d")
      doc_count=$(ls "$d"doc_*.txt 2>/dev/null | wc -l | tr -d ' ')
      if [ -f "${d}index.txt" ]; then
        idx="index: built"
      else
        idx="index: not built"
      fi
      printf "  %-16s  %s docs   %s\n" "$ver" "$doc_count" "$idx"
      found=1
    done
    [ "$found" -eq 0 ] && echo "  (none — run build-index.sh fetch)"
    echo ""
    echo "TTL config (override with env vars):"
    echo "  Docs:   ${DOC_TTL}s  (OPENCLAW_SAGE_DOC_TTL)"
    echo "  Dir:    ${CACHE_DIR}  (OPENCLAW_SAGE_CACHE_DIR)"
    echo "  Source: ${SOURCE}  (OPENCLAW_SAGE_SOURCE)"
    ;;

  refresh)
    echo "Clearing docs.json cache for version: $VERSION"
    rm -f "${VERSION_CACHE_DIR}/docs.json"
    echo "docs.json cleared. Next sitemap.sh or build-index.sh fetch will re-fetch."
    ;;

  clear-docs)
    count=$(ls "$VERSION_CACHE_DIR"/doc_*.txt 2>/dev/null | wc -l | tr -d ' ')
    rm -f "${VERSION_CACHE_DIR}"/doc_*.txt \
          "${VERSION_CACHE_DIR}"/doc_*.md \
          "${VERSION_CACHE_DIR}/index.txt" \
          "${VERSION_CACHE_DIR}/index_meta.json"
    echo "Cleared $count cached docs and index from version: $VERSION"
    ;;

  tags)
    if [[ "$SOURCE" == local:* ]]; then
      echo "Tag listing not available for local source mode."
      echo "The local repo on disk is the only available version."
      exit 0
    fi
    TAGS_CACHE="${CACHE_DIR}/github_tags.json"
    if ! is_cache_fresh "$TAGS_CACHE" "$DOC_TTL"; then
      echo "Fetching available OpenClaw release tags..." >&2
      if ! curl -sf --max-time 10 \
          -H "Accept: application/vnd.github+json" \
          -H "User-Agent: openclaw-sage" \
          "https://api.github.com/repos/openclaw/openclaw/tags?per_page=30" \
          -o "$TAGS_CACHE" 2>/dev/null; then
        echo "Error: failed to fetch tags from GitHub API" >&2
        exit 1
      fi
    fi
    python3 - "$TAGS_CACHE" <<'PYEOF'
import sys, json
with open(sys.argv[1]) as f:
    tags = json.load(f)
print("Available OpenClaw releases (most recent first):")
for t in tags:
    print(f"  {t['name']}")
print()
print("Fetch a version: ./scripts/build-index.sh fetch --version <tag>")
PYEOF
    ;;

  dir)
    echo "$VERSION_CACHE_DIR"
    ;;

  *)
    echo "Usage: cache.sh {status|refresh|clear-docs|tags|dir} [--version <tag>]"
    ;;
esac
