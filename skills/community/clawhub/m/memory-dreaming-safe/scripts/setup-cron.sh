#!/bin/bash
# setup-cron.sh — Create the dreaming cron job in OpenClaw
#
# Reads dreaming-config.json from workspace root (or uses defaults).
# Creates an isolated agentTurn cron that runs the dream cycle.
#
# Usage: bash scripts/setup-cron.sh [--config path/to/config.json]

set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
CONFIG_FILE="${1:-$WORKSPACE/dreaming-config.json}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Read config or use defaults
if [ -f "$CONFIG_FILE" ]; then
  SCHEDULE=$(jq -r '.schedule // "0 */8 * * *"' "$CONFIG_FILE")
  TIMEZONE=$(jq -r '.timezone // "UTC"' "$CONFIG_FILE")
  MODEL=$(jq -r '.model // "anthropic/claude-sonnet-4-6"' "$CONFIG_FILE")
  MIN_HOURS=$(jq -r '.gate.minHours // 6' "$CONFIG_FILE")
else
  echo "No config found at $CONFIG_FILE — using defaults"
  SCHEDULE="0 */8 * * *"
  TIMEZONE="UTC"
  MODEL="anthropic/claude-sonnet-4-6"
  MIN_HOURS=6
fi

echo "Setting up memory-dreaming cron:"
echo "  Schedule: $SCHEDULE ($TIMEZONE)"
echo "  Model: $MODEL"
echo "  Gate: ${MIN_HOURS}h minimum between dreams"
echo ""

# The dream prompt — this is what the cron agent receives
DREAM_PROMPT="AUTONOMOUS DREAM CYCLE — Memory consolidation.

Read the memory-dreaming skill SKILL.md at $SKILL_DIR/SKILL.md for full instructions.
Then execute the 4-phase dream cycle:

1. ORIENT: Read MEMORY.md, recent memory/*.md files, .learnings/, and memory/dreaming-log.md
2. GATHER: Grep session transcripts + daily logs for corrections, decisions, new facts since last dream
3. CONSOLIDATE: Update MEMORY.md — merge duplicates, absolute dates, delete contradictions, promote learnings
4. SYNC: Update Obsidian vault (if configured in dreaming-config.json), track plans, write dreaming log

Gate check: Read memory/dreaming-log.md — if last dream was <${MIN_HOURS}h ago, skip and reply NO_REPLY.
Config: Read dreaming-config.json in workspace root for Obsidian vault path and other settings.

Be token-efficient. Grep narrowly, don't read full transcripts. Write a summary to memory/dreaming-log.md when done."

echo "Creating cron job..."
echo "(Use openclaw cron tools to create the job — this script outputs the config)"
echo ""
echo "Cron config:"
echo "  name: memory-dreaming"
echo "  schedule: { kind: 'cron', expr: '$SCHEDULE', tz: '$TIMEZONE' }"
echo "  sessionTarget: isolated"
echo "  payload: { kind: 'agentTurn', message: <dream prompt>, model: '$MODEL', timeoutSeconds: 300 }"
echo "  delivery: { mode: 'none' }"
echo ""
echo "To create via OpenClaw, ask the agent:"
echo "  'Set up the memory-dreaming cron job'"
echo ""
echo "Or use the OpenClaw cron API directly."
