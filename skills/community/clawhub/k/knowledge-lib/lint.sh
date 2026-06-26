#!/bin/bash
# knowledge-base: Lint and health check
# Usage: lint.sh [--deep]
# --deep: suggest LLM deep-lint steps (agent must execute them)

set -uo pipefail

KB_DIR="${KNOWLEDGE_BASE_DIR:-$HOME/.openclaw/workspace/knowledge}"
DATE=$(date +%Y-%m-%d)
DEEP="${1:-}"

RAW_COUNT=$(find "$KB_DIR/raw" -name "*.md" 2>/dev/null | wc -l)
UNCOMPILED=$(grep -rl "status: raw" "$KB_DIR/raw" --include="*.md" 2>/dev/null | wc -l) || UNCOMPILED=0
SUMMARIES=$(find "$KB_DIR/wiki/summaries" -name "*.md" 2>/dev/null | wc -l)
CONCEPTS=$(find "$KB_DIR/wiki/concepts" -name "*.md" 2>/dev/null | wc -l)
ANALYSES=$(find "$KB_DIR/wiki/analyses" -name "*.md" 2>/dev/null | wc -l) || ANALYSES=0
OUTPUTS=$(find "$KB_DIR/output" \( -name "*.md" -o -name "*.html" -o -name "*.png" \) 2>/dev/null | wc -l)
NO_FRONTMATTER=0
ORPHAN_DAYS=30

echo "=== Knowledge Base Lint Report ==="
echo "Date: $DATE"
echo ""
echo "--- Stats ---"
echo "Raw: $RAW_COUNT | Uncompiled: $UNCOMPILED | Summaries: $SUMMARIES | Concepts: $CONCEPTS | Analyses: $ANALYSES | Outputs: $OUTPUTS"

# Check for pages missing frontmatter
echo ""
echo "--- Pages missing frontmatter ---"
for dir in concepts summaries analyses; do
  COUNT=0
  for f in "$KB_DIR/wiki/$dir"/*.md; do
    [ -f "$f" ] || continue
    if ! head -1 "$f" | grep -q '^---$'; then
      COUNT=$((COUNT + 1))
      echo "  ⚠️  $dir/$(basename "$f")"
    fi
  done
  NO_FRONTMATTER=$((NO_FRONTMATTER + COUNT))
done
if [ "$NO_FRONTMATTER" -eq 0 ]; then
  echo "  ✅ All pages have frontmatter"
fi

# Uncompiled docs
if [ "$UNCOMPILED" -gt 0 ]; then
  echo ""
  echo "--- Uncompiled raw docs ---"
  grep -rl "status: raw" "$KB_DIR/raw" --include="*.md" 2>/dev/null | while read -r f; do
    echo "  → $(basename "$f")"
  done
fi

# Orphan pages (no inbound links, older than 30 days)
ORPHANS=$(find "$KB_DIR/wiki/concepts" -name "*.md" -mtime +"$ORPHAN_DAYS" 2>/dev/null | wc -l || echo 0)
if [ "$ORPHANS" -gt 0 ]; then
  echo ""
  echo "--- Orphan concepts (>${ORPHAN_DAYS}d, may need review) ---"
  find "$KB_DIR/wiki/concepts" -name "*.md" -mtime +"$ORPHAN_DAYS" 2>/dev/null | while read -r f; do
    NAME=$(basename "$f" .md)
    # Check if any other page links to this concept
    LINKS=$(grep -rl "\[\[$NAME\]\]" "$KB_DIR/wiki" --include="*.md" 2>/dev/null | wc -l)
    if [ "$LINKS" -le 1 ]; then
      echo "  📎 $NAME (inbound links: $LINKS)"
    fi
  done
fi

# Superseded / disputed pages
SUPERSEDED=$(grep -rl 'status: superseded\|status: disputed' "$KB_DIR/wiki" --include="*.md" 2>/dev/null | wc -l) || SUPERSEDED=0
if [ "$SUPERSEDED" -gt 0 ]; then
  echo ""
  echo "--- Superseded/Disputed pages ---"
  grep -rl 'status: superseded\|status: disputed' "$KB_DIR/wiki" --include="*.md" 2>/dev/null | while read -r f; do
    STATUS=$(grep 'status:' "$f" | head -1 | sed 's/status: //')
    echo "  ⚠️  $(basename "$f" .md) [$STATUS]"
  done
fi

# Summary
ISSUES=$((UNCOMPILED + NO_FRONTMATTER + ORPHANS + SUPERSEDED))
echo ""
echo "--- Summary ---"
echo "Issues found: $ISSUES (uncompiled: $UNCOMPILED, no-frontmatter: $NO_FRONTMATTER, orphan: $ORPHANS, superseded: $SUPERSEDED)"

if [ "$DEEP" = "--deep" ]; then
  echo ""
  echo "--- LLM Deep Lint (agent must execute) ---"
  echo "1. Contradiction scan: read pages sharing 'related' tags, check for conflicting claims"
  echo "2. Stale claim check: find 'status: active' pages contradicted by newer summaries"
  echo "3. Missing concepts: scan summaries for important terms lacking concept pages"
  echo "4. Missing cross-refs: find concepts that should link but don't"
  echo "5. Data gaps: suggest new sources for incomplete coverage areas"
  echo "6. Suggested queries: propose new questions worth exploring"
fi

# Append to log.md
LOG_FILE="$KB_DIR/wiki/log.md"
mkdir -p "$(dirname "$LOG_FILE")"
echo "## [${DATE}] lint | issues: ${ISSUES} | uncompiled: ${UNCOMPILED} | orphan: ${ORPHANS} | superseded: ${SUPERSEDED}" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

echo ""
echo "Log updated: $LOG_FILE"
