#!/usr/bin/env bash
# scripts/todo-write.sh
# Create, update, complete, and delete Microsoft To Do tasks.
#
# Subcommands:
#   create --title T [--body B] [--due YYYY-MM-DD] [--list-id ID] [--apply]
#   update --task-id ID [--title T] [--body B] [--due YYYY-MM-DD] [--list-id ID] [--apply]
#   complete --task-id ID [--list-id ID] [--apply]
#   delete --task-id ID [--list-id ID] [--apply]
#   get --task-id ID [--list-id ID] [--format json|summary|raw]
#
# Safety rules:
#   1. Dry-run by default; --apply required for real writes.
#   2. Delete always shows the task first, then asks for "YES" confirmation.
#   3. Update shows current values and proposed changes before applying.
#   4. Never logs tokens.

set -Eeuo pipefail
IFS=$' \t\n'

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
CAL_LIB="$SCRIPT_DIR/_lib.sh"
# shellcheck source=./_lib.sh
. "$CAL_LIB"

usage() {
    cat >&2 <<'USAGE'
Usage: todo-write.sh <subcommand> [options]

Subcommands:
  create --title T         [--body B] [--due YYYY-MM-DD] [--list-id ID] [--apply]
  update --task-id ID      [--title T] [--body B] [--due YYYY-MM-DD] [--list-id ID] [--apply]
  complete --task-id ID    [--list-id ID] [--apply]
  delete --task-id ID      [--list-id ID] [--apply]
  get --task-id ID         [--list-id ID] [--format json|summary|raw]

Options:
  --task-id ID         Task ID (for get/update/complete/delete)
  --title T            Task title (create/update)
  --body B             Task body / notes (create/update)
  --due YYYY-MM-DD     Due date (create/update)
  --list-id ID         To Do list ID (default: defaultList)
  --format json|summary|raw  Output format for get (default: summary)
  --apply              Actually execute the write (default: dry-run)
  --yes                Skip the "type YES" confirmation for any write
  -h, --help           Show this help

Safety:
  - update/create default to dry-run (prints the JSON payload; may perform
    read-only Graph lookups such as resolving the default list or fetching
    the task to display — never writes)
  - delete always shows the task first; confirmation is a typed YES at the
    terminal, or an explicit --yes flag for non-interactive use
  - pass --apply to execute any write

Examples:
  # Create a task (dry-run)
  todo-write.sh create --title "Buy milk" --due 2026-06-24

  # Actually create
  todo-write.sh create --title "Buy milk" --due 2026-06-24 --apply

  # Mark task as completed
  todo-write.sh complete --task-id "AAMk..." --apply

  # Update title and body
  todo-write.sh update --task-id "AAMk..." --title "Buy oat milk" --apply

  # Delete a task (always requires --apply + YES confirmation)
  todo-write.sh delete --task-id "AAMk..." --apply
USAGE
}

# ---- Common helpers --------------------------------------------------------

# Resolve list ID: if --list-id given, use it; otherwise find defaultList.
_resolve_list_id() {
    local explicit_id="${1:-}"
    if [[ -n "$explicit_id" ]]; then
        printf '%s' "$explicit_id"
        return 0
    fi
    local resp list_id
    resp=$(graph_request GET "${OUTLOOK_TODO_GRAPH_BASE}/me/todo/lists?\$top=10")
    list_id=$(printf '%s' "$resp" | jq -r '.value[] | select((.wellknownListName//.wellKnownListName//"") == "defaultList") | .id' | head -n 1)
    if [[ -z "$list_id" ]]; then
        list_id=$(printf '%s' "$resp" | jq -r '.value[0].id // empty')
    fi
    [[ -n "$list_id" ]] || die "no To Do task lists found"
    printf '%s' "$list_id"
}

# URL-safe encode an ID
_urlencode_id() {
    python3 -c "import sys, urllib.parse; print(urllib.parse.quote(sys.argv[1], safe=''))" "$1"
}

# Format a single task object for summary
print_task_summary() {
    local json="$1"
    printf '%s' "$json" | jq -r '
        def due: if .dueDateTime then "\(.dueDateTime.dateTime // "-") \(.dueDateTime.timeZone // "")" else "-" end;
        "ID:       \(.id)",
        "Title:    \(.title // "-")",
        "Status:   \(.status // "-")",
        "Due:      \(due)",
        "Body:     \(.body.content // "-")",
        "List:     \(.parentList.displayName // "-")"
    ' >&2
}

# Build a JSON task body from the provided fields
build_task_body() {
    local title="${1:-}" body="${2:-}" due="${3:-}"

    local jq_filter='{}'
    local -a jq_args=()

    if [[ -n "$title" ]]; then
        jq_filter+=' | .title=$title'
        jq_args+=(--arg title "$title")
    fi
    if [[ -n "$body" ]]; then
        jq_filter+=' | .body={contentType: "text", content: $body}'
        jq_args+=(--arg body "$body")
    fi
    if [[ -n "$due" ]]; then
        jq_filter+=' | .dueDateTime={dateTime: $dueT, timeZone: $dueTz}'
        # Validate date format
        if ! [[ "$due" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
            die "invalid due date: $due (expected YYYY-MM-DD)"
        fi
        jq_args+=(--arg dueT "${due}T00:00:00" --arg dueTz "UTC")
    fi

    jq_filter+=' | with_entries(select(.value != null and .value != "" and .value != []))'

    jq -n "${jq_args[@]}" "$jq_filter"
}

# ---- Subcommands -----------------------------------------------------------

cmd_get() {
    local task_id="" list_id="" format="summary"
    while (( $# > 0 )); do
        case "$1" in
            --task-id)  task_id="$2"; shift 2 ;;
            --list-id)  list_id="$2"; shift 2 ;;
            --format)   format="$2"; shift 2 ;;
            -h|--help)  usage; exit 0 ;;
            *)          die "unknown option: $1" ;;
        esac
    done
    [[ -n "$task_id" ]] || die "--task-id is required"

    load_config || die "config missing"
    load_tokens || die "tokens missing"
    ensure_fresh_token

    list_id=$(_resolve_list_id "$list_id")
    local enc_list enc_task
    enc_list=$(_urlencode_id "$list_id")
    enc_task=$(_urlencode_id "$task_id")

    local url="${OUTLOOK_TODO_GRAPH_BASE}/me/todo/lists/$enc_list/tasks/$enc_task"
    log_info "GET $url"
    local resp
    resp=$(graph_request GET "$url")

    case "$format" in
        raw)  echo "$resp" | jq -c . ;;
        json) echo "$resp" | jq . ;;
        summary) print_task_summary "$resp" ;;
        *) die "unknown format: $format" ;;
    esac
}

cmd_create() {
    local title="" body="" due="" list_id="" apply=0 yes=0
    while (( $# > 0 )); do
        case "$1" in
            --title)    title="$2"; shift 2 ;;
            --body)     body="$2"; shift 2 ;;
            --due)      due="$2"; shift 2 ;;
            --list-id)  list_id="$2"; shift 2 ;;
            --apply)    apply=1; shift ;;
            --yes)      yes=1; shift ;;
            -h|--help)  usage; exit 0 ;;
            *)          die "unknown option: $1" ;;
        esac
    done
    [[ -n "$title" ]] || die "--title is required for create"

    load_config || die "config missing"
    load_tokens || die "tokens missing"
    ensure_fresh_token

    list_id=$(_resolve_list_id "$list_id")
    local enc_list
    enc_list=$(_urlencode_id "$list_id")

    local payload
    payload=$(build_task_body "$title" "$body" "$due")

    echo "--- Proposed new task ---" >&2
    echo "$payload" | jq . >&2
    echo "" >&2

    if ! require_apply_and_confirm "$apply" "$yes" "CREATE task '$title'"; then
        exit 0
    fi

    local url="${OUTLOOK_TODO_GRAPH_BASE}/me/todo/lists/$enc_list/tasks"
    echo "POST $url ..." >&2
    local resp
    resp=$(graph_request POST "$url" "$payload")
    echo "--- Created task ---" >&2
    print_task_summary "$resp" >&2
}

cmd_update() {
    local task_id="" title="" body="" due="" list_id="" apply=0 yes=0
    while (( $# > 0 )); do
        case "$1" in
            --task-id)  task_id="$2"; shift 2 ;;
            --title)    title="$2"; shift 2 ;;
            --body)     body="$2"; shift 2 ;;
            --due)      due="$2"; shift 2 ;;
            --list-id)  list_id="$2"; shift 2 ;;
            --apply)    apply=1; shift ;;
            --yes)      yes=1; shift ;;
            -h|--help)  usage; exit 0 ;;
            *)          die "unknown option: $1" ;;
        esac
    done
    [[ -n "$task_id" ]] || die "--task-id is required"

    if [[ -z "$title" && -z "$body" && -z "$due" ]]; then
        die "at least one field to update is required (--title, --body, --due)"
    fi

    load_config || die "config missing"
    load_tokens || die "tokens missing"
    ensure_fresh_token

    list_id=$(_resolve_list_id "$list_id")
    local enc_list enc_task
    enc_list=$(_urlencode_id "$list_id")
    enc_task=$(_urlencode_id "$task_id")

    # 1. Fetch current state
    local url="${OUTLOOK_TODO_GRAPH_BASE}/me/todo/lists/$enc_list/tasks/$enc_task"
    log_info "GET $url (fetch current state)"
    local current
    current=$(graph_request GET "$url")

    echo "--- Current task ---" >&2
    print_task_summary "$current" >&2
    echo "" >&2

    # 2. Build PATCH body
    local payload
    payload=$(build_task_body "$title" "$body" "$due")

    echo "--- Proposed changes ---" >&2
    echo "$payload" | jq . >&2
    echo "" >&2

    # 3. Dry-run or apply (with confirmation)
    if ! require_apply_and_confirm "$apply" "$yes" "UPDATE task $task_id"; then
        exit 0
    fi

    echo "Applying PATCH to $url ..." >&2
    local resp
    resp=$(graph_request PATCH "$url" "$payload")
    echo "--- Updated task ---" >&2
    print_task_summary "$resp" >&2
}

cmd_complete() {
    local task_id="" list_id="" apply=0 yes=0
    while (( $# > 0 )); do
        case "$1" in
            --task-id)  task_id="$2"; shift 2 ;;
            --list-id)  list_id="$2"; shift 2 ;;
            --apply)    apply=1; shift ;;
            --yes)      yes=1; shift ;;
            -h|--help)  usage; exit 0 ;;
            *)          die "unknown option: $1" ;;
        esac
    done
    [[ -n "$task_id" ]] || die "--task-id is required"

    load_config || die "config missing"
    load_tokens || die "tokens missing"
    ensure_fresh_token

    list_id=$(_resolve_list_id "$list_id")
    local enc_list enc_task
    enc_list=$(_urlencode_id "$list_id")
    enc_task=$(_urlencode_id "$task_id")

    local url="${OUTLOOK_TODO_GRAPH_BASE}/me/todo/lists/$enc_list/tasks/$enc_task"
    log_info "GET $url (fetching before complete)"
    local current
    current=$(graph_request GET "$url")

    echo "--- Task to complete ---" >&2
    print_task_summary "$current" >&2
    echo "" >&2

    local payload='{"status": "completed"}'

    if ! require_apply_and_confirm "$apply" "$yes" "COMPLETE task $task_id"; then
        exit 0
    fi

    echo "Applying PATCH (status=completed) to $url ..." >&2
    local resp
    resp=$(graph_request PATCH "$url" "$payload")
    echo "--- Completed task ---" >&2
    print_task_summary "$resp" >&2
}

cmd_delete() {
    local task_id="" list_id="" apply=0 yes=0
    while (( $# > 0 )); do
        case "$1" in
            --task-id)  task_id="$2"; shift 2 ;;
            --list-id)  list_id="$2"; shift 2 ;;
            --apply)    apply=1; shift ;;
            --yes)      yes=1; shift ;;
            -h|--help)  usage; exit 0 ;;
            *)          die "unknown option: $1" ;;
        esac
    done
    [[ -n "$task_id" ]] || die "--task-id is required"

    load_config || die "config missing"
    load_tokens || die "tokens missing"
    ensure_fresh_token

    list_id=$(_resolve_list_id "$list_id")
    local enc_list enc_task
    enc_list=$(_urlencode_id "$list_id")
    enc_task=$(_urlencode_id "$task_id")

    local url="${OUTLOOK_TODO_GRAPH_BASE}/me/todo/lists/$enc_list/tasks/$enc_task"
    log_info "GET $url (fetching before delete)"
    local current
    current=$(graph_request GET "$url")

    echo "--- Task to be deleted ---" >&2
    print_task_summary "$current" >&2
    echo "" >&2

    if ! require_apply_and_confirm "$apply" "$yes" "DELETE task $task_id"; then
        exit 0
    fi

    graph_request DELETE "$url" >/dev/null
    log_info "task deleted ($task_id)"
}

# ---- Dispatch --------------------------------------------------------------

SUBCMD="${1:-}"
shift || true

case "$SUBCMD" in
    -h|--help|"")  usage; exit 0 ;;
    get)            cmd_get "$@" ;;
    create)         cmd_create "$@" ;;
    update)         cmd_update "$@" ;;
    complete)       cmd_complete "$@" ;;
    delete)         cmd_delete "$@" ;;
    *)              die "unknown subcommand: $SUBCMD" ;;
esac