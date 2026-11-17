#!/usr/bin/env bash
set -euo pipefail

TOKEN="${INFINIMO_TOKEN:-${INFINIMO_API_KEY:?Set INFINIMO_TOKEN or INFINIMO_API_KEY}}"

curl -s -G "https://www.clawec.com/api/aigc/ec_media/image/create/dic" \
  -H "Token: $TOKEN" \
  --data-urlencode "platform=1" \
  --data-urlencode "terminal=4" \
  --data-urlencode "language=en"
