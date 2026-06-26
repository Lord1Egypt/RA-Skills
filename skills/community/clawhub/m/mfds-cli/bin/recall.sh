#!/usr/bin/env bash
# `mfds-cli recall` — drug recall / sales-stop / disposal orders
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
. "$DIR/_mfds_common.sh"

mfds_parse_args "$@"

if [[ "${HELP:-0}" == 1 ]]; then
  cat <<'EOF'
Usage: mfds-cli recall [flags]

Drug recall, sales-stop, and disposal orders (MdcinExecRslt2Service).

Flags:
  --year YYYY            시정조치년도
  --name "<text>"        품목명
  --maker "<text>"       제조/수입업체명
  --action <code>        시정조치코드 (회수, 판매중지, 폐기, …)
  --rows N / --page N
  --format jsonl|json|xml
  --raw / --endpoint <url>
EOF
  exit 0
fi

mfds_require_key

URL="${ENDPOINT:-https://apis.data.go.kr/1471000/MdcinExecRslt2Service/getMdcinExecRsltList}"

QS="$(mfds_qs \
  "serviceKey=$KEY" \
  "pageNo=$PAGE" \
  "numOfRows=$ROWS" \
  "type=json" \
  "DSPSL_YEAR=${YEAR}" \
  "ITEM_NAME=${NAME}" \
  "ENTRPS_NM=${MAKER}" \
  "DSPSL_TYPE=${ACTION}" \
)"

mfds_request "$URL" "$QS" "recall"
