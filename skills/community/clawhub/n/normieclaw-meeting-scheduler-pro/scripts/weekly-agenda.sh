#!/usr/bin/env bash
set -euo pipefail

# Meeting Scheduler Pro — Weekly Agenda Generator
# Generates a week-ahead meeting prep document
#
# Usage:
#   ./weekly-agenda.sh                  # Next Monday–Friday
#   ./weekly-agenda.sh 2026-03-23       # Specific week start (Monday)
#   ./weekly-agenda.sh 2026-03-23 /tmp/weekly.md  # Custom output

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG="$PACKAGE_DIR/config/settings.json"

# Determine week start
if [[ -n "${1:-}" ]]; then
    WEEK_START="$1"
else
    # Calculate next Monday
    DOW=$(date +%u)  # 1=Monday, 7=Sunday
    if [[ "$(uname)" == "Darwin" ]]; then
        DAYS_UNTIL_MONDAY=$(( (8 - DOW) % 7 ))
        [[ $DAYS_UNTIL_MONDAY -eq 0 ]] && DAYS_UNTIL_MONDAY=7
        WEEK_START=$(date -v+"${DAYS_UNTIL_MONDAY}d" +%Y-%m-%d)
    else
        DAYS_UNTIL_MONDAY=$(( (8 - DOW) % 7 ))
        [[ $DAYS_UNTIL_MONDAY -eq 0 ]] && DAYS_UNTIL_MONDAY=7
        WEEK_START=$(date -d "+${DAYS_UNTIL_MONDAY} days" +%Y-%m-%d)
    fi
fi

# Calculate week end (Friday)
if [[ "$(uname)" == "Darwin" ]]; then
    WEEK_END=$(date -j -f "%Y-%m-%d" "$WEEK_START" -v+4d +%Y-%m-%d)
else
    WEEK_END=$(date -d "$WEEK_START + 4 days" +%Y-%m-%d)
fi

OUTPUT="${2:-}"

echo "Generating weekly agenda: $WEEK_START to $WEEK_END"
echo ""

# Fetch events for the week
EVENTS=$(gog calendar events list --from "$WEEK_START" --to "$WEEK_END" 2>/dev/null || echo "")

# Read settings
TIMEZONE="America/New_York"
MAX_MEETINGS=6
if [[ -f "$CONFIG" ]]; then
    TIMEZONE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['availability']['working_hours']['timezone'])" 2>/dev/null || echo "America/New_York")
    MAX_MEETINGS=$(python3 -c "import json; print(json.load(open('$CONFIG'))['availability']['max_meetings_per_day'])" 2>/dev/null || echo "6")
fi

# Count meetings per day
MEETING_COUNT=0
if [[ -n "$EVENTS" ]]; then
    MEETING_COUNT=$(echo "$EVENTS" | grep -c "^" || echo "0")
fi

# Build the report
REPORT="# Weekly Meeting Agenda

**Week of:** $WEEK_START to $WEEK_END
**Generated:** $(date '+%Y-%m-%d %H:%M %Z')
**Timezone:** $TIMEZONE

---

## Overview

**Total meetings this week:** $MEETING_COUNT
**Daily limit:** $MAX_MEETINGS

---

## Schedule

$EVENTS

---

## Prep Needed

Review each meeting above and generate prep briefs. For each meeting:
1. Who are you meeting with? (role, company, last interaction)
2. What's the purpose? (from event title/description)
3. What happened last time? (check meeting-notes/ directory)
4. Any open action items from previous meetings?

---

## Calendar Health

- Check for back-to-back meetings without buffers
- Verify no meetings in protected time blocks
- Confirm daily meeting counts are under the limit ($MAX_MEETINGS)

---

_Run this through your agent for full prep briefs: \"Prep me for next week's meetings.\"_
"

if [[ -n "$OUTPUT" ]]; then
    echo "$REPORT" > "$OUTPUT"
    echo "Weekly agenda saved to $OUTPUT"
else
    echo "$REPORT"
fi
