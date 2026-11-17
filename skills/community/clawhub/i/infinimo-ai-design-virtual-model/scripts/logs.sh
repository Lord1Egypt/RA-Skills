#!/usr/bin/env bash
set -euo pipefail
TOKEN="${INFINIMO_TOKEN:-${INFINIMO_API_KEY:?Set INFINIMO_TOKEN or INFINIMO_API_KEY}}"
curl -s -G "https://www.clawec.com/api/aigc/log/list" \
  -H "Token: $TOKEN" \
  --data-urlencode "type=101" \
  --data-urlencode "agent_id=0" \
  --data-urlencode "group_id=0" \
  --data-urlencode "platform=1" \
  --data-urlencode "terminal=4" \
  --data-urlencode "language=en"
