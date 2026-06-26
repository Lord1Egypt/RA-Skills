#!/bin/bash
# knowledge-base: Ingest a URL into the knowledge base
# Usage: ingest.sh <url> <category> [slug]
# Output: path to the raw file created

set -euo pipefail

KB_DIR="${KNOWLEDGE_BASE_DIR:-$HOME/.openclaw/workspace/knowledge}"
URL="$1"
CATEGORY="${2:-ai-llm}"
SLUG="${3:-}"
DATE=$(date +%Y-%m-%d)

if [ -z "$URL" ]; then
  echo "Usage: ingest.sh <url> [category] [slug]"
  exit 1
fi

# Auto-generate slug from URL if not provided
if [ -z "$SLUG" ]; then
  SLUG=$(echo "$URL" | sed 's|https\?://||; s|/.*||; s|[^a-zA-Z0-9-]|-|g' | head -c 60)
fi

RAW_DIR="$KB_DIR/raw/$CATEGORY"
mkdir -p "$RAW_DIR"

RAW_FILE="$RAW_DIR/${DATE}-${SLUG}.md"

# Check if already ingested
if [ -f "$RAW_FILE" ]; then
  echo "EXISTS: $RAW_FILE"
  exit 0
fi

# Fetch content (agent will populate this via web_fetch, we just create the stub)
cat > "$RAW_FILE" << EOF
---
source: ${URL}
category: ${CATEGORY}
ingested: ${DATE}
status: raw
---
# (Title will be filled by agent)

> Source: ${URL}
> Category: ${CATEGORY}
> Status: raw (awaiting compile)

EOF

# Append to log.md
LOG_FILE="$KB_DIR/wiki/log.md"
mkdir -p "$(dirname "$LOG_FILE")"
echo "## [${DATE}] ingest | ${SLUG} | ${CATEGORY}" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "**Source**: ${URL}" >> "$LOG_FILE"
echo "**Status**: raw (awaiting compile)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

echo "$RAW_FILE"
