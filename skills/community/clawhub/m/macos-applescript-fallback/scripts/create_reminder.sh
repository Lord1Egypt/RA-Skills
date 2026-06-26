#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   create_reminder.sh "任务内容" "2026-03-22 20:00:00"
# If datetime omitted, creates reminder without remind-me date.

TITLE="${1:-}"
REMIND_AT="${2:-}"

if [[ -z "$TITLE" ]]; then
  echo "Usage: $0 <title> [\"YYYY-MM-DD HH:MM:SS\"]" >&2
  exit 1
fi

if [[ -z "$REMIND_AT" ]]; then
  /usr/bin/osascript - "$TITLE" <<'APPLESCRIPT'
on run argv
  set titleText to item 1 of argv
  tell application "Reminders"
    set r to make new reminder with properties {name:titleText}
    return id of r
  end tell
end run
APPLESCRIPT
else
  /usr/bin/osascript - "$TITLE" "$REMIND_AT" <<'APPLESCRIPT'
on run argv
  set titleText to item 1 of argv
  set remindAtText to item 2 of argv
  set remindAtDate to date remindAtText
  tell application "Reminders"
    set r to make new reminder with properties {name:titleText, remind me date:remindAtDate}
    return id of r
  end tell
end run
APPLESCRIPT
fi
