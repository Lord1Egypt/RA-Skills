#!/bin/bash
# Capture a learning for self-improvement

set -e

LEARNINGS_FILE="$HOME/.openclaw/workspace/memory/learnings.jsonl"

# Ensure memory directory exists
mkdir -p "$(dirname "$LEARNINGS_FILE")"

# Parse arguments
TYPE=""
SEVERITY="medium"
CONTEXT=""
ISSUE=""
CORRECTION=""
LESSON=""
TAGS=""
TASK_SLUG=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --type)
            TYPE="$2"
            shift 2
            ;;
        --severity)
            SEVERITY="$2"
            shift 2
            ;;
        --context)
            CONTEXT="$2"
            shift 2
            ;;
        --issue)
            ISSUE="$2"
            shift 2
            ;;
        --correction)
            CORRECTION="$2"
            shift 2
            ;;
        --lesson)
            LESSON="$2"
            shift 2
            ;;
        --tags)
            TAGS="$2"
            shift 2
            ;;
        --task-slug)
            TASK_SLUG="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Validate required fields
if [[ -z "$TYPE" ]]; then
    echo "❌ Error: --type is required (error|correction|success|insight)"
    exit 1
fi

if [[ -z "$CONTEXT" ]]; then
    echo "❌ Error: --context is required"
    exit 1
fi

if [[ -z "$LESSON" ]]; then
    echo "❌ Error: --lesson is required"
    exit 1
fi

# Validate type
case $TYPE in
    error|correction|success|insight)
        ;;
    *)
        echo "❌ Error: Invalid type. Must be: error, correction, success, or insight"
        exit 1
        ;;
esac

# Validate severity
case $SEVERITY in
    critical|high|medium|low)
        ;;
    *)
        echo "❌ Error: Invalid severity. Must be: critical, high, medium, or low"
        exit 1
        ;;
esac

# Generate timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Create JSON learning entry
cat >> "$LEARNINGS_FILE" << EOF
{"timestamp":"$TIMESTAMP","type":"$TYPE","severity":"$SEVERITY","context":"$CONTEXT","issue":"$ISSUE","correction":"$CORRECTION","lesson":"$LESSON","tags":"$TAGS","taskSlug":"$TASK_SLUG"}
EOF

echo "✅ Learning captured successfully!"
echo ""
echo "📝 Summary:"
echo "   Type: $TYPE"
echo "   Severity: $SEVERITY"
echo "   Context: $CONTEXT"
echo "   Lesson: $LESSON"
echo "   Tags: $TAGS"
echo ""
echo "📁 Stored in: $LEARNINGS_FILE"
