#!/bin/bash
# Create a recurring reminder
# Usage: create-recurring.sh "message" "schedule" [--channel CHANNEL] [--to RECIPIENT]

# Load skill config (external env vars override config.env)
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
[[ -f "$SKILL_DIR/config.env" ]] && source "$SKILL_DIR/config.env"

MESSAGE="$1"
SCHEDULE="$2"
shift 2

# Parse optional flags
while [[ $# -gt 0 ]]; do
    case "$1" in
        --channel) CHANNEL="$2"; shift 2 ;;
        --to)      TO="$2";      shift 2 ;;
        *) echo "Unknown option: $1" && exit 1 ;;
    esac
done

# Fallbacks if not set in config.env or flags
CHANNEL="${CHANNEL:-telegram}"
REMINDERS_FILE="${REMINDERS_FILE:-$HOME/reminders.md}"
TIMEZONE="${TIMEZONE:-$(timedatectl show -p Timezone --value 2>/dev/null || date +%Z)}"

[[ -z "$MESSAGE" ]]  && echo "Error: No message provided" && exit 1
[[ -z "$SCHEDULE" ]] && echo "Error: No schedule provided" && exit 1
[[ -z "$TO" ]]       && echo "Error: No recipient provided. Set TO in config.env or pass --to" && exit 1

# Parse schedule to cron expression or duration
parse_schedule() {
    local input="$1"

    # Every X minutes/hours
    if [[ "$input" =~ every[[:space:]]+([0-9]+)[[:space:]]+(minute|hour)s? ]]; then
        local amount="${BASH_REMATCH[1]}"
        local unit="${BASH_REMATCH[2]}"
        case "$unit" in
            minute) echo "duration:${amount}m" ;;
            hour)   echo "duration:${amount}h" ;;
        esac
        return
    fi

    # Daily at specific time
    if [[ "$input" =~ (daily|every[[:space:]]+day)[[:space:]]+at[[:space:]]+([0-9]{1,2})(:[0-9]{2})?(am|pm)? ]]; then
        local hour="${BASH_REMATCH[2]}"
        local minute="${BASH_REMATCH[3]:-:00}"
        local ampm="${BASH_REMATCH[4]}"
        minute="${minute#:}"

        if [[ "$ampm" == "pm" ]] && [[ $hour -lt 12 ]]; then hour=$((hour + 12))
        elif [[ "$ampm" == "am" ]] && [[ $hour -eq 12 ]]; then hour=0; fi

        echo "cron:$minute $hour * * *"
        return
    fi

    # Weekday at time (e.g., "every Monday at 2pm")
    if [[ "$input" =~ every[[:space:]]+(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)[[:space:]]+at[[:space:]]+([0-9]{1,2})(:[0-9]{2})?(am|pm)? ]]; then
        local day="${BASH_REMATCH[1]}"
        local hour="${BASH_REMATCH[2]}"
        local minute="${BASH_REMATCH[3]:-:00}"
        local ampm="${BASH_REMATCH[4]}"
        minute="${minute#:}"

        if [[ "$ampm" == "pm" ]] && [[ $hour -lt 12 ]]; then hour=$((hour + 12))
        elif [[ "$ampm" == "am" ]] && [[ $hour -eq 12 ]]; then hour=0; fi

        local dow
        case "$day" in
            Sunday)    dow=0 ;; Monday)    dow=1 ;; Tuesday)   dow=2 ;;
            Wednesday) dow=3 ;; Thursday)  dow=4 ;; Friday)    dow=5 ;; Saturday)  dow=6 ;;
        esac

        echo "cron:$minute $hour * * $dow"
        return
    fi

    # Weekly (defaults to Monday 9am)
    if [[ "$input" =~ ^weekly$ ]]; then
        echo "cron:0 9 * * 1"
        return
    fi

    echo "error"
}

PARSED=$(parse_schedule "$SCHEDULE")
if [[ "$PARSED" == "error" ]]; then
    echo "Error: Could not parse schedule: $SCHEDULE"
    exit 1
fi

if [[ "$PARSED" =~ ^duration:(.+)$ ]]; then
    DURATION="${BASH_REMATCH[1]}"
    JOB_OUTPUT=$(openclaw cron add \
        --name "Recurring: $MESSAGE" \
        --every "$DURATION" \
        --session isolated \
        --wake now \
        --message "⏰ $MESSAGE" \
        --deliver \
        --channel "$CHANNEL" \
        --to "$TO" \
        --json 2>&1)
    SCHEDULE_DISPLAY="every $DURATION"
elif [[ "$PARSED" =~ ^cron:(.+)$ ]]; then
    CRON_EXPR="${BASH_REMATCH[1]}"
    JOB_OUTPUT=$(openclaw cron add \
        --name "Recurring: $MESSAGE" \
        --cron "$CRON_EXPR" \
        --tz "$TIMEZONE" \
        --session isolated \
        --wake now \
        --message "⏰ $MESSAGE" \
        --deliver \
        --channel "$CHANNEL" \
        --to "$TO" \
        --json 2>&1)
    SCHEDULE_DISPLAY="cron: $CRON_EXPR"
fi

if [[ $? -ne 0 ]]; then
    echo "Error creating cron job: $JOB_OUTPUT"
    exit 1
fi

JSON_OUTPUT=$(echo "$JOB_OUTPUT" | grep -A100 "^{" | grep -B100 "^}")
JOB_ID=$(echo "$JSON_OUTPUT" | jq -r '.id' 2>/dev/null)

mkdir -p "$(dirname "$REMINDERS_FILE")"
echo "- [recurring] $SCHEDULE_DISPLAY | $MESSAGE (id: $JOB_ID)" >> "$REMINDERS_FILE"

echo "✅ Recurring reminder set: $SCHEDULE_DISPLAY"
echo "📝 Logged to $REMINDERS_FILE"
echo "🆔 Job ID: $JOB_ID"
