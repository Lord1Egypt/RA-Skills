#!/usr/bin/env bash
# MaybeAI Sheet — Formulas
# Usage: export MAYBEAI_API_TOKEN=your_token_here
#        export DOC_ID=your_document_id_here
#        export SQL_FORMULA_WORKSHEET=Report
#        export SQL_FORMULA_CELL=A1
#        export SQL_FORMULA_QUERY='select "Region", sum("Revenue") as "Revenue" from "Orders" group by "Region" order by "Revenue" desc'
#        bash 06-formulas.sh

BASE_URL="https://play-be.omnimcp.ai"
TOKEN="${MAYBEAI_API_TOKEN:?Please set MAYBEAI_API_TOKEN}"
DOC_ID="${DOC_ID:?Please set DOC_ID}"
DOC_URI="https://www.maybe.ai/docs/spreadsheets/d/$DOC_ID"
DOC_URI_GID0="${DOC_URI}?gid=0"
SQL_FORMULA_WORKSHEET="${SQL_FORMULA_WORKSHEET:-}"
SQL_FORMULA_CELL="${SQL_FORMULA_CELL:-A1}"
SQL_FORMULA_QUERY="${SQL_FORMULA_QUERY:-}"

# ── Set Formula in Cell ───────────────────────────────────────────────────────
echo "=== Set Formula in Cell ==="
curl -s -X POST "$BASE_URL/api/v1/excel/formula/set" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI\",
    \"worksheet_name\": \"Sheet1\",
    \"cell\": \"E2\",
    \"formula\": \"=SUM(B2:D2)\",
    \"skip_recalculation\": false
  }" \
  | jq .

# ── Batch Set Formula Block ───────────────────────────────────────────────────
echo "=== Batch Set Formula Block ==="
curl -s -X POST "$BASE_URL/api/v1/excel/formula/batch_set" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI\",
    \"skip_recalculation\": true,
    \"recalculate_mode\": \"worksheet\",
    \"operations\": [
      {
        \"worksheet_name\": \"Sheet1\",
        \"range_address\": \"E2:G2\",
        \"formulas\": [[
          \"=SUM(B2:D2)\",
          \"=AVERAGE(B2:D2)\",
          \"=MAX(B2:D2)\"
        ]]
      }
    ]
  }" \
  | jq .

# ── Calculate Single Formula ──────────────────────────────────────────────────
echo "=== Calc Single Formula ==="
curl -s -X POST "$BASE_URL/api/v1/excel/calc-formula" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI_GID0\",
    \"cellAddress\": \"B11\",
    \"formula\": \"=SUM(B2:B10)\"
  }" \
  | jq .

# ── Calculate Multiple Formulas ───────────────────────────────────────────────
echo "=== Calc Multiple Formulas ==="
curl -s -X POST "$BASE_URL/api/v1/excel/calc_formulas" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI_GID0\",
    \"formulas\": [
      {\"cell\": \"B11\", \"formula\": \"=SUM(B2:B10)\"},
      {\"cell\": \"C11\", \"formula\": \"=AVERAGE(C2:C10)\"},
      {\"cell\": \"D11\", \"formula\": \"=MAX(D2:D10)\"}
    ]
  }" \
  | jq .

# ── Recalculate All Formulas in Document ──────────────────────────────────────
echo "=== Recalculate All Formulas ==="
curl -s -X POST "$BASE_URL/api/v1/excel/recalculate_formulas" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_URI\"}" \
  | jq .

# ── Optional: Live SQL Formula Showcase ───────────────────────────────────────
if [ -n "$SQL_FORMULA_WORKSHEET" ] && [ -n "$SQL_FORMULA_QUERY" ]; then
  echo "=== Compile SQL For Live SQL Formula ==="
  SQL_COMPILE_PAYLOAD=$(
    jq -n \
      --arg uri "$DOC_URI_GID0" \
      --arg sql "$SQL_FORMULA_QUERY" \
      '{uri: $uri, sql: $sql}'
  )
  curl -s -X POST "$BASE_URL/api/v1/excel/sql/compile" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "$SQL_COMPILE_PAYLOAD" \
    | jq .

  SQL_FORMULA_TEXT=$(
    jq -rn \
      --arg sql "$SQL_FORMULA_QUERY" \
      '$sql | gsub("\""; "\"\"") | "=SQL(\"" + . + "\")"'
  )

  echo "=== Write Live SQL Formula ==="
  SQL_FORMULA_SET_PAYLOAD=$(
    jq -n \
      --arg uri "$DOC_URI" \
      --arg worksheet_name "$SQL_FORMULA_WORKSHEET" \
      --arg cell "$SQL_FORMULA_CELL" \
      --arg formula "$SQL_FORMULA_TEXT" \
      '{
        uri: $uri,
        worksheet_name: $worksheet_name,
        cell: $cell,
        formula: $formula,
        skip_recalculation: false
      }'
  )
  curl -s -X POST "$BASE_URL/api/v1/excel/formula/set" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "$SQL_FORMULA_SET_PAYLOAD" \
    | jq .
fi
