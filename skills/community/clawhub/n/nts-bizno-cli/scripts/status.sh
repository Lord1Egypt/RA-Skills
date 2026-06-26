#!/usr/bin/env bash
# status.sh — 사업자등록 상태조회 (operating status lookup).
#
# Usage:
#   scripts/status.sh <bno> [<bno> ...]
#
# At least one b_no is required. Up to 100 per request (NTS limit).
# Each b_no may be in any of these forms: 1234567890, 123-45-67890.
#
# Output: JSONL — one object per b_no, decoded into:
#   { b_no, b_no_formatted, b_stt_cd, b_stt, tax_type_cd, tax_type,
#     end_dt, utcc_yn, tax_type_change_dt, invoice_apply_dt,
#     rbf_tax_type_cd, rbf_tax_type, raw }
#
# Conventions (from NTS):
#   b_stt_cd: "01"=계속사업자, "02"=휴업자, "03"=폐업자, ""=등록되지 않은 번호
#   b_stt:    matching Korean label that the API returns directly.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$here/_common.sh"

if [[ $# -lt 1 ]]; then
  cat >&2 <<EOF
Usage: $0 <bno> [<bno> ...]

Examples:
  $0 1234567890
  $0 123-45-67890 234-56-78901
  cat bnos.txt | xargs $0
EOF
  exit 64
fi

require_bin curl jq
require_key

declare -a bnos=()
for arg in "$@"; do bnos+=("$(strip_bno "$arg")"); done

if [[ "${#bnos[@]}" -gt 100 ]]; then
  echo "error: at most 100 b_no values per request (got ${#bnos[@]}). Split into batches." >&2
  exit 64
fi

body=$(jq -nc --argjson v "$(printf '%s\n' "${bnos[@]}" | jq -Rsc 'split("\n") | map(select(length>0))')" '{b_no:$v}')

resp=$(nts_post status "$body")

echo "$resp" | jq -c '.data[]? | {
  b_no,
  b_no_formatted: ((.b_no // "") | if length == 10 then "\(.[0:3])-\(.[3:5])-\(.[5:10])" else . end),
  b_stt_cd,
  b_stt,
  tax_type_cd,
  tax_type,
  end_dt,
  utcc_yn,
  tax_type_change_dt,
  invoice_apply_dt,
  rbf_tax_type_cd,
  rbf_tax_type,
  raw: .
}'
