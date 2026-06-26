#!/bin/zsh
set -euo pipefail

MAIL_ACCOUNT="谷歌"
MAILBOX="INBOX"
DAYS=2
MAX_RESULTS=60
BODY_LIMIT=2000

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mail-account)
      MAIL_ACCOUNT="$2"
      shift 2
      ;;
    --mailbox)
      MAILBOX="$2"
      shift 2
      ;;
    --days)
      DAYS="$2"
      shift 2
      ;;
    --max-results)
      MAX_RESULTS="$2"
      shift 2
      ;;
    *)
      echo "未知参数: $1" >&2
      exit 1
      ;;
  esac
done

typeset -i FETCH_LIMIT=$(( MAX_RESULTS * 5 ))
if (( FETCH_LIMIT < 120 )); then
  FETCH_LIMIT=120
fi
if (( FETCH_LIMIT > 500 )); then
  FETCH_LIMIT=500
fi

escape_applescript() {
  local value="$1"
  value="${value//\\/\\\\}"
  value="${value//\"/\\\"}"
  printf '%s' "$value"
}

ACCOUNT_ESCAPED="$(escape_applescript "$MAIL_ACCOUNT")"
typeset -a MAILBOX_CANDIDATES
MAILBOX_CANDIDATES=("$MAILBOX")
for candidate in "Inbox" "收件箱"; do
  if [[ ! " ${MAILBOX_CANDIDATES[*]} " =~ " ${candidate} " ]]; then
    MAILBOX_CANDIDATES+=("$candidate")
  fi
done

RAW_OUTPUT=""
for candidate in "${MAILBOX_CANDIDATES[@]}"; do
  MAILBOX_ESCAPED="$(escape_applescript "$candidate")"
  if RAW_OUTPUT="$(
    osascript \
      -e 'tell application "Mail"' \
      -e "set acc to account \"$ACCOUNT_ESCAPED\"" \
      -e "set mbx to mailbox \"$MAILBOX_ESCAPED\" of acc" \
      -e 'set output to ""' \
      -e 'set processedCount to 0' \
      -e 'repeat with m in messages of mbx' \
      -e "if processedCount is greater than or equal to $FETCH_LIMIT then exit repeat" \
      -e 'set msgId to (id of m) as string' \
      -e 'set subj to subject of m as string' \
      -e 'set sndr to sender of m as string' \
      -e 'set ts to (date received of m) as string' \
      -e 'set c to content of m as string' \
      -e "if (length of c) > $BODY_LIMIT then set c to text 1 thru $BODY_LIMIT of c" \
      -e "set lineText to \"$ACCOUNT_ESCAPED\" & (character id 31) & \"$MAILBOX_ESCAPED\" & (character id 31) & msgId & (character id 31) & subj & (character id 31) & sndr & (character id 31) & ts & (character id 31) & c" \
      -e 'set output to output & lineText & (character id 30)' \
      -e 'set processedCount to processedCount + 1' \
      -e 'end repeat' \
      -e 'return output' \
      -e 'end tell'
  )"; then
    break
  fi
done

printf '%s' "$RAW_OUTPUT" | python3 - "$DAYS" "$MAX_RESULTS" <<'PY'
import datetime as dt
import json
import re
import sys

days = int(sys.argv[1])
max_results = int(sys.argv[2])
raw = sys.stdin.read()

cutoff = dt.datetime.now() - dt.timedelta(days=days)
emails = []

pattern = re.compile(
    r"(?P<year>\d{4})年(?P<month>\d{1,2})月(?P<day>\d{1,2})日.*?(?P<hour>\d{1,2}):(?P<minute>\d{2})(?::(?P<second>\d{2}))?"
)

for record in raw.split("\x1e"):
    if not record.strip():
        continue
    parts = record.split("\x1f")
    if len(parts) != 7:
        continue
    account, mailbox, message_id, subject, sender, received_at_raw, body = parts
    match = pattern.search(received_at_raw.strip())
    if not match:
        continue
    values = {key: int(value) for key, value in match.groupdict(default="0").items()}
    try:
        received_at = dt.datetime(
            values["year"], values["month"], values["day"],
            values["hour"], values["minute"], values["second"]
        )
    except ValueError:
        continue
    if received_at < cutoff:
        continue
    emails.append({
        "message_id": message_id.strip(),
        "subject": subject.strip(),
        "sender": sender.strip(),
        "received_at": received_at.strftime("%Y-%m-%d %H:%M"),
        "account": account.strip(),
        "mailbox": mailbox.strip(),
        "body": body.strip(),
    })

emails.sort(key=lambda item: item["received_at"], reverse=True)
print(json.dumps({"emails": emails[:max_results]}, ensure_ascii=False, indent=2))
PY
