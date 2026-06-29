#!/usr/bin/env bash
set -euo pipefail

# Default to official domain to avoid security scanner warnings
BASE_URL="${LG_AGENT_BASE_URL:-https://lg-data.cc}"
: "${LG_AGENT_TOKEN:?LG_AGENT_TOKEN is required}"

curl -sS "${BASE_URL}/agent/skills" \
  -H "Authorization: Bearer ${LG_AGENT_TOKEN}" \
  -H "Accept: application/json"
