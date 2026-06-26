#!/usr/bin/env bash
set -euo pipefail
_PEXO_CONFIG="${PEXO_CONFIG:-$HOME/.pexo/config}"
[[ -f "$_PEXO_CONFIG" ]] && source "$_PEXO_CONFIG"
PEXO_LAST_HTTP_CODE=0

pexo_require_config() {
    [[ -n "${PEXO_BASE_URL:-}" ]] || { echo 'Missing PEXO_BASE_URL' >&2; return 1; }
    [[ -n "${PEXO_API_KEY:-}" ]] || { echo 'Missing PEXO_API_KEY' >&2; return 1; }
}

_pexo_auth_header() { printf 'Authorization: Bearer %s' "$PEXO_API_KEY"; }

detect_asset_type() {
    local ext="${1##*.}"; ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
    case "$ext" in jpg|jpeg|png|webp|bmp|tiff|heic|heif) echo "IMAGE" ;; mp4|mov|avi) echo "VIDEO" ;; mp3|wav|aac|m4a|ogg|flac) echo "AUDIO" ;; *) echo "UNKNOWN" ;; esac
}

detect_mime() { file --brief --mime-type "$1" 2>/dev/null || echo "application/octet-stream"; }

_pexo_request_json() {
    local method="$1"; local path="$2"; local body="${3:-}"; shift 3 || true
    pexo_require_config
    local body_file header_file err_file response http_code curl_status=0
    body_file=$(mktemp); header_file=$(mktemp); err_file=$(mktemp)
    if [[ -n "$body" ]]; then
        http_code=$(curl -sS --connect-timeout 10 --max-time 60 -X "$method" -H "$(_pexo_auth_header)" -H "Content-Type: application/json" -D "$header_file" -o "$body_file" -w '%{http_code}' -d "$body" "$@" "${PEXO_BASE_URL}${path}" 2>"$err_file") || curl_status=$?
    else
        http_code=$(curl -sS --connect-timeout 10 --max-time 60 -X "$method" -H "$(_pexo_auth_header)" -H "Content-Type: application/json" -D "$header_file" -o "$body_file" -w '%{http_code}' "$@" "${PEXO_BASE_URL}${path}" 2>"$err_file") || curl_status=$?
    fi
    response=$(cat "$body_file"); export PEXO_LAST_HTTP_CODE="${http_code:-0}"
    if [[ $curl_status -ne 0 && "${http_code:-0}" == "000" ]]; then echo "Network error: $(cat "$err_file")" >&2; rm -f "$body_file" "$header_file" "$err_file"; return 1; fi
    if [[ "${http_code:-0}" -ge 400 ]]; then echo "HTTP $http_code: $response" >&2; rm -f "$body_file" "$header_file" "$err_file"; return 1; fi
    echo "$response"; rm -f "$body_file" "$header_file" "$err_file"
}

pexo_get() { local path="$1"; shift || true; _pexo_request_json GET "$path" "" "$@"; }
pexo_post() { local path="$1"; local body="${2:-}"; shift 2 || true; _pexo_request_json POST "$path" "$body" "$@"; }

pexo_post_sse_ack() {
    local path="$1"; local body="${2:-}"; local timeout="${3:-20}"
    pexo_require_config
    curl -sS -N --connect-timeout 10 --max-time "$timeout" -X POST -H "$(_pexo_auth_header)" -H "Content-Type: application/json" -H "Accept: text/event-stream" -d "$body" "${PEXO_BASE_URL}${path}" 2>/dev/null | sed '/^: stream opened$/q' >/dev/null
}
