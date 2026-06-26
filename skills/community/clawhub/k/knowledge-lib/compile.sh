#!/bin/bash
# knowledge-base: Compile a raw document into wiki
# Usage: compile.sh <raw-file> [--force]
# Reads the raw file, agent should have already populated it

set -euo pipefail

KB_DIR="${KNOWLEDGE_BASE_DIR:-$HOME/.openclaw/workspace/knowledge}"
RAW_FILE="$1"
FORCE="${2:-}"
DATE=$(date +%Y-%m-%d)

if [ ! -f "$RAW_FILE" ]; then
  echo "ERROR: File not found: $RAW_FILE"
  exit 1
fi

# Check if already compiled
BASENAME=$(basename "$RAW_FILE" .md)
SUMMARY_FILE="$KB_DIR/wiki/summaries/$BASENAME.md"

if [ -f "$SUMMARY_FILE" ] && [ "$FORCE" != "--force" ]; then
  echo "SKIP: Already compiled → $SUMMARY_FILE"
  exit 0
fi

# Update raw file status
sed -i 's/status: raw/status: compiled/' "$RAW_FILE"

# Append to log.md
LOG_FILE="$KB_DIR/wiki/log.md"
mkdir -p "$(dirname "$LOG_FILE")"
echo "## [${DATE}] compile | ${BASENAME} | pages touched: 0 | conflicts: 0" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "**Note**: Agent should update page count and conflict count after compilation." >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

echo "READY: $RAW_FILE"
echo "SUMMARY_TARGET: $SUMMARY_FILE"
echo "LOG_UPDATED: $LOG_FILE"
