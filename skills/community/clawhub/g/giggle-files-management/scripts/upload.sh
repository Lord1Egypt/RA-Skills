#!/usr/bin/env bash
set -euo pipefail

# Usage: upload.sh <file_path> [custom_filename]

API_BASE="https://api.giggle.pro/api/v1/assets"

# --- Resolve API key (GIGGLE_ASSET_SERVICE_KEY > STORYCLAW_API_KEY) ---
API_KEY="${GIGGLE_ASSET_SERVICE_KEY:-${STORYCLAW_API_KEY:-}}"
if [[ -z "$API_KEY" ]]; then
  echo '{"error":"No API key. Set GIGGLE_ASSET_SERVICE_KEY or STORYCLAW_API_KEY."}' >&2
  exit 1
fi

FILE_PATH="${1:?Usage: upload.sh <file_path> [custom_filename]}"
if [[ ! -f "$FILE_PATH" ]]; then
  echo "{\"error\":\"File not found: $FILE_PATH\"}" >&2
  exit 1
fi

BASENAME="$(basename "$FILE_PATH")"
CUSTOM_NAME="${2:-$BASENAME}"

# --- Detect content type from extension ---
detect_content_type() {
  local ext="${1##*.}"
  ext="$(echo "$ext" | tr '[:upper:]' '[:lower:]')"
  case "$ext" in
    jpg|jpeg)  echo "image/jpeg" ;;
    png)       echo "image/png" ;;
    gif)       echo "image/gif" ;;
    webp)      echo "image/webp" ;;
    svg)       echo "image/svg+xml" ;;
    bmp)       echo "image/bmp" ;;
    ico)       echo "image/x-icon" ;;
    mp4)       echo "video/mp4" ;;
    webm)      echo "video/webm" ;;
    mov)       echo "video/quicktime" ;;
    avi)       echo "video/x-msvideo" ;;
    mp3)       echo "audio/mpeg" ;;
    wav)       echo "audio/wav" ;;
    ogg)       echo "audio/ogg" ;;
    flac)      echo "audio/flac" ;;
    pdf)       echo "application/pdf" ;;
    json)      echo "application/json" ;;
    xml)       echo "application/xml" ;;
    zip)       echo "application/zip" ;;
    tar)       echo "application/x-tar" ;;
    gz|tgz)    echo "application/gzip" ;;
    txt)       echo "text/plain" ;;
    html|htm)  echo "text/html" ;;
    css)       echo "text/css" ;;
    js)        echo "application/javascript" ;;
    csv)       echo "text/csv" ;;
    md)        echo "text/markdown" ;;
    doc)       echo "application/msword" ;;
    docx)      echo "application/vnd.openxmlformats-officedocument.wordprocessingml.document" ;;
    xls)       echo "application/vnd.ms-excel" ;;
    xlsx)      echo "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" ;;
    ppt)       echo "application/vnd.ms-powerpoint" ;;
    pptx)      echo "application/vnd.openxmlformats-officedocument.presentationml.presentation" ;;
    *)         echo "application/octet-stream" ;;
  esac
}

CONTENT_TYPE="$(detect_content_type "$CUSTOM_NAME")"

# --- Step 1: Get presigned URL ---
PRESIGN_RESP="$(curl -sS -X POST "$API_BASE/get-presigned-url" \
  -H "Content-Type: application/json" \
  -H "Accept: */*" \
  -H "x-api-key: $API_KEY" \
  -d "{\"file_name\":\"$CUSTOM_NAME\",\"content_type\":\"$CONTENT_TYPE\",\"is_public\":true}")"

PRESIGN_CODE="$(echo "$PRESIGN_RESP" | jq -r '.code // empty')"
if [[ "$PRESIGN_CODE" != "200" ]]; then
  echo "{\"error\":\"Presign failed\",\"response\":$PRESIGN_RESP}" >&2
  exit 1
fi

OBJECT_KEY="$(echo "$PRESIGN_RESP" | jq -r '.data.object_key')"
SIGNED_URL="$(echo "$PRESIGN_RESP" | jq -r '.data.signed_url')"

# --- Step 2: Upload file to presigned URL ---
HTTP_CODE="$(curl -sS -o /dev/null -w '%{http_code}' -X PUT \
  -T "$FILE_PATH" \
  -H "Content-Type: $CONTENT_TYPE" \
  "$SIGNED_URL")"

if [[ "$HTTP_CODE" -lt 200 || "$HTTP_CODE" -ge 300 ]]; then
  echo "{\"error\":\"Upload failed with HTTP $HTTP_CODE\"}" >&2
  exit 1
fi

# --- Step 3: Register asset ---
REGISTER_RESP="$(curl -sS -X POST "$API_BASE/register" \
  -H "Content-Type: application/json" \
  -H "Accept: */*" \
  -H "x-api-key: $API_KEY" \
  -d "{\"object_key\":\"$OBJECT_KEY\",\"name\":\"$CUSTOM_NAME\"}")"

REGISTER_CODE="$(echo "$REGISTER_RESP" | jq -r '.code // empty')"
if [[ "$REGISTER_CODE" != "200" ]]; then
  echo "{\"error\":\"Register failed\",\"response\":$REGISTER_RESP}" >&2
  exit 1
fi

# --- Output result ---
echo "$REGISTER_RESP" | jq '{
  public_url: .data.public_url,
  download_url: .data.download_url,
  content_type: .data.head_object.ContentType,
  asset_id: .data.asset_id,
  thumbnail_url: .data.thumbnail_url
}'
