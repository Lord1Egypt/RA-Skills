#!/usr/bin/env bash
# show-tree.sh — Show current orchestrator state guidance
# Usage: bash scripts/show-tree.sh [--json]
#
# NOTE: This script cannot display a subagent tree from a shell.
# It provides guidance on what to check using OpenClaw's built-in tools.
# For actual subagent tree display, use within an OpenClaw session:
#   subagents(list) — list active subagents

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DATA_DIR="${ORCHESTRATOR_DATA_DIR:-$(dirname "$(dirname "$SKILL_DIR")")/orchestrator-data}"
OUTPUT_JSON=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --json) OUTPUT_JSON=true; shift ;;
    *) echo "Usage: $0 [--json]"; exit 1 ;;
  esac
done

echo "🌳 Orchestrator Subagent Tree"
echo "=============================="
echo ""

echo "⚠️  Shell-based subagent tree display is not available."
echo ""
echo "  From within an OpenClaw session, use these tools:"
echo ""
echo "  • subagents(list)"
echo "    → List active subagents with status"
echo ""
echo "  • sessions_list(activeMinutes: 60)"
echo "    → Find recently active sessions"
echo ""
echo "  • sessions_history(sessionKey: \"...\")"
echo "    → Check detailed session info"
echo ""

# Show data directory state
echo "📁 Data directory: $DATA_DIR"
if [ -f "$DATA_DIR/models.json" ]; then
  COUNT=$(grep -c '"id"' "$DATA_DIR/models.json" 2>/dev/null || echo "0")
  echo "   models.json: $COUNT models"
fi
if [ -f "$DATA_DIR/session_log.md" ]; then
  LINES=$(wc -l < "$DATA_DIR/session_log.md" 2>/dev/null || echo "0")
  echo "   session_log.md: $LINES entries"
fi
if [ -d "$DATA_DIR/sessions" ]; then
  COUNT=$(ls "$DATA_DIR/sessions"/*.md 2>/dev/null | wc -l || echo "0")
  echo "   sessions/: $COUNT session state files"
fi
echo ""
echo "Run the above commands from within your OpenClaw session for live data."