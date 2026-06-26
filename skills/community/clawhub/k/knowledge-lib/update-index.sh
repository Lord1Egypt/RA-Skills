#!/bin/bash
# knowledge-base: Update the wiki index page
# Usage: update-index.sh
# Regenerates wiki/index.md with current stats and recent entries

set -euo pipefail

KB_DIR="${KNOWLEDGE_BASE_DIR:-$HOME/.openclaw/workspace/knowledge}"
DATE=$(date +%Y-%m-%d)

SUMMARIES=$(find "$KB_DIR/wiki/summaries" -name "*.md" 2>/dev/null | wc -l)
CONCEPTS=$(find "$KB_DIR/wiki/concepts" -name "*.md" 2>/dev/null | wc -l)
ANALYSES=$(find "$KB_DIR/wiki/analyses" -name "*.md" 2>/dev/null | wc -l) || ANALYSES=0
RAW=$(find "$KB_DIR/raw" -name "*.md" 2>/dev/null | wc -l)

# Build recent summaries list (last 10)
RECENT_SUMMARIES=""
for f in $(find "$KB_DIR/wiki/summaries" -name "*.md" -printf "%T@ %p\n" 2>/dev/null | sort -rn | head -10 | cut -d' ' -f2-); do
  [ -f "$f" ] || continue
  BNAME=$(basename "$f" .md)
  DATE_STR=$(echo "$BNAME" | grep -oP '^\d{4}-\d{2}-\d{2}' || echo "unknown")
  TITLE=$(grep -m1 '^# ' "$f" 2>/dev/null | sed 's/^# //' || echo "$BNAME")
  RECENT_SUMMARIES="${RECENT_SUMMARIES}| ${DATE_STR} | ${TITLE} |\n"
done

# Build concepts list
CONCEPT_LIST=""
for f in $(find "$KB_DIR/wiki/concepts" -name "*.md" | sort); do
  [ -f "$f" ] || continue
  BNAME=$(basename "$f" .md)
  # Check status
  STATUS=$(grep 'status:' "$f" 2>/dev/null | head -1 | sed 's/status: //' || echo "active")
  SOURCES=$(grep 'sources:' "$f" 2>/dev/null | head -1 | sed 's/sources: //' || echo "?")
  if [ "$STATUS" = "active" ]; then
    CONCEPT_LIST="${CONCEPT_LIST}- [[${BNAME}]] (${SOURCES} sources)\n"
  else
    CONCEPT_LIST="${CONCEPT_LIST}- ~~[[${BNAME}]]~~ [${STATUS}] (${SOURCES} sources)\n"
  fi
done

# Build recent analyses list (last 5)
RECENT_ANALYSES=""
for f in $(find "$KB_DIR/wiki/analyses" -name "*.md" -printf "%T@ %p\n" 2>/dev/null | sort -rn | head -5 | cut -d' ' -f2-); do
  [ -f "$f" ] || continue
  BNAME=$(basename "$f" .md)
  TITLE=$(grep -m1 '^# ' "$f" 2>/dev/null | sed 's/^# //' || echo "$BNAME")
  RECENT_ANALYSES="${RECENT_ANALYSES}- [${TITLE}](wiki/analyses/${BNAME}.md)\n"
done

# Build superseded/disputed count
SUPERSEDED=$(grep -rl 'status: superseded' "$KB_DIR/wiki" --include="*.md" 2>/dev/null | wc -l) || SUPERSEDED=0
DISPUTED=$(grep -rl 'status: disputed' "$KB_DIR/wiki" --include="*.md" 2>/dev/null | wc -l) || DISPUTED=0

mkdir -p "$KB_DIR/wiki"
cat > "$KB_DIR/wiki/index.md" << EOF
# ViVi Knowledge Wiki

> Last updated: ${DATE}

## Stats

| Metric | Count |
|--------|-------|
| Raw documents | ${RAW} |
| Summaries | ${SUMMARIES} |
| Concepts (active) | ${CONCEPTS} |
| Analyses | ${ANALYSES} |
| Superseded | ${SUPERSEDED} |
| Disputed | ${DISPUTED} |

## Concepts

${CONCEPT_LIST}

## Recent Summaries

| Date | Topic |
|------|-------|
${RECENT_SUMMARIES}

## Recent Analyses

${RECENT_ANALYSES}

## Recent Activity

See [log.md](wiki/log.md) for full history.

EOF

echo "✅ Index updated: $KB_DIR/wiki/index.md"
