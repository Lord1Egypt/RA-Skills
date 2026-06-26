#!/usr/bin/env bash
set -euo pipefail
source "$(cd "$(dirname "$0")" && pwd)/lib.sh"

if [[ $# -lt 1 ]]; then
  echo "Usage: bash ./scripts/fetch-doc.sh <path-or-url>"
  exit 1
fi

url=$(normalize_doc_url "$1")
cache_path=$(download_doc "$url")
echo "# Source: $url"
echo "# Cached: $cache_path"
echo
cat "$cache_path"
