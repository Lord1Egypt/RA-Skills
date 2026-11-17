#!/usr/bin/env bash
# Read Microsoft To Do lists/tasks via shared Outlook Graph auth.
set -Eeuo pipefail
IFS=$' \t\n'

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
CAL_LIB="$SCRIPT_DIR/_lib.sh"
# shellcheck source=./_lib.sh
. "$CAL_LIB"

usage() {
  cat >&2 <<'USAGE'
Usage: todo-read.sh <lists|tasks> [options]

Commands:
  lists                   List Microsoft To Do task lists.
  tasks                   List tasks from one task list.

Options:
  --list-id ID            Task list id for tasks.
  --list-name NAME        Task list display name for tasks.
  --status STATUS         notCompleted (default) | all | completed | notStarted | inProgress
  --top N                 Page size (default 100; 1..1000).
  --format FMT            summary (default) | json | ids | raw
  -h, --help              Show help.
USAGE
}

CMD="${1:-}"
shift || true
[[ -n "$CMD" && "$CMD" != "-h" && "$CMD" != "--help" ]] || { usage; exit 0; }
case "$CMD" in lists|tasks) : ;; *) usage; die "unknown command: $CMD" ;; esac

FORMAT="summary"
STATUS="notCompleted"
TOP=100
LIST_ID=""
LIST_NAME=""
while (( $# > 0 )); do
  case "$1" in
    --list-id) LIST_ID="${2:-}"; shift 2 ;;
    --list-name) LIST_NAME="${2:-}"; shift 2 ;;
    --status) STATUS="${2:-}"; shift 2 ;;
    --top) TOP="${2:-}"; shift 2 ;;
    --format) FORMAT="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) die "unknown argument: $1" ;;
  esac
done
case "$FORMAT" in summary|json|ids|raw) : ;; *) die "invalid --format: $FORMAT" ;; esac
case "$STATUS" in notCompleted|all|completed|notStarted|inProgress) : ;; *) die "invalid --status: $STATUS" ;; esac
[[ "$TOP" =~ ^[0-9]+$ ]] || die "--top must be numeric"
(( TOP >= 1 && TOP <= 1000 )) || die "--top must be 1..1000"

load_config || die "config missing; run scripts/setup-device-code.sh first"
ensure_fresh_token

collect_pages() {
  local path="$1"
  local tmp resp_file page=0 next="$path" resp next_link
  tmp=$(mktemp)
  resp_file=$(mktemp)
  printf '[]\n' > "$tmp"
  trap 'rm -f "$tmp" "$resp_file"' RETURN
  while :; do
    page=$((page + 1))
    (( page <= 20 )) || { log_warn "stopped after 20 pages"; break; }
    graph_request GET "$next" > "$resp_file"
    python3 - "$tmp" "$resp_file" <<'PY'
import json, sys
acc_path, resp_path = sys.argv[1], sys.argv[2]
try:
    with open(acc_path, 'r', encoding='utf-8') as f:
        current = json.load(f)
except Exception:
    current = []
with open(resp_path, 'r', encoding='utf-8') as f:
    resp = json.load(f)
current.extend(resp.get('value') or [])
with open(acc_path, 'w', encoding='utf-8') as f:
    json.dump(current, f, ensure_ascii=False)
PY
    next_link=$(jq -r '."@odata.nextLink" // empty' "$resp_file")
    [[ -n "$next_link" ]] || break
    next="$next_link"
  done
  cat "$tmp"
}

print_lists() {
  local lists="$1"
  case "$FORMAT" in
    json) printf '%s\n' "$lists" | jq . ;;
    raw) printf '%s\n' "$lists" ;;
    ids) printf '%s\n' "$lists" | jq -r '.[]?.id // empty' ;;
    summary)
      printf '%-40s  %-16s  %s\n' "ID" "WELL_KNOWN" "DISPLAY_NAME"
      printf '%-40s  %-16s  %s\n' "----------------------------------------" "----------------" "------------"
      printf '%s\n' "$lists" | jq -r '.[] | [(.id//"-"), (.wellknownListName//.wellKnownListName//"-"), (.displayName//"-")] | @tsv' |
        awk -F'\t' '{ printf "%-40s  %-16s  %s\n", $1, $2, $3 }'
      ;;
  esac
}

print_tasks() {
  local tasks="$1"
  local filtered
  case "$STATUS" in
    all) filtered="$tasks" ;;
    notCompleted) filtered=$(printf '%s\n' "$tasks" | jq -c '[.[] | select((.status // "") != "completed")]') ;;
    *) filtered=$(printf '%s\n' "$tasks" | jq -c --arg st "$STATUS" '[.[] | select((.status // "") == $st)]') ;;
  esac
  case "$FORMAT" in
    json) printf '%s\n' "$filtered" | jq . ;;
    raw) printf '%s\n' "$filtered" ;;
    ids) printf '%s\n' "$filtered" | jq -r '.[]?.id // empty' ;;
    summary)
      printf '%-40s  %-12s  %-19s  %s\n' "ID" "STATUS" "DUE" "TITLE"
      printf '%-40s  %-12s  %-19s  %s\n' "----------------------------------------" "------------" "-------------------" "-----"
      printf '%s\n' "$filtered" | jq -r '
        .[] | [
          (.id//"-"),
          (.status//"-"),
          (.dueDateTime.dateTime//"-"),
          (.title//"-")
        ] | @tsv' | awk -F'\t' '{ printf "%-40s  %-12s  %-19s  %s\n", $1, $2, $3, $4 }'
      ;;
  esac
}

if [[ "$CMD" == "lists" ]]; then
  DATA=$(collect_pages "/me/todo/lists?\$top=$TOP")
  print_lists "$DATA"
  exit 0
fi

LISTS=$(collect_pages "/me/todo/lists?\$top=100")
if [[ -z "$LIST_ID" ]]; then
  if [[ -n "$LIST_NAME" ]]; then
    LIST_ID=$(printf '%s\n' "$LISTS" | jq -r --arg name "$LIST_NAME" '.[] | select((.displayName//"") == $name) | .id' | head -n 1)
    [[ -n "$LIST_ID" ]] || die "no task list found with displayName=$LIST_NAME"
  else
    LIST_ID=$(printf '%s\n' "$LISTS" | jq -r '.[] | select((.wellknownListName//.wellKnownListName//"") == "defaultList") | .id' | head -n 1)
    if [[ -z "$LIST_ID" ]]; then
      LIST_ID=$(printf '%s\n' "$LISTS" | jq -r '.[0].id // empty')
    fi
    [[ -n "$LIST_ID" ]] || die "no To Do task lists found"
  fi
fi
ENC_ID=$(python3 - <<'PY' "$LIST_ID"
import sys, urllib.parse
print(urllib.parse.quote(sys.argv[1], safe=''))
PY
)
DATA=$(collect_pages "/me/todo/lists/$ENC_ID/tasks?\$top=$TOP")
print_tasks "$DATA"
