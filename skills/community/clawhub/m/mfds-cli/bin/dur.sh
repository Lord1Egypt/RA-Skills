#!/usr/bin/env bash
# `mfds-cli dur` — DUR contraindication / warning lookup
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
. "$DIR/_mfds_common.sh"

mfds_parse_args "$@"

if [[ "${HELP:-0}" == 1 ]]; then
  cat <<'EOF'
Usage: mfds-cli dur --type <type> [flags]

Drug Utilization Review (DUR) lookups from MFDS DURPrdlstInfoService03.

--type values:
  interaction         병용금기            (drug A + drug B)
  age                 특정연령대금기      (forbidden under N years)
  pregnancy           임부금기
  capacity            용량주의            (daily-dose cap)
  period              투여기간주의        (max consecutive days)
  elderly             노인주의            (65+)
  efficacy-duplicate  효능군중복          (same therapeutic class)
  extended-release    서방정분할주의

Flags:
  --name "<text>"       itemName 품목명
  --ingredient "<text>" ingrName 주성분명
  --type-name "<text>"  typeName DUR 유형명
  --rows N / --page N
  --format jsonl|json|xml
  --raw / --endpoint <url>
EOF
  exit 0
fi

mfds_require_key

case "$DUR_TYPE" in
  interaction)        SUB="getUsjntTabooInfoList03" ;;
  age)                SUB="getSpcifyAgrdeTabooInfoList03" ;;
  pregnancy)          SUB="getPwnmTabooInfoList03" ;;
  capacity)           SUB="getCpctyAtentInfoList03" ;;
  period)             SUB="getMdctnPdAtentInfoList03" ;;
  elderly)            SUB="getOdsnAtentInfoList03" ;;
  efficacy-duplicate) SUB="getEfcyDplctInfoList03" ;;
  extended-release)   SUB="getSeobangjeongPartitnAtentInfoList03" ;;
  *)
    echo "mfds-cli: unknown --type '$DUR_TYPE' (run 'mfds-cli dur --help')" >&2
    exit 64
    ;;
esac

URL="${ENDPOINT:-https://apis.data.go.kr/1471000/DURPrdlstInfoService03/$SUB}"

QS="$(mfds_qs \
  "serviceKey=$KEY" \
  "pageNo=$PAGE" \
  "numOfRows=$ROWS" \
  "type=json" \
  "itemName=${NAME}" \
  "ingrName=${INGREDIENT}" \
  "typeName=${TYPE_NAME}" \
)"

mfds_request "$URL" "$QS" "dur"
