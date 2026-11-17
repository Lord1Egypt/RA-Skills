#!/usr/bin/env bash

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=scripts/_lib.sh
source "$SCRIPT_DIR/_lib.sh"

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  die "usage: $0 <image_path> [language=mw]"
fi

IMAGE="$1"
LANGUAGE="${2:-mw}"

validate_file "$IMAGE"
validate_ocr_language "$LANGUAGE"

EXTENSION="${IMAGE##*.}"
EXTENSION=$(printf '%s' "$EXTENSION" | tr '[:upper:]' '[:lower:]')
case "$EXTENSION" in
  jpg|jpeg) ENCODING="jpg" ;;
  png|bmp|webp|tif|tiff|gif) ENCODING="$EXTENSION" ;;
  *) die "unsupported image extension: $EXTENSION" ;;
esac

require_commands curl python3
load_key

HEADER_FILE=$(mktemp)
BODY_FILE=$(mktemp)
REQUEST_FILE=$(mktemp)
trap 'rm -f "$HEADER_FILE" "$BODY_FILE" "$REQUEST_FILE"' EXIT

python3 - "$IMAGE" "$LANGUAGE" "$ENCODING" > "$REQUEST_FILE" <<'PY'
import base64
import json
import sys

with open(sys.argv[1], "rb") as handle:
    encoded = base64.b64encode(handle.read()).decode("ascii")
print(json.dumps({
    "image_base64": encoded,
    "language": sys.argv[2],
    "image_encoding": sys.argv[3],
}))
PY

perform_request POST "$HEADER_FILE" "$BODY_FILE" \
  "$BASE_URL/ocr/" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  --data-binary "@$REQUEST_FILE"

extract_business_value "$BODY_FILE" data.text
emit_billing_summary "$HEADER_FILE" "$BODY_FILE"
