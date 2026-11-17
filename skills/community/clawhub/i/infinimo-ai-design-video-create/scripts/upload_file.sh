#!/usr/bin/env bash
set -euo pipefail
FILE="${1:?Usage: upload_file.sh <file-path>}"
TOKEN="${INFINIMO_TOKEN:-${INFINIMO_API_KEY:?Set INFINIMO_TOKEN or INFINIMO_API_KEY}}"
curl -s -X POST "https://www.clawec.com/api/upload/file" \
  -H "Token: $TOKEN" \
  -F "file=@${FILE}" -F "platform=1" -F "terminal=4" -F "language=en"
