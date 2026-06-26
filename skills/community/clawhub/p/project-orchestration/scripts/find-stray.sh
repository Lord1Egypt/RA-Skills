#!/usr/bin/env bash
# find-stray.sh — Find stray/stale subagents that may be orphaned
# Usage: bash scripts/find-stray.sh [--older-than MINUTES]
#
# NOTE: This script cannot directly inspect OpenClaw subagents from a shell.
# It provides guidance on what to check using OpenClaw's built-in tools.
# For actual subagent inspection, use within an OpenClaw session:
#   sessions_list() — list all sessions
#   subagents(list) — check subagent status

set -euo pipefail

OLDER_THAN=30

while [[ $# -gt 0 ]]; do
    case "$1" in
        --older-than) OLDER_THAN="$2"; shift 2 ;;
        *) echo "Usage: $0 [--older-than MINUTES]"; exit 1 ;;
    esac
done

echo "🔍 Finding stray/stale subagents..."
echo "  Threshold: older than ${OLDER_THAN} minutes"
echo ""

echo "⚠️  Shell-based subagent inspection is limited."
echo ""
echo "  From within an OpenClaw session, use these tools:"
echo ""
echo "  • sessions_list(activeMinutes: $OLDER_THAN)"
echo "    → Find sessions older than $OLDER_THAN minutes"
echo ""
echo "  • subagents(list)"
echo "    → Check subagent status and health"
echo ""
echo "  • sessions_history(sessionKey: \"...\")"
echo "    → Check if a session is stuck or making progress"
echo ""
echo "✅ No automated checks available from shell."
echo "   Run the above commands from within your OpenClaw session."