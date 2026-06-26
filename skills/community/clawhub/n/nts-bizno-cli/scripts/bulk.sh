#!/usr/bin/env bash
# bulk.sh — read a list of business numbers from a file, status-check in batches.
#
# Usage:
#   scripts/bulk.sh <file>            # one b_no per line (XXX-XX-XXXXX or 10 digits)
#   scripts/bulk.sh -                 # read from stdin
#
# - Skips blank lines and lines starting with #.
# - Validates each b_no's checksum locally first; bad checksums are flagged
#   via JSONL with {b_no, error:"checksum_failed"} and never sent to NTS.
# - Sends API requests in batches of 100 (NTS hard limit).
# - Output: JSONL identical in shape to status.sh, with bad-checksum rows mixed in.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$here/_common.sh"

require_bin curl jq

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <file|->" >&2; exit 64
fi

src="$1"
if [[ "$src" == "-" ]]; then
  raw=$(cat)
else
  if [[ ! -f "$src" ]]; then echo "error: file not found: $src" >&2; exit 64; fi
  raw=$(cat "$src")
fi

declare -a good=()
while IFS= read -r line; do
  line="${line%%#*}"                         # strip trailing comment
  line="$(printf '%s' "$line" | tr -d '\r' | xargs || true)"
  [[ -z "$line" ]] && continue
  bno=$(strip_bno "$line")
  if checksum_bno "$bno"; then
    good+=("$bno")
  else
    jq -nc --arg b "$bno" --arg in "$line" '{b_no:$b, b_no_input:$in, error:"checksum_failed"}'
  fi
done <<< "$raw"

# Emit zero-result early.
if [[ "${#good[@]}" -eq 0 ]]; then exit 0; fi
require_key

# Batch in groups of 100.
n=${#good[@]}
i=0
while [[ $i -lt $n ]]; do
  end=$(( i + 100 ))
  [[ $end -gt $n ]] && end=$n
  batch=("${good[@]:i:end-i}")
  body=$(jq -nc --argjson v "$(printf '%s\n' "${batch[@]}" | jq -Rsc 'split("\n") | map(select(length>0))')" '{b_no:$v}')
  resp=$(nts_post status "$body")
  echo "$resp" | jq -c '.data[]? | {
    b_no,
    b_no_formatted: ((.b_no // "") | if length == 10 then "\(.[0:3])-\(.[3:5])-\(.[5:10])" else . end),
    b_stt_cd, b_stt, tax_type_cd, tax_type, end_dt, utcc_yn,
    tax_type_change_dt, invoice_apply_dt, rbf_tax_type_cd, rbf_tax_type
  }'
  i=$end
done
