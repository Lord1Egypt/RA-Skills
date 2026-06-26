#!/bin/bash
# Sync Todoist tasks to TASK.md
# - Separates personal tasks (remind user) from agent tasks (internal plan, no remind)
# - Merges with local TASK.md manual content
# - State change detection to save tokens

set -e

TASK_FILE="$HOME/.openclaw/workspace/TASK.md"
TASK_MANUAL_FILE="$HOME/.openclaw/workspace/TASK-manual.md"
STATE_FILE="$HOME/.openclaw/workspace/.todoist-state.json"
TOKEN_FILE="$HOME/.openclaw/workspace/.todoist-token"
IDENTITY_FILE="$HOME/.openclaw/workspace/.agent-identity.json"

# Skip if Todoist not configured
[ ! -f "$TOKEN_FILE" ] && exit 0

TOKEN=$(cat "$TOKEN_FILE")
API_BASE="https://api.todoist.com/api/v1"

# Save manual content BEFORE we overwrite TASK.md
MANUAL_CONTENT=""
if [ -f "$TASK_FILE" ]; then
    # Use awk for better cross-platform compatibility
    MANUAL_CONTENT=$(awk '/<!-- MANUAL:START -->/,/<!-- MANUAL:END -->/' "$TASK_FILE" 2>/dev/null || true)
fi

# Load identity (current agent)
load_identity() {
    if [ -f "$IDENTITY_FILE" ]; then
        CURRENT_AGENT=$(jq -r .current_agent "$IDENTITY_FILE")
        AGENT_LABEL=$(jq -r ".agents.$CURRENT_AGENT.todoist_label" "$IDENTITY_FILE")
    else
        CURRENT_AGENT="main"
        AGENT_LABEL=""
    fi
}
load_identity

# Get project IDs
get_project_id() {
    curl -s "$API_BASE/projects" -H "Authorization: Bearer $TOKEN" | \
        jq -r ".results[] | select(.name | contains(\"$1\")) | .id" | head -1
}

PERSONAL_PROJECT_ID=$(get_project_id "个人事务")
AGENT_PROJECT_ID=$(get_project_id "Agent 任务")

# Fetch all tasks
all_tasks=$(curl -s "$API_BASE/tasks" -H "Authorization: Bearer $TOKEN")

# Calculate dates
today=$(date +%Y-%m-%d)
tomorrow=$(date -v+1d +%Y-%m-%d 2>/dev/null || date -d "+1 day" +%Y-%m-%d 2>/dev/null || echo "")

# Helper: check if task is agent task (has agent label OR in Agent project)
is_agent_task() {
    local labels="$1"
    local project_id="$2"
    # Has agent label
    if echo "$labels" | jq -e "index(\"$AGENT_LABEL\")" > /dev/null 2>&1; then
        echo "true"
        return
    fi
    # In Agent project
    if [ -n "$AGENT_PROJECT_ID" ] && [ "$project_id" = "$AGENT_PROJECT_ID" ]; then
        echo "true"
        return
    fi
    echo "false"
}

# Categorize tasks: PERSONAL (remind user) vs AGENT (internal, no remind)
# Personal = in 个人事务 project AND no agent label
# Agent = in Agent project OR has agent label

parse_tasks() {
    local filter="$1"  # overdue/today/tomorrow/nodue
    local result=""
    local date_filter=""

    case "$filter" in
        overdue) date_filter=".due.date < \"$today\" and .due.date != null" ;;
        today) date_filter=".due.date == \"$today\"" ;;
        tomorrow) date_filter=".due.date == \"$tomorrow\"" ;;
        nodue) date_filter=".due.date == null" ;;
    esac

    echo "$all_tasks" | jq -r ".results[] | select($date_filter) | \"\(.id)|\(.content)|\(.due.date // \"\")|\(.labels | tostring)|\(.project_id)\"" 2>/dev/null | while IFS='|' read -r id content date labels project_id; do
        [ -z "$content" ] && continue

        if [ "$(is_agent_task "$labels" "$project_id")" = "true" ]; then
            # Agent task - for internal plan, don't remind user
            echo "AGENT|$id|$content|$date"
        else
            # Personal task - remind user
            echo "PERSONAL|$id|$content|$date"
        fi
    done
}

# Count by type
count_by_type() {
    local data="$1"
    local type="$2"
    echo "$data" | grep "^$type|" | wc -l | tr -d ' '
}

# Parse all categories
overdue_data=$(parse_tasks "overdue")
today_data=$(parse_tasks "today")
tomorrow_data=$(parse_tasks "tomorrow")
nodue_data=$(parse_tasks "nodue")

# Count personal tasks (for remind)
overdue_personal_count=$(count_by_type "$overdue_data" "PERSONAL")
today_personal_count=$(count_by_type "$today_data" "PERSONAL")
overdue_agent_count=$(count_by_type "$overdue_data" "AGENT")
today_agent_count=$(count_by_type "$today_data" "AGENT")

# Total counts
tomorrow_count=$(echo "$tomorrow_data" | grep -v '^$' | wc -l | tr -d ' ')
nodue_count=$(echo "$nodue_data" | grep -v '^$' | wc -l | tr -d ' ')

# Build state hash (only PERSONAL urgent tasks)
personal_urgent_ids=$(echo "$overdue_data"$'\n'"$today_data" | grep "^PERSONAL|" | cut -d'|' -f2 | sort | tr '\n' ',')
current_state="{\"personal_urgent_ids\":\"$personal_urgent_ids\",\"personal_overdue\":$overdue_personal_count,\"personal_today\":$today_personal_count,\"agent_overdue\":$overdue_agent_count,\"agent_today\":$today_agent_count,\"updated\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}"

# Check state change (only personal tasks matter for reminding user)
state_changed=false
if [ -f "$STATE_FILE" ]; then
    old_ids=$(jq -r '.personal_urgent_ids' "$STATE_FILE" 2>/dev/null || echo "")
    if [ "$old_ids" != "$personal_urgent_ids" ]; then
        state_changed=true
    fi
else
    state_changed=true
fi

# Save state
echo "$current_state" > "$STATE_FILE"

# Total tasks
total=$((overdue_personal_count + today_personal_count + overdue_agent_count + today_agent_count + tomorrow_count + nodue_count))

# No tasks - remove TASK.md if exists
if [ "$total" -eq 0 ]; then
    [ -f "$TASK_FILE" ] && rm "$TASK_FILE"
    [ -f "$TASK_MANUAL_FILE" ] && rm "$TASK_MANUAL_FILE"
    exit 0
fi

# Build TASK.md
{
    echo "# 当前任务"
    echo ""
    echo "_自动同步自 Todoist ($(date '+%Y-%m-%d %H:%M'))_"
    echo ""

    # Personal tasks (remind user)
    if [ "$overdue_personal_count" -gt 0 ]; then
        echo "## 🔴 个人逾期任务 ($overdue_personal_count)"
        echo ""
        echo "$overdue_data" | grep "^PERSONAL|" | while IFS='|' read -r type id content date; do
            [ -n "$content" ] && echo "- [ ] $content (逾期: $date)"
        done
        echo ""
    fi

    if [ "$today_personal_count" -gt 0 ]; then
        echo "## 📅 个人今日任务 ($today_personal_count)"
        echo ""
        echo "$today_data" | grep "^PERSONAL|" | while IFS='|' read -r type id content date; do
            [ -n "$content" ] && echo "- [ ] $content"
        done
        echo ""
    fi

    if [ "$today_personal_count" -eq 0 ] && [ "$overdue_personal_count" -eq 0 ]; then
        # Only show tomorrow/nodue if no urgent personal tasks
        if [ "$tomorrow_count" -gt 0 ]; then
            echo "## 📆 明日任务 ($tomorrow_count)"
            echo ""
            echo "$tomorrow_data" | while IFS='|' read -r type id content date; do
                [ -n "$content" ] && echo "- [ ] $content"
            done
            echo ""
        fi

        if [ "$nodue_count" -gt 0 ]; then
            echo "## 📌 待办（无日期）($nodue_count)"
            echo ""
            echo "$nodue_data" | while IFS='|' read -r type id content date; do
                [ -n "$content" ] && echo "- [ ] $content"
            done
            echo ""
        fi
    fi

    # Agent tasks (internal plan, separate section)
    local_agent_urgent=$((overdue_agent_count + today_agent_count))
    if [ "$local_agent_urgent" -gt 0 ]; then
        echo "---"
        echo ""
        echo "## 🤖 Agent 内部任务 ($CURRENT_AGENT)"
        echo "_这些是 Agent 的计划任务，不会提醒用户_"
        echo ""

        if [ "$overdue_agent_count" -gt 0 ]; then
            echo "### 逾期"
            echo "$overdue_data" | grep "^AGENT|" | while IFS='|' read -r type id content date; do
                [ -n "$content" ] && echo "- [ ] $content (逾期: $date)"
            done
            echo ""
        fi

        if [ "$today_agent_count" -gt 0 ]; then
            echo "### 今日"
            echo "$today_data" | grep "^AGENT|" | while IFS='|' read -r type id content date; do
                [ -n "$content" ] && echo "- [ ] $content"
            done
            echo ""
        fi
    fi

    # Preserve manual tasks from existing TASK.md (between <!-- MANUAL --> markers)
    if [ -n "$MANUAL_CONTENT" ]; then
        echo "---"
        echo ""
        # Output manual content without the marker lines
        echo "$MANUAL_CONTENT" | grep -v '<!-- MANUAL:' | grep -v '^$'
        echo ""
    fi

} > "$TASK_FILE"

# Output reminder ONLY for PERSONAL urgent tasks (not agent tasks)
# User wants to be reminded about buying coffee, not about agent's internal plan
personal_urgent=$((overdue_personal_count + today_personal_count))
if [ "$personal_urgent" -gt 0 ] && [ "$state_changed" = true ]; then
    if [ "$overdue_personal_count" -gt 0 ] && [ "$today_personal_count" -gt 0 ]; then
        echo "⚠️ 个人任务变化：有 $overdue_personal_count 个逾期 + $today_personal_count 个今日任务待处理"
    elif [ "$overdue_personal_count" -gt 0 ]; then
        echo "⚠️ 个人任务变化：有 $overdue_personal_count 个逾期任务待处理"
    else
        echo "📅 个人任务变化：今日有 $today_personal_count 个任务待处理"
    fi
fi

# Agent tasks are internal plans - don't remind user about them