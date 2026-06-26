#!/usr/bin/env bash
# MaybeAI Sheet — Formatting (Freeze, Cell Styles, Filters, Conditional Formats)
# Usage: export MAYBEAI_API_TOKEN=your_token_here
#        export DOC_ID=your_document_id_here
#        bash 08-formatting.sh

BASE_URL="https://play-be.omnimcp.ai"
TOKEN="${MAYBEAI_API_TOKEN:?Please set MAYBEAI_API_TOKEN}"
DOC_ID="${DOC_ID:?Please set DOC_ID}"
DOC_URI="https://www.maybe.ai/docs/spreadsheets/d/$DOC_ID"

# ── Freeze Panes ──────────────────────────────────────────────────────────────
# freeze_rows=1 locks the header row; freeze_columns=0 means no column freeze
echo "=== Freeze Header Row ==="
curl -s -X POST "$BASE_URL/api/v1/excel/freeze_panes" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI\",
    \"worksheet_name\": \"Sheet1\",
    \"freeze_rows\": 1,
    \"freeze_columns\": 0
  }" \
  | jq .

# Freeze both first row and first column
echo "=== Freeze Row + Column ==="
curl -s -X POST "$BASE_URL/api/v1/excel/freeze_panes" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI\",
    \"worksheet_name\": \"Sheet1\",
    \"freeze_rows\": 1,
    \"freeze_columns\": 1
  }" \
  | jq .

# ── Batch Set Cell Style ──────────────────────────────────────────────────────
# Single-range style requests still use range_addresses with one item.
echo "=== Batch Set Cell Style (single range as one-item array) ==="
curl -s -X POST "$BASE_URL/api/v1/excel/batch_set_cell_style" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI\",
    \"worksheet_name\": \"Sheet1\",
    \"range_addresses\": [\"B2:B100\"],
    \"style\": {
      \"format\": \"date\"
    }
  }" \
  | jq .

# Common LLM-friendly pattern: same style for data columns plus header row.
echo "=== Batch Set Cell Style (multiple ranges) ==="
curl -s -X POST "$BASE_URL/api/v1/excel/batch_set_cell_style" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI\",
    \"worksheet_name\": \"Sheet1\",
    \"range_addresses\": [\"B2:B100\", \"E2:E100\", \"A1:F1\"],
    \"style\": {
      \"bold\": true,
      \"horizontal\": \"center\",
      \"wrap_text\": true,
      \"bg_color\": \"#D9EAD3\"
    }
  }" \
  | jq .

# Friendly finance/report table styling.
# Keep write_new_worksheet data-only, then run a small explicit style pass.
# Example layout: 科目 | 期末余额 | 期初余额 | 变动额 | 变动率 | 占比 | 备注
# If any response contains source_info.styles_ignored=true, the worksheet engine
# did not apply styles (commonly PG-backed sheets with style_engine=none).
echo "=== Friendly Report Table Style (header, section, totals, numeric columns) ==="
curl -s -X POST "$BASE_URL/api/v1/excel/batch_set_cell_style" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI\",
    \"worksheet_name\": \"Sheet1\",
    \"range_addresses\": [\"A1:G1\"],
    \"style\": {
      \"bold\": true,
      \"font_color\": \"#FFFFFF\",
      \"bg_color\": \"#173E56\",
      \"horizontal\": \"center\",
      \"vertical\": \"middle\",
      \"wrap_text\": true
    }
  }" \
  | jq .

curl -s -X POST "$BASE_URL/api/v1/excel/batch_set_cell_style" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI\",
    \"worksheet_name\": \"Sheet1\",
    \"range_addresses\": [\"A2:G2\"],
    \"style\": {
      \"bold\": true,
      \"font_color\": \"#FFFFFF\",
      \"bg_color\": \"#2E91C8\"
    }
  }" \
  | jq .

curl -s -X POST "$BASE_URL/api/v1/excel/batch_set_cell_style" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI\",
    \"worksheet_name\": \"Sheet1\",
    \"range_addresses\": [\"A9:G9\"],
    \"style\": {
      \"bold\": true,
      \"bg_color\": \"#E8ECEF\"
    }
  }" \
  | jq .

curl -s -X POST "$BASE_URL/api/v1/excel/batch_set_cell_style" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI\",
    \"worksheet_name\": \"Sheet1\",
    \"range_addresses\": [\"B2:D100\"],
    \"style\": {
      \"format\": \"decimal\",
      \"format_code\": \"#,##0\",
      \"horizontal\": \"right\"
    }
  }" \
  | jq .

curl -s -X POST "$BASE_URL/api/v1/excel/batch_set_cell_style" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI\",
    \"worksheet_name\": \"Sheet1\",
    \"range_addresses\": [\"E2:F100\"],
    \"style\": {
      \"format\": \"percent\",
      \"format_code\": \"0.0%\",
      \"horizontal\": \"right\"
    }
  }" \
  | jq .

# ── Set Auto Filter ───────────────────────────────────────────────────────────
echo "=== Set Auto Filter ==="
curl -s -X POST "$BASE_URL/api/v1/excel/set_auto_filter" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI\",
    \"worksheet_name\": \"Sheet1\",
    \"auto_filter\": {
      \"ref\": \"A1:F100\",
      \"filter_columns\": []
    }
  }" \
  | jq .

# ── Remove Auto Filter ────────────────────────────────────────────────────────
echo "=== Remove Auto Filter ==="
curl -s -X POST "$BASE_URL/api/v1/excel/remove_auto_filter" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_URI\", \"worksheet_name\": \"Sheet1\"}" \
  | jq .

# ── Set Conditional Formats ───────────────────────────────────────────────────
# Highlights cells in B2:B100 red when value > 90
echo "=== Set Conditional Formats (highlight high scores) ==="
curl -s -X POST "$BASE_URL/api/v1/excel/set_conditional_formats" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI\",
    \"worksheet_name\": \"Sheet1\",
    \"formats\": [
      {
        \"sqref\": \"B2:B100\",
        \"type\": \"cell\",
        \"criteria\": \">\",
        \"value\": \"90\",
        \"format\": {
          \"font\": {\"color\": \"FF0000\", \"bold\": true},
          \"fill\": {\"type\": \"pattern\", \"color\": \"FFEB9C\"}
        }
      }
    ]
  }" \
  | jq .

# Highlight cells below threshold in red (e.g. flag low scores)
echo "=== Set Conditional Formats (flag low scores) ==="
curl -s -X POST "$BASE_URL/api/v1/excel/set_conditional_formats" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI\",
    \"worksheet_name\": \"Sheet1\",
    \"formats\": [
      {
        \"sqref\": \"B2:B100\",
        \"type\": \"cell\",
        \"criteria\": \"<\",
        \"value\": \"60\",
        \"format\": {
          \"font\": {\"color\": \"FFFFFF\"},
          \"fill\": {\"type\": \"pattern\", \"color\": \"FF0000\"}
        }
      }
    ]
  }" \
  | jq .
