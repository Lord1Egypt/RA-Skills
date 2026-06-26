#!/bin/bash
# Review learnings from the past N days

set -e

LEARNINGS_FILE="$HOME/.openclaw/workspace/memory/learnings.jsonl"

# Parse arguments
DAYS=7
TAG=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --days)
            DAYS="$2"
            shift 2
            ;;
        --tag)
            TAG="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

# Check if learnings file exists
if [[ ! -f "$LEARNINGS_FILE" ]]; then
    echo "📭 No learnings found yet."
    exit 0
fi

# Calculate cutoff date
CUTOFF_DATE=$(date -u -v-${DAYS}d +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u -d "$DAYS days ago" +"%Y-%m-%dT%H:%M:%SZ")

echo "📊 Learning Review"
echo "=================="
echo "Period: Last $DAYS days (since $CUTOFF_DATE)"
echo ""

# Count by type
ERROR_COUNT=$(cat "$LEARNINGS_FILE" | jq -r "select(.timestamp >= \"$CUTOFF_DATE\") | .type" | grep -c "error" || echo "0")
CORRECTION_COUNT=$(cat "$LEARNINGS_FILE" | jq -r "select(.timestamp >= \"$CUTOFF_DATE\") | .type" | grep -c "correction" || echo "0")
SUCCESS_COUNT=$(cat "$LEARNINGS_FILE" | jq -r "select(.timestamp >= \"$CUTOFF_DATE\") | .type" | grep -c "success" || echo "0")
INSIGHT_COUNT=$(cat "$LEARNINGS_FILE" | jq -r "select(.timestamp >= \"$CUTOFF_DATE\") | .type" | grep -c "insight" || echo "0")

TOTAL=$((ERROR_COUNT + CORRECTION_COUNT + SUCCESS_COUNT + INSIGHT_COUNT))

echo "📈 Summary:"
echo "   ❌ Errors: $ERROR_COUNT"
echo "   ✏️  Corrections: $CORRECTION_COUNT"
echo "   ✅ Successes: $SUCCESS_COUNT"
echo "   💡 Insights: $INSIGHT_COUNT"
echo "   ─────────────────"
echo "   📝 Total: $TOTAL"
echo ""

if [[ $TOTAL -eq 0 ]]; then
    echo "🎉 No learnings in this period! Keep it up!"
    exit 0
fi

# Show top lessons
echo "🎯 Key Lessons:"
echo ""

cat "$LEARNINGS_FILE" | jq -r "select(.timestamp >= \"$CUTOFF_DATE\")" | while read -r line; do
    if [[ -n "$line" ]]; then
        TYPE=$(echo "$line" | jq -r '.type')
        LESSON=$(echo "$line" | jq -r '.lesson')
        CONTEXT=$(echo "$line" | jq -r '.context')
        
        case $TYPE in
            error) EMOJI="❌" ;;
            correction) EMOJI="✏️" ;;
            success) EMOJI="✅" ;;
            insight) EMOJI="💡" ;;
            *) EMOJI="📝" ;;
        esac
        
        echo "$EMOJI $LESSON"
        echo "   Context: $CONTEXT"
        echo ""
    fi
done

# Show most common tags
echo "🏷️  Common Tags:"
cat "$LEARNINGS_FILE" | jq -r "select(.timestamp >= \"$CUTOFF_DATE\") | .tags" | tr ',' '\n' | sort | uniq -c | sort -rn | head -10 | while read count tag; do
    if [[ -n "$tag" ]]; then
        echo "   $tag ($count)"
    fi
done

echo ""
echo "💡 Tip: Review these lessons before starting similar tasks!"
