#!/bin/bash
# Fetch a specific doc and display as readable text
# Usage: fetch-doc.sh [--version <tag>] <path> [--toc] [--section <heading>] [--max-lines <n>]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/lib.sh"

parse_version_flag "$@"
set -- "${REMAINING_ARGS[@]}"

if [ -z "$1" ] || [[ "$1" == --* ]]; then
  echo "Usage: fetch-doc.sh [--version <tag>] <path> [--toc] [--section <heading>] [--max-lines <n>]"
  echo "  fetch-doc.sh gateway/configuration"
  echo "  fetch-doc.sh gateway/configuration --toc"
  echo "  fetch-doc.sh gateway/configuration --section 'Retry Settings'"
  echo "  fetch-doc.sh gateway/configuration --max-lines 50"
  exit 1
fi

DOC_PATH="${1#/}"
shift

MODE="text"
MAX_LINES=""
SECTION=""

while [ $# -gt 0 ]; do
  case "$1" in
    --toc)       MODE="toc" ;;
    --section)   shift; MODE="section"; SECTION="$1" ;;
    --max-lines) shift; MAX_LINES="$1" ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
  shift
done

SAFE_PATH="$(echo "$DOC_PATH" | tr '/' '_')"
CACHE_FILE="${VERSION_CACHE_DIR}/doc_${SAFE_PATH}.txt"
MD_CACHE="${VERSION_CACHE_DIR}/doc_${SAFE_PATH}.md"

# Fetch doc using fetch_markdown from lib.sh, with fetch-doc-specific error handling
_do_fetch() {
  echo "Fetching: $DOC_PATH" >&2
  local ref="$VERSION"
  [ "$VERSION" = "latest" ] && ref="main"
  if ! fetch_markdown "$SAFE_PATH" "$ref"; then
    echo "Error: Failed to fetch: $DOC_PATH" >&2
    echo "Check the path is valid. Run ./scripts/sitemap.sh to see available docs." >&2
    exit 1
  fi
}

# Ensure plain text is fresh
if ! is_cache_fresh "$CACHE_FILE" "$DOC_TTL"; then
  if ! check_online; then
    echo "Offline: cannot reach GitHub" >&2
    if [ -f "$CACHE_FILE" ]; then
      echo "Using stale cached content for: $DOC_PATH" >&2
    else
      echo "No cache for: $DOC_PATH — attempting fetch anyway" >&2
      _do_fetch
    fi
  else
    _do_fetch
  fi
fi

case "$MODE" in
  toc)
    if [ ! -f "$MD_CACHE" ]; then
      echo "Error: --toc requires a fetched cache (run without --toc first)." >&2
      exit 1
    fi
    grep '^#' "$MD_CACHE" | while IFS= read -r line; do
      hashes=$(echo "$line" | sed 's/[^#].*//')
      level=${#hashes}
      text=$(echo "$line" | sed 's/^#* *//')
      printf '%*s%s\n' "$(( (level - 1) * 2 ))" '' "$text"
    done
    ;;

  section)
    if [ -z "$SECTION" ]; then
      echo "Error: --section requires a heading name. Use --toc first to list sections." >&2
      exit 1
    fi
    if [ ! -f "$MD_CACHE" ]; then
      echo "Error: --section requires a fetched cache (run without flags first)." >&2
      exit 1
    fi
    python3 - "$MD_CACHE" "$SECTION" <<'PYEOF'
import sys, re

with open(sys.argv[1], encoding='utf-8', errors='replace') as f:
    text = f.read()
query = sys.argv[2].lower()

headings = [(m.start(), len(m.group(1)), m.group(2).strip())
            for m in re.finditer(r'^(#{1,6})\s+(.+)$', text, re.M)]

if not headings:
    print("No headings found in document.", file=sys.stderr)
    sys.exit(1)

match_idx = next((i for i, (_, _, txt) in enumerate(headings)
                  if query in txt.lower()), None)
if match_idx is None:
    print(f"Section not found: {sys.argv[2]}", file=sys.stderr)
    for _, lvl, txt in headings:
        print(f"  {'  '*(lvl-1)}{txt}", file=sys.stderr)
    sys.exit(1)

start = headings[match_idx][0]
level = headings[match_idx][1]
end = next((headings[i][0] for i in range(match_idx+1, len(headings))
            if headings[i][1] <= level), len(text))
print(text[start:end].strip())
PYEOF
    ;;

  text)
    if [ -n "$MAX_LINES" ]; then
      head -n "$MAX_LINES" "$CACHE_FILE"
    else
      cat "$CACHE_FILE"
    fi
    ;;
esac
