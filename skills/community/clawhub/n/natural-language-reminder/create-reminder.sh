#!/bin/bash
# Create a one-time reminder
# Usage: create-reminder.sh "message" "when" [--channel CHANNEL] [--to RECIPIENT]
#
# Environment variables (override defaults):
#   CLAWDBOT_DIR     Path to clawdbot directory (default: directory of this script)
#   REMINDERS_FILE   Path to reminders log file (default: ~/reminders.md)
#   TIMEZONE         Timezone for date parsing (default: system timezone)
#   CHANNEL          Delivery channel, e.g. telegram, slack (default: telegram)
#   TO               Recipient ID/address

MESSAGE="$1"
WHEN="$2"
shift 2

# Parse optional flags
CHANNEL="${CHANNEL:-telegram}"
TO="${TO:-}"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --channel) CHANNEL="$2"; shift 2 ;;
        --to)      TO="$2";      shift 2 ;;
        *) echo "Unknown option: $1" && exit 1 ;;
    esac
done

# Defaults from environment or fallback
CLAWDBOT_DIR="${CLAWDBOT_DIR:-$(cd "$(dirname "$0")" && pwd)}"
REMINDERS_FILE="${REMINDERS_FILE:-$HOME/reminders.md}"
TIMEZONE="${TIMEZONE:-$(timedatectl show -p Timezone --value 2>/dev/null || date +%Z)}"

[[ -z "$MESSAGE" ]] && echo "Error: No message provided" && exit 1
[[ -z "$WHEN" ]]    && echo "Error: No time provided" && exit 1
[[ -z "$TO" ]]      && echo "Error: No recipient provided. Set --to or TO env var" && exit 1

# Parse natural language to timestamp
parse_time() {
    local input="$1"
    local now=$(date +%s)

    # Relative times with "in X minutes/hours/days"
    if [[ "$input" =~ in[[:space:]]+([0-9]+)[[:space:]]+(minute|hour|day)s? ]]; then
        local amount="${BASH_REMATCH[1]}"
        local unit="${BASH_REMATCH[2]}"
        case "$unit" in
            minute) date -d "+${amount} minutes" --iso-8601=seconds ;;
            hour)   date -d "+${amount} hours"   --iso-8601=seconds ;;
            day)    date -d "+${amount} days"    --iso-8601=seconds ;;
        esac
        return
    fi

    # Time of day shortcuts
    case "$input" in
        "later today"|"later"|"this afternoon")
            date -d "today 17:00" --iso-8601=seconds; return ;;
        "tonight")
            date -d "today 20:00" --iso-8601=seconds; return ;;
        "tomorrow")
            date -d "tomorrow 09:00" --iso-8601=seconds; return ;;
    esac

    # Try GNU date parsing
    date -d "$input" --iso-8601=seconds 2>/dev/null
}

TIMESTAMP=$(parse_time "$WHEN")
if [[ -z "$TIMESTAMP" ]]; then
    echo "Error: Could not parse time: $WHEN"
    exit 1
fi

DISPLAY_TIME=$(date -d "$TIMESTAMP" '+%Y-%m-%d %H:%M')

# Create cron job
cd "$CLAWDBOT_DIR" || { echo "Error: CLAWDBOT_DIR not found: $CLAWDBOT_DIR"; exit 1; }

JOB_OUTPUT=$(npx tsx src/index.ts cron add \
    --name "Reminder: $MESSAGE" \
    --at "$TIMESTAMP" \
    --session isolated \
    --wake now \
    --message "⏰ Reminder: $MESSAGE" \
    --deliver \
    --channel "$CHANNEL" \
    --to "$TO" \
    --json 2>&1)

if [[ $? -ne 0 ]]; then
    echo "Error creating cron job: $JOB_OUTPUT"
    exit 1
fi

# Extract JSON from output (skip npm warnings)
JSON_OUTPUT=$(echo "$JOB_OUTPUT" | grep -A100 "^{" | grep -B100 "^}")
JOB_ID=$(echo "$JSON_OUTPUT" | jq -r '.id' 2>/dev/null)

# Log to markdown
mkdir -p "$(dirname "$REMINDERS_FILE")"
echo "- [scheduled] $DISPLAY_TIME | $MESSAGE (id: $JOB_ID)" >> "$REMINDERS_FILE"

echo "✅ Reminder set for $DISPLAY_TIME"
echo "📝 Logged to $REMINDERS_FILE"
echo "🆔 Job ID: $JOB_ID"
