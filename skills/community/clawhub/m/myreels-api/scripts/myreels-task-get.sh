#!/usr/bin/env bash
[ -n "${BASH_VERSION:-}" ] || exec bash "$0" "$@"

usage() {
  cat <<'EOF'
Usage:
  myreels-task-get.sh <task_id> [--raw]
  myreels-task-get.sh -h | --help

Description:
  Query a task and derive the next action for agent-side orchestration.

Options:
  --raw    Return the raw query response without simplification

Returns:
  Default:
    Simplified JSON with status, progress, nextAction, nextActionHint, and resultUrls when present
  --raw:
    Raw API response body

nextAction mapping:
  pending     -> WAIT
  processing  -> WAIT
  completed   -> DELIVER
  done        -> DELIVER
  failed      -> FAILED
  cancelled   -> FAILED
  warning     -> REVIEW
  other       -> REVIEW
EOF
}

source "$(dirname "$0")/_common.sh"

task_id=""
raw=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --raw)
      raw=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    -*)
      echo "Error: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
    *)
      if [[ -n "$task_id" ]]; then
        echo "Error: unexpected argument: $1" >&2
        usage >&2
        exit 2
      fi
      task_id="$1"
      shift
      ;;
  esac
done

[[ -n "$task_id" ]] || { usage >&2; exit 2; }

payload=$(myreels_get_auth "/query/task/${task_id}")
myreels_require_api_ok "$payload" "Task query failed" || exit 1

if [[ "$raw" == "true" ]]; then
  echo "$payload" | jq '.'
  exit 0
fi

task_status=$(echo "$payload" | jq -r '.data.status // ""')

case "$task_status" in
  pending|processing)
    next_action="WAIT"
    hint="Task is still running. Poll again using the documented interval for the task type."
    ;;
  completed|done)
    next_action="DELIVER"
    hint="Task completed. Deliver resultUrls to the user and persist them on your side if needed."
    ;;
  failed|cancelled)
    next_action="FAILED"
    hint="Task failed. Review the request body, model choice, and response message before retrying."
    ;;
  warning)
    next_action="REVIEW"
    hint="Task returned warning status. Inspect the response message and resultUrls before deciding whether to deliver or retry."
    ;;
  *)
    next_action="REVIEW"
    hint="Unknown task status. Inspect the raw response before retrying."
    ;;
esac

echo "$payload" | jq \
  --arg taskID "$task_id" \
  --arg nextAction "$next_action" \
  --arg nextActionHint "$hint" \
  '{
    taskID: $taskID,
    status: (.data.status // null),
    progress: (.data.progress // null),
    nextAction: $nextAction,
    nextActionHint: $nextActionHint
  }
  + (if (.message // "") != "" then {message: .message} else {} end)
  + (if (.data.resultUrls? // null) != null then {resultUrls: .data.resultUrls} else {} end)'
