#!/bin/bash
# knowledge-base: Health check and stats
# Usage: health.sh

set -uo pipefail

KB_DIR="${KNOWLEDGE_BASE_DIR:-$HOME/.openclaw/workspace/knowledge}"

RAW_COUNT=$(find "$KB_DIR/raw" -name "*.md" 2>/dev/null | wc -l)
UNCOMPILED=$(grep -rl "status: raw" "$KB_DIR/raw" --include="*.md" 2>/dev/null | wc -l) || UNCOMPILED=0
SUMMARIES=$(find "$KB_DIR/wiki/summaries" -name "*.md" 2>/dev/null | wc -l)
CONCEPTS=$(find "$KB_DIR/wiki/concepts" -name "*.md" 2>/dev/null | wc -l)
OUTPUTS=$(find "$KB_DIR/output" \( -name "*.md" -o -name "*.html" -o -name "*.png" \) 2>/dev/null | wc -l)

ORPHAN_DAYS=30
ORPHANS=$(find "$KB_DIR/wiki/concepts" -name "*.md" -mtime +"$ORPHAN_DAYS" 2>/dev/null | wc -l || echo 0)

echo "=== Knowledge Base Health ==="
echo "Raw: $RAW_COUNT | Uncompiled: $UNCOMPILED | Summaries: $SUMMARIES | Concepts: $CONCEPTS | Orphans: $ORPHANS"

if [ "$UNCOMPILED" -gt 0 ]; then
  echo ""
  echo "Uncompiled:"
  grep -rl "status: raw" "$KB_DIR/raw" --include="*.md" 2>/dev/null | while read -r f; do
    echo "  → $(basename "$f")"
  done
fi

if [ "$ORPHANS" -gt 0 ]; then
  echo ""
  echo "Orphan concepts (>${ORPHAN_DAYS}d):"
  find "$KB_DIR/wiki/concepts" -name "*.md" -mtime +"$ORPHAN_DAYS" 2>/dev/null | while read -r f; do
    echo "  → $(basename "$f" .md)"
  done
fi
