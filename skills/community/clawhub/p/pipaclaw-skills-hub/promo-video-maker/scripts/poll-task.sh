#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KIND="${1:?usage: poll-task.sh image|video TASK_ID [INTERVAL_SECONDS] [MAX_ATTEMPTS]}"
TASK_ID="${2:?usage: poll-task.sh image|video TASK_ID [INTERVAL_SECONDS] [MAX_ATTEMPTS]}"
INTERVAL="${3:-3}"
MAX_ATTEMPTS="${4:-40}"

for ((i=1; i<=MAX_ATTEMPTS; i++)); do
  RESPONSE="$("$SCRIPT_DIR/hub-api.sh" GET "/api/v1/hub/tasks/$KIND/$TASK_ID")"

  STATUS="$(
    printf '%s' "$RESPONSE" | python3 -c '
import json
import sys

payload = json.load(sys.stdin)
task = (payload.get("data") or {}).get("task") or {}
print(task.get("status", "unknown"))
'
  )"

  echo "[$i/$MAX_ATTEMPTS] $STATUS"
  echo "$RESPONSE"

  if [[ "$STATUS" == "completed" || "$STATUS" == "failed" || "$STATUS" == "dead" ]]; then
    exit 0
  fi

  sleep "$INTERVAL"
done

echo "task still not finished after $MAX_ATTEMPTS attempts" >&2
exit 1
