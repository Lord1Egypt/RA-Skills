#!/usr/bin/env bash
# 魔镜 — Reflection Summary Generator
# Generates a reflection note capturing session insights, themes, and action items.
#
# Usage: bash generate_summary.sh <session-label> [output-dir]
#   session-label: A short descriptor like "2025-06-15-first-session"
#   output-dir:    Directory to write the markdown file (default: ./reflections)
#
# Example:
#   bash generate_summary.sh "2025-06-15-life-timeline"
#
# The script will open an interactive prompt in the terminal.
# Paste or type the session content, then press Ctrl+D to finish.

set -euo pipefail

LABEL="${1:-}"
OUTPUT_DIR="${2:-reflections}"

if [ -z "$LABEL" ]; then
    echo "Usage: bash generate_summary.sh <session-label> [output-dir]"
    echo "Example: bash generate_summary.sh '2025-06-15-first-session'"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

OUTPUT_FILE="${OUTPUT_DIR}/${LABEL}.md"

echo ""
echo "===================================="
echo "  魔镜 Reflection Summary Generator"
echo "===================================="
echo ""
echo "Paste or type the session conversation below."
echo "When done, press Ctrl+D (or Ctrl+Z on Windows)."
echo "------------------------------------"
echo ""

# Read session transcript from stdin
SESSION_TRANSCRIPT=$(cat)

# Build the markdown file
cat > "$OUTPUT_FILE" << EOFSYNOPSIS
# 魔镜 Reflection: ${LABEL}

**Date:** $(date '+%Y-%m-%d %H:%M')
**Session Label:** ${LABEL}

---

## Key Themes

TODO: Extract 2-5 themes that emerged during the session

## Turning Points / Insights

TODO: List significant realizations, emotional moments, or discoveries

## Patterns Noticed

TODO: Any recurring patterns in behavior, relationships, or thinking

## Core Values Surfaced

TODO: What matters most to them, based on today's conversation

## Action Items / Next Steps

- [ ] TODO: First small step

## Questions for Next Time

- TODO: Things to follow up on in the next session

---

*This reflection was generated as a private record for ongoing introspection.*
EOFSYNOPSIS

echo ""
echo "✅ Reflection saved to: ${OUTPUT_FILE}"
echo ""
echo "Next: Open the file and fill in the TODOs based on the session content."
