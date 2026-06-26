#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

python3 "$SCRIPT_DIR/gmail_auto_draft.py" \
  --auth-mode "${AUTH_MODE:-local}" \
  --max-emails "${MAX_EMAILS:-5}" \
  --poll-interval "${POLL_INTERVAL:-0}" \
  --query-file "$BASE_DIR/references/upwork-demo/gmail_query.txt" \
  --agency-profile-file "$BASE_DIR/references/upwork-demo/agency_profile.txt" \
  --style-rules-file "$BASE_DIR/references/upwork-demo/style_rules.txt" \
  "$@"
