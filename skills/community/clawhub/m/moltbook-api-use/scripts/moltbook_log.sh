#!/usr/bin/env bash
# Append a single JSONL log entry for Moltbook-related activity.
#
# Usage:
#   moltbook_log.sh \
#     --actions '["upvoted post …","commented on …"]' \
#     --links   '["postId/...","https://..."]' \
#     --notes   "Late-night Moltbook check; upvoted Hazel..." \
#     --run-id  "cron:..."  # optional
#
# The script does NOT talk to the Moltbook API. It only writes into
# logs/moltbook_cron_history.jsonl, preserving the existing structure.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LOG_DIR="$ROOT/logs"
LOG_FILE="$LOG_DIR/moltbook_cron_history.jsonl"

mkdir -p "$LOG_DIR"

ACTIONS="[]"
LINKS="[]"
NOTES=""
RUN_ID=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --actions)
      ACTIONS="$2"; shift 2;;
    --links)
      LINKS="$2"; shift 2;;
    --notes)
      NOTES="$2"; shift 2;;
    --run-id)
      RUN_ID="$2"; shift 2;;
    --help|-h)
      cat <<EOF
Usage: moltbook_log.sh --actions JSON_ARRAY [--links JSON_ARRAY] [--notes TEXT] [--run-id ID]

Appends a JSON object to logs/moltbook_cron_history.jsonl with fields:
  ts, date, actions, links, notes, runId?
EOF
      exit 0;;
    *)
      echo "Unknown arg: $1" >&2
      exit 1;;
  esac
done

# Basic sanity defaults
if [[ -z "$ACTIONS" ]]; then
  ACTIONS="[]"
fi
if [[ -z "$LINKS" ]]; then
  LINKS="[]"
fi

TS="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
DATE="$(date -u +"%Y-%m-%d")"

# Escape notes for JSON string
escape_notes() {
  local s="$1"
  s="${s//\\/\\\\}"
  s="${s//\"/\\\"}"
  s="${s//$'\n'/\\n}"
  s="${s//$'\r'/\\r}"
  s="${s//$'\t'/\\t}"
  printf '%s' "$s"
}

ESC_NOTES="$(escape_notes "$NOTES")"

if [[ -n "$RUN_ID" ]]; then
  printf '{"ts":"%s","date":"%s","actions":%s,"links":%s,"notes":"%s","runId":"%s"}
' \
    "$TS" "$DATE" "$ACTIONS" "$LINKS" "$ESC_NOTES" "$RUN_ID" >>"$LOG_FILE"
else
  printf '{"ts":"%s","date":"%s","actions":%s,"links":%s,"notes":"%s"}
' \
    "$TS" "$DATE" "$ACTIONS" "$LINKS" "$ESC_NOTES" >>"$LOG_FILE"
fi
