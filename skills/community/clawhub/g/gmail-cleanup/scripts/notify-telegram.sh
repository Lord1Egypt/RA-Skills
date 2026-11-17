#!/usr/bin/env bash
# gmail-cleanup - send a digest/notification to Telegram via OpenClaw.
# Usage: notify-telegram.sh <message-file>   (use '-' to read the body from stdin)
set -euo pipefail

STATE="${GMAIL_CLEANUP_STATE:-$HOME/.openclaw/workspace/state/gmail-cleanup}"
CFG="${GMAIL_CLEANUP_CONFIG:-$STATE/config.json}"

TARGET="${TELEGRAM_TARGET:-$(python3 -c "import json,sys;print(json.load(open('$CFG')).get('notify',{}).get('target',''))" 2>/dev/null || true)}"
CHANNEL="$(python3 -c "import json,sys;print(json.load(open('$CFG')).get('notify',{}).get('channel','telegram'))" 2>/dev/null || echo telegram)"

if [ -z "$TARGET" ]; then
  echo "notify: no notify.target configured in $CFG" >&2
  exit 1
fi

SRC="${1:?usage: notify-telegram.sh <message-file|->}"
if [ "$SRC" = "-" ]; then
  BODY="$(cat)"
else
  BODY="$(cat "$SRC")"
fi

openclaw message send --channel "$CHANNEL" --target "$TARGET" --message "$BODY"
