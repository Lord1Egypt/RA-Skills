#!/bin/bash
# Search learnings by keyword, tag, or type

set -e

LEARNINGS_FILE="$HOME/.openclaw/workspace/memory/learnings.jsonl"

# Parse arguments
QUERY=""
TAG=""
TYPE=""
LIMIT=10

while [[ $# -gt 0 ]]; do
    case $1 in
        --tag)
            TAG="$2"
            shift 2
            ;;
        --type)
            TYPE="$2"
            shift 2
            ;;
        --limit)
            LIMIT="$2"
            shift 2
            ;;
        *)
            QUERY="$1"
            shift
            ;;
    esac
done

# Check if learnings file exists
if [[ ! -f "$LEARNINGS_FILE" ]]; then
    echo "📭 No learnings found. Start by capturing your first learning!"
    echo ""
    echo "Usage: ./capture-learning.sh --type error --context \"...\" --lesson \"...\""
    exit 0
fi

# Count total learnings
TOTAL=$(wc -l < "$LEARNINGS_FILE")

echo "📚 Searching learnings..."
echo "   Total learnings: $TOTAL"
echo ""

# Build search filter
FILTER="select(true"
if [[ -n "$TAG" ]]; then
    FILTER="$FILTER and (.tags | contains(\"$TAG\"))"
fi

if [[ -n "$TYPE" ]]; then
    FILTER="$FILTER and (.type == \"$TYPE\")"
fi

if [[ -n "$QUERY" ]]; then
    FILTER="$FILTER and ((.context + .lesson + .issue) | ascii_downcase | contains(\"$QUERY\" | ascii_downcase))"
fi
FILTER="$FILTER)"

# Execute search
if [[ -n "$FILTER" ]]; then
    RESULTS=$(cat "$LEARNINGS_FILE" | jq -c "$FILTER" | tail -n "$LIMIT")
else
    RESULTS=$(tail -n "$LIMIT" "$LEARNINGS_FILE")
fi

if [[ -z "$RESULTS" ]]; then
    echo "📭 No matching learnings found."
    exit 0
fi

# Display results
echo "📋 Results (showing last $(echo "$RESULTS" | wc -l) of $TOTAL):"
echo ""

echo "$RESULTS" | while read -r line; do
    TIMESTAMP=$(echo "$line" | jq -r '.timestamp')
    TYPE=$(echo "$line" | jq -r '.type')
    SEVERITY=$(echo "$line" | jq -r '.severity')
    CONTEXT=$(echo "$line" | jq -r '.context')
    LESSON=$(echo "$line" | jq -r '.lesson')
    TAGS=$(echo "$line" | jq -r '.tags')
    
    # Type emoji
    case $TYPE in
        error) EMOJI="❌" ;;
        correction) EMOJI="✏️" ;;
        success) EMOJI="✅" ;;
        insight) EMOJI="💡" ;;
        *) EMOJI="📝" ;;
    esac
    
    # Severity indicator
    case $SEVERITY in
        critical) SEV_ICON="🔴" ;;
        high) SEV_ICON="🟠" ;;
        medium) SEV_ICON="🟡" ;;
        low) SEV_ICON="🟢" ;;
        *) SEV_ICON="⚪" ;;
    esac
    
    echo "$EMOJI $SEV_ICON [$TIMESTAMP]"
    echo "   Context: $CONTEXT"
    echo "   Lesson: $LESSON"
    echo "   Tags: $TAGS"
    echo ""
done
