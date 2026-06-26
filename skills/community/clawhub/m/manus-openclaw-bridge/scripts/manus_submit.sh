#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
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

PROMPT="${1:-}"
if [[ -z "$PROMPT" ]]; then
  echo "Usage: $0 \"<prompt>\"" >&2
  exit 1
fi

AGENT_PROFILE="${MANUS_AGENT_PROFILE:-manus-1.6}"
TASK_MODE="${MANUS_TASK_MODE:-agent}"

curl --silent --show-error --fail \
  --request POST \
  --url "$MANUS_API_BASE/v1/tasks" \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --header "API_KEY: ${MANUS_API_KEY}" \
  --data "{\"prompt\":\"${PROMPT//\"/\\\"}\",\"agentProfile\":\"${AGENT_PROFILE}\",\"taskMode\":\"${TASK_MODE}\"}"
