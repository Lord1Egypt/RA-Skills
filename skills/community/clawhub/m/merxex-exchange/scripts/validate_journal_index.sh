#!/bin/bash
#
# Journal Index Validator
# Validates that all .html files in the journal/ directory are indexed in journal.html
# Exit code 0: All files indexed (PASS)
# Exit code 1: Unindexed files found (FAIL)
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JOURNAL_DIR="$SCRIPT_DIR/journal"
JOURNAL_INDEX="$SCRIPT_DIR/journal.html"

echo "📋 Journal Index Validation"
echo "==========================="

# Check if journal directory exists
if [ ! -d "$JOURNAL_DIR" ]; then
    echo "❌ ERROR: Journal directory not found: $JOURNAL_DIR"
    exit 1
fi

# Check if journal.html exists
if [ ! -f "$JOURNAL_INDEX" ]; then
    echo "❌ ERROR: Journal index not found: $JOURNAL_INDEX"
    exit 1
fi

# Get list of all .html files in journal directory (excluding journal.html itself)
FILES=$(ls "$JOURNAL_DIR"/*.html 2>/dev/null | xargs -n1 basename | sort)
FILE_COUNT=$(echo "$FILES" | wc -l)

# Get list of indexed files from journal.html
INDEXED=$(grep -o 'journal/[^"]*\.html' "$JOURNAL_INDEX" | xargs -n1 basename | sort)
INDEXED_COUNT=$(echo "$INDEXED" | wc -l)

echo "📁 Total .html files in journal/: $FILE_COUNT"
echo "📑 Total entries in journal.html: $INDEXED_COUNT"
echo ""

# Find unindexed files
UNINDEXED=$(comm -23 <(echo "$FILES") <(echo "$INDEXED"))

if [ -n "$UNINDEXED" ]; then
    UNINDEXED_COUNT=$(echo "$UNINDEXED" | wc -l)
    echo "❌ CONTENT GAP DETECTED: $UNINDEXED_COUNT unindexed file(s)"
    echo ""
    echo "Unindexed files:"
    echo "$UNINDEXED" | while read -r file; do
        echo "  - $file"
    done
    echo ""
    echo "To fix, add entries to journal.html for the files listed above."
    echo ""
    exit 1
else
    echo "✅ Journal index valid: All $FILE_COUNT files are indexed"
    echo ""
    exit 0
fi