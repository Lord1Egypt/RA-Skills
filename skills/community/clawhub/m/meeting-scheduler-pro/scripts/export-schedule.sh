#!/usr/bin/env bash
set -euo pipefail

# Meeting Scheduler Pro — Export Schedule
# Exports upcoming meetings to a formatted markdown file
#
# Usage:
#   ./export-schedule.sh              # Next 7 days, output to stdout
#   ./export-schedule.sh 14           # Next 14 days
#   ./export-schedule.sh 7 /tmp/schedule.md  # Custom output path

DAYS="${1:-7}"
OUTPUT="${2:-}"

# Calculate date range
START_DATE=$(date +%Y-%m-%d)
if [[ "$(uname)" == "Darwin" ]]; then
    END_DATE=$(date -v+"${DAYS}d" +%Y-%m-%d)
else
    END_DATE=$(date -d "+${DAYS} days" +%Y-%m-%d)
fi

# Fetch events
EVENTS=$(gog calendar events list --from "$START_DATE" --to "$END_DATE" 2>/dev/null || echo "")

if [[ -z "$EVENTS" ]]; then
    echo "No meetings found for the next $DAYS days ($START_DATE to $END_DATE)."
    exit 0
fi

# Build markdown output
MARKDOWN="# Meeting Schedule: $START_DATE to $END_DATE

_Exported $(date '+%Y-%m-%d %H:%M %Z')_

---

$EVENTS

---

**Total days:** $DAYS
**Export range:** $START_DATE to $END_DATE
"

if [[ -n "$OUTPUT" ]]; then
    echo "$MARKDOWN" > "$OUTPUT"
    echo "Schedule exported to $OUTPUT"
else
    echo "$MARKDOWN"
fi
