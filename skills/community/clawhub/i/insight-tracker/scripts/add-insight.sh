#!/bin/bash
#
# add-insight.sh - Add a new insight
# Usage: ./add-insight.sh "Insight content" --tags tag1,tag2 --priority high
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="${INSIGHT_DATA_DIR:-$SKILL_DIR/data}"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Parse arguments
CONTENT=""
TAGS=""
PRIORITY="medium"
SOURCE="session"

while [[ $# -gt 0 ]]; do
    case $1 in
        --tags)
            TAGS="$2"
            shift 2
            ;;
        --priority)
            PRIORITY="$2"
            shift 2
            ;;
        --source)
            SOURCE="$2"
            shift 2
            ;;
        -*)
            echo "Unknown option: $1"
            exit 1
            ;;
        *)
            CONTENT="$1"
            shift
            ;;
    esac
done

if [[ -z "$CONTENT" ]]; then
    echo "Usage: $0 \"Insight content\" [--tags tag1,tag2] [--priority high|medium|low] [--source source]"
    exit 1
fi

case "$PRIORITY" in
    high|medium|low)
        ;;
    *)
        echo "Priority must be high, medium, or low"
        exit 1
        ;;
esac

write_indented() {
    local value="$1"
    while IFS= read -r line; do
        printf '  %s\n' "$line"
    done <<< "$value"
}

# Create data directory
mkdir -p "$DATA_DIR"

# Generate ID
DATE=$(date +%Y%m%d)
COUNTER=1
while [[ -f "$DATA_DIR/INS-${DATE}-$(printf "%03d" $COUNTER).md" ]]; do
    COUNTER=$((COUNTER + 1))
done
INSIGHT_ID="INS-${DATE}-$(printf "%03d" $COUNTER)"
CREATED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Create insight file without expanding user content through a heredoc.
{
    printf '%s\n' '---'
    printf 'id: %s\n' "$INSIGHT_ID"
    printf '%s\n' 'content: |-'
    write_indented "$CONTENT"
    printf 'source: %s\n' "$SOURCE"
    printf 'tags: %s\n' "${TAGS:-general}"
    printf 'priority: %s\n' "$PRIORITY"
    printf '%s\n' 'status: active'
    printf 'created: %s\n' "$CREATED_AT"
    printf '%s\n\n' '---'
    printf '# %s\n\n' "$INSIGHT_ID"
    printf '%s\n' '## Content'
    printf '%s\n\n' "$CONTENT"
    printf '%s\n' '## Metadata'
    printf -- '- **Source**: %s\n' "$SOURCE"
    printf -- '- **Tags**: %s\n' "${TAGS:-general}"
    printf -- '- **Priority**: %s\n' "$PRIORITY"
    printf -- '- **Status**: active\n'
    printf -- '- **Created**: %s\n' "$CREATED_AT"
} > "$DATA_DIR/$INSIGHT_ID.md"

echo -e "${GREEN}✅ Insight added: $INSIGHT_ID${NC}"
echo -e "${BLUE}📄 Location: $DATA_DIR/$INSIGHT_ID.md${NC}"
