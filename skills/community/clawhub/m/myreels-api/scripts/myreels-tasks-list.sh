#!/usr/bin/env bash
[ -n "${BASH_VERSION:-}" ] || exec bash "$0" "$@"

usage() {
  cat <<'EOF'
Usage:
  myreels-tasks-list.sh [--page <n>] [--limit <n>] [--status <value>] [--start-date <iso>] [--raw]
  myreels-tasks-list.sh -h | --help

Description:
  Query the authenticated user's task list through GET /generation/tasks.

Options:
  --page <n>               Page number (default: 1)
  --limit <n>              Page size (default: 10)
  --status <value>         Filter by task status:
                           pending, processing, completed, failed, cancelled, warning
  --start-date <iso>       Filter by start date, preferably ISO-8601
  --raw                    Return the full Worker response instead of .data

Returns:
  Default:
    .data from GET /generation/tasks
  --raw:
    full Worker response wrapper

Notes:
  For GET requests, the script sends filters as query parameters.
EOF
}

source "$(dirname "$0")/_common.sh"

urlencode() {
  jq -nr --arg v "$1" '$v|@uri'
}

page="1"
limit="10"
status=""
start_date=""
raw=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --page)
      [[ $# -ge 2 ]] || { echo "Error: --page requires a value" >&2; exit 2; }
      page="$2"
      shift 2
      ;;
    --limit)
      [[ $# -ge 2 ]] || { echo "Error: --limit requires a value" >&2; exit 2; }
      limit="$2"
      shift 2
      ;;
    --status)
      [[ $# -ge 2 ]] || { echo "Error: --status requires a value" >&2; exit 2; }
      status="$2"
      shift 2
      ;;
    --start-date)
      [[ $# -ge 2 ]] || { echo "Error: --start-date requires a value" >&2; exit 2; }
      start_date="$2"
      shift 2
      ;;
    --raw)
      raw=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Error: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ ! "$page" =~ ^[1-9][0-9]*$ ]]; then
  echo "Error: page must be a positive integer: $page" >&2
  exit 2
fi

if [[ ! "$limit" =~ ^[1-9][0-9]*$ ]]; then
  echo "Error: limit must be a positive integer: $limit" >&2
  exit 2
fi

if [[ -n "$status" ]]; then
  case "$status" in
    pending|processing|completed|failed|cancelled|warning)
      ;;
    *)
      echo "Error: invalid status: $status" >&2
      echo "Allowed: pending processing completed failed cancelled warning" >&2
      exit 2
      ;;
  esac
fi

query="page=$(urlencode "$page")&limit=$(urlencode "$limit")"
if [[ -n "$status" ]]; then
  query="${query}&status=$(urlencode "$status")"
fi
if [[ -n "$start_date" ]]; then
  query="${query}&startDate=$(urlencode "$start_date")"
fi

payload=$(myreels_get_auth "/generation/tasks?${query}")
myreels_require_api_ok "$payload" "Task list query failed" || exit 1

if [[ "$raw" == "true" ]]; then
  echo "$payload" | jq '.'
else
  echo "$payload" | jq '.data // {}'
fi
