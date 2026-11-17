#!/usr/bin/env bash

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck source=scripts/_lib.sh
source "$SCRIPT_DIR/_lib.sh"

if [ "$#" -lt 3 ] || [ "$#" -gt 4 ]; then
  die "usage: $0 <file.docx|file.pdf> <from:auto|zh|mw|mn> <to:zh|mw|mn> [mode=mongolian_only|all]"
fi

DOCUMENT="$1"
FROM="$2"
TO="$3"
MODE="${4:-mongolian_only}"

validate_file "$DOCUMENT"
case "$FROM" in
  auto|zh|mw|mn) ;;
  *) die "source language must be one of: auto, zh, mw, mn" ;;
esac
validate_language "$TO"
if [ "$FROM" != "auto" ] && [ "$FROM" = "$TO" ]; then
  die "source and target languages must differ"
fi
case "$MODE" in
  mongolian_only|all) ;;
  *) die "mode must be 'mongolian_only' or 'all'" ;;
esac

EXTENSION="${DOCUMENT##*.}"
EXTENSION=$(printf '%s' "$EXTENSION" | tr '[:upper:]' '[:lower:]')
case "$EXTENSION" in
  docx) ENDPOINT="word/translation/" ;;
  pdf) ENDPOINT="pdf/translation/" ;;
  *) die "document must have a .docx or .pdf extension" ;;
esac

require_commands curl python3
load_key

HEADER_FILE=$(mktemp)
BODY_FILE=$(mktemp)
trap 'rm -f "$HEADER_FILE" "$BODY_FILE"' EXIT

perform_request POST "$HEADER_FILE" "$BODY_FILE" \
  "$BASE_URL/$ENDPOINT" \
  -H "Authorization: Bearer $KEY" \
  -F "from=$FROM" \
  -F "to=$TO" \
  -F "mode=$MODE" \
  -F "file=@$DOCUMENT"

extract_business_value "$BODY_FILE" data.text
emit_billing_summary "$HEADER_FILE" "$BODY_FILE"
