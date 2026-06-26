#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  cat <<'EOF' >&2
Usage:
  POYO_API_KEY=... submit_sora_2.sh <payload.json>
  submit_sora_2.sh <api_key> <payload.json>

Examples:
  POYO_API_KEY="$POYO_API_KEY" submit_sora_2.sh payload.json
  submit_sora_2.sh "$POYO_API_KEY" payload.json
EOF
  exit 1
fi

if [[ $# -eq 1 ]]; then
  : "${POYO_API_KEY:?POYO_API_KEY is required when api_key is not passed explicitly}"
  api_key="$POYO_API_KEY"
  payload_file="$1"
else
  api_key="$1"
  payload_file="$2"
fi

curl -sS https://api.poyo.ai/api/generate/submit \
  -H "Authorization: Bearer ${api_key}" \
  -H 'Content-Type: application/json' \
  --data @"${payload_file}"
