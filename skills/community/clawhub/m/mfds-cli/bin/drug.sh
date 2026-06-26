#!/usr/bin/env bash
# `mfds-cli drug` — drug master search (의약품 허가정보)
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
. "$DIR/_mfds_common.sh"

mfds_parse_args "$@"

if [[ "${HELP:-0}" == 1 ]]; then
  cat <<'EOF'
Usage: mfds-cli drug [flags]

Searches the MFDS Drug Product Permission Master (DrugPrdtPrmsnInfoService06).

Flags:
  --name "<text>"        품목명 (Korean or English)
  --maker "<text>"       업체명
  --item-seq <13-digit>  품목기준코드
  --bizrno <10-digit>    업체 사업자등록번호
  --type-code <code>     prduct_type — 전문/일반/원료의약품 등
  --cancel-name <text>   include cancelled drugs (substring of 취소사유)
  --rows N               page size (default 30, max 100)
  --page N               page number (default 1)
  --format jsonl|json|xml
  --raw                  pass through API response without normalization
  --endpoint <url>       override the default endpoint
EOF
  exit 0
fi

mfds_require_key

URL="${ENDPOINT:-https://apis.data.go.kr/1471000/DrugPrdtPrmsnInfoService06/getDrugPrdtPrmsnDtlInq05}"

QS="$(mfds_qs \
  "serviceKey=$KEY" \
  "pageNo=$PAGE" \
  "numOfRows=$ROWS" \
  "type=json" \
  "item_name=${NAME}" \
  "entp_name=${MAKER}" \
  "item_seq=${ITEM_SEQ}" \
  "bizrno=${BIZRNO}" \
  "prduct_type=${TYPE_CODE}" \
  "cancel_name=${CANCEL_NAME}" \
)"

mfds_request "$URL" "$QS" "drug"
