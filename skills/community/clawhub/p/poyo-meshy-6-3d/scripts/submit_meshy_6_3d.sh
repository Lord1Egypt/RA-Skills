#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  cat <<'EOF' >&2
Usage:
  export POYO_API_KEY
  submit_meshy_6_3d.sh <payload.json>

The payload file should contain a PoYo submit request for a Meshy 6 3D model.
EOF
  exit 1
fi

: "${POYO_API_KEY:?POYO_API_KEY is required}"
payload_file="$1"

curl -sS https://api.poyo.ai/api/generate/submit \
  -H "Authorization: Bearer ${POYO_API_KEY}" \
  -H 'Content-Type: application/json' \
  --data @"${payload_file}"
