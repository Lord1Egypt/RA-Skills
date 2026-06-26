#!/usr/bin/env bash
# log-session.sh — Log a session run with full state for cross-session resume
# Usage: bash scripts/log-session.sh <project> <task> <model> <status> [notes] [--context "..." | --context-file <path>]
#
# Writes:
#   session_log.md          — Quick reference table (append)
#   sessions/YYYY-MM-DD-HHMM-<project-slug>-<task-slug>.md  — Full session state (for resume)
#
# Data is stored in $ORCHESTRATOR_DATA_DIR (default: ../../orchestrator-data/ from skill root)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="${ORCHESTRATOR_DATA_DIR:-$(dirname "$(dirname "$SKILL_DIR")")/orchestrator-data}"
SESSION_LOG="$DATA_DIR/session_log.md"
SESSIONS_DIR="$DATA_DIR/sessions"

PROJECT="${1:-}"
TASK="${2:-}"
MODEL="${3:-}"
STATUS="${4:-}"
NOTES="${5:-}"
CONTEXT=""
CONTEXT_FILE=""

# Parse optional flags
shift 5 2>/dev/null || true
while [ $# -gt 0 ]; do
    case "$1" in
        --context) CONTEXT="$2"; shift 2 ;;
        --context-file) CONTEXT_FILE="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

if [ -z "$PROJECT" ] || [ -z "$TASK" ]; then
    echo "Usage: bash scripts/log-session.sh <project> <task> <model> <status> [notes] [--context \"...\" | --context-file <path>]"
    echo "Set ORCHESTRATOR_DATA_DIR to override data directory (default: $DATA_DIR)"
    exit 1
fi

mkdir -p "$DATA_DIR" "$SESSIONS_DIR"

TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
DATE_STAMP=$(date '+%Y-%m-%d')
TIME_STAMP=$(date '+%H%M')

# Build filesystem-safe slugs (no spaces, no special chars)
slugify() { echo "$1" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//'; }
PROJECT_SLUG=$(slugify "$PROJECT")
TASK_SLUG=$(slugify "$TASK")
SESSION_FILE="$SESSIONS_DIR/$DATE_STAMP-$TIME_STAMP-$PROJECT_SLUG-$TASK_SLUG.md"

# Escape pipe characters for markdown table safety
TABLE_TASK=$(echo "$TASK" | sed 's/|/\\|/g')
TABLE_NOTES=$(echo "$NOTES" | sed 's/|/\\|/g')

EMOJI=""
case "$STATUS" in
    complete) EMOJI="✅" ;;  failed) EMOJI="❌" ;;  partial) EMOJI="⚠️" ;;  blocked) EMOJI="🚫" ;;
    *) EMOJI="❓" ;;
esac

# --- Quick reference (session_log.md) ---
if [ ! -f "$SESSION_LOG" ]; then
    cat > "$SESSION_LOG" << 'EOF'
# Session Log
*Auto-generated session tracking*

| Date | Project | Task | Model | Status | Notes |
|------|---------|------|-------|--------|-------|
EOF
fi
echo "| $TIMESTAMP | $PROJECT | $TABLE_TASK | $MODEL | $EMOJI $STATUS | $TABLE_NOTES |" >> "$SESSION_LOG"

# --- Detailed session state (sessions/YYYY-MM-DD-HHMM-*.md) ---
{
    echo "# Session: $PROJECT / $TASK"
    echo ""
    echo "- **Date:** $TIMESTAMP"
    echo "- **Model:** $MODEL"
    echo "- **Status:** $EMOJI $STATUS"
    echo "- **Session file:** $SESSION_FILE"
    echo ""
    echo "## Notes"
    echo "$NOTES"
    echo ""

    if [ -n "$CONTEXT_FILE" ] && [ -f "$CONTEXT_FILE" ]; then
        echo "## Context"
        echo ""
        cat "$CONTEXT_FILE"
        echo ""
    elif [ -n "$CONTEXT" ]; then
        echo "## Context"
        echo ""
        echo "$CONTEXT"
        echo ""
    fi
} > "$SESSION_FILE"

echo "✅ Session logged: $PROJECT / $TASK [$STATUS]"
echo "   State: $SESSION_FILE"