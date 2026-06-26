#!/usr/bin/env bash
# MaybeAI Sheet — Charts & Pictures
# Usage: export MAYBEAI_API_TOKEN=your_token_here
#        export DOC_ID=your_document_id_here
#        bash 07-charts-pictures.sh

BASE_URL="https://play-be.omnimcp.ai"
TOKEN="${MAYBEAI_API_TOKEN:?Please set MAYBEAI_API_TOKEN}"
DOC_ID="${DOC_ID:?Please set DOC_ID}"
DOC_URI="https://www.maybe.ai/docs/spreadsheets/d/$DOC_ID"
PICTURE_FILE_BASE64="${PICTURE_FILE_BASE64:-iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQIHWP4////fwAJ+wP9KobjigAAAABJRU5ErkJggg==}"
DATA_SHEET="${DATA_SHEET:-Sheet1}"
DASHBOARD_SHEET="${DASHBOARD_SHEET:-Dashboard}"
TREND_CHART_ID="${TREND_CHART_ID:-revenue-trend-json-1}"
REGION_CHART_ID="${REGION_CHART_ID:-revenue-region-json-1}"
PAYLOAD_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "$PAYLOAD_DIR"
}
trap cleanup EXIT

post_json() {
  local endpoint="$1"
  local payload_file="$2"
  curl -s -X POST "$BASE_URL$endpoint" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    --data-binary "@$payload_file"
}

# Notes:
# - This script follows the sheet-dashboard chart API conventions.
# - For add_chart and set_chart, use type=json with an ECharts renderer in chart.html.
# - Always set both the outer cell and chart.format.from/to.

# ── Add Full-Width Trend Chart ────────────────────────────────────────────────
echo "=== Add Full-Width Trend Chart ==="
TREND_ADD_PAYLOAD="$PAYLOAD_DIR/add-trend-chart.json"
jq -n \
  --arg uri "$DOC_URI" \
  --arg worksheet_name "$DASHBOARD_SHEET" \
  --arg cell "B2" \
  --arg chart_id "$TREND_CHART_ID" \
  --arg title "Monthly Revenue Trend" \
  --arg sql "SELECT \"Month\", SUM(\"Revenue\") AS \"Revenue\" FROM \"$DATA_SHEET\" GROUP BY \"Month\" ORDER BY \"Month\"" \
  --arg html "{ library: 'echarts', handler: (data) => ({ title: { text: 'Monthly Revenue Trend' }, tooltip: { trigger: 'axis' }, xAxis: { type: 'category', data: data.map(item => item['Month']) }, yAxis: { type: 'value', name: 'Revenue' }, series: [{ type: 'line', smooth: true, data: data.map(item => Number(item['Revenue']) || 0) }] }) }" \
  '{
    uri: $uri,
    worksheet_name: $worksheet_name,
    cell: $cell,
    chart: {
      chart_id: $chart_id,
      type: "json",
      title: $title,
      width: 1313,
      height: 324,
      sql: $sql,
      spec: {
        style: {
          title: $title,
          smooth: true,
          legend: "bottom"
        },
        boxAdaptation: {
          showDataZoom: "auto"
        }
      },
      html: $html,
      series: [],
      legend: "bottom",
      show_blanks: "gap",
      x_axis_name: "Month",
      y_axis_name: "Revenue",
      format: {
        from: { col: 1, row: 1, col_off: 0, row_off: 0 },
        to: { col: 14, row: 13, col_off: 0, row_off: 0 },
        lock_aspect_ratio: true,
        offset_x: 0,
        offset_y: 0,
        scale_x: 1,
        scale_y: 1
      }
    }
  }' > "$TREND_ADD_PAYLOAD"
post_json "/api/v1/excel/add_chart" "$TREND_ADD_PAYLOAD" | jq .

# ── Add Comparison Chart ──────────────────────────────────────────────────────
echo "=== Add Comparison Chart ==="
REGION_ADD_PAYLOAD="$PAYLOAD_DIR/add-region-chart.json"
jq -n \
  --arg uri "$DOC_URI" \
  --arg worksheet_name "$DASHBOARD_SHEET" \
  --arg cell "B15" \
  --arg chart_id "$REGION_CHART_ID" \
  --arg title "Revenue By Region" \
  --arg sql "SELECT \"Region\", SUM(\"Revenue\") AS \"Revenue\" FROM \"$DATA_SHEET\" GROUP BY \"Region\" ORDER BY \"Revenue\" DESC" \
  --arg html "{ library: 'echarts', handler: (data) => ({ title: { text: 'Revenue By Region' }, tooltip: { trigger: 'axis' }, xAxis: { type: 'category', data: data.map(item => item['Region']) }, yAxis: { type: 'value', name: 'Revenue' }, series: [{ type: 'bar', data: data.map(item => Number(item['Revenue']) || 0) }] }) }" \
  '{
    uri: $uri,
    worksheet_name: $worksheet_name,
    cell: $cell,
    chart: {
      chart_id: $chart_id,
      type: "json",
      title: $title,
      width: 404,
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
      x_axis_name: "Region",
      y_axis_name: "Revenue",
      format: {
        from: { col: 1, row: 14, col_off: 0, row_off: 0 },
        to: { col: 5, row: 24, col_off: 0, row_off: 0 },
        lock_aspect_ratio: true,
        offset_x: 0,
        offset_y: 0,
        scale_x: 1,
        scale_y: 1
      }
    }
  }' > "$REGION_ADD_PAYLOAD"
post_json "/api/v1/excel/add_chart" "$REGION_ADD_PAYLOAD" | jq .

# ── Inspect Charts ────────────────────────────────────────────────────────────
echo "=== Get Charts Metadata ==="
GET_CHARTS_PAYLOAD="$PAYLOAD_DIR/get-charts.json"
jq -n \
  --arg uri "$DOC_URI" \
  --arg worksheet_name "$DASHBOARD_SHEET" \
  '{
    uri: $uri,
    worksheet_name: $worksheet_name
  }' > "$GET_CHARTS_PAYLOAD"
post_json "/api/v1/excel/get_charts" "$GET_CHARTS_PAYLOAD" | jq .

# ── Edit Chart ────────────────────────────────────────────────────────────────
echo "=== Edit Trend Chart By chart_id ==="
TREND_SET_PAYLOAD="$PAYLOAD_DIR/set-trend-chart.json"
jq -n \
  --arg uri "$DOC_URI" \
  --arg worksheet_name "$DASHBOARD_SHEET" \
  --arg cell "B2" \
  --arg chart_id "$TREND_CHART_ID" \
  --arg title "Monthly Revenue Trend Updated" \
  --arg sql "SELECT \"Month\", SUM(\"Revenue\") AS \"Revenue\" FROM \"$DATA_SHEET\" GROUP BY \"Month\" ORDER BY \"Month\"" \
  --arg html "{ library: 'echarts', handler: (data) => ({ title: { text: 'Monthly Revenue Trend Updated' }, tooltip: { trigger: 'axis' }, legend: { top: 8 }, xAxis: { type: 'category', data: data.map(item => item['Month']) }, yAxis: { type: 'value', name: 'Revenue' }, series: [{ type: 'line', smooth: true, data: data.map(item => Number(item['Revenue']) || 0) }] }) }" \
  '{
    uri: $uri,
    worksheet_name: $worksheet_name,
    cell: $cell,
    chart: {
      chart_id: $chart_id,
      type: "json",
      title: $title,
      width: 1313,
      height: 324,
      sql: $sql,
      spec: {
        style: {
          title: $title,
          smooth: true,
          legend: "top"
        },
        boxAdaptation: {
          showDataZoom: "auto"
        }
      },
      html: $html,
      series: [],
      legend: "top",
      show_blanks: "gap",
      x_axis_name: "Month",
      y_axis_name: "Revenue",
      format: {
        from: { col: 1, row: 1, col_off: 0, row_off: 0 },
        to: { col: 14, row: 13, col_off: 0, row_off: 0 },
        lock_aspect_ratio: true,
        offset_x: 0,
        offset_y: 0,
        scale_x: 1,
        scale_y: 1
      }
    }
  }' > "$TREND_SET_PAYLOAD"
post_json "/api/v1/excel/set_chart" "$TREND_SET_PAYLOAD" | jq .

# ── Delete Chart ──────────────────────────────────────────────────────────────
echo "=== Delete Comparison Chart By chart_id ==="
DELETE_CHART_PAYLOAD="$PAYLOAD_DIR/delete-chart.json"
jq -n \
  --arg uri "$DOC_URI" \
  --arg worksheet_name "$DASHBOARD_SHEET" \
  --arg chart_id "$REGION_CHART_ID" \
  '{
    uri: $uri,
    worksheet_name: $worksheet_name,
    chart_id: $chart_id
  }' > "$DELETE_CHART_PAYLOAD"
post_json "/api/v1/excel/delete_chart" "$DELETE_CHART_PAYLOAD" | jq .

# ── Add Picture ───────────────────────────────────────────────────────────────
echo "=== Add Picture ==="
curl -s -X POST "$BASE_URL/api/v1/excel/add_picture" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"uri\": \"$DOC_URI\",
    \"worksheet_name\": \"$DASHBOARD_SHEET\",
    \"cell\": \"J15\",
    \"picture\": {
      \"file_base64\": \"$PICTURE_FILE_BASE64\",
      \"extension\": \"png\"
    }
  }" \
  | jq .

# ── Read Pictures ─────────────────────────────────────────────────────────────
echo "=== Read Pictures ==="
curl -s -X POST "$BASE_URL/api/v1/excel/read_picture" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_URI\", \"worksheet_name\": \"$DASHBOARD_SHEET\", \"cell\": \"J15\"}" \
  | jq .

# ── Delete Picture ────────────────────────────────────────────────────────────
echo "=== Delete Picture ==="
curl -s -X POST "$BASE_URL/api/v1/excel/delete_picture" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_URI\", \"worksheet_name\": \"$DASHBOARD_SHEET\", \"cell\": \"J15\"}" \
  | jq .
