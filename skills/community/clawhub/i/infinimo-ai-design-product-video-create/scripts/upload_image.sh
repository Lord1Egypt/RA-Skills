#!/usr/bin/env bash
set -euo pipefail
FILE="${1:?Usage: upload_image.sh <image-path>}"
TOKEN="${INFINIMO_TOKEN:-${INFINIMO_API_KEY:?Set INFINIMO_TOKEN or INFINIMO_API_KEY}}"
curl -s -X POST "https://www.clawec.com/api/upload/image" \
  -H "Token: $TOKEN" \
  -F "file=@${FILE}" -F "platform=1" -F "terminal=4" -F "language=en"
