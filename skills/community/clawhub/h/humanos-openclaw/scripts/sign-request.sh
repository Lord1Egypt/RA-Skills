#!/usr/bin/env bash
set -euo pipefail

via_curl() {
  local method="$1"
  local path="$2"
  local body="${3:-}"
  local base_url="${VIA_API_URL:-https://api.humanos.id}"

  local timestamp
  if timestamp=$(date +%s%3N 2>/dev/null) && [[ "$timestamp" =~ ^[0-9]{13}$ ]]; then
    :
  else
    timestamp="$(( $(date +%s) * 1000 ))"
  fi

  local sign_payload
  if [[ -n "$body" ]]; then
    sign_payload="${timestamp}.${body}"
  else
    sign_payload="${timestamp}"
  fi

  local signature
  signature=$(printf '%s' "$sign_payload" | openssl dgst -sha256 -hmac "$VIA_SIGNATURE_SECRET" | awk '{print $NF}')

  curl -s -X "$method" \
    "${base_url}${path}" \
    -H "Authorization: Bearer ${VIA_API_KEY}" \
    -H "X-Timestamp: ${timestamp}" \
    -H "X-Signature: ${signature}" \
    -H "Content-Type: application/json" \
    ${body:+-d "$body"} | jq .
}
