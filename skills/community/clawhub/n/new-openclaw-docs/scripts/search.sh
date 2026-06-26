#!/bin/bash
# Search cached docs by keyword

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/.openclawdocs-env.sh"

if [[ -z "$1" ]]; then
  echo "Usage: search.sh <keyword> [keyword2] ..."
  echo ""
  echo "Examples:"
  echo "  search.sh discord"
  echo "  search.sh webhook retry"
  exit 1
fi

echo "🔍 Searching cached docs for: $@"
echo ""

if [[ ! -d "$OPENCLAW_DOCS_CACHE_DIR" ]] || [[ -z "$(ls "$OPENCLAW_DOCS_CACHE_DIR"/*.md 2>/dev/null)" ]]; then
  echo "⚠️  No cached docs found. Use 'fetch-doc.sh' to cache documentation first."
  exit 1
fi

# Search with all keywords (each must be present)
results=0
for file in "$OPENCLAW_DOCS_CACHE_DIR"/*.md; do
  [[ ! -f "$file" ]] && continue
  
  # Check if all keywords match
  match=true
  for keyword in "$@"; do
    if ! grep -qi "$keyword" "$file"; then
      match=false
      break
    fi
  done
  
  if [[ "$match" == true ]]; then
    # Extract human-readable path
    doc_path="${file##*/}"
    doc_path="${doc_path%.md}"
    doc_path="${doc_path//_//}"
    
    # Show matching lines
    echo "📄 $doc_path"
    grep -in "$@" "$file" | head -3 | sed 's/^/   /'
    echo ""
    ((results++))
  fi
done

if [[ $results -eq 0 ]]; then
  echo "❌ No matches found for: $@"
  exit 1
fi

echo "✓ Found in $results doc(s)"
