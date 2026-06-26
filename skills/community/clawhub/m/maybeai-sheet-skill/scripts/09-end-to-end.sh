#!/usr/bin/env bash
# MaybeAI Sheet — End-to-End Workflow Examples
#
# This script demonstrates three complete workflows:
#   1. Upload → read → update → export
#   2. Build a report from scratch
#   3. Append new data and recalculate
#
# Usage:
#   export MAYBEAI_API_TOKEN=your_token_here
#   export EXCEL_FILE_PATH=/absolute/path/to/file.xlsx
#   export UPLOAD_USER_ID=demo-user   # optional compatibility field
#   bash 09-end-to-end.sh

BASE_URL="https://play-be.omnimcp.ai"
TOKEN="${MAYBEAI_API_TOKEN:?Please set MAYBEAI_API_TOKEN}"
EXCEL_FILE_PATH="${EXCEL_FILE_PATH:-./sample.xlsx}"
UPLOAD_USER_ID="${UPLOAD_USER_ID:-}"
PAYLOAD_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "$PAYLOAD_DIR"
}
trap cleanup EXIT

echo "============================================================"
echo " Workflow 1: Upload → Read → Update → Export"
echo "============================================================"

# Step 1: Upload
echo "[1/4] Uploading ${EXCEL_FILE_PATH} ..."
UPLOAD_CURL_ARGS=(
  -s
  -X POST "$BASE_URL/api/v1/excel/upload"
  -H "Authorization: Bearer $TOKEN"
  -F "file=@${EXCEL_FILE_PATH}"
)
if [ -n "$UPLOAD_USER_ID" ]; then
  UPLOAD_CURL_ARGS+=(-F "user_id=${UPLOAD_USER_ID}")
fi
UPLOAD_RESP=$(curl "${UPLOAD_CURL_ARGS[@]}")
echo "$UPLOAD_RESP" | jq .
DOC_ID=$(echo "$UPLOAD_RESP" | jq -r '.document_id // ((.uri // "") | split("/d/") | last | split("?") | first)')
DOC_URI=$(echo "$UPLOAD_RESP" | jq -r '.uri // empty')
if [ -z "$DOC_URI" ] || [ "$DOC_URI" = "null" ]; then
  DOC_URI="https://www.maybe.ai/docs/spreadsheets/d/$DOC_ID"
fi
DOC_URI_GID0="${DOC_URI}?gid=0"
echo "Document ID: $DOC_ID"
echo "Document URI: $DOC_URI"

# Step 2: List worksheets
echo "[2/4] Listing worksheets ..."
curl -s -X POST "$BASE_URL/api/v1/excel/list_worksheets" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_URI\"}" \
  | jq .

# Step 3: Read Sheet1
echo "[3/4] Reading Sheet1 ..."
curl -s -X POST "$BASE_URL/api/v1/excel/read_sheet" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_URI\", \"worksheet_name\": \"Sheet1\"}" \
  | jq .

# Step 4: Update a range and export
echo "[4/4] Updating A1:B2 and exporting ..."
curl -s -X POST "$BASE_URL/api/v1/excel/update_range" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI\",
    \"worksheet_name\": \"Sheet1\",
    \"range_address\": \"A1:B2\",
    \"values\": [[\"Product\",\"Q1\"],[\"Widget\",5000]]
  }" | jq .

curl -s -o "./workflow1_output.xlsx" \
  "$BASE_URL/api/v1/excel/export/$DOC_ID"
echo "Exported to ./workflow1_output.xlsx"

echo ""
echo "============================================================"
echo " Workflow 2: Build a Report from Scratch"
echo "============================================================"

# Upload blank template (or use existing DOC_ID from step above)
echo "[1/5] Using document from Workflow 1 (DOC_ID=$DOC_ID)"

# Write summary sheet
echo "[2/5] Writing Summary worksheet ..."
curl -s -X POST "$BASE_URL/api/v1/excel/write_new_worksheet" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI\",
    \"worksheet_name\": \"Summary\",
    \"values\": [
      [\"Month\",\"Revenue\",\"Cost\",\"Profit\"],
      [\"Jan\", 50000, 30000, \"=C2-D2\"],
      [\"Feb\", 62000, 35000, \"=C3-D3\"],
      [\"Mar\", 71000, 38000, \"=C4-D4\"]
    ]
  }" | jq .

# Freeze header row
echo "[3/5] Freezing header row ..."
curl -s -X POST "$BASE_URL/api/v1/excel/freeze_panes" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_URI\", \"worksheet_name\": \"Summary\", \"freeze_rows\": 1, \"freeze_columns\": 0}" \
  | jq .

# Add auto filter
echo "[4/5] Adding auto filter ..."
curl -s -X POST "$BASE_URL/api/v1/excel/set_auto_filter" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_URI\", \"worksheet_name\": \"Summary\", \"auto_filter\": {\"ref\": \"A1:D4\"}}" \
  | jq .

# Add a JSON ECharts revenue chart
echo "[5/5] Adding revenue chart ..."
SUMMARY_CHART_PAYLOAD="$PAYLOAD_DIR/summary-chart.json"
jq -n \
  --arg uri "$DOC_URI" \
  --arg worksheet_name "Summary" \
  --arg cell "F2" \
  --arg chart_id "summary-revenue-json-1" \
  --arg title "Quarterly Revenue" \
  --arg sql "SELECT \"Month\", \"Revenue\" FROM \"Summary\" ORDER BY \"Month\"" \
  --arg html "{ library: 'echarts', handler: (data) => ({ title: { text: 'Quarterly Revenue' }, tooltip: { trigger: 'axis' }, xAxis: { type: 'category', data: data.map(item => item['Month']) }, yAxis: { type: 'value', name: 'Revenue' }, series: [{ type: 'bar', data: data.map(item => Number(item['Revenue']) || 0) }] }) }" \
  '{
    uri: $uri,
    worksheet_name: $worksheet_name,
    cell: $cell,
    chart: {
      chart_id: $chart_id,
      type: "json",
      title: $title,
      width: 808,
      height: 270,
      sql: $sql,
      spec: {
        style: {
          title: $title,
          legend: "bottom"
        },
        boxAdaptation: {
          showDataZoom: "auto"
        }
      },
      html: $html,
      series: [],
      legend: "bottom",
      x_axis_name: "Month",
      y_axis_name: "Revenue",
      format: {
        from: { col: 5, row: 1, col_off: 0, row_off: 0 },
        to: { col: 13, row: 11, col_off: 0, row_off: 0 },
        lock_aspect_ratio: true,
        offset_x: 0,
        offset_y: 0,
        scale_x: 1,
        scale_y: 1
      }
    }
  }' > "$SUMMARY_CHART_PAYLOAD"
curl -s -X POST "$BASE_URL/api/v1/excel/add_chart" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  --data-binary "@$SUMMARY_CHART_PAYLOAD" | jq .

echo ""
echo "============================================================"
echo " Workflow 3: Append New Data and Recalculate"
echo "============================================================"

echo "[1/3] Appending new rows to Sheet1 ..."
curl -s -X POST "$BASE_URL/api/v1/excel/append_rows" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI_GID0\",
    \"data\": [
      {\"Month\": \"Apr\", \"Revenue\": 80000, \"Cost\": 42000},
      {\"Month\": \"May\", \"Revenue\": 95000, \"Cost\": 48000}
    ]
  }" | jq .

echo "[2/3] Recalculating all formulas ..."
curl -s -X POST "$BASE_URL/api/v1/excel/recalculate_formulas" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_URI\"}" \
  | jq .

echo "[3/3] Reading updated sheet ..."
curl -s -X POST "$BASE_URL/api/v1/excel/read_sheet" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_URI\", \"worksheet_name\": \"Sheet1\"}" \
  | jq .

echo ""
echo "All workflows complete."
