#!/bin/bash
# ClickUp API Query Helper
# Handles pagination, subtasks, and common query patterns

set -euo pipefail

# Check for required environment variables
if [ -z "${CLICKUP_API_KEY:-}" ]; then
    echo "Error: CLICKUP_API_KEY not set" >&2
    exit 1
fi

if [ -z "${CLICKUP_TEAM_ID:-}" ]; then
    echo "Error: CLICKUP_TEAM_ID not set" >&2
    exit 1
fi

if [ -z "${CLICKUP_ASSIGNEE_ID:-}" ]; then
    echo "Error: CLICKUP_ASSIGNEE_ID not set" >&2
    exit 1
fi

# Usage function
usage() {
    cat << EOF
Usage: $0 <command> [options]

Commands:
  tasks --end <time>
                     Get open tasks due or overdue at the given end time
  task-count --end <time>
                     Count open tasks due or overdue at the given end time
  completed-tasks --start <time> --end <time>
                     Get tasks completed during the given time range
  create-task <list-id> <title> <due-date>
                     Create a task in a list and assign it to CLICKUP_ASSIGNEE_ID
  close-task <task-id>
                     Mark a task complete by moving it to a closed status
  assignees          List task count by assignee
  task <task-id>     Get specific task details
  spaces             List all spaces
  lists              List all lists in a space
  
Options:
  --start <time>     Start of a completion window
  --end <time>       End of a completion/due window
  --space <id>       Filter by space ID
  --list <id>        Filter by list ID
  
Examples:
  $0 tasks --end "2026-03-28 17:00"
  $0 task-count --end "2026-03-28 17:00"
  $0 completed-tasks --start "2026-03-24" --end "2026-03-28 17:00"
  $0 spaces
  $0 lists 123456
  $0 create-task 123456789 "Follow up with customer" "2026-03-28 17:00"
  $0 close-task 86segjm6qd
  $0 assignees
  $0 task 901612795398
Environment variables required:
  CLICKUP_API_KEY    Your ClickUp API token
  CLICKUP_TEAM_ID    Your team/workspace ID
  CLICKUP_ASSIGNEE_ID Your ClickUp assignee ID for create-task
EOF
    exit 1
}

# API call helper
clickup_api() {
    local endpoint="$1"
    curl -s "https://api.clickup.com/api/v2${endpoint}" \
        -H "Authorization: ${CLICKUP_API_KEY}"
}

clickup_api_post_json() {
    local endpoint="$1"
    local payload="$2"
    curl -s "https://api.clickup.com/api/v2${endpoint}" \
        -X POST \
        -H "Authorization: ${CLICKUP_API_KEY}" \
        -H "Content-Type: application/json" \
        -d "$payload"
}

clickup_api_put_json() {
    local endpoint="$1"
    local payload="$2"
    curl -s "https://api.clickup.com/api/v2${endpoint}" \
        -X PUT \
        -H "Authorization: ${CLICKUP_API_KEY}" \
        -H "Content-Type: application/json" \
        -d "$payload"
}

parse_human_time_to_ms() {
    local raw_time="$1"
    local boundary="${2:-exact}"
    local parsed_seconds=""

    if date -j -f "%Y-%m-%d" "1970-01-01" +%s >/dev/null 2>&1; then
        parse_human_time_to_ms_bsd "$raw_time" "$boundary"
        return 0
    fi

    if date -d "1970-01-01" +%s >/dev/null 2>&1; then
        parse_human_time_to_ms_gnu "$raw_time" "$boundary"
        return 0
    fi

    echo "Error: unsupported 'date' implementation; expected BSD or GNU date" >&2
    exit 1
}

parse_human_time_to_ms_bsd() {
    local raw_time="$1"
    local boundary="${2:-exact}"
    local datetime_formats=(
        "%Y-%m-%d %H:%M:%S"
        "%Y-%m-%d %H:%M"
        "%m/%d/%Y %H:%M:%S"
        "%m/%d/%Y %H:%M"
        "%b %d %Y %H:%M:%S"
        "%b %d %Y %H:%M"
        "%B %d %Y %H:%M:%S"
        "%B %d %Y %H:%M"
    )
    local date_only_formats=(
        "%Y-%m-%d"
        "%m/%d/%Y"
        "%b %d %Y"
        "%B %d %Y"
    )
    local format parsed_seconds

    for format in "${datetime_formats[@]}"; do
        if parsed_seconds=$(date -j -f "$format" "$raw_time" +%s 2>/dev/null); then
            echo $((parsed_seconds * 1000))
            return 0
        fi
    done

    for format in "${date_only_formats[@]}"; do
        if parsed_seconds=$(date -j -f "$format" "$raw_time" +%s 2>/dev/null); then
            if [ "$boundary" = "end" ]; then
                echo $(((parsed_seconds + 86399) * 1000))
            else
                echo $((parsed_seconds * 1000))
            fi
            return 0
        fi
    done

    echo "Error: could not parse time '$raw_time'" >&2
    echo "Supported examples: 2026-03-28, 2026-03-28 17:00, 03/28/2026, Mar 28 2026 17:00" >&2
    exit 1
}

parse_human_time_to_ms_gnu() {
    local raw_time="$1"
    local boundary="${2:-exact}"
    local parsed_seconds=""
    local date_only_patterns=(
        "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
        "^[0-9]{2}/[0-9]{2}/[0-9]{4}$"
        "^[A-Za-z]{3} [0-9]{1,2} [0-9]{4}$"
        "^[A-Za-z]+ [0-9]{1,2} [0-9]{4}$"
    )
    local pattern

    for pattern in "${date_only_patterns[@]}"; do
        if [[ "$raw_time" =~ $pattern ]]; then
            if [ "$boundary" = "end" ]; then
                parsed_seconds=$(date -d "$raw_time 23:59:59" +%s 2>/dev/null) || break
            else
                parsed_seconds=$(date -d "$raw_time 00:00:00" +%s 2>/dev/null) || break
            fi
            echo $((parsed_seconds * 1000))
            return 0
        fi
    done

    if parsed_seconds=$(date -d "$raw_time" +%s 2>/dev/null); then
        echo $((parsed_seconds * 1000))
        return 0
    fi

    echo "Error: could not parse time '$raw_time'" >&2
    echo "Supported examples: 2026-03-28, 2026-03-28 17:00, 03/28/2026, Mar 28 2026 17:00" >&2
    exit 1
}

# Get all tasks with pagination
fetch_all_tasks_raw() {
    local include_closed="${1:-false}"
    local all_tasks="[]"
    local page=0
    local last_page="false"
    local endpoint=""
    
    while [ "$last_page" = "false" ]; do
        endpoint="/team/${CLICKUP_TEAM_ID}/task?include_closed=${include_closed}&subtasks=true&page=${page}"

        local result=$(clickup_api "$endpoint")
        
        # Merge tasks
        all_tasks=$(echo "$all_tasks $result" | jq -s '.[0] + .[1].tasks')
        
        # Check if last page
        last_page=$(echo "$result" | jq -r '.last_page')
        
        if [ "$last_page" = "true" ]; then
            break
        fi
        
        ((page++))
    done
    
    echo "{\"tasks\": $all_tasks, \"total\": $(echo "$all_tasks" | jq 'length')}"
}

# Return a reduced task payload for output consumers.
get_all_tasks() {
    local end_time="$1"
    local end_ms=""
    local tasks

    end_ms=$(parse_human_time_to_ms "$end_time" end)
    tasks=$(fetch_all_tasks_raw false)

    echo "$tasks" | jq --argjson end_ms "$end_ms" '{
        tasks: [
            .tasks[] as $task |
            select($task.due_date != null)
            | select(($task.due_date | tonumber) <= $end_ms)
            | select(($task.status.type // "") != "closed")
            |
            {
                list_name: $task.list.name,
                title: $task.name,
                description: $task.description,
                assignees: [
                    ($task.assignees // [])[]
                    | {
                        id: .id,
                        name: (.username // .email // .initials)
                    }
                ],
                subtask_titles: [
                    .tasks[]
                    | select(.parent == $task.id)
                    | .name
                ],
                due_date: (
                    if $task.due_date == null
                    then null
                    else ($task.due_date | tonumber / 1000 | strftime("%Y-%m-%d %H:%M:%S"))
                    end
                )
            }
        ],
        total: ([.tasks[]
            | select(.due_date != null)
            | select((.due_date | tonumber) <= $end_ms)
            | select((.status.type // "") != "closed")
        ] | length)
    }'
}

# Return tasks completed during the provided time range.
get_completed_tasks_between() {
    local start_time="$1"
    local end_time="$2"
    local tasks start_ms end_ms

    start_ms=$(parse_human_time_to_ms "$start_time" start)
    end_ms=$(parse_human_time_to_ms "$end_time" end)

    if [ "$start_ms" -gt "$end_ms" ]; then
        echo "Error: start time must be before end time" >&2
        exit 1
    fi

    tasks=$(fetch_all_tasks_raw true)

    echo "$tasks" | jq --argjson start_ms "$start_ms" --argjson end_ms "$end_ms" '{
        tasks: [
            .tasks[] as $task
            | select(($task.date_closed // $task.date_done) != null)
            | select((($task.date_closed // $task.date_done) | tonumber) >= $start_ms and (($task.date_closed // $task.date_done) | tonumber) <= $end_ms)
            | {
                title: $task.name,
                description: $task.description,
                subtask_titles: [
                    .tasks[]
                    | select(.parent == $task.id)
                    | .name
                ],
                due_date: (
                    if $task.due_date == null
                    then null
                    else ($task.due_date | tonumber / 1000 | strftime("%Y-%m-%d %H:%M:%S"))
                    end
                ),
                completed_at: (($task.date_closed // $task.date_done) | tonumber / 1000 | strftime("%Y-%m-%d %H:%M:%S"))
            }
        ],
        total: ([.tasks[]
            | select((.date_closed // .date_done) != null)
            | select(((.date_closed // .date_done) | tonumber) >= $start_ms and ((.date_closed // .date_done) | tonumber) <= $end_ms)
        ] | length)
    }'
}

# Count tasks by type
task_count() {
    local end_time="$1"
    local end_ms=""
    local tasks

    end_ms=$(parse_human_time_to_ms "$end_time" end)
    tasks=$(fetch_all_tasks_raw false)
    
    echo "$tasks" | jq --argjson end_ms "$end_ms" '{
        total: ([.tasks[]
            | select(.due_date != null)
            | select((.due_date | tonumber) <= $end_ms)
            | select((.status.type // "") != "closed")
        ] | length),
        parent_tasks: ([.tasks[]
            | select(.due_date != null)
            | select((.due_date | tonumber) <= $end_ms)
            | select((.status.type // "") != "closed")
            | select(.parent == null)
        ] | length),
        subtasks: ([.tasks[]
            | select(.due_date != null)
            | select((.due_date | tonumber) <= $end_ms)
            | select((.status.type // "") != "closed")
            | select(.parent != null)
        ] | length),
        as_of: ($end_ms / 1000 | strftime("%Y-%m-%d %H:%M:%S"))
    }'
}

# Get assignee breakdown
assignee_breakdown() {
    local tasks=$(fetch_all_tasks_raw false)
    
    echo "$tasks" | jq -r '.tasks[] | 
        if .assignees and (.assignees | length) > 0 
        then .assignees[0].username 
        else "Unassigned" 
        end' | sort | uniq -c | sort -rn | \
        awk '{printf "{\"assignee\": \"%s\", \"count\": %d}\n", substr($0, index($0,$2)), $1}'
}

# Get specific task
get_task() {
    local task_id="$1"
    clickup_api "/task/${task_id}"
}

# Create a task in a list and assign it to the configured user.
create_task() {
    local list_id="$1"
    local title="$2"
    local due_date="$3"
    local due_date_ms=""
    local payload=""
    local response=""
    local response_body=""
    local http_status=""

    due_date_ms=$(parse_human_time_to_ms "$due_date" end)

    payload=$(jq -n \
        --arg title "$title" \
        --arg assignee_id "${CLICKUP_ASSIGNEE_ID}" \
        --arg due_date_ms "$due_date_ms" \
        '{
            name: $title,
            assignees: [($assignee_id | tonumber)],
            due_date: ($due_date_ms | tonumber)
        }')

    response=$(curl -s -w '\n%{http_code}' "https://api.clickup.com/api/v2/list/${list_id}/task" \
        -X POST \
        -H "Authorization: ${CLICKUP_API_KEY}" \
        -H "Content-Type: application/json" \
        -d "$payload")

    response_body=$(echo "$response" | sed '$d')
    http_status=$(echo "$response" | tail -n 1)

    if [[ "$http_status" =~ ^2[0-9][0-9]$ ]]; then
        echo "$response_body" | jq '{
            success: true,
            status: "created",
            task: {
                id: .id,
                title: .name,
                list_name: .list.name,
                assignees: [
                    (.assignees // [])[]
                    | {
                        id: .id,
                        name: (.username // .email // .initials)
                    }
                ],
                due_date: (
                    if .due_date == null
                    then null
                    else (.due_date | tonumber / 1000 | strftime("%Y-%m-%d %H:%M:%S"))
                    end
                ),
                url: .url
            }
        }'
    else
        echo "$response_body" | jq '{
            success: false,
            status: "failed",
            error: (.err // .error // .ECODE // .message // "Unknown ClickUp API error")
        }'
    fi
}

# Mark a task complete by moving it to a closed status in its list.
close_task() {
    local task_id="$1"
    local task_response=""
    local list_id=""
    local closed_status=""
    local payload=""
    local response=""
    local response_body=""
    local http_status=""

    task_response=$(clickup_api "/task/${task_id}")
    list_id=$(echo "$task_response" | jq -r '.list.id // empty')

    if [ -z "$list_id" ]; then
        echo "$task_response" | jq '{
            success: false,
            status: "failed",
            error: (.err // .error // .ECODE // .message // "Unable to determine the task list")
        }'
        return 0
    fi

    closed_status=$(clickup_api "/list/${list_id}" | jq -r '.statuses[]? | select(.type == "closed") | .status' | head -n 1)

    if [ -z "$closed_status" ]; then
        jq -n '{
            success: false,
            status: "failed",
            error: "No closed status is configured for this task list"
        }'
        return 0
    fi

    payload=$(jq -n --arg status "$closed_status" '{status: $status}')
    response=$(curl -s -w '\n%{http_code}' "https://api.clickup.com/api/v2/task/${task_id}" \
        -X PUT \
        -H "Authorization: ${CLICKUP_API_KEY}" \
        -H "Content-Type: application/json" \
        -d "$payload")

    response_body=$(echo "$response" | sed '$d')
    http_status=$(echo "$response" | tail -n 1)

    if [[ "$http_status" =~ ^2[0-9][0-9]$ ]]; then
        echo "$response_body" | jq '{
            success: true,
            status: "completed",
            task: {
                id: .id,
                title: .name,
                completed_at: (
                    if .date_closed == null and .date_done == null
                    then null
                    else ((.date_closed // .date_done) | tonumber / 1000 | strftime("%Y-%m-%d %H:%M:%S"))
                    end
                ),
                current_status: .status.status,
                url: .url
            }
        }'
    else
        echo "$response_body" | jq '{
            success: false,
            status: "failed",
            error: (.err // .error // .ECODE // .message // "Unknown ClickUp API error")
        }'
    fi
}

# List spaces
list_spaces() {
    clickup_api "/team/${CLICKUP_TEAM_ID}/space" | jq '[.spaces[] | {id, name}]'
}

# List all lists in a space, including folderless lists and lists inside folders.
list_lists() {
    local space_id="$1"
    local folderless_lists folders folder_lists all_lists

    folderless_lists=$(clickup_api "/space/${space_id}/list" | jq '.lists')
    folders=$(clickup_api "/space/${space_id}/folder")
    folder_lists=$(echo "$folders" | jq -c '[.folders[]? | .id]' | while read -r folder_ids; do
        if [ "$folder_ids" = "[]" ]; then
            echo "[]"
        else
            echo "$folder_ids" | jq -r '.[]' | while read -r folder_id; do
                clickup_api "/folder/${folder_id}/list" | jq '.lists'
            done | jq -s 'add // []'
        fi
    done)

    all_lists=$(printf '%s\n%s\n' "$folderless_lists" "${folder_lists:-[]}" | jq -s 'add // [] | map({id, name})')
    echo "$all_lists"
}

# Main command routing
case "${1:-}" in
    tasks)
        shift
        end_time=""

        while [ $# -gt 0 ]; do
            case "$1" in
                --end)
                    if [ -z "${2:-}" ]; then
                        echo "Error: --end requires a value" >&2
                        usage
                    fi
                    end_time="$2"
                    shift
                    ;;
                *)
                    echo "Error: unknown option '$1'" >&2
                    usage
                    ;;
            esac
            shift
        done

        if [ -z "$end_time" ]; then
            echo "Error: tasks requires --end <time>" >&2
            usage
        fi

        get_all_tasks "$end_time"
        ;;
    task-count)
        shift
        end_time=""

        while [ $# -gt 0 ]; do
            case "$1" in
                --end)
                    if [ -z "${2:-}" ]; then
                        echo "Error: --end requires a value" >&2
                        usage
                    fi
                    end_time="$2"
                    shift
                    ;;
                *)
                    echo "Error: unknown option '$1'" >&2
                    usage
                    ;;
            esac
            shift
        done

        if [ -z "$end_time" ]; then
            echo "Error: task-count requires --end <time>" >&2
            usage
        fi

        task_count "$end_time"
        ;;
    completed-tasks)
        shift
        start_time=""
        end_time=""

        while [ $# -gt 0 ]; do
            case "$1" in
                --start)
                    if [ -z "${2:-}" ]; then
                        echo "Error: --start requires a value" >&2
                        usage
                    fi
                    start_time="$2"
                    shift
                    ;;
                --end)
                    if [ -z "${2:-}" ]; then
                        echo "Error: --end requires a value" >&2
                        usage
                    fi
                    end_time="$2"
                    shift
                    ;;
                *)
                    echo "Error: unknown option '$1'" >&2
                    usage
                    ;;
            esac
            shift
        done

        if [ -z "$start_time" ] || [ -z "$end_time" ]; then
            echo "Error: completed-tasks requires --start <time> and --end <time>" >&2
            usage
        fi

        get_completed_tasks_between "$start_time" "$end_time"
        ;;
    assignees)
        assignee_breakdown
        ;;
    create-task)
        if [ -z "${2:-}" ] || [ -z "${3:-}" ] || [ -z "${4:-}" ]; then
            echo "Error: list ID, title, and due date are required" >&2
            usage
        fi
        create_task "$2" "$3" "$4"
        ;;
    close-task)
        if [ -z "${2:-}" ]; then
            echo "Error: task ID is required" >&2
            usage
        fi
        close_task "$2"
        ;;
    task)
        if [ -z "${2:-}" ]; then
            echo "Error: task ID required" >&2
            usage
        fi
        get_task "$2"
        ;;
    spaces)
        list_spaces
        ;;
    lists)
        if [ -z "${2:-}" ]; then
            echo "Error: space ID required" >&2
            usage
        fi
        list_lists "$2"
        ;;
    *)
        usage
        ;;
esac
