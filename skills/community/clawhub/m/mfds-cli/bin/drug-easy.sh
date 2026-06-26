#!/usr/bin/env bash
# `mfds-cli drug-easy` — consumer-friendly drug leaflet (e약은요)
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
. "$DIR/_mfds_common.sh"

mfds_parse_args "$@"

if [[ "${HELP:-0}" == 1 ]]; then
  cat <<'EOF'
Usage: mfds-cli drug-easy [flags]

Consumer drug leaflet (e약은요) — efficacy, dosage, warnings, side effects.

Flags:
  --name "<text>"            itemName 품목명
  --maker "<text>"           entpName 업체명
  --item-seq <13-digit>      itemSeq
  --query-efficacy "<text>"  search inside 효능 본문
  --query-method "<text>"    search inside 용법 본문
  --query-warning "<text>"   search inside 주의사항 본문
  --query-side-effect "<text>" search inside 부작용 본문
  --query-storage "<text>"   search inside 보관법 본문
  --rows N / --page N
  --format jsonl|json|xml
  --raw / --endpoint <url>
EOF
  exit 0
fi

mfds_require_key

URL="${ENDPOINT:-https://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList}"

QS="$(mfds_qs \
  "serviceKey=$KEY" \
  "pageNo=$PAGE" \
  "numOfRows=$ROWS" \
  "type=json" \
  "itemName=${NAME}" \
  "entpName=${MAKER}" \
  "itemSeq=${ITEM_SEQ}" \
  "efcyQesitm=${QUERY_EFFICACY}" \
  "useMethodQesitm=${QUERY_METHOD}" \
  "atpnQesitm=${QUERY_WARNING}" \
  "seQesitm=${QUERY_SIDE_EFFECT}" \
  "depositMethodQesitm=${QUERY_STORAGE}" \
)"

mfds_request "$URL" "$QS" "drug-easy"
