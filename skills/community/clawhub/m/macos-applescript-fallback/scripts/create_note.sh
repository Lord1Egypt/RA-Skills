#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   create_note.sh "<h1>标题</h1><p>正文</p>" [accountName]
# accountName defaults to iCloud; falls back to default account if not found.

BODY_HTML="${1:-}"
ACCOUNT_NAME="${2:-iCloud}"

if [[ -z "$BODY_HTML" ]]; then
  echo "Usage: $0 <html-body> [account-name]" >&2
  exit 1
fi

/usr/bin/osascript - "$BODY_HTML" "$ACCOUNT_NAME" <<'APPLESCRIPT'
on run argv
  set bodyHtml to item 1 of argv
  set accountName to item 2 of argv

  tell application "Notes"
    if exists account accountName then
      tell account accountName
        set n to make new note with properties {body:bodyHtml}
      end tell
    else
      set n to make new note with properties {body:bodyHtml}
    end if
    activate
    return id of n
  end tell
end run
APPLESCRIPT
