#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)"

HOST="${HOST:-}"
AUTH_TOKEN="${AUTH_TOKEN:-}"
TASK_ID="${TASK_ID:-}"
MAX_POLL_ATTEMPTS="${MAX_POLL_ATTEMPTS:-20}"
POLL_INTERVAL_SECONDS="${POLL_INTERVAL_SECONDS:-2}"
MAX_TIME="${MAX_TIME:-20}"

if [[ -z "$HOST" ]]; then
  echo "HOST is required." >&2
  exit 2
fi

if [[ -z "$AUTH_TOKEN" ]]; then
  echo "AUTH_TOKEN is required." >&2
  exit 2
fi

normalize_host() {
  local value="$1"
  printf '%s' "${value%/}"
}

extract_json_field() {
  local json="$1"
  local path="$2"
  python3 - "$json" "$path" <<'PY'
import json
import sys

raw = sys.argv[1]
path = sys.argv[2]
try:
    data = json.loads(raw)
except json.JSONDecodeError:
    print("")
    sys.exit(0)

node = data
for part in path.split("."):
    if isinstance(node, dict) and part in node:
        node = node[part]
    else:
        print("")
        sys.exit(0)

if node is None:
    print("")
elif isinstance(node, bool):
    print("true" if node else "false")
else:
    print(str(node))
PY
}

request_json() {
  local method="$1"
  local url="$2"
  local body="${3:-}"

  if [[ -n "$body" ]]; then
    curl -sS --max-time "$MAX_TIME" \
      -X "$method" "$url" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer ${AUTH_TOKEN}" \
      -d "$body"
    return
  fi

  curl -sS --max-time "$MAX_TIME" \
    -X "$method" "$url" \
    -H "Authorization: Bearer ${AUTH_TOKEN}"
}

HOST="$(normalize_host "$HOST")"
SUBMIT_URL="${HOST}/v1/tasks/export"

if [[ -z "$TASK_ID" ]]; then
  echo "[INFO] TASK_ID not provided, submitting async task..."
  SUBMIT_BODY='{"scope":"daily","format":"csv"}'
  SUBMIT_RESPONSE="$(request_json "POST" "$SUBMIT_URL" "$SUBMIT_BODY")"
  TASK_ID="$(extract_json_field "$SUBMIT_RESPONSE" "data.taskId")"

  if [[ -z "$TASK_ID" ]]; then
    echo "[FAIL] could not extract data.taskId from submit response." >&2
    echo "[DETAIL] submit response: $SUBMIT_RESPONSE" >&2
    exit 1
  fi
fi

echo "[INFO] using TASK_ID=${TASK_ID}"

STATUS_URL="${HOST}/v1/tasks/${TASK_ID}"
attempt=1
terminal_state=""
last_response=""

while (( attempt <= MAX_POLL_ATTEMPTS )); do
  last_response="$(request_json "GET" "$STATUS_URL")"
  state="$(extract_json_field "$last_response" "data.state")"
  progress="$(extract_json_field "$last_response" "data.progress")"

  echo "[POLL] attempt=${attempt}/${MAX_POLL_ATTEMPTS} state=${state:-unknown} progress=${progress:-n/a}"

  case "${state}" in
    succeeded)
      terminal_state="succeeded"
      break
      ;;
    failed|canceled|cancelled)
      terminal_state="$state"
      break
      ;;
    *)
      ;;
  esac

  sleep "$POLL_INTERVAL_SECONDS"
  ((attempt++))
done

if [[ "$terminal_state" != "succeeded" ]]; then
  echo "[FAIL] async task did not reach succeeded state." >&2
  echo "[DETAIL] terminal_state=${terminal_state:-timeout}" >&2
  echo "[DETAIL] last_status_response=${last_response:-<empty>}" >&2
  exit 1
fi

echo "[INFO] polling succeeded, running reusable assertions..."
TASK_ID="$TASK_ID" AUTH_TOKEN="$AUTH_TOKEN" HOST="$HOST" bash "${SCRIPT_DIR}/async-job-polling.api-verify.sh"
