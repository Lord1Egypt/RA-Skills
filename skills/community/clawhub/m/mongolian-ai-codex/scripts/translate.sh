#!/usr/bin/env bash

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=scripts/_lib.sh
source "$SCRIPT_DIR/_lib.sh"

if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
  die "usage: $0 <from:zh|mw|mn> <to:zh|mw|mn> [text]; omit text to read stdin"
fi

FROM="$1"
TO="$2"
shift 2

validate_language "$FROM"
validate_language "$TO"
[ "$FROM" != "$TO" ] || die "source and target languages must differ"

TEXT=$(read_text_argument "$@")
[ -n "$TEXT" ] || die "translation text must not be empty"

TEXT_LENGTH=$(unicode_length "$TEXT")
[ "$TEXT_LENGTH" -le 4000 ] ||
  die "translation text exceeds 4,000 Unicode code points; split it on natural boundaries"

require_commands curl python3
load_key

HEADER_FILE=$(mktemp)
BODY_FILE=$(mktemp)
REQUEST_FILE=$(mktemp)
trap 'rm -f "$HEADER_FILE" "$BODY_FILE" "$REQUEST_FILE"' EXIT

python3 - "$FROM" "$TO" "$TEXT" > "$REQUEST_FILE" <<'PY'
import json
import sys

print(json.dumps(
    {"from": sys.argv[1], "to": sys.argv[2], "content": sys.argv[3]},
    ensure_ascii=False,
))
PY

perform_request POST "$HEADER_FILE" "$BODY_FILE" \
  "$BASE_URL/translation/" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  --data-binary "@$REQUEST_FILE"

RESULT=$(json_extract_first "$BODY_FILE" data.tgtText 2>/dev/null) ||
  die "the service response did not contain the expected translation"

if ! python3 - "$TO" "$RESULT" <<'PY'
import re
import sys

target, text = sys.argv[1:]
has_han = bool(re.search(r"[\u3400-\u4dbf\u4e00-\u9fff]", text))
has_mongolian = bool(re.search(r"[\u1800-\u18af]", text))
valid = not (
    (target == "zh" and has_mongolian)
    or (target == "mw" and has_han)
    or (target == "mn" and has_mongolian)
)
raise SystemExit(0 if valid else 1)
PY
then
  die "the service returned text in the wrong script for target '$TO'; retry only with user approval"
fi

printf '%s\n' "$RESULT"
emit_billing_summary "$HEADER_FILE" "$BODY_FILE"
