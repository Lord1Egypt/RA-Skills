#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<EOF
Usage: $0 --to <email> --subject <subject> --text <body.txt> --html <body.html> --attach <brief.html> [--account <gmail>]
EOF
}

ACCOUNT="alex.data.assistant@gmail.com"
TO=""
SUBJECT=""
TEXT=""
HTML=""
ATTACH=""
DRY_RUN=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --account) ACCOUNT="$2"; shift 2 ;;
    --to) TO="$2"; shift 2 ;;
    --subject) SUBJECT="$2"; shift 2 ;;
    --text) TEXT="$2"; shift 2 ;;
    --html) HTML="$2"; shift 2 ;;
    --attach) ATTACH="$2"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    *) usage; exit 2 ;;
  esac
done

[[ -n "$TO" && -n "$SUBJECT" && -n "$TEXT" && -n "$HTML" && -n "$ATTACH" ]] || { usage; exit 2; }
[[ -f "$TEXT" && -f "$HTML" && -f "$ATTACH" ]] || { echo "missing input artifact" >&2; exit 2; }

HTML_BODY=$(cat "$HTML")
CMD=(gog gmail send
  --to "$TO"
  --subject "$SUBJECT"
  --body-file "$TEXT"
  --body-html "$HTML_BODY"
  --attach "$ATTACH")

if [[ "$DRY_RUN" -eq 1 ]]; then
  CMD+=(--dry-run)
fi

GOG_ACCOUNT="$ACCOUNT" "${CMD[@]}"
