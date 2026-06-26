#!/bin/bash
# Show recently accessed docs (local mtime)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/lib.sh"

parse_version_flag "$@"
set -- "${REMAINING_ARGS[@]}"
DAYS=${1:-7}

if ! [[ "$DAYS" =~ ^[0-9]+$ ]]; then
  echo "Usage: recent.sh [--version <tag>] [days]" >&2
  echo "  days must be a positive integer (default: 7)" >&2
  exit 1
fi

echo "=== Recently accessed locally (last $DAYS days) ==="
echo ""

found=0
while IFS= read -r f; do
  path=$(basename "$f" .txt | sed 's/^doc_//; s/_/\//g')
  echo "  $path"
  found=1
done < <(find "$VERSION_CACHE_DIR" -name "doc_*.txt" -mtime "-${DAYS}" 2>/dev/null)

if [ "$found" -eq 0 ]; then
  echo "  (none — fetch docs with ./scripts/build-index.sh fetch)"
fi

echo ""
echo "Note: Source-level change dates are not available from docs.json."
echo "Run ./scripts/cache.sh status to see cached versions and fetch dates."
echo "Run ./scripts/cache.sh tags to list available OpenClaw release tags."
