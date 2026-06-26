#!/usr/bin/env bash
# cleanup-stale.sh — Clean up stale/orphaned subagents
# Usage: bash scripts/cleanup-stale.sh [--dry-run] [--older-than MINUTES]
#
# NOTE: This script cannot directly kill OpenClaw subagents from a shell.
# It provides guidance on what to check using OpenClaw's built-in tools.
# For actual cleanup, use within an OpenClaw session:
#   workboard_reclaim(id) — release stale claims
#   workboard_release(id) — release completed claims

set -euo pipefail

DRY_RUN=false
OLDER_THAN=30

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run) DRY_RUN=true; shift ;;
        --older-than) OLDER_THAN="$2"; shift 2 ;;
        *) echo "Usage: $0 [--dry-run] [--older-than MINUTES]"; exit 1 ;;
    esac
done

echo "🧹 Cleaning up stale subagents..."
echo "  Threshold: older than ${OLDER_THAN} minutes"
if $DRY_RUN; then echo "  Mode: DRY RUN (no changes)"; fi
echo ""

echo "⚠️  Shell-based subagent cleanup is limited."
echo ""
echo "  From within an OpenClaw session, use these tools:"
echo ""
echo "  • sessions_list(activeMinutes: $OLDER_THAN)"
echo "    → Find sessions older than $OLDER_THAN minutes"
echo ""
echo "  • workboard_reclaim(id: \"...\", reason: \"stale\")"
echo "    → Release stale claims so others can pick them up"
echo ""
echo "  • workboard_release(id: \"...\", status: \"blocked\")"
echo "    → Release completed or blocked cards"
echo ""
echo "✅ No automated cleanup available from shell."
echo "   Run the above commands from within your OpenClaw session."