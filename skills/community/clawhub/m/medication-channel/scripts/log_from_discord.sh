#!/usr/bin/env bash
set -euo pipefail

SCRIPT="$(cd "$(dirname "$0")" && pwd)/tracker_v2.py"

if [[ $# -lt 4 ]]; then
  echo "Usage: $0 <message_text> <channel_id> <message_id> <author_id> [timestamp_utc]" >&2
  exit 1
fi

TEXT="$1"
CHANNEL_ID="$2"
MESSAGE_ID="$3"
AUTHOR_ID="$4"
TIMESTAMP_UTC="${5:-}"

python3 "$SCRIPT" log-from-message "$TEXT" "$CHANNEL_ID" "$MESSAGE_ID" "$AUTHOR_ID" "$TIMESTAMP_UTC"
