#!/usr/bin/env bash
# find-stuck.sh — Find potentially stuck subagents
# Usage: bash scripts/find-stuck.sh [--timeout MINUTES]
#
# NOTE: This script cannot directly inspect OpenClaw subagents from a shell.
# It provides guidance on what to check using OpenClaw's built-in tools.
# For actual subagent inspection, use within an OpenClaw session:
#   sessions_list(activeMinutes: N) — find long-running sessions
#   sessions_history(sessionKey) — check if a session is making progress

set -euo pipefail

TIMEOUT=15

while [[ $# -gt 0 ]]; do
    case "$1" in
        --timeout) TIMEOUT="$2"; shift 2 ;;
        *) echo "Usage: $0 [--timeout MINUTES]"; exit 1 ;;
    esac
done

echo "🔍 Finding stuck subagents..."
echo "  Timeout threshold: ${TIMEOUT} minutes without progress"
echo ""

echo "⚠️  Shell-based subagent inspection is limited."
echo ""
echo "  From within an OpenClaw session, use these tools:"
echo ""
echo "  • sessions_list(activeMinutes: $TIMEOUT)"
echo "    → Find sessions running longer than $TIMEOUT minutes"
echo ""
echo "  • sessions_history(sessionKey: \"...\")"
echo "    → Check if a session is making progress"
echo ""
echo "  • subagents(list)"
echo "    → List active subagents with status"
echo ""
echo "  • workboard_runs(id: \"...\")"
echo "    → Check run attempts for a workboard card"
echo ""
echo "✅ No automated checks available from shell."
echo "   Run the above commands from within your OpenClaw session."