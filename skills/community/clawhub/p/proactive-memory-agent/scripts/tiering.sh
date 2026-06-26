#!/bin/bash
# Proactive Memory Agent - Memory Tiering
# Automatically organizes content into HOT/WARM/COLD tiers

set -e

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE/memory"
LEARNINGS_DIR="$WORKSPACE/.learnings"
STATE_FILE="$MEMORY_DIR/.proactive-memory-state.json"

echo "🗂️  Proactive Memory Agent - Memory Tiering"
echo "============================================"
echo ""

# Check initialization
if [ ! -f "$STATE_FILE" ]; then
    echo "⚠️  Not initialized. Run: init.sh"
    exit 1
fi

# Step 1: Audit current state
echo "📋 Step 1: Auditing memory state..."

# Count files in each tier
hot_count=$(find "$WORKSPACE/SESSION-STATE.md" "$MEMORY_DIR/hot" -type f 2>/dev/null | wc -l || echo 0)
warm_count=$(find "$WORKSPACE/.learnings" "$MEMORY_DIR/warm" -type f 2>/dev/null | wc -l || echo 0)
cold_count=$(find "$WORKSPACE/MEMORY.md" "$MEMORY_DIR/cold" -type f 2>/dev/null | wc -l || echo 0)

echo "   🔥 HOT files:   $hot_count"
echo "   🌡️  WARM files:  $warm_count"
echo "   ❄️  COLD files:  $cold_count"
echo ""

# Step 2: Identify dead context (completed tasks)
echo "📋 Step 2: Identifying dead context..."

# Check SESSION-STATE for completed tasks
if [ -f "$WORKSPACE/SESSION-STATE.md" ]; then
    # Extract completed tasks (marked with ✅ or "Status: completed")
    completed_tasks=$(grep -E "(✅|Status: completed|Status: done)" "$WORKSPACE/SESSION-STATE.md" 2>/dev/null | wc -l || echo 0)
    
    if [ "$completed_tasks" -gt 0 ]; then
        echo "   Found $completed_tasks completed tasks in SESSION-STATE"
        echo "   Archiving to memory/warm/archived-tasks/..."
        
        mkdir -p "$MEMORY_DIR/warm/archived-tasks"
        timestamp=$(date +"%Y%m%d-%H%M%S")
        
        # Archive current SESSION-STATE (preserving history)
        cp "$WORKSPACE/SESSION-STATE.md" "$MEMORY_DIR/warm/archived-tasks/session-state-$timestamp.md"
        
        # Reset SESSION-STATE for new task
        cat > "$WORKSPACE/SESSION-STATE.md" << 'EOF'
# Session State (HOT Memory)

**Last Updated:** [Auto-updated]
**Status:** Active

## Current Task
[New task - update me]

## Key Decisions
- 

## User Preferences
- 

## Next Steps
1. 

## Working Notes
EOF
        echo "   ✓ Archived old session state"
    fi
fi

# Step 3: Promote recurring patterns from WARM to COLD
echo ""
echo "📋 Step 3: Checking for promotion candidates..."

if [ -d "$LEARNINGS_DIR" ]; then
    # Find learnings with "promote" or high recurrence
    promote_candidates=$(grep -l "Status: promoted\|Recurrence-Count: [3-9]\|Recurrence-Count: [0-9][0-9]" "$LEARNINGS_DIR"/*.md 2>/dev/null | wc -l || echo 0)
    
    if [ "$promote_candidates" -gt 0 ]; then
        echo "   Found $promote_candidates learning(s) ready for promotion"
        echo "   Review and promote manually to:"
        echo "      - Behavioral patterns → SOUL.md"
        echo "      - Workflow improvements → AGENTS.md"
        echo "      - Tool gotchas → TOOLS.md"
    else
        echo "   No promotion candidates found"
    fi
fi

# Step 4: Archive old working buffer content
echo ""
echo "📋 Step 4: Archiving working buffer..."

if [ -f "$MEMORY_DIR/working-buffer.md" ]; then
    # Check if buffer has content and is old
    buffer_lines=$(wc -l < "$MEMORY_DIR/working-buffer.md" 2>/dev/null || echo 0)
    
    if [ "$buffer_lines" -gt 50 ]; then
        echo "   Working buffer has $buffer_lines lines"
        echo "   Archiving to memory/cold/working-buffers/..."
        
        mkdir -p "$MEMORY_DIR/cold/working-buffers"
        timestamp=$(date +"%Y%m%d-%H%M%S")
        
        # Archive and reset
        cp "$MEMORY_DIR/working-buffer.md" "$MEMORY_DIR/cold/working-buffers/buffer-$timestamp.md"
        
        # Reset buffer
        cat > "$MEMORY_DIR/working-buffer.md" << 'EOF'
# Working Buffer (Danger Zone Log)

**Status:** INACTIVE
**Purpose:** Capture exchanges when context > 60%

---
EOF
        echo "   ✓ Archived and reset working buffer"
    else
        echo "   Working buffer small ($buffer_lines lines), no action needed"
    fi
fi

# Step 5: Update state
echo ""
echo "📋 Step 5: Updating state..."

if command -v jq >/dev/null 2>&1; then
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    jq --arg ts "$timestamp" '.stats.tiering_operations += 1 | .last_tiering = $ts' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
fi

echo "   ✓ State updated"

# Summary
echo ""
echo "✅ Memory tiering complete!"
echo ""
echo "Summary:"
echo "   • Old session states archived to warm/"
echo "   • Working buffers archived to cold/"
echo "   • SESSION-STATE reset for new task"
echo ""
echo "Next steps:"
echo "   1. Review promotion candidates in .learnings/"
echo "   2. Run detect.sh to verify new distribution"
echo "   3. Promote valuable patterns to AGENTS.md/SOUL.md"
