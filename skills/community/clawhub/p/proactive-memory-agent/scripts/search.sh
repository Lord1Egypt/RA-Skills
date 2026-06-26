#!/bin/bash
# Proactive Memory Agent - Unified Search
# Searches across all memory tiers

set -e

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE/memory"
LEARNINGS_DIR="$WORKSPACE/.learnings"

# Colors
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Usage
if [ -z "$1" ]; then
    echo "🔍 Proactive Memory Agent - Unified Search"
    echo "==========================================="
    echo ""
    echo "Usage: search.sh [options] <query>"
    echo ""
    echo "Options:"
    echo "   --hot     Search HOT tier only (current session)"
    echo "   --warm    Search WARM tier only (learnings)"
    echo "   --cold    Search COLD tier only (archive)"
    echo "   --all     Search all tiers (default)"
    echo ""
    echo "Examples:"
    echo "   search.sh 'error'"
    echo "   search.sh --warm 'decision'"
    echo "   search.sh --hot 'current task'"
    echo ""
    exit 0
fi

# Parse options
TIER="all"
QUERY=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --hot)
            TIER="hot"
            shift
            ;;
        --warm)
            TIER="warm"
            shift
            ;;
        --cold)
            TIER="cold"
            shift
            ;;
        --all)
            TIER="all"
            shift
            ;;
        *)
            QUERY="$1"
            shift
            ;;
    esac
done

if [ -z "$QUERY" ]; then
    echo "❌ Error: No search query provided"
    echo "   Usage: search.sh <query>"
    exit 1
fi

echo "🔍 Searching for: '$QUERY'"
echo "   Tier: $TIER"
echo ""

# Search function
search_files() {
    local dir="$1"
    local label="$2"
    local color="$3"
    
    if [ ! -d "$dir" ]; then
        return
    fi
    
    local matches=$(grep -r -l -i "$QUERY" "$dir" 2>/dev/null | head -10)
    
    if [ -n "$matches" ]; then
        echo -e "${color}📁 $label${NC}"
        echo "$matches" | while read -r file; do
            local basename=$(basename "$file")
            local preview=$(grep -i "$QUERY" "$file" 2>/dev/null | head -1 | cut -c1-80)
            echo "   📄 $basename"
            echo "      → $preview"
        done
        echo ""
    fi
}

# Search by tier
if [ "$TIER" == "all" ] || [ "$TIER" == "hot" ]; then
    echo -e "${GREEN}🔥 HOT Tier (Current Session)${NC}"
    
    # SESSION-STATE.md
    if [ -f "$WORKSPACE/SESSION-STATE.md" ]; then
        if grep -q -i "$QUERY" "$WORKSPACE/SESSION-STATE.md" 2>/dev/null; then
            echo "   📄 SESSION-STATE.md"
            grep -i "$QUERY" "$WORKSPACE/SESSION-STATE.md" 2>/dev/null | head -2 | sed 's/^/      → /'
        fi
    fi
    
    # HOT_MEMORY.md
    if [ -f "$MEMORY_DIR/hot/HOT_MEMORY.md" ]; then
        if grep -q -i "$QUERY" "$MEMORY_DIR/hot/HOT_MEMORY.md" 2>/dev/null; then
            echo "   📄 HOT_MEMORY.md"
            grep -i "$QUERY" "$MEMORY_DIR/hot/HOT_MEMORY.md" 2>/dev/null | head -2 | sed 's/^/      → /'
        fi
    fi
    
    # Working Buffer
    if [ -f "$MEMORY_DIR/working-buffer.md" ]; then
        if grep -q -i "$QUERY" "$MEMORY_DIR/working-buffer.md" 2>/dev/null; then
            echo "   📄 working-buffer.md"
            grep -i "$QUERY" "$MEMORY_DIR/working-buffer.md" 2>/dev/null | head -2 | sed 's/^/      → /'
        fi
    fi
    
    echo ""
fi

if [ "$TIER" == "all" ] || [ "$TIER" == "warm" ]; then
    echo -e "${YELLOW}🌡️  WARM Tier (Learnings)${NC}"
    
    # .learnings/
    if [ -d "$LEARNINGS_DIR" ]; then
        for file in "$LEARNINGS_DIR"/*.md; do
            if [ -f "$file" ] && grep -q -i "$QUERY" "$file" 2>/dev/null; then
                local basename=$(basename "$file")
                echo "   📄 $basename"
                grep -i "$QUERY" "$file" 2>/dev/null | head -2 | sed 's/^/      → /'
            fi
        done
    fi
    
    # warm/
    if [ -d "$MEMORY_DIR/warm" ]; then
        search_files "$MEMORY_DIR/warm" "WARM Archive" "$YELLOW"
    fi
    
    echo ""
fi

if [ "$TIER" == "all" ] || [ "$TIER" == "cold" ]; then
    echo -e "${BLUE}❄️  COLD Tier (Archive)${NC}"
    
    # MEMORY.md
    if [ -f "$WORKSPACE/MEMORY.md" ]; then
        if grep -q -i "$QUERY" "$WORKSPACE/MEMORY.md" 2>/dev/null; then
            echo "   📄 MEMORY.md"
            grep -i "$QUERY" "$WORKSPACE/MEMORY.md" 2>/dev/null | head -2 | sed 's/^/      → /'
        fi
    fi
    
    # cold/
    if [ -d "$MEMORY_DIR/cold" ]; then
        search_files "$MEMORY_DIR/cold" "COLD Archive" "$BLUE"
    fi
    
    # snapshots/
    if [ -d "$MEMORY_DIR/snapshots" ]; then
        local snapshot_matches=$(find "$MEMORY_DIR/snapshots" -name "*.md" -exec grep -l -i "$QUERY" {} \; 2>/dev/null | head -5)
        if [ -n "$snapshot_matches" ]; then
            echo "   📁 Snapshots/"
            echo "$snapshot_matches" | while read -r file; do
                echo "      📄 $(basename "$file")"
            done
        fi
    fi
    
    echo ""
fi

echo "✅ Search complete"
