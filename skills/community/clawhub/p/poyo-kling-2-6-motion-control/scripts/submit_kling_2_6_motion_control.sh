#!/bin/sh
set -eu

api_key="${POYO_API_KEY:-${1:-}}"
if [ -z "$api_key" ]; then
  echo "Usage: submit_kling_2_6_motion_control.sh [api_key] [payload.json]" >&2
  echo "Or set POYO_API_KEY and pass [payload.json]. If no payload file is given, JSON is read from stdin." >&2
  exit 1
fi

payload="${2:-${1:+}}"
if [ -n "${POYO_API_KEY:-}" ]; then
  payload="${1:-}"
fi

if [ -n "$payload" ] && [ "$payload" != "$api_key" ]; then
  body=$(cat "$payload")
else
  body=$(cat)
fi

curl -sS https://api.poyo.ai/api/generate/submit   -H "Authorization: Bearer $api_key"   -H 'Content-Type: application/json'   -d "$body"
