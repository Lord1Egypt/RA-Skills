#!/usr/bin/env bash
# MaybeAI Sheet — File Management
# Usage: export MAYBEAI_API_TOKEN=your_token_here
#        export BASE_URL=https://play-be.omnimcp.ai   (or your self-hosted URL)
#        export EXCEL_FILE_PATH=/absolute/path/to/file.xlsx
#        export IMPORT_ENGINE=postgres  # recommended for table-like files >10K rows or >100K cells
#        export UPLOAD_USER_ID=demo-user   # optional compatibility field
#        export UPLOAD_ONLY=1   # optional, stop after upload test
#        bash 01-file-management.sh

set -u

BASE_URL="${BASE_URL:-https://play-be.omnimcp.ai}"
TOKEN="${MAYBEAI_API_TOKEN:?Please set MAYBEAI_API_TOKEN}"
EXCEL_FILE_PATH="${EXCEL_FILE_PATH:-./sample.xlsx}"
IMPORT_ENGINE="${IMPORT_ENGINE:-}"
UPLOAD_USER_ID="${UPLOAD_USER_ID:-}"
UPLOAD_ONLY="${UPLOAD_ONLY:-0}"

if [ ! -f "$EXCEL_FILE_PATH" ]; then
  echo "Excel file not found: $EXCEL_FILE_PATH" >&2
  exit 1
fi

UPLOAD_RESP_FILE="$(mktemp)"

cleanup() {
  rm -f "$UPLOAD_RESP_FILE"
}
trap cleanup EXIT

# ── Upload / Import Excel File ───────────────────────────────────────────────
# Returns: { "document_id": "...", "uri": "...", ... }
# Build request URIs as https://www.maybe.ai/docs/spreadsheets/d/$DOC_ID for subsequent calls.
if [ "$IMPORT_ENGINE" = "postgres" ] || [ "$IMPORT_ENGINE" = "pg" ]; then
  echo "=== Import Excel File via SheetTable/PG ==="
  UPLOAD_ENDPOINT="$BASE_URL/api/v1/excel/import"
else
  echo "=== Upload Excel File via Excelize ==="
  UPLOAD_ENDPOINT="$BASE_URL/api/v1/excel/upload"
fi

UPLOAD_CURL_ARGS=(
  -sS
  -o "$UPLOAD_RESP_FILE"
  -w "%{http_code}"
  -X POST "$UPLOAD_ENDPOINT"
  -H "Authorization: Bearer $TOKEN"
  -F "file=@${EXCEL_FILE_PATH}"
)

if [ "$IMPORT_ENGINE" = "postgres" ] || [ "$IMPORT_ENGINE" = "pg" ]; then
  UPLOAD_CURL_ARGS+=(-F "engine=postgres")
fi

if [ -n "$UPLOAD_USER_ID" ]; then
  UPLOAD_CURL_ARGS+=(-F "user_id=${UPLOAD_USER_ID}")
fi

UPLOAD_HTTP_CODE=$(curl "${UPLOAD_CURL_ARGS[@]}")
cat "$UPLOAD_RESP_FILE" | jq . 2>/dev/null || cat "$UPLOAD_RESP_FILE"
echo "Upload HTTP status: $UPLOAD_HTTP_CODE"

if [ "$UPLOAD_HTTP_CODE" -ge 400 ]; then
  echo "Upload failed; stop here and switch to copy_excel + append_rows/update_range fallback." >&2
  exit 1
fi

DOC_ID=$(
  jq -r '.document_id // .documentId // ((.uri // .fileUri // "") | split("/d/") | last | split("?") | first)' \
    "$UPLOAD_RESP_FILE"
)
DOC_URI=$(
  jq -r '.uri // .fileUri // empty' "$UPLOAD_RESP_FILE"
)

if [ -z "$DOC_ID" ] || [ "$DOC_ID" = "null" ]; then
  echo "Upload succeeded but no document_id/uri was returned." >&2
  exit 1
fi

if [ -z "$DOC_URI" ] || [ "$DOC_URI" = "null" ]; then
  DOC_URI="https://www.maybe.ai/docs/spreadsheets/d/$DOC_ID"
fi

echo "Document ID: $DOC_ID"
echo "Document URI: $DOC_URI"

if [ "$UPLOAD_ONLY" = "1" ]; then
  exit 0
fi

# ── Import File by URL ───────────────────────────────────────────────────────
echo "=== Import File by URL ==="
curl -s -X POST "$BASE_URL/api/v1/excel/import_by_url" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/data.xlsx"}' \
  | jq .

# ── List Files ───────────────────────────────────────────────────────────────
echo "=== List Files ==="
curl -s -X POST "$BASE_URL/api/v1/excel/list_files" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}' \
  | jq .

# ── Search Files ─────────────────────────────────────────────────────────────
echo "=== Search Files ==="
curl -s -X POST "$BASE_URL/api/v1/excel/search_files" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "sales"}' \
  | jq .

# ── Rename File ──────────────────────────────────────────────────────────────
echo "=== Rename File ==="
curl -s -X POST "$BASE_URL/api/v1/excel/rename_file" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_URI\", \"new_filename\": \"renamed_sales_report.xlsx\"}" \
  | jq .

# ── Delete File ──────────────────────────────────────────────────────────────
echo "=== Delete File ==="
curl -s -X POST "$BASE_URL/api/v1/excel/delete_file" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_URI\"}" \
  | jq .

# ── Export (Download) File ───────────────────────────────────────────────────
echo "=== Export File ==="
curl -s -o "./exported.xlsx" \
  "$BASE_URL/api/v1/excel/export/$DOC_ID"
echo "Saved to ./exported.xlsx"

# ── Copy Excel Document ──────────────────────────────────────────────────────
echo "=== Copy Excel ==="
curl -s -X POST "$BASE_URL/api/v1/excel/copy_excel" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"uri\": \"$DOC_URI\"}" \
  | jq .
