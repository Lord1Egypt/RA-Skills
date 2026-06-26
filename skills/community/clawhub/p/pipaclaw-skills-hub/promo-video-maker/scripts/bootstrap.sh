#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="${PROMO_VIDEO_MAKER_CONFIG_DIR:-${MALIANG_HUB_CONFIG_DIR:-$HOME/.config/maliang-hub}}"
KEY_FILE="$CONFIG_DIR/api_key"
CODE_FILE="$CONFIG_DIR/short_code"
BASE_URL="${PROMO_VIDEO_MAKER_BASE_URL:-${MALIANG_HUB_BASE_URL:-https://nano.djdog.ai}}"

mkdir -p "$CONFIG_DIR"

if [[ ! -f "$KEY_FILE" || ! -s "$KEY_FILE" ]]; then
  MACHINE_ID="$(hostname)"
  CURL_OPTS=(--http1.1 -sS)
  PROVISION_RESULT="$(curl "${CURL_OPTS[@]}" -X POST "$BASE_URL/api/v1/provision" \
    -H "Content-Type: application/json" \
    -d "{\"machine_id\":\"$MACHINE_ID\"}")"

  printf '%s' "$PROVISION_RESULT" | python3 -c '
import json
import pathlib
import sys

payload = json.load(sys.stdin)
data = payload.get("data") or {}
api_key = data.get("api_key")
short_code = data.get("short_code")
if not api_key or not short_code:
    raise SystemExit("provision failed: missing api_key or short_code")

pathlib.Path(sys.argv[1]).write_text(api_key)
pathlib.Path(sys.argv[2]).write_text(short_code)
' "$KEY_FILE" "$CODE_FILE"

  chmod 600 "$KEY_FILE"
fi

API_KEY="$(cat "$KEY_FILE")"
SHORT_CODE="$(cat "$CODE_FILE" 2>/dev/null || true)"

python3 - <<'PY' "$API_KEY" "$SHORT_CODE" "$BASE_URL"
import json
import sys

api_key, short_code, base_url = sys.argv[1:4]
print(json.dumps({
    "api_key_prefix": api_key[:14] + "...",
    "short_code": short_code,
    "base_url": base_url,
    "recharge_url": f"{base_url}/recharge/{short_code}" if short_code else None,
}, ensure_ascii=False))
PY
