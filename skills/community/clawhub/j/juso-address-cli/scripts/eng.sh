#!/usr/bin/env bash
# juso-address-cli / eng.sh
# English road-address search (addrEngLinkApi).
# Prints one JSON object per matching English address (JSONL).
#
# Usage:
#   eng.sh <keyword> [--per-page N] [--page N]
#
# Env: JUSO_CONFM_KEY (required)

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: eng.sh <keyword> [--per-page N] [--page N]" >&2
  exit 64
fi

keyword="$1"; shift
per_page="10"
page="1"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --per-page) per_page="$2"; shift 2;;
    --page)     page="$2"; shift 2;;
    *) echo "unknown flag: $1" >&2; exit 64;;
  esac
done

: "${JUSO_CONFM_KEY:?JUSO_CONFM_KEY is not set — get a key at https://business.juso.go.kr/addrlink/openApi/apiExprn.do}"

resp=$(curl -sS --get \
  --data-urlencode "confmKey=${JUSO_CONFM_KEY}" \
  --data-urlencode "currentPage=${page}" \
  --data-urlencode "countPerPage=${per_page}" \
  --data-urlencode "keyword=${keyword}" \
  --data-urlencode "resultType=json" \
  "https://business.juso.go.kr/addrlink/addrEngLinkApi.do")

code=$(printf '%s' "$resp" | jq -r '.results.common.errorCode // empty')
if [[ -n "$code" && "$code" != "0" ]]; then
  msg=$(printf '%s' "$resp" | jq -r '.results.common.errorMessage // "unknown"')
  echo "juso API error ${code}: ${msg}" >&2
  exit 1
fi

printf '%s' "$resp" | jq -c '.results.juso[]? // empty'
