#!/bin/bash
# paired-sms-watch-tg-hook - sends a Telegram alert when paired-sms-watch fires.
# Reads token + chat_id from ~/.config/paired-sms-watch/telegram.env (mode 600).
# Receives BTSMS_* env vars from paired-sms-watch parent.
# Logs to ${PAIRED_DATA_DIR}/sms-hook.log.
#
# Special handling: if SMS body starts with "Hi Agent," AND sender is whitelisted,
# delegate to paired-respond which composes a richer Gemini-drafted alert.

set -u
LOG="${HOME}/bt-skill-expansion/sms-hook.log"
CFG="${HOME}/.config/paired-sms-watch/telegram.env"
mkdir -p "$(dirname "$LOG")"

if [ ! -r "$CFG" ]; then
    echo "$(date -Iseconds) ERROR: config not readable: $CFG" >> "$LOG"
    exit 2
fi
. "$CFG"

if [ -z "${TG_BOT_TOKEN:-}" ] || [ -z "${TG_CHAT_ID:-}" ]; then
    echo "$(date -Iseconds) ERROR: TG_BOT_TOKEN or TG_CHAT_ID not set" >> "$LOG"
    exit 3
fi

# Check for "Hi Agent," trigger - delegate to paired-respond which handles
# whitelist check + Gemini call + Telegram alert. We still send the basic
# notification too, so user always sees the SMS arrive.
BODY="${BTSMS_SUBJECT:-}"
PAIRED_TRIGGERED=0
if echo "$BODY" | grep -qiE "^[[:space:]]*hi[[:space:]]+paired[[:space:]]*[,:!\.]?[[:space:]]*"; then
    if [ -x "${HOME}/bin/paired-respond" ]; then
        # Run in background so we don't block the basic notification
        # but capture exit so we know if it fired
        ("${HOME}/bin/paired-respond" >> "$LOG" 2>&1 &)
        PAIRED_TRIGGERED=1
        echo "$(date -Iseconds) Agent trigger matched body='${BODY:0:60}', delegated to paired-respond" >> "$LOG"
    fi
fi

# Always send the basic "📩 New SMS" alert too
SENDER="${BTSMS_SENDER:-?}"
ADDR="${BTSMS_SENDER_ADDR:-?}"
SUBJECT="${BTSMS_SUBJECT:-(empty)}"
TS="${BTSMS_TIMESTAMP:-?}"
TYPE="${BTSMS_TYPE:-sms}"

case "$TYPE" in
  sms-gsm) TYPE_LBL="SMS" ;;
  mms)     TYPE_LBL="MMS" ;;
  *)       TYPE_LBL="$TYPE" ;;
esac

PRETTY_TS=""
if [[ "$TS" =~ ^[0-9]{8}T[0-9]{6}$ ]]; then
    HOUR="${TS:9:2}"
    MIN="${TS:11:2}"
    PRETTY_TS=" at ${HOUR}:${MIN}"
fi

TEXT_RAW="$(printf '📩 New %s%s\nFrom: %s (%s)\n\n%s' \
    "$TYPE_LBL" "$PRETTY_TS" "$SENDER" "$ADDR" "$SUBJECT")"
TEXT_JSON=$(python3 -c "import sys, json; print(json.dumps(sys.argv[1]))" "$TEXT_RAW")

RESPONSE=$(curl -sS -m 10 \
    -X POST "https://api.telegram.org/bot${TG_BOT_TOKEN}/sendMessage" \
    -H "Content-Type: application/json" \
    -d "{\"chat_id\": ${TG_CHAT_ID}, \"text\": ${TEXT_JSON}, \"disable_notification\": false}" \
    2>&1)

OK=$(echo "$RESPONSE" | python3 -c "import sys,json
try: print(json.loads(sys.stdin.read()).get('ok', False))
except: print('parse-fail')" 2>/dev/null)

if [ "$OK" = "True" ]; then
    if [ "$PAIRED_TRIGGERED" = "1" ]; then
        echo "$(date -Iseconds) OK: basic notif + Agent delegate fired: ${TEXT_RAW:0:80}..." >> "$LOG"
    else
        echo "$(date -Iseconds) OK: sent to chat ${TG_CHAT_ID}: ${TEXT_RAW:0:80}..." >> "$LOG"
    fi
    exit 0
else
    echo "$(date -Iseconds) FAIL: response=${RESPONSE:0:200}" >> "$LOG"
    exit 1
fi
