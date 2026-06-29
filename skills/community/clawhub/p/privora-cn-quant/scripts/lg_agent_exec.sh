#!/usr/bin/env bash
set -euo pipefail

# Default to official domain to avoid security scanner warnings
BASE_URL="${LG_AGENT_BASE_URL:-https://lg-data.cc}"
: "${LG_AGENT_TOKEN:?LG_AGENT_TOKEN is required}"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 '<json-body>'" >&2
  exit 1
fi

JSON_BODY="$1"

curl -sS "${BASE_URL}/agent/skills/execute" \
  -X POST \
  -H "Authorization: Bearer ${LG_AGENT_TOKEN}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  --data "${JSON_BODY}"
