#!/usr/bin/env bash
# wiki-search.sh — Search the wiki (qmd if available, else grep)
#
# Usage:
#   bash wiki-search.sh <vault-path> "<query>"
#   bash wiki-search.sh <vault-path> -- "<query>"   # for queries starting with --
#   bash wiki-search.sh --help
set -o pipefail
export LC_ALL=C
. "$(dirname "$0")/lib.sh"

# Parse args: support -- as option terminator
VAULT=""
QUERY=""
_past_separator=false
for arg in "$@"; do
  if [ "$arg" = "--" ] && ! $_past_separator; then
    _past_separator=true
    continue
  fi
  if ! $_past_separator; then
    case "$arg" in
      --help|-h) echo "Usage: bash wiki-search.sh <vault-path> \"<query>\""; echo "Search wiki pages. Uses qmd if available, falls back to grep."; echo "Use -- before queries starting with --."; exit 0 ;;
      --*) echo "Error: unknown option '$arg'. Use -- to pass queries starting with --." >&2; exit 2 ;;
    esac
  fi
  if [ -z "$VAULT" ]; then
    VAULT="$arg"
  elif [ -z "$QUERY" ]; then
    QUERY="$arg"
  fi
done

[ -z "$VAULT" ] && { echo "Usage: wiki-search.sh <vault-path> \"<query>\"" >&2; exit 2; }
[ -z "$QUERY" ] && { echo "Usage: wiki-search.sh <vault-path> \"<query>\"" >&2; exit 2; }
WIKI="$VAULT/wiki"

[ -d "$WIKI" ] || { echo "Error: $WIKI not found" >&2; exit 1; }

# ── Strategy 1: qmd (semantic search) ────────────────────
if command -v qmd >/dev/null 2>&1; then
  echo "🔍 Searching with qmd: \"$QUERY\""
  # Run qmd from the wiki dir; fall back to grep if qmd fails
  if (cd "$WIKI" && qmd search -- "$QUERY"); then
    exit 0
  fi
  echo "  ⚠️  qmd failed, falling back to grep" >&2
  echo ""
fi

# ── Strategy 2: grep fallback ─────────────────────────────
echo "🔍 Searching wiki for: \"$QUERY\""
echo ""

found=0
while IFS= read -r file; do
  if grep -iqF -- "$QUERY" "$file" 2>/dev/null; then
    title=$(get_field "$file" title)
    [ -z "$title" ] && title=$(basename "$file" .md | tr '-' ' ')
    relpath="${file#"$VAULT"/}"
    # Extract first matching line for context
    snippet=$(grep -iF -- "$QUERY" "$file" 2>/dev/null | head -1 | sed 's/^[[:space:]]*//' | cut -c1-120)
    printf '  📄 %s\n     %s\n     ↳ %s\n\n' "$title" "$relpath" "$snippet"
    found=$((found + 1))
  fi
done < <(find "$WIKI" -type f -name '*.md' 2>/dev/null | sort)

if [ "$found" -eq 0 ]; then
  echo "  No results found for: \"$QUERY\""
  exit 1
fi
echo "  $found result(s) found."
