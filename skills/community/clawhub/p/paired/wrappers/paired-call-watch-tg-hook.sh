#!/bin/bash
# paired-call-watch-tg-hook - dual-mode incoming call handler.
#
# Receives BTCALL_* env vars from paired-call-watch parent.
# Logs to ${PAIRED_DATA_DIR}/call-hook.log.
#
# Workflow:
#   1. Always send Telegram notification (current behavior preserved)
#   2. If caller is on the trusted-numbers list, also invoke
#      paired-call-handler which hangs up + sends an auto-SMS reply
#
# Exit code controls paired-call-watch decision:
#   0 = answer the call (we never use this — SCO audio blocked)
#   1 = ignore (default - let it ring on phone, OR caller already hung up)
#   2 = hang up immediately
#
# Trust list: ${HOME}/.config/paired/trusted-numbers.conf
# Edit with: paired-trusted add 07XXX [name]

set -u
LOG="${HOME}/bt-skill-expansion/call-hook.log"
CFG="${HOME}/.config/paired-sms-watch/telegram.env"
TRUSTED_LIST="${HOME}/.config/paired/trusted-numbers.conf"
HANDLER="${HOME}/bin/paired-call-handler"
mkdir -p "$(dirname "$LOG")"

if [ ! -r "$CFG" ]; then
    echo "$(date -Iseconds) ERROR: config not readable: $CFG" >> "$LOG"
    exit 1
fi
. "$CFG"

if [ -z "${TG_BOT_TOKEN:-}" ] || [ -z "${TG_CHAT_ID:-}" ]; then
    echo "$(date -Iseconds) ERROR: TG_BOT_TOKEN or TG_CHAT_ID not set" >> "$LOG"
    exit 1
fi

NUMBER="${BTCALL_NUMBER:-?}"
NAME="${BTCALL_NAME:-}"
TS="${BTCALL_TIMESTAMP:-?}"
TYPE="${BTCALL_TYPE:-?}"

# Normalize for trusted-list comparison (UK format -> 07...)
NORM=""
if [ -n "$NUMBER" ] && [ "$NUMBER" != "?" ]; then
    NORM=$(echo "$NUMBER" | tr -d ' -' | sed -E 's/^\+44/0/; s/^0044/0/; s/^44(.{10})$/0\1/')
fi

# Is this number trusted? Read the file, strip comments, normalize each line.
IS_TRUSTED="no"
if [ -n "$NORM" ] && [ -r "$TRUSTED_LIST" ]; then
    while IFS= read -r line; do
        # Strip comment + whitespace
        clean=$(echo "$line" | sed 's/#.*$//' | tr -d '[:space:]')
        [ -z "$clean" ] && continue
        norm_line=$(echo "$clean" | sed -E 's/^\+44/0/; s/^0044/0/; s/^44(.{10})$/0\1/')
        if [ "$norm_line" = "$NORM" ]; then
            IS_TRUSTED="yes"
            break
        fi
    done < "$TRUSTED_LIST"
fi

PRETTY_TS=""
if [[ "$TS" =~ ^[0-9]{8}T[0-9]{6}$ ]]; then
    HOUR="${TS:9:2}"
    MIN="${TS:11:2}"
    PRETTY_TS=" at ${HOUR}:${MIN}"
fi

WHO="${NAME:-$NUMBER}"
[ -n "$NAME" ] && [ "$NAME" != "$NUMBER" ] && WHO="${NAME} (${NUMBER})"

# Branch on trust
if [ "$IS_TRUSTED" = "yes" ] && [ "$TYPE" = "incoming" ]; then
    echo "$(date -Iseconds) TRUSTED caller ${NORM}: invoking handler for hangup+auto-SMS" >> "$LOG"
    # Pass BTCALL_* env vars through
    if [ -x "$HANDLER" ]; then
        "$HANDLER" >> "$LOG" 2>&1
        HANDLER_RC=$?
        echo "$(date -Iseconds) handler returned ${HANDLER_RC}" >> "$LOG"
    else
        echo "$(date -Iseconds) ERROR: handler not executable: $HANDLER" >> "$LOG"
        # Fall through to basic Telegram notification
    fi
    # Handler already posted its own Telegram alert; don't double-notify
    exit 1
fi

# Untrusted (or non-incoming): basic Telegram notification only
TEXT_RAW="$(printf '📞 Incoming call%s\nFrom: %s' "$PRETTY_TS" "$WHO")"
TEXT_JSON=$(python3 -c "import sys, json; print(json.dumps(sys.argv[1]))" "$TEXT_RAW")

RESPONSE=$(curl -sS -m 10 \
    -X POST "https://api.telegram.org/bot${TG_BOT_TOKEN}/sendMessage" \
    -H "Content-Type: application/json" \
    -d "{\"chat_id\": ${TG_CHAT_ID}, \"text\": ${TEXT_JSON}}" 2>&1)

OK=$(echo "$RESPONSE" | python3 -c "import sys,json
try: print(json.loads(sys.stdin.read()).get('ok', False))
except: print('parse-fail')" 2>/dev/null)

if [ "$OK" = "True" ]; then
    echo "$(date -Iseconds) OK: notified about untrusted call from ${WHO}" >> "$LOG"
else
    echo "$(date -Iseconds) FAIL: response=${RESPONSE:0:200}" >> "$LOG"
fi

exit 1
