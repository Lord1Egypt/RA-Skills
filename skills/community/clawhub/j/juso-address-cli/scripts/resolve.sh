#!/usr/bin/env bash
# juso-address-cli / resolve.sh
# Convenience: raw address string → top match → entrance coordinates.
# Emits one JSON object combining search fields + entX/entY.
#
# Usage:
#   resolve.sh <raw-address>
#
# Env:
#   JUSO_CONFM_KEY        (required)   grade-A or grade-B, for search
#   JUSO_CONFM_KEY_COORD  (required)   grade-B, for coord

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: resolve.sh <raw-address>" >&2
  exit 64
fi

raw="$1"
here="$(cd "$(dirname "$0")" && pwd)"

: "${JUSO_CONFM_KEY:?JUSO_CONFM_KEY is not set}"

match=$("${here}/search.sh" "$raw" --per-page 1 | head -n 1)
if [[ -z "$match" ]]; then
  echo "no match for: $raw" >&2
  exit 2
fi

if [[ -z "${JUSO_CONFM_KEY_COORD:-}" ]]; then
  # No coord key — emit search match alone so the caller still gets structured data.
  printf '%s\n' "$match"
  exit 0
fi

admcode=$(printf '%s' "$match" | jq -r '.admCd')
rnmgmcd=$(printf '%s' "$match" | jq -r '.rnMgtSn')
udrtyn=$(printf '%s' "$match" | jq -r '.udrtYn')
buldmnnm=$(printf '%s' "$match" | jq -r '.buldMnnm')
buldslno=$(printf '%s' "$match" | jq -r '.buldSlno')

coord=$("${here}/coord.sh" \
  --admcode "$admcode" \
  --rnmgmcd "$rnmgmcd" \
  --udrtyn "$udrtyn" \
  --buldmnnm "$buldmnnm" \
  --buldslno "$buldslno" \
  --srchwrd "$raw" || true)

if [[ -z "$coord" ]]; then
  printf '%s\n' "$match"
  exit 0
fi

jq -c -n --argjson a "$match" --argjson b "$coord" '$a + {entX:$b.entX, entY:$b.entY, bdNm:($b.bdNm // $a.bdNm)}'
