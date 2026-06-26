#!/bin/bash
# Cache management for OpenClaw docs

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/.openclawdocs-env.sh"

case "$1" in
  status)
    echo "📦 Cache Status"
    echo "==============="
    echo "Location: $OPENCLAW_DOCS_CACHE_DIR"
    echo "TTL: $OPENCLAW_DOCS_TTL seconds"
    echo ""
    
    count=$(find "$OPENCLAW_DOCS_CACHE_DIR" -name "*.md" -type f 2>/dev/null | wc -l)
    if [[ $count -eq 0 ]]; then
      echo "Cache is empty"
    else
      echo "Cached docs: $count"
      echo ""
      echo "Age of cached files:"
      openclawdocs_list_cache
    fi
    ;;
    
  clean)
    echo "🧹 Cleaning expired cache..."
    openclawdocs_cache_cleanup
    removed=$(($(find "$OPENCLAW_DOCS_CACHE_DIR" -name "*.md" -type f 2>/dev/null | wc -l)))
    echo "✓ Cleanup complete"
    ;;
    
  refresh)
    echo "🔄 Refreshing cache..."
    rm -rf "$OPENCLAW_DOCS_CACHE_DIR"/*.md 2>/dev/null
    echo "✓ Cache cleared. Docs will be re-downloaded on next fetch."
    ;;
    
  *)
    echo "Usage: cache.sh {status|clean|refresh}"
    echo ""
    echo "  status   Show cache status and age of all cached files"
    echo "  clean    Remove expired cache entries"
    echo "  refresh  Clear all cached docs (forces re-download)"
    exit 1
    ;;
esac
