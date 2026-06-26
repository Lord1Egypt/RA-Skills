#!/bin/bash
# dedup-articles.sh — Filter out articles already in knowledge directory
# Usage: echo '<jsonl>' | dedup-articles.sh <knowledge_dir>
# Input:  JSONL on stdin (each line has a "url" field)
# Output: JSONL on stdout (only articles whose URL is NOT in any existing .md file)
set -euo pipefail

KNOWLEDGE_DIR="${1:?Usage: echo '<jsonl>' | dedup-articles.sh <knowledge_dir>}"

# Build set of known URLs from existing Markdown files
KNOWN_URLS=""
if [ -d "$KNOWLEDGE_DIR" ] && ls "$KNOWLEDGE_DIR"/*.md &>/dev/null; then
  KNOWN_URLS=$(grep -rh '^url:' "$KNOWLEDGE_DIR"/*.md 2>/dev/null | sed 's/^url:[[:space:]]*//' | sed 's/[[:space:]]*$//' || true)
fi

# Filter stdin JSONL: pass through lines whose url is NOT in KNOWN_URLS
while IFS= read -r line; do
  [ -z "$line" ] && continue
  url=$(echo "$line" | jq -r '.url' 2>/dev/null || echo "")
  [ -z "$url" ] && continue
  if [ -z "$KNOWN_URLS" ] || ! echo "$KNOWN_URLS" | grep -qF "$url"; then
    echo "$line"
  fi
done
