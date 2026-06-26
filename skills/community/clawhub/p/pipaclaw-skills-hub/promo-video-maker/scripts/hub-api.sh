#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/bootstrap.sh" >/dev/null

CONFIG_DIR="${PROMO_VIDEO_MAKER_CONFIG_DIR:-${MALIANG_HUB_CONFIG_DIR:-$HOME/.config/maliang-hub}}"
BASE_URL="${PROMO_VIDEO_MAKER_BASE_URL:-${MALIANG_HUB_BASE_URL:-https://nano.djdog.ai}}"
API_KEY="$(cat "$CONFIG_DIR/api_key")"
CURL_OPTS=(--http1.1 -sS)

METHOD="${1:?usage: hub-api.sh METHOD PATH [JSON_BODY]}"
PATHNAME="${2:?usage: hub-api.sh METHOD PATH [JSON_BODY]}"
BODY="${3-}"

if [[ -n "$BODY" ]]; then
  curl "${CURL_OPTS[@]}" -X "$METHOD" "$BASE_URL$PATHNAME" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "$BODY"
else
  curl "${CURL_OPTS[@]}" -X "$METHOD" "$BASE_URL$PATHNAME" \
    -H "Authorization: Bearer $API_KEY"
fi
