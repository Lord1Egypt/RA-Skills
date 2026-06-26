#!/usr/bin/env bash
set -euo pipefail

CONFIG_FILE="${MANUS_CONFIG_FILE:-$HOME/.config/manus-openclaw-bridge/manus.env}"

if [[ -f "$CONFIG_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$CONFIG_FILE"
fi

if [[ -z "${MANUS_API_KEY:-}" ]]; then
  echo "MANUS_API_KEY is not set. Put it in $CONFIG_FILE" >&2
  exit 1
fi

if [[ -z "${MANUS_API_BASE:-}" ]]; then
  echo "MANUS_API_BASE is not set. Put it in $CONFIG_FILE" >&2
  exit 1
fi

if [[ ! "$MANUS_API_BASE" =~ ^https:// ]]; then
  echo "MANUS_API_BASE must start with https://" >&2
  exit 1
fi

TASK_ID="${1:-}"
if [[ -z "$TASK_ID" ]]; then
  echo "Usage: $0 <task_id>" >&2
  exit 1
fi

curl --silent --show-error --fail \
  --request GET \
  --url "$MANUS_API_BASE/v1/tasks/${TASK_ID}" \
  --header 'accept: application/json' \
  --header "API_KEY: ${MANUS_API_KEY}"
