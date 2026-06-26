#!/bin/bash
# Track changes to documentation

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$script_dir/.openclawdocs-env.sh"

SNAPSHOT_DIR="$OPENCLAW_DOCS_CACHE_DIR/.snapshots"

case "$1" in
  snapshot)
    echo "💾 Creating snapshot of current cache state..."
    mkdir -p "$SNAPSHOT_DIR"
    timestamp=$(date +%s_%Y-%m-%d_%H-%M)
    snapshot_file="$SNAPSHOT_DIR/snapshot_$timestamp.txt"
    find "$OPENCLAW_DOCS_CACHE_DIR" -name "*.md" -type f -exec ls -lh {} \; | sort > "$snapshot_file"
    echo "✓ Snapshot saved: snapshot_$timestamp"
    ;;
    
  list)
    echo "📸 Snapshots"
    if [[ ! -d "$SNAPSHOT_DIR" ]] || [[ -z "$(ls "$SNAPSHOT_DIR" 2>/dev/null)" ]]; then
      echo "No snapshots yet"
    else
      ls -1 "$SNAPSHOT_DIR" | sed 's/^/  /'
    fi
    ;;
    
  since)
    if [[ -z "$2" ]]; then
      echo "Usage: track-changes.sh since <date>"
      echo "Example: track-changes.sh since 2026-02-01"
      exit 1
    fi
    echo "📊 Changes since $2"
    
    target_date=$(date -d "$2" +%s 2>/dev/null)
    if [[ $? -ne 0 ]]; then
      echo "❌ Invalid date format. Use: YYYY-MM-DD"
      exit 1
    fi
    
    echo ""
    for file in "$OPENCLAW_DOCS_CACHE_DIR"/*.md; do
      [[ ! -f "$file" ]] && continue
      file_time=$(stat -c %Y "$file")
      if [[ $file_time -gt $target_date ]]; then
        doc_path="${file##*/}"
        doc_path="${doc_path%.md}"
        doc_path="${doc_path//_//}"
        modified=$(date -d @"$file_time" '+%Y-%m-%d %H:%M')
        echo "  $doc_path - $modified"
      fi
    done
    ;;
    
  *)
    echo "Usage: track-changes.sh {snapshot|list|since <date>}"
    echo ""
    echo "  snapshot           Save current cache state"
    echo "  list               Show all snapshots"
    echo "  since <date>       Show cached docs modified since date (YYYY-MM-DD)"
    exit 1
    ;;
esac
