#!/usr/bin/env bash
set -euo pipefail

START="${1:-1}"
SIZE="${2:-5}"
TOKEN="${INFINIMO_TOKEN:-${INFINIMO_API_KEY:?Set INFINIMO_TOKEN or INFINIMO_API_KEY}}"

curl -s -G "https://www.clawec.com/api/aigc/ec_media/image/create/logs/product" \
  -H "Token: $TOKEN" \
  --data-urlencode "start=${START}" \
  --data-urlencode "size=${SIZE}" \
  --data-urlencode "platform=1" \
  --data-urlencode "terminal=4" \
  --data-urlencode "language=en"
