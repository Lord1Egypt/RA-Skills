#!/usr/bin/env bash
# validate.sh — 사업자등록 진위확인 (authenticity verification).
#
# Verifies that a given (b_no, opening date, representative name) tuple
# matches what NTS holds. This is the official onboarding/KYB check.
#
# Usage A — single record via flags:
#   scripts/validate.sh \
#     --b-no 1234567890 \
#     --start-dt 20100315 \
#     --p-nm "홍길동" \
#     [--corp-no 1101111111111] \
#     [--b-nm "회사명"] \
#     [--b-sector "업종"] \
#     [--b-type "업태"] \
#     [--p-nm2 "외국인 영문명"]
#
# Usage B — JSON file with batch of up to 100 records:
#   scripts/validate.sh --file payload.json
#   # payload.json must be {"businesses":[{...},{...}]} matching NTS schema.
#
# Output: JSONL — one row per record echoing the request and the verdict:
#   { b_no, valid, status_code, request_param, raw }
#
# valid is true iff status_code == "01" (확인) — i.e. NTS confirms a match.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$here/_common.sh"

require_bin curl jq
require_key

usage() {
  cat >&2 <<EOF
Usage:
  $0 --b-no <10-digit> --start-dt <YYYYMMDD> --p-nm <대표자명> [more flags]
  $0 --file <payload.json>

Optional flags (single-record mode):
  --corp-no <13-digit>      법인등록번호
  --b-nm <상호>             상호명
  --b-sector <업종>         주업종
  --b-type <업태>           주업태
  --p-nm2 <영문명>          외국인 대표 영문명
EOF
}

mode=""
file=""
declare -A f=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --file)      mode="file"; file="$2"; shift 2 ;;
    --b-no)      f[b_no]="$(strip_bno "$2")"; shift 2 ;;
    --start-dt)  f[start_dt]="$2"; shift 2 ;;
    --p-nm)      f[p_nm]="$2"; shift 2 ;;
    --p-nm2)    f[p_nm2]="$2"; shift 2 ;;
    --corp-no)   f[corp_no]="$2"; shift 2 ;;
    --b-nm)      f[b_nm]="$2"; shift 2 ;;
    --b-sector)  f[b_sector]="$2"; shift 2 ;;
    --b-type)    f[b_type]="$2"; shift 2 ;;
    -h|--help)   usage; exit 0 ;;
    *) echo "error: unknown flag: $1" >&2; usage; exit 64 ;;
  esac
done

build_record() {
  jq -nc \
    --arg b_no "${f[b_no]:-}" \
    --arg start_dt "${f[start_dt]:-}" \
    --arg p_nm "${f[p_nm]:-}" \
    --arg p_nm2 "${f[p_nm2]:-}" \
    --arg corp_no "${f[corp_no]:-}" \
    --arg b_nm "${f[b_nm]:-}" \
    --arg b_sector "${f[b_sector]:-}" \
    --arg b_type "${f[b_type]:-}" \
    '{b_no:$b_no, start_dt:$start_dt, p_nm:$p_nm, p_nm2:$p_nm2,
      corp_no:$corp_no, b_nm:$b_nm, b_sector:$b_sector, b_type:$b_type}'
}

if [[ "$mode" == "file" ]]; then
  if [[ ! -f "$file" ]]; then
    echo "error: payload file not found: $file" >&2; exit 64
  fi
  body=$(jq -c '.' "$file")
else
  if [[ -z "${f[b_no]:-}" || -z "${f[start_dt]:-}" || -z "${f[p_nm]:-}" ]]; then
    echo "error: --b-no, --start-dt, and --p-nm are required (or use --file)." >&2
    usage; exit 64
  fi
  if [[ ! "${f[start_dt]}" =~ ^[0-9]{8}$ ]]; then
    echo "error: --start-dt must be YYYYMMDD (8 digits)." >&2; exit 64
  fi
  rec=$(build_record)
  body=$(jq -nc --argjson r "$rec" '{businesses:[$r]}')
fi

resp=$(nts_post validate "$body")

# Each record in .data carries: {b_no, valid:"01"|"02", valid_msg, request_param, status:{...}}
# valid="01" means 확인 (matches), "02" means 불일치/미등록.
echo "$resp" | jq -c '.data[]? | {
  b_no: (.request_param.b_no // .b_no),
  b_no_formatted: ((.request_param.b_no // .b_no // "") | if length == 10 then "\(.[0:3])-\(.[3:5])-\(.[5:10])" else . end),
  valid: (.valid == "01"),
  valid_code: .valid,
  valid_msg: (.valid_msg // ""),
  status: .status,
  request_param: .request_param,
  raw: .
}'
