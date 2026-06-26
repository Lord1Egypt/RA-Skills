#!/usr/bin/env bash
# juso-address-cli / coord.sh
# Entrance-coordinate lookup (addrCoordApi) — grade-B (운영용) 확인키 required.
# Prints a single JSON object with entX/entY (EPSG:5179-like grid by default).
#
# Usage:
#   coord.sh --admcode <code> --rnmgmcd <rnMgtSn> --udrtyn <0|1> \
#            --buldmnnm <N> --buldslno <N> [--srchwrd <raw>]
#
# Env: JUSO_CONFM_KEY_COORD (required, grade-B)

set -euo pipefail

admcode=""
rnmgmcd=""
udrtyn="0"
buldmnnm=""
buldslno="0"
srchwrd=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --admcode)  admcode="$2"; shift 2;;
    --rnmgmcd)  rnmgmcd="$2"; shift 2;;
    --udrtyn)   udrtyn="$2"; shift 2;;
    --buldmnnm) buldmnnm="$2"; shift 2;;
    --buldslno) buldslno="$2"; shift 2;;
    --srchwrd)  srchwrd="$2"; shift 2;;
    *) echo "unknown flag: $1" >&2; exit 64;;
  esac
done

if [[ -z "$admcode" || -z "$rnmgmcd" || -z "$buldmnnm" ]]; then
  echo "usage: coord.sh --admcode <code> --rnmgmcd <rnMgtSn> --udrtyn <0|1> --buldmnnm <N> --buldslno <N> [--srchwrd <raw>]" >&2
  echo "hint: run scripts/search.sh first to get admCd, rnMgtSn, udrtYn, buldMnnm, buldSlno" >&2
  exit 64
fi

: "${JUSO_CONFM_KEY_COORD:?JUSO_CONFM_KEY_COORD is not set — grade-B key required for coord lookup}"

resp=$(curl -sS --get \
  --data-urlencode "confmKey=${JUSO_CONFM_KEY_COORD}" \
  --data-urlencode "admCd=${admcode}" \
  --data-urlencode "rnMgtSn=${rnmgmcd}" \
  --data-urlencode "udrtYn=${udrtyn}" \
  --data-urlencode "buldMnnm=${buldmnnm}" \
  --data-urlencode "buldSlno=${buldslno}" \
  --data-urlencode "srchwrd=${srchwrd}" \
  --data-urlencode "resultType=json" \
  "https://business.juso.go.kr/addrlink/addrCoordApi.do")

code=$(printf '%s' "$resp" | jq -r '.results.common.errorCode // empty')
if [[ -n "$code" && "$code" != "0" ]]; then
  msg=$(printf '%s' "$resp" | jq -r '.results.common.errorMessage // "unknown"')
  echo "juso API error ${code}: ${msg}" >&2
  exit 1
fi

printf '%s' "$resp" | jq -c '.results.juso[0] // empty'
