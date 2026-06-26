#!/usr/bin/env bash
# Make phone calls via macOS Phone/FaceTime.
# Usage: call.sh [--dry-run] [--no-confirm] [--scheme tel|tel-phoneapp|facetime-audio] +491234567890
#
# macOS may show a confirmation sheet/dialog after opening phone URLs.
# This script opens the call URL and tries to click a visible confirmation button
# via Accessibility UI scripting. If no dialog appears, it treats that as OK
# because current macOS Phone.app can start the call directly after user approval.

set -euo pipefail

AUTO_CONFIRM=1
DRY_RUN=0
SCHEME="${PHONE_CALL_URL_SCHEME:-tel}"
TIMEOUT_SECONDS="${PHONE_CALL_CONFIRM_TIMEOUT:-10}"
NUMBER=""

usage() {
  cat <<EOF
Usage: $0 [--dry-run] [--no-confirm] [--confirm] [--scheme tel|tel-phoneapp|facetime-audio] [--timeout seconds] <phone-number>
Example: $0 +491234567890
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=1; shift ;;
    --no-confirm)
      AUTO_CONFIRM=0; shift ;;
    --confirm)
      AUTO_CONFIRM=1; shift ;;
    --scheme)
      SCHEME="${2:-}"; shift 2 ;;
    --timeout)
      TIMEOUT_SECONDS="${2:-}"; shift 2 ;;
    -h|--help)
      usage; exit 0 ;;
    *)
      NUMBER="$1"; shift ;;
  esac
done

if [[ -z "$NUMBER" ]]; then
  usage >&2
  exit 1
fi

case "$SCHEME" in
  tel|tel-phoneapp|facetime-audio|telephony) ;;
  *)
    echo "Unsupported scheme: $SCHEME" >&2
    echo "Use tel, tel-phoneapp, facetime-audio, or telephony." >&2
    exit 2 ;;
esac

if ! [[ "$TIMEOUT_SECONDS" =~ ^[0-9]+$ ]] || [[ "$TIMEOUT_SECONDS" -lt 1 ]]; then
  echo "Invalid timeout: $TIMEOUT_SECONDS" >&2
  exit 2
fi

# Clean number: keep digits and normalize to one leading +.
DIGITS="$(printf '%s' "$NUMBER" | tr -cd '0-9')"
CLEAN_NUMBER="+$DIGITS"

if [[ ! "$CLEAN_NUMBER" =~ ^\+[0-9]{7,15}$ ]]; then
  echo "Invalid phone number. Use E.164 format, e.g. +4915112345678" >&2
  exit 2
fi

CALL_URL="$SCHEME:$CLEAN_NUMBER"

if [[ "$DRY_RUN" == "1" ]]; then
  echo "DRY_RUN: would open $CALL_URL"
  [[ "$AUTO_CONFIRM" == "1" ]] && echo "DRY_RUN: would auto-confirm macOS call dialog if present (timeout ${TIMEOUT_SECONDS}s)"
  exit 0
fi

echo "Opening macOS call URL: $CALL_URL"
open "$CALL_URL"

if [[ "$AUTO_CONFIRM" != "1" ]]; then
  echo "Call URL opened. Auto-confirm disabled."
  exit 0
fi

# Try to press the system/FaceTime/Phone confirmation button.
# Handles English and German UI labels and searches nested UI elements.
osascript "$TIMEOUT_SECONDS" <<'APPLESCRIPT'
on clickMatchingButton(container, buttonNames)
  tell application "System Events"
    try
      if role of container is "AXButton" then
        set n to ""
        set d to ""
        try
          set n to name of container as text
        end try
        try
          set d to description of container as text
        end try
        repeat with btnName in buttonNames
          if n is (btnName as text) or d is (btnName as text) then
            click container
            return true
          end if
        end repeat
      end if
    end try
    try
      repeat with child in UI elements of container
        if my clickMatchingButton(child, buttonNames) then return true
      end repeat
    end try
  end tell
  return false
end clickMatchingButton

set timeoutSeconds to item 1 of argv as integer
set deadline to (current date) + timeoutSeconds
set clicked to false
set buttonNames to {"Call", "Anrufen", "Anruf", "Audio", "FaceTime Audio", "Fortfahren", "Continue", "OK", "Wählen", "Dial"}
set candidateProcesses to {"Phone", "Telefon", "FaceTime", "CoreServicesUIAgent", "UserNotificationCenter"}

repeat while ((current date) < deadline and clicked is false)
  delay 0.25
  tell application "System Events"
    repeat with procName in candidateProcesses
      if exists process (procName as text) then
        tell process (procName as text)
          try
            repeat with win in windows
              if my clickMatchingButton(win, buttonNames) then
                set clicked to true
                exit repeat
              end if
            end repeat
          end try
        end tell
      end if
      if clicked then exit repeat
    end repeat
  end tell
end repeat

if clicked then
  return "Call confirmation clicked."
else
  return "No visible macOS call confirmation button found; continuing because Phone.app may have started the call directly."
end if
APPLESCRIPT

echo "Call initiated; confirmation attempted if a dialog was visible."
