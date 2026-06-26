#!/bin/bash
# Proactive Memory Agent - Pre-Compaction Checkpoint
# Creates checkpoint before context compaction occurs

set -e

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE/memory"
HOT_MEMORY="$MEMORY_DIR/hot/HOT_MEMORY.md"
STATE_FILE="$MEMORY_DIR/.proactive-memory-state.json"

echo "🚀 Proactive Memory Agent - Pre-Compaction Checkpoint"
echo "======================================================"
echo ""

# Check initialization
if [ ! -f "$STATE_FILE" ]; then
    echo "⚠️  Not initialized. Run: init.sh"
    exit 1
fi

# Create timestamp
TIMESTAMP=$(date "+%Y-%m-%d %H:%M")
ISO_TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "📋 Creating checkpoint at $TIMESTAMP"
echo ""

# Step 1: Read current SESSION-STATE
echo "📋 Step 1: Reading current session state..."

SESSION_TASK=""
SESSION_DECISIONS=""
SESSION_NEXT=""

if [ -f "$WORKSPACE/SESSION-STATE.md" ]; then
    SESSION_TASK=$(grep "^## Current Task" -A 1 "$WORKSPACE/SESSION-STATE.md" 2>/dev/null | tail -1 | sed 's/^[[:space:]]*//' || echo "[See SESSION-STATE.md]")
    SESSION_DECISIONS=$(grep "^## Key Decisions" -A 5 "$WORKSPACE/SESSION-STATE.md" 2>/dev/null | grep "^-" | head -3 | sed 's/^[[:space:]]*//' || echo "[See SESSION-STATE.md]")
    SESSION_NEXT=$(grep "^## Next Steps" -A 3 "$WORKSPACE/SESSION-STATE.md" 2>/dev/null | grep "^[0-9]" | head -1 | sed 's/^[[:space:]]*//' || echo "[See SESSION-STATE.md]")
    echo "   ✓ Read SESSION-STATE.md"
else
    echo "   ⚠️  SESSION-STATE.md not found"
fi

echo ""

# Step 2: Update HOT_MEMORY.md
echo "📋 Step 2: Updating HOT_MEMORY.md..."

mkdir -p "$MEMORY_DIR/hot"

cat > "$HOT_MEMORY" << EOF
# HOT Memory — Context Budget 10% Zone

**Updated:** $TIMESTAMP
**Checkpoint:** Pre-compaction

## Current Status
**Task:** $SESSION_TASK

## Key Decisions Made
$SESSION_DECISIONS

## Next Immediate Step
$SESSION_NEXT

## Blockers (if any)
- [None / see SESSION-STATE.md]

---
*This checkpoint was created before context compaction*
*After compaction, read this file FIRST to recover context*
EOF

echo "   ✓ Updated HOT_MEMORY.md"
echo ""

# Step 3: Create snapshot
echo "📋 Step 3: Creating memory snapshot..."

mkdir -p "$MEMORY_DIR/snapshots"
SNAPSHOT_FILE="$MEMORY_DIR/snapshots/checkpoint-$(date +%Y%m%d-%H%M%S).md"

cat > "$SNAPSHOT_FILE" << EOF
# Memory Snapshot — $TIMESTAMP

## Session Context Summary

**Task:** $SESSION_TASK

**Key Decisions:**
$SESSION_DECISIONS

**Next Steps:**
$SESSION_NEXT

## Files Referenced
EOF

# Add file references from SESSION-STATE if available
if [ -f "$WORKSPACE/SESSION-STATE.md" ]; then
    grep -E "(\.md|\.js|\.ts|\.py|\.sh|\.json)" "$WORKSPACE/SESSION-STATE.md" 2>/dev/null | head -10 >> "$SNAPSHOT_FILE" || true
fi

echo "" >> "$SNAPSHOT_FILE"
echo "## Recovery Instructions" >> "$SNAPSHOT_FILE"
echo "1. Read HOT_MEMORY.md for immediate context" >> "$SNAPSHOT_FILE"
echo "2. Read SESSION-STATE.md for full details" >> "$SNAPSHOT_FILE"
echo "3. Read Working Buffer if available" >> "$SNAPSHOT_FILE"
echo "4. Check .learnings/ for error patterns" >> "$SNAPSHOT_FILE"

echo "   ✓ Created snapshot: $(basename "$SNAPSHOT_FILE")"
echo ""

# Step 4: Update state
echo "📋 Step 4: Updating state..."

if command -v jq >/dev/null 2>&1; then
    jq --arg ts "$ISO_TIMESTAMP" '.stats.checkpoints += 1 | .last_checkpoint = $ts' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
fi

echo "   ✓ State updated"

# Step 5: Optional - trigger compaction if requested
if [ "$1" == "--compact" ] || [ "$1" == "-c" ]; then
    echo ""
    echo "📋 Step 5: Triggering compaction..."
    
    if command -v openclaw >/dev/null 2>&1; then
        echo "   Triggering OpenClaw compaction..."
        openclaw sessions --active 1 > /dev/null 2>&1 || echo "   (Compaction handled by system)"
    else
        echo "   ⚠️  OpenClaw CLI not available"
        echo "   Compaction will occur automatically when needed"
    fi
fi

echo ""
echo "✅ Checkpoint complete!"
echo ""
echo "Recovery files created:"
echo "   • HOT_MEMORY.md — Quick context recovery"
echo "   • $SNAPSHOT_FILE — Full snapshot"
echo ""
echo "After compaction:"
echo "   1. Read HOT_MEMORY.md FIRST"
echo "   2. Check working-buffer.md for danger zone logs"
echo "   3. Continue from where you left off"
echo ""
