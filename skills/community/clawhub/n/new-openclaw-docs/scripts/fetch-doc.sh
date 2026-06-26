#!/bin/bash
# Fetch a specific doc from OpenClaw docs

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/.openclawdocs-env.sh"

if [[ -z "$1" ]]; then
  echo "Usage: fetch-doc.sh <path>"
  echo ""
  echo "Examples:"
  echo "  fetch-doc.sh gateway/configuration"
  echo "  fetch-doc.sh providers/discord"
  echo "  fetch-doc.sh start/getting-started"
  exit 1
fi

path="$1"
# Remove .md extension if provided
path="${path%.md}"

echo "⏳ Fetching $path..."

if content=$(openclawdocs_download "$path" 2>/dev/null); then
  echo "✓ Success"
  echo ""
  echo "Source: $OPENCLAW_DOCS_BASE_URL/$path"
  echo ""
  echo "---"
  echo "$content"
else
  cache_file=$(openclawdocs_cache_path "$path")
  if [[ -f "$cache_file" ]]; then
    cat "$cache_file"
    echo ""
    echo "⚠️  (offline - showing cached version)"
  else
    echo "❌ Failed to fetch $path (not found locally or offline)"
    exit 1
  fi
fi
