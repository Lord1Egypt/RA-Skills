#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 payload.json" >&2
  exit 2
fi

: "${POYO_API_KEY:?POYO_API_KEY is required}"

payload_file="$1"

curl --fail-with-body --request POST \
  --url "https://api.poyo.ai/api/generate/submit" \
  --header "Authorization: Bearer ${POYO_API_KEY}" \
  --header "Content-Type: application/json" \
  --data @"${payload_file}"
