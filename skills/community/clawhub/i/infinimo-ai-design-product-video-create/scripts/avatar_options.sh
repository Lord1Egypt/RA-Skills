#!/usr/bin/env bash
set -euo pipefail
START="${1:-1}"
SIZE="${2:-10}"
GENDER="${3:-}"
RACE="${4:-}"
TOKEN="${INFINIMO_TOKEN:-${INFINIMO_API_KEY:?Set INFINIMO_TOKEN or INFINIMO_API_KEY}}"
ARGS=(--data-urlencode "start=${START}" --data-urlencode "size=${SIZE}" \
  --data-urlencode "platform=1" --data-urlencode "terminal=4" --data-urlencode "language=en")
[[ -n "$GENDER" ]] && ARGS+=(--data-urlencode "gender=${GENDER}")
[[ -n "$RACE" ]] && ARGS+=(--data-urlencode "race=${RACE}")
curl -s -G "https://www.clawec.com/api/aigc/ec_product_video/image/create/avatar_options" \
  -H "Token: $TOKEN" "${ARGS[@]}"
