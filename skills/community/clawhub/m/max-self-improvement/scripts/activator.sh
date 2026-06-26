#!/bin/bash
# Activator Script for Max-Self-Improvement
# Prompts evaluation after task completion

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
LEARNINGS_DIR="$SKILL_DIR/.learnings"

# Check if learnings directory exists
if [ ! -d "$LEARNINGS_DIR" ]; then
    echo "Creating .learnings directory..."
    mkdir -p "$LEARNINGS_DIR"
fi

# Print reminder for self-improvement
echo "=========================================="
echo "Max-Self-Improvement Reminder"
echo "=========================================="
echo ""
echo "After completing your current task, consider:"
echo ""
echo "1. Did anything unexpected happen?"
echo "   → Log to $LEARNINGS_DIR/ERRORS.md"
echo ""
echo "2. Did you learn a better approach?"
echo "   → Log to $LEARNINGS_DIR/LEARNINGS.md"
echo ""
echo "3. Did the user request something new?"
echo "   → Log to $LEARNINGS_DIR/FEATURE_REQUESTS.md"
echo ""
echo "=========================================="

# Count pending items
if [ -f "$LEARNINGS_DIR/LEARNINGS.md" ]; then
    PENDING=$(grep -c "Status: pending" "$LEARNINGS_DIR/LEARNINGS.md" 2>/dev/null || echo "0")
    echo "Pending learnings: $PENDING"
fi

if [ -f "$LEARNINGS_DIR/ERRORS.md" ]; then
    PENDING=$(grep -c "Status: pending" "$LEARNINGS_DIR/ERRORS.md" 2>/dev/null || echo "0")
    echo "Pending errors: $PENDING"
fi

echo "=========================================="
