#!/usr/bin/env bash
# MaybeAI Sheet — Writing & Editing Data
# Usage: export MAYBEAI_API_TOKEN=your_token_here
#        export DOC_ID=your_document_id_here
#        bash 03-write-data.sh

BASE_URL="https://play-be.omnimcp.ai"
TOKEN="${MAYBEAI_API_TOKEN:?Please set MAYBEAI_API_TOKEN}"
DOC_ID="${DOC_ID:?Please set DOC_ID}"
DOC_URI="https://www.maybe.ai/docs/spreadsheets/d/$DOC_ID"
DOC_URI_GID0="${DOC_URI}?gid=0"

# ── Update Range ──────────────────────────────────────────────────────────────
echo "=== Update Range ==="
curl -s -X POST "$BASE_URL/api/v1/excel/update_range" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI\",
    \"worksheet_name\": \"Sheet1\",
    \"range_address\": \"A1:C3\",
    \"values\": [
      [\"Name\", \"Score\", \"Grade\"],
      [\"Alice\",  95,      \"A\"],
      [\"Bob\",    82,      \"B\"]
    ]
  }" \
  | jq .

# ── Update Range by Lookup ────────────────────────────────────────────────────
# Updates or appends rows by key on the worksheet selected from uri
echo "=== Update Range by Lookup ==="
curl -s -X POST "$BASE_URL/api/v1/excel/update_range_by_lookup" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI_GID0\",
    \"data\": [
      {\"Name\": \"Alice\", \"Score\": 98, \"Grade\": \"A+\"}
    ],
    \"on\": [\"Name\"],
    \"override\": false,
    \"skip_recalculation\": false
  }" \
  | jq .

# ── Clear Range ───────────────────────────────────────────────────────────────
echo "=== Clear Range ==="
curl -s -X POST "$BASE_URL/api/v1/excel/clear_range" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_URI\", \"worksheet_name\": \"Sheet1\", \"range_address\": \"D1:F10\"}" \
  | jq .

# ── Append Rows ───────────────────────────────────────────────────────────────
echo "=== Append Rows ==="
curl -s -X POST "$BASE_URL/api/v1/excel/append_rows" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI_GID0\",
    \"data\": [
      {\"Name\": \"Charlie\", \"Score\": 77, \"Grade\": \"C\"},
      {\"Name\": \"Diana\", \"Score\": 91, \"Grade\": \"A-\"}
    ]
  }" \
  | jq .

# ── Write New Worksheet (full data at once) ──────────────────────────────────
echo "=== Write New Worksheet ==="
curl -s -X POST "$BASE_URL/api/v1/excel/write_new_worksheet" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI\",
    \"worksheet_name\": \"Summary\",
    \"values\": [
      [\"Category\", \"Total\"],
      [\"Sales\", \"12000\"],
      [\"Returns\", \"300\"]
    ]
  }" \
  | jq .

# ── Copy Range with Formulas ──────────────────────────────────────────────────
echo "=== Copy Range with Formulas ==="
curl -s -X POST "$BASE_URL/api/v1/excel/copy_range_with_formulas" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI\",
    \"worksheet_name\": \"Sheet1\",
    \"from_range\": \"A1:D10\",
    \"to_range\": \"F1\",
    \"auto_fill\": false
  }" \
  | jq .

# ── Copy Range by Lookup ──────────────────────────────────────────────────────
echo "=== Copy Range by Lookup ==="
curl -s -X POST "$BASE_URL/api/v1/excel/copy_range_by_lookup" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI_GID0\",
    \"from_range\": \"A2:C2\",
    \"lookup_column\": \"Name\",
    \"on\": [\"Name\"],
    \"skip_if_exists\": true
  }" \
  | jq .
