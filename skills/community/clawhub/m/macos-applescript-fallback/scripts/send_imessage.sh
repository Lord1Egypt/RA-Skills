#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   send_imessage.sh "zhangqianyi1995@icloud.com" "测试消息"

TARGET="${1:-}"
TEXT="${2:-}"

if [[ -z "$TARGET" || -z "$TEXT" ]]; then
  echo "Usage: $0 <buddy(手机号/AppleID)> <message>" >&2
  exit 1
fi

/usr/bin/osascript - "$TARGET" "$TEXT" <<'APPLESCRIPT'
on run argv
  set targetBuddy to item 1 of argv
  set messageText to item 2 of argv

  tell application "Messages"
    set imService to first service whose service type = iMessage
    send messageText to buddy targetBuddy of imService
    return "sent"
  end tell
end run
APPLESCRIPT
