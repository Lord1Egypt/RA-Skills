#!/bin/bash
#
# list-insights.sh - List insights with filtering
# Usage: ./list-insights.sh [--tag tag] [--priority high|medium|low] [--status active|archived]
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
FILTER_TAG=""
FILTER_PRIORITY=""
FILTER_STATUS=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --tag)
            FILTER_TAG="$2"
            shift 2
            ;;
        --priority)
            FILTER_PRIORITY="$2"
            shift 2
            ;;
        --status)
            FILTER_STATUS="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Check if data directory exists
if [[ ! -d "$DATA_DIR" ]]; then
    echo "No insights found (data directory doesn't exist)"
    exit 0
fi

# Find all insight files
INSIGHTS=$(find "$DATA_DIR" -name "INS-*.md" -type f 2>/dev/null | sort -r)

if [[ -z "$INSIGHTS" ]]; then
    echo "No insights found"
    exit 0
fi

# Header
echo -e "${BLUE}📋 Insights${NC}"
echo "============"

# Filter and display
COUNT=0
for insight in $INSIGHTS; do
    # Extract metadata
    ID=$(basename "$insight" .md)
    CONTENT=$(grep "^content:" "$insight" 2>/dev/null | cut -d: -f2- | sed 's/^ *//' | head -1)
    TAGS=$(grep "^tags:" "$insight" 2>/dev/null | cut -d: -f2- | sed 's/^ *//')
    PRIORITY=$(grep "^priority:" "$insight" 2>/dev/null | cut -d: -f2- | sed 's/^ *//')
    STATUS=$(grep "^status:" "$insight" 2>/dev/null | cut -d: -f2- | sed 's/^ *//')
    
    # Apply filters
    if [[ -n "$FILTER_TAG" && ! "$TAGS" =~ $FILTER_TAG ]]; then
        continue
    fi
    if [[ -n "$FILTER_PRIORITY" && "$PRIORITY" != "$FILTER_PRIORITY" ]]; then
        continue
    fi
    if [[ -n "$FILTER_STATUS" && "$STATUS" != "$FILTER_STATUS" ]]; then
        continue
    fi
    
    # Display
    PRIORITY_COLOR="$NC"
    if [[ "$PRIORITY" == "high" ]]; then
        PRIORITY_COLOR="\033[0;31m"  # Red
    elif [[ "$PRIORITY" == "medium" ]]; then
        PRIORITY_COLOR="\033[1;33m"  # Yellow
    fi
    
    echo ""
    echo -e "${GREEN}$ID${NC} [${PRIORITY_COLOR}${PRIORITY}${NC}] (${STATUS})"
    echo "  Content: $CONTENT"
    echo "  Tags: $TAGS"
    
    COUNT=$((COUNT + 1))
done

echo ""
echo "============"
echo "Total: $COUNT insights"
