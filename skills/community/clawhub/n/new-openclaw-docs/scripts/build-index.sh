#!/bin/bash
# Full-text index management

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/.openclawdocs-env.sh"

case "$1" in
  fetch)
    echo "📥 Downloading all OpenClaw docs..."
    # Note: This is a stub. Full implementation requires querying sitemap
    echo "⚠️  Feature requires direct OpenClaw API access (planned)"
    echo "   Workaround: Use fetch-doc.sh to cache docs as needed"
    ;;
    
  build)
    echo "🔨 Building search index..."
    echo "⚠️  Feature requires 'qmd' package (install with: npm i -g qmd)"
    echo "   For now, use search.sh for keyword-based search"
    ;;
    
  search)
    shift
    if [[ -z "$1" ]]; then
      echo "Usage: build-index.sh search <query>"
      exit 1
    fi
    echo "🔍 Full-text semantic search requires qmd (not installed)"
    echo "   Using keyword search instead:"
    "$script_dir/search.sh" "$@"
    ;;
    
  *)
    echo "Usage: build-index.sh {fetch|build|search <query>}"
    echo ""
    echo "Note: Advanced features require 'qmd' package for semantic search"
    exit 1
    ;;
esac
