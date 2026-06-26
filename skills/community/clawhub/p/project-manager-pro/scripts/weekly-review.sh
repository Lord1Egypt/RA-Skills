#!/usr/bin/env bash
set -euo pipefail

# Project Manager Pro — Weekly Review Generator
# Produces a summary of the past week's task activity.
# Called by the agent on Sundays or manually.

DATA_DIR="${HOME}/.openclaw/workspace/pm-pro"
TASKS_FILE="$DATA_DIR/tasks.json"
PROJECTS_FILE="$DATA_DIR/projects.json"
ARCHIVE_DIR="$DATA_DIR/archive"

if [ ! -f "$TASKS_FILE" ]; then
    echo "❌ No tasks file found. Run setup.sh first."
    exit 1
fi

# Date calculations
if [[ "$(uname)" == "Darwin" ]]; then
    WEEK_START=$(date -v-7d +%Y-%m-%d)
    TODAY=$(date +%Y-%m-%d)
    NEXT_WEEK=$(date -v+7d +%Y-%m-%d)
    MONTH_FILE="$ARCHIVE_DIR/$(date +%Y-%m).json"
else
    WEEK_START=$(date -d "7 days ago" +%Y-%m-%d)
    TODAY=$(date +%Y-%m-%d)
    NEXT_WEEK=$(date -d "7 days" +%Y-%m-%d)
    MONTH_FILE="$ARCHIVE_DIR/$(date +%Y-%m).json"
fi

echo "📊 Weekly Summary — Week of ${WEEK_START} to ${TODAY}"
echo ""

# Completed this week
COMPLETED=$(jq -r --arg start "$WEEK_START" --arg end "$TODAY" '
    [.[] | select(.status == "done" and .completed_date != null and .completed_date >= $start and .completed_date <= $end)] | length
' "$TASKS_FILE")
echo "✅ Completed: $COMPLETED tasks"

# Created this week
CREATED=$(jq -r --arg start "$WEEK_START" --arg end "$TODAY" '
    [.[] | select(.created_date >= $start and .created_date <= $end)] | length
' "$TASKS_FILE")
echo "🆕 Created: $CREATED tasks"

# Net progress
NET=$((COMPLETED - CREATED))
if [ "$NET" -gt 0 ]; then
    echo "📈 Net progress: +${NET} tasks cleared"
elif [ "$NET" -lt 0 ]; then
    echo "📉 Net: ${NET} (more created than completed)"
else
    echo "📊 Net: Even (created = completed)"
fi
echo ""

# Completed task titles
if [ "$COMPLETED" -gt 0 ]; then
    echo "🏆 Completed this week:"
    jq -r --arg start "$WEEK_START" --arg end "$TODAY" '
        .[] | select(.status == "done" and .completed_date != null and .completed_date >= $start and .completed_date <= $end) |
        "  • \(.title)\(if .project then " (📁 \(.project))" else "" end)"
    ' "$TASKS_FILE"
    echo ""
fi

# Overdue tasks
OVERDUE=$(jq -r --arg today "$TODAY" '
    [.[] | select(.status != "done" and .due_date != null and .due_date < $today)] | length
' "$TASKS_FILE")
if [ "$OVERDUE" -gt 0 ]; then
    echo "⚠️ Overdue ($OVERDUE):"
    jq -r --arg today "$TODAY" '
        .[] | select(.status != "done" and .due_date != null and .due_date < $today) |
        "  • \(.title) — due \(.due_date) · \(.priority)"
    ' "$TASKS_FILE"
    echo ""
fi

# Blocked tasks
BLOCKED=$(jq '[.[] | select(.status == "blocked")] | length' "$TASKS_FILE")
if [ "$BLOCKED" -gt 0 ]; then
    echo "🚫 Blocked ($BLOCKED):"
    jq -r '.[] | select(.status == "blocked") | "  • \(.title)"' "$TASKS_FILE"
    echo ""
fi

# Next week preview
NEXT_WEEK_TASKS=$(jq -r --arg today "$TODAY" --arg next "$NEXT_WEEK" '
    [.[] | select(.status != "done" and .due_date != null and .due_date >= $today and .due_date <= $next)] | length
' "$TASKS_FILE")
echo "📅 Next week: $NEXT_WEEK_TASKS tasks due"
if [ "$NEXT_WEEK_TASKS" -gt 0 ]; then
    jq -r --arg today "$TODAY" --arg next "$NEXT_WEEK" '
        .[] | select(.status != "done" and .due_date != null and .due_date >= $today and .due_date <= $next) |
        "  • \(.title) — \(.due_date) · \(.priority)"
    ' "$TASKS_FILE" | head -10
fi
echo ""

# Project status
if [ -f "$PROJECTS_FILE" ] && [ "$(jq 'length' "$PROJECTS_FILE")" -gt 0 ]; then
    echo "📁 Project Status:"
    jq -r '.[] | select(.status == "active") |
        "  • \(.name): \(.completed_count)/\(.task_count) tasks (\(if .task_count > 0 then ((.completed_count * 100 / .task_count) | floor) else 0 end)%)\(if .target_date then " — target \(.target_date)" else "" end)"
    ' "$PROJECTS_FILE"
    echo ""
fi

# Auto-archive old completed tasks
if [ -d "$ARCHIVE_DIR" ]; then
    if [[ "$(uname)" == "Darwin" ]]; then
        ARCHIVE_CUTOFF=$(date -v-30d +%Y-%m-%d)
    else
        ARCHIVE_CUTOFF=$(date -d "30 days ago" +%Y-%m-%d)
    fi

    ARCHIVE_COUNT=$(jq -r --arg cutoff "$ARCHIVE_CUTOFF" '
        [.[] | select(.status == "done" and .completed_date != null and .completed_date < $cutoff)] | length
    ' "$TASKS_FILE")

    if [ "$ARCHIVE_COUNT" -gt 0 ]; then
        # Append to monthly archive
        if [ -f "$MONTH_FILE" ]; then
            EXISTING=$(cat "$MONTH_FILE")
        else
            EXISTING="[]"
        fi

        jq -r --arg cutoff "$ARCHIVE_CUTOFF" '
            [.[] | select(.status == "done" and .completed_date != null and .completed_date < $cutoff)]
        ' "$TASKS_FILE" | jq -s ".[0] + .[1]" <(echo "$EXISTING") - > "${MONTH_FILE}.tmp"
        mv "${MONTH_FILE}.tmp" "$MONTH_FILE"

        # Remove archived from active
        jq --arg cutoff "$ARCHIVE_CUTOFF" '
            [.[] | select(.status != "done" or .completed_date == null or .completed_date >= $cutoff)]
        ' "$TASKS_FILE" > "${TASKS_FILE}.tmp"
        mv "${TASKS_FILE}.tmp" "$TASKS_FILE"

        echo "🗄 Archived $ARCHIVE_COUNT completed tasks (older than 30 days)"
    fi
fi

echo "───────────"
echo "Generated: $(date '+%Y-%m-%d %H:%M')"
