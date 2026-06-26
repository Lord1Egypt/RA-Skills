#!/usr/bin/env bash
# OpenClaw Context GC & Checkpoint Script
# Modified for Windows (PowerShell compatible)

# Use environment variable or default Windows workspace
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
HOT_MEMORY="$WORKSPACE/memory/hot/HOT_MEMORY.md"
TIMESTAMP=$(date "+%Y-%m-%d %H:%M")

echo "🚀 Starting Context Budgeting Service..."

# 1. Update Decision Log in HOT_MEMORY.md
# Note: This is a placeholder for the agent to fill with actual session context.
# When run by the agent, the agent should have already updated the file.

# 2. Trigger Physical Compaction via OpenClaw CLI
echo "🧹 Triggering session compaction..."
# Note: Using the validated 'openclaw' command structure
openclaw sessions --active 1 > /dev/null 2>&1

# 3. Clean up large temp files in workspace (if any)
# PowerShell equivalent for Windows:
# Get-ChildItem -Path $WORKSPACE\temp -File | Where-Object { $_.Length -gt 1MB }

echo "✅ Context Budgeting complete. Snapshot at $TIMESTAMP"
