#!/usr/bin/env bash
set -euo pipefail

# Project Manager Pro — Export Tasks
# Usage: ./export-tasks.sh [markdown|csv|json] [output-path]

DATA_DIR="${HOME}/.openclaw/workspace/pm-pro"
TASKS_FILE="$DATA_DIR/tasks.json"
PROJECTS_FILE="$DATA_DIR/projects.json"

FORMAT="${1:-markdown}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT="${2:-$DATA_DIR/exports/tasks_export_${TIMESTAMP}}"

# Validate
if [ ! -f "$TASKS_FILE" ]; then
    echo "❌ No tasks file found at $TASKS_FILE"
    echo "   Run setup.sh first."
    exit 1
fi

TASK_COUNT=$(jq 'length' "$TASKS_FILE")
if [ "$TASK_COUNT" -eq 0 ]; then
    echo "📋 No tasks to export."
    exit 0
fi

# Ensure export directory
mkdir -p "$(dirname "$OUTPUT")"

case "$FORMAT" in
    markdown|md)
        OUTPUT="${OUTPUT}.md"
        {
            echo "# Task Export — $(date '+%B %d, %Y')"
            echo ""
            echo "**Total tasks:** $TASK_COUNT"
            echo ""

            # Overdue
            echo "## 🔴 Overdue"
            echo ""
            jq -r --arg today "$(date +%Y-%m-%d)" '
                .[] | select(.status != "done" and .due_date != null and .due_date < $today) |
                "- **\(.title)** — Due: \(.due_date) · \(.priority) · Status: \(.status)"
            ' "$TASKS_FILE" || echo "_None_"
            echo ""

            # By priority
            for p in P1 P2 P3 P4; do
                LABEL=""
                case "$p" in
                    P1) LABEL="🔴 P1 — Critical" ;;
                    P2) LABEL="🟡 P2 — High" ;;
                    P3) LABEL="🟠 P3 — Medium" ;;
                    P4) LABEL="⚪ P4 — Low" ;;
                esac
                echo "## $LABEL"
                echo ""
                jq -r --arg p "$p" '
                    .[] | select(.priority == $p and .status != "done") |
                    "- **\(.title)**\(if .due_date then " — Due: \(.due_date)" else "" end) · \(.status)\(if .project then " · 📁 \(.project)" else "" end)"
                ' "$TASKS_FILE" || echo "_None_"
                echo ""
            done

            # Completed
            echo "## ✅ Completed"
            echo ""
            jq -r '
                .[] | select(.status == "done") |
                "- ~~\(.title)~~ — Completed: \(.completed_date // "unknown")"
            ' "$TASKS_FILE" || echo "_None_"
            echo ""

            # Projects summary
            if [ -f "$PROJECTS_FILE" ] && [ "$(jq 'length' "$PROJECTS_FILE")" -gt 0 ]; then
                echo "## 📁 Projects"
                echo ""
                jq -r '.[] | "- **\(.name)** — \(.status) · Target: \(.target_date // "none") · \(.completed_count)/\(.task_count) tasks done"' "$PROJECTS_FILE"
                echo ""
            fi
        } > "$OUTPUT"
        echo "✅ Exported $TASK_COUNT tasks to $OUTPUT"
        ;;

    csv)
        OUTPUT="${OUTPUT}.csv"
        {
            echo "id,title,priority,status,due_date,project,tags,time_estimate_min,created_date,completed_date"
            jq -r '.[] | [
                .id,
                (.title | gsub(","; ";")),
                .priority,
                .status,
                (.due_date // ""),
                (.project // ""),
                ((.tags // []) | join(";")),
                (.time_estimate_min // ""),
                .created_date,
                (.completed_date // "")
            ] | @csv' "$TASKS_FILE"
        } > "$OUTPUT"
        echo "✅ Exported $TASK_COUNT tasks to $OUTPUT"
        ;;

    json)
        OUTPUT="${OUTPUT}.json"
        jq '.' "$TASKS_FILE" > "$OUTPUT"
        echo "✅ Exported $TASK_COUNT tasks to $OUTPUT"
        ;;

    *)
        echo "❌ Unknown format: $FORMAT"
        echo "   Usage: ./export-tasks.sh [markdown|csv|json] [output-path]"
        exit 1
        ;;
esac
