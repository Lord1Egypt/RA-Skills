#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   create_calendar_event.sh "跑步" "个人" "2026-03-23 08:00:00" "2026-03-23 08:30:00"

TITLE="${1:-}"
CAL_NAME="${2:-个人}"
START_AT="${3:-}"
END_AT="${4:-}"

if [[ -z "$TITLE" || -z "$START_AT" || -z "$END_AT" ]]; then
  echo "Usage: $0 <title> <calendar-name> <start:'YYYY-MM-DD HH:MM:SS'> <end:'YYYY-MM-DD HH:MM:SS'>" >&2
  exit 1
fi

/usr/bin/osascript - "$TITLE" "$CAL_NAME" "$START_AT" "$END_AT" <<'APPLESCRIPT'
on run argv
  set eventTitle to item 1 of argv
  set calName to item 2 of argv
  set startText to item 3 of argv
  set endText to item 4 of argv

  set startDate to date startText
  set endDate to date endText

  tell application "Calendar"
    if exists calendar calName then
      set targetCal to calendar calName
    else
      set targetCal to calendar 1
    end if

    tell targetCal
      set e to make new event at end of events with properties {summary:eventTitle, start date:startDate, end date:endDate}
    end tell

    return id of e
  end tell
end run
APPLESCRIPT
