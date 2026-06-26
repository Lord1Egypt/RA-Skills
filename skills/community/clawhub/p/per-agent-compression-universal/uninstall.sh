#!/bin/bash
# Uninstall Per-Agent Memory Compression Skill (Universal)
# Removes all peragent_compression_* cron tasks

set -e

echo "🗑️  Uninstalling Per-Agent Memory Compression Skill..."

TASKS=$(openclaw cron list --json 2>/dev/null | jq -r '.jobs[] | select(.name | test("^per_agent_compression_")) | .id')

if [ -z "$TASKS" ]; then
  echo "ℹ️  No per-agent compression tasks found. Already uninstalled?"
  exit 0
fi

COUNT=0
for TASK_ID in $TASKS; do
  openclaw cron delete "$TASK_ID" 2>/dev/null || true
  COUNT=$((COUNT + 1))
done

echo "✅ Uninstalled $COUNT task(s)."
echo ""
echo "💡 Verify: openclaw cron list | grep peragent_compression (should be empty)"
