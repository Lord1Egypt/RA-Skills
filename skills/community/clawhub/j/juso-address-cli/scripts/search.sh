#!/usr/bin/env bash
# juso-address-cli / search.sh
# 도로명주소 / 지번주소 keyword search against juso.go.kr addrLinkApi.
# Prints one JSON object per matching address (JSONL) on stdout.
#
# Usage:
#   search.sh <keyword> [--per-page N] [--page N] [--history Y|N] [--sort road|location|none]
#
# Env: JUSO_CONFM_KEY (required, grade-A or grade-B)

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: search.sh <keyword> [--per-page N] [--page N] [--history Y|N] [--sort road|location|none]" >&2
  exit 64
fi

keyword="$1"; shift
per_page="10"
page="1"
history="N"
sort="none"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --per-page) per_page="$2"; shift 2;;
    --page)     page="$2"; shift 2;;
    --history)  history="$2"; shift 2;;
    --sort)     sort="$2"; shift 2;;
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
  --data-urlencode "hstryYn=${history}" \
  --data-urlencode "firstSort=${sort}" \
  "https://business.juso.go.kr/addrlink/addrLinkApi.do")

code=$(printf '%s' "$resp" | jq -r '.results.common.errorCode // empty')
if [[ -n "$code" && "$code" != "0" ]]; then
  msg=$(printf '%s' "$resp" | jq -r '.results.common.errorMessage // "unknown"')
  echo "juso API error ${code}: ${msg}" >&2
  exit 1
fi

printf '%s' "$resp" | jq -c '.results.juso[]? // empty'
