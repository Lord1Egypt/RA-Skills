#!/bin/bash
# Proactive Memory Agent - Context Detection
# Checks context usage and memory tier distribution

set -e

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE/memory"
STATE_FILE="$MEMORY_DIR/.proactive-memory-state.json"

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if OpenClaw CLI is available
if ! command -v openclaw >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  OpenClaw CLI not found. Run 'session_status' manually to check context.${NC}"
    echo ""
fi

# Get context percentage from session_status if available
get_context_percent() {
    if command -v openclaw >/dev/null 2>&1; then
        # Try to get context from openclaw status
        openclaw status 2>/dev/null | grep -i "context" | head -1 || echo "Unknown"
    else
        echo "Manual check required"
    fi
}

# Calculate file sizes by tier
calculate_tiers() {
    local hot_size=0
    local warm_size=0
    local cold_size=0
    
    # HOT tier (SESSION-STATE + hot/ + working-buffer)
    if [ -f "$WORKSPACE/SESSION-STATE.md" ]; then
        hot_size=$((hot_size + $(wc -c < "$WORKSPACE/SESSION-STATE.md" 2>/dev/null || echo 0)))
    fi
    if [ -f "$MEMORY_DIR/working-buffer.md" ]; then
        hot_size=$((hot_size + $(wc -c < "$MEMORY_DIR/working-buffer.md" 2>/dev/null || echo 0)))
    fi
    if [ -d "$MEMORY_DIR/hot" ]; then
        hot_size=$((hot_size + $(find "$MEMORY_DIR/hot" -type f -exec wc -c {} + 2>/dev/null | tail -1 | awk '{print $1}' || echo 0)))
    fi
    
    # WARM tier (.learnings/ + warm/)
    if [ -d "$WORKSPACE/.learnings" ]; then
        warm_size=$((warm_size + $(find "$WORKSPACE/.learnings" -type f -exec wc -c {} + 2>/dev/null | tail -1 | awk '{print $1}' || echo 0)))
    fi
    if [ -d "$MEMORY_DIR/warm" ]; then
        warm_size=$((warm_size + $(find "$MEMORY_DIR/warm" -type f -exec wc -c {} + 2>/dev/null | tail -1 | awk '{print $1}' || echo 0)))
    fi
    
    # COLD tier (MEMORY.md + cold/)
    if [ -f "$WORKSPACE/MEMORY.md" ]; then
        cold_size=$((cold_size + $(wc -c < "$WORKSPACE/MEMORY.md" 2>/dev/null || echo 0)))
    fi
    if [ -d "$MEMORY_DIR/cold" ]; then
        cold_size=$((cold_size + $(find "$MEMORY_DIR/cold" -type f -exec wc -c {} + 2>/dev/null | tail -1 | awk '{print $1}' || echo 0)))
    fi
    
    # Convert to KB
    hot_kb=$((hot_size / 1024))
    warm_kb=$((warm_size / 1024))
    cold_kb=$((cold_size / 1024))
    total_kb=$((hot_kb + warm_kb + cold_kb))
    
    echo "HOT:$hot_kb WARM:$warm_kb COLD:$cold_kb TOTAL:$total_kb"
}

# Main output
echo "🧠 Proactive Memory Agent - Context Detection"
echo "=============================================="
echo ""

# Check initialization
if [ ! -f "$STATE_FILE" ]; then
    echo -e "${YELLOW}⚠️  Not initialized. Run: init.sh${NC}"
    echo ""
    exit 1
fi

# Context usage
echo "📊 Context Usage:"
echo "   $(get_context_percent)"
echo ""

# Memory tier distribution
echo "📁 Memory Tier Distribution:"
tiers=$(calculate_tiers)
hot_kb=$(echo "$tiers" | grep -o 'HOT:[0-9]*' | cut -d: -f2)
warm_kb=$(echo "$tiers" | grep -o 'WARM:[0-9]*' | cut -d: -f2)
cold_kb=$(echo "$tiers" | grep -o 'COLD:[0-9]*' | cut -d: -f2)
total_kb=$(echo "$tiers" | grep -o 'TOTAL:[0-9]*' | cut -d: -f2)

printf "   🔥 HOT:   %5s KB  (Current session)\n" "$hot_kb"
printf "   🌡️  WARM:  %5s KB  (Learning records)\n" "$warm_kb"
printf "   ❄️  COLD:  %5s KB  (Archive)\n" "$cold_kb"
printf "   ─────────────────────────\n"
printf "   📦 Total: %5s KB\n" "$total_kb"
echo ""

# Budget compliance
echo "📋 Context Budget Zones (10/40/20/20):"
if [ "$total_kb" -gt 0 ]; then
    hot_pct=$((hot_kb * 100 / total_kb))
    warm_pct=$((warm_kb * 100 / total_kb))
    cold_pct=$((cold_kb * 100 / total_kb))
    
    printf "   Objective (10%%):     🔥 HOT %3d%% %s\n" "$hot_pct" "$([ "$hot_pct" -gt 15 ] && echo -e "${YELLOW}⚠️${NC}" || echo "✅")"
    printf "   Short-term (40%%):    🌡️  WARM %3d%% %s\n" "$warm_pct" "$([ "$warm_pct" -gt 50 ] && echo -e "${YELLOW}⚠️${NC}" || echo "✅")"
    printf "   Background (40%%):    ❄️  COLD %3d%% %s\n" "$((warm_pct + cold_pct))" "$([ $((warm_pct + cold_pct)) -gt 50 ] && echo -e "${YELLOW}⚠️${NC}" || echo "✅")"
fi
echo ""

# Status assessment
if [ "$hot_kb" -gt 100 ] || [ "$warm_kb" -gt 500 ]; then
    echo -e "${YELLOW}⚠️  WARNING: Memory usage above optimal levels${NC}"
    echo "   Recommendation: Run tiering.sh to archive old content"
elif [ -f "$MEMORY_DIR/working-buffer.md" ] && grep -q "Status: ACTIVE" "$MEMORY_DIR/working-buffer.md" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Working Buffer is ACTIVE (context > 60%)${NC}"
    echo "   All exchanges being logged to working-buffer.md"
else
    echo -e "${GREEN}✅ Memory system healthy${NC}"
fi

echo ""
echo "Commands:"
echo "   tiering.sh    — Archive old content to lower tiers"
echo "   checkpoint.sh — Create pre-compaction checkpoint"
echo "   search.sh     — Search across all memory tiers"
