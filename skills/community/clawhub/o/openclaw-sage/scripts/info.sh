#!/bin/bash
# Lightweight doc metadata — reads from cache only, does not fetch
# Usage: info.sh [--version <tag>] <path> [--json]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/lib.sh"

parse_version_flag "$@"
set -- "${REMAINING_ARGS[@]}"

if [ -z "$1" ] || [[ "$1" == --* ]]; then
  echo "Usage: info.sh [--version <tag>] <path> [--json]"
  echo "Example: info.sh gateway/configuration"
  echo "Note: doc must be cached first — run ./scripts/build-index.sh fetch first."
  exit 1
fi

DOC_PATH="${1#/}"
shift

JSON=false
[[ "${OPENCLAW_SAGE_OUTPUT}" == "json" ]] && JSON=true
for arg in "$@"; do
  [ "$arg" = "--json" ] && JSON=true
done

SAFE_PATH="$(echo "$DOC_PATH" | tr '/' '_')"
CACHE_FILE="${VERSION_CACHE_DIR}/doc_${SAFE_PATH}.txt"
MD_CACHE="${VERSION_CACHE_DIR}/doc_${SAFE_PATH}.md"
URL="${DOCS_BASE_URL}/${DOC_PATH}"

# Neither cache file exists — report not cached and exit
if [ ! -f "$CACHE_FILE" ] && [ ! -f "$MD_CACHE" ]; then
  if $JSON && command -v python3 &>/dev/null; then
    python3 - "$DOC_PATH" "$URL" <<'PYEOF'
import sys, json
print(json.dumps({"error": "not_cached", "path": sys.argv[1], "url": sys.argv[2]}))
PYEOF
  else
    echo "Not cached: $DOC_PATH"
    echo "Run: ./scripts/fetch-doc.sh $DOC_PATH"
  fi
  exit 1
fi

if command -v python3 &>/dev/null; then
  $JSON && _json_flag="true" || _json_flag="false"
  python3 - "$MD_CACHE" "$CACHE_FILE" "$DOC_PATH" "$URL" "$DOC_TTL" "$_json_flag" <<'PYEOF'
import sys, re, os, json, time
from datetime import datetime

md_cache  = sys.argv[1]
txt_cache  = sys.argv[2]
doc_path   = sys.argv[3]
url        = sys.argv[4]
doc_ttl    = int(sys.argv[5])
as_json    = sys.argv[6] == 'true'

title    = None
headings = []
word_count = None
cached_at  = None
fresh      = None

# Title from YAML frontmatter and headings from markdown
if os.path.exists(md_cache):
    with open(md_cache, encoding='utf-8', errors='replace') as f:
        md = f.read()
    fm = re.match(r'^---\s*\n(.*?)\n---\s*(?:\n|$)', md, re.S)
    if fm:
        m = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', fm.group(1), re.M)
        if m: title = m.group(1).strip() or None
    headings = [m.group(1).strip()
                for m in re.finditer(r'^#{1,6}\s+(.+)$', md, re.M)]
    headings = [h for h in headings if h]

# Word count and cache metadata from plain text cache
if os.path.exists(txt_cache):
    with open(txt_cache, encoding='utf-8', errors='replace') as f:
        content = f.read()
    word_count = len(content.split())
    mtime = os.path.getmtime(txt_cache)
    fresh = (time.time() - mtime) < doc_ttl
    cached_at = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M')

if as_json:
    print(json.dumps({
        'path':       doc_path,
        'url':        url,
        'title':      title,
        'headings':   headings,
        'word_count': word_count,
        'cached_at':  cached_at,
        'fresh':      fresh,
    }, indent=2))
else:
    freshness = ' (fresh)' if fresh else ' (stale)' if fresh is not None else ''
    print(f"title:     {title or '(unknown)'}")
    print(f"headings:  {', '.join(headings) if headings else '(none found)'}")
    if word_count is not None:
        print(f"words:     {word_count:,}")
    if cached_at:
        print(f"cached_at: {cached_at}{freshness}")
    print(f"url:       {url}")
PYEOF

else
  # Fallback without python3
  if $JSON; then
    echo '{"error":"python3 required for --json output"}' >&2
    exit 1
  fi

  if [ -f "$MD_CACHE" ]; then
    title=$(grep '^title:' "$MD_CACHE" 2>/dev/null \
            | sed "s/^title:[[:space:]]*['\"]//; s/['\"][[:space:]]*$//" | head -1)
    echo "title:     ${title:-(unknown)}"
  fi

  if [ -f "$CACHE_FILE" ]; then
    word_count=$(wc -w < "$CACHE_FILE")
    echo "words:     $word_count"
    mtime=$(get_mtime "$CACHE_FILE")
    cached_at=$(date -d "@${mtime}" "+%Y-%m-%d %H:%M" 2>/dev/null \
                || date -r "$CACHE_FILE" "+%Y-%m-%d %H:%M" 2>/dev/null)
    if is_cache_fresh "$CACHE_FILE" "$DOC_TTL"; then
      echo "cached_at: ${cached_at} (fresh)"
    else
      echo "cached_at: ${cached_at} (stale)"
    fi
  fi

  echo "url:       $URL"
fi
