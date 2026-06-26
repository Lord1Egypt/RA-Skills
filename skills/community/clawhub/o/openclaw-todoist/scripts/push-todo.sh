#!/bin/bash
# Push daily todos to DingTalk
# 获取今日待办 + 逾期任务，发送到钉钉

set -e

TOKEN_FILE="$HOME/.openclaw/workspace/.todoist-token"
STATE_FILE="$HOME/.openclaw/workspace/.todoist-state.json"

# Skip if Todoist not configured
[ ! -f "$TOKEN_FILE" ] && exit 0

TOKEN=$(cat "$TOKEN_FILE")
API_BASE="https://api.todoist.com/api/v1"

# Fetch all tasks
all_tasks=$(curl -s "$API_BASE/tasks" -H "Authorization: Bearer $TOKEN")

# Calculate dates
today=$(date +%Y-%m-%d)

# Parse tasks
parse_tasks() {
    local filter="$1"
    local date_filter=""

    case "$filter" in
        overdue) date_filter=".due.date < \"$today\" and .due.date != null" ;;
        today) date_filter=".due.date == \"$today\"" ;;
    esac

    echo "$all_tasks" | jq -r ".results[] | select($date_filter) | \"\(.content)\"" 2>/dev/null || true
}

# Get tasks
overdue_tasks=$(parse_tasks "overdue")
today_tasks=$(parse_tasks "today")

overdue_count=$(echo "$overdue_tasks" | grep -v '^$' | wc -l | tr -d ' ')
today_count=$(echo "$today_tasks" | grep -v '^$' | wc -l | tr -d ' ')

# Build message
message=""

if [ "$overdue_count" -gt 0 ]; then
    message+="🔴 **逾期任务** ($overdue_count)"
    message+=$'\n'
    while IFS= read -r task; do
        [ -n "$task" ] && message+="• $task"$'\n'
    done <<< "$overdue_tasks"
    message+=$'\n'
fi

if [ "$today_count" -gt 0 ]; then
    message+="📅 **今日待办** ($today_count)"
    message+=$'\n'
    while IFS= read -r task; do
        [ -n "$task" ] && message+="• $task"$'\n'
    done <<< "$today_tasks"
fi

# If no tasks
if [ -z "$message" ]; then
    message="✅ 今日无待办任务，又是美好的一天！"
fi

# Send to DingTalk
openclaw message send --channel dingtalk --target 343600 -m "$message"