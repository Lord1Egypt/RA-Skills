#!/bin/bash
# validate-knowledge.sh — Validate a knowledge article Markdown file
# Usage: validate-knowledge.sh <article.md>
# Exit 0 if valid, 1 if invalid
set -euo pipefail

ARTICLE="${1:?Usage: validate-knowledge.sh <article.md>}"

if [ ! -s "$ARTICLE" ]; then
  echo "ERROR: Article file is empty or missing: $ARTICLE"
  exit 1
fi

ERRORS=0

check_field() {
  local field="$1"
  if ! grep -q "^${field}:" "$ARTICLE"; then
    echo "ERROR: Missing frontmatter field: $field"
    ERRORS=$((ERRORS + 1))
  fi
}

# Check YAML frontmatter exists
if ! head -1 "$ARTICLE" | grep -q "^---"; then
  echo "ERROR: Missing YAML frontmatter"
  ERRORS=$((ERRORS + 1))
else
  check_field "date"
  check_field "source"
  check_field "url"
  check_field "domain"
fi

# Check has a heading
if ! grep -q "^# " "$ARTICLE"; then
  echo "ERROR: Missing article title (# heading)"
  ERRORS=$((ERRORS + 1))
fi

# Check word count (should be 50-300 words in body)
BODY=$(sed -n '/^---$/,/^---$/!p' "$ARTICLE" | tail -n +2)
WORD_COUNT=$(echo "$BODY" | wc -w | tr -d ' ')
if [ "$WORD_COUNT" -lt 30 ]; then
  echo "WARNING: Article body is very short ($WORD_COUNT words)"
fi

if [ "$ERRORS" -gt 0 ]; then
  echo "Validation failed: $ERRORS error(s)"
  exit 1
fi

echo "Article validation passed ($WORD_COUNT words)"
exit 0
