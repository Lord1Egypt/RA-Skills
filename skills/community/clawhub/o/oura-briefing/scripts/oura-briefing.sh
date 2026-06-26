#!/usr/bin/env bash
# oura-briefing.sh — Fetch and summarize Oura Ring v2 data
# Usage: oura-briefing.sh [--date YYYY-MM-DD] [--json] [--wake-check] [--token TOKEN]
set -euo pipefail

DATE=$(date +%Y-%m-%d)
YESTERDAY=$(date -v-1d +%Y-%m-%d 2>/dev/null || date -d "yesterday" +%Y-%m-%d)
JSON_MODE=0
WAKE_CHECK=0
TOKEN="${OURA_API_TOKEN:-}"

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --date) DATE="$2"; YESTERDAY="$2"; shift 2 ;;
    --json) JSON_MODE=1; shift ;;
    --wake-check) WAKE_CHECK=1; shift ;;
    --token) TOKEN="$2"; shift 2 ;;
    *) shift ;;
  esac
done

# Sleep is filed under the day the session starts; fetch a window around the target date
SLEEP_START=$(date -v-1d -j -f "%Y-%m-%d" "$DATE" +%Y-%m-%d 2>/dev/null || date -d "$DATE -1 day" +%Y-%m-%d)
SLEEP_END="$DATE"

if [[ -z "$TOKEN" ]]; then
  echo "ERROR: OURA_API_TOKEN not set. Set env var or pass --token." >&2
  exit 1
fi

API="https://api.ouraring.com/v2/usercollection"
HDR="Authorization: Bearer $TOKEN"

# Fetch data
SLEEP=$(curl -sf "$API/sleep?start_date=$SLEEP_START&end_date=$SLEEP_END" -H "$HDR" || echo '{"data":[]}')
READINESS=$(curl -sf "$API/daily_readiness?start_date=$DATE&end_date=$DATE" -H "$HDR" || echo '{"data":[]}')
ACTIVITY=$(curl -sf "$API/daily_activity?start_date=$DATE&end_date=$DATE" -H "$HDR" || echo '{"data":[]}')

if [[ $JSON_MODE -eq 1 ]]; then
  jq -n \
    --argjson sleep "$SLEEP" \
    --argjson readiness "$READINESS" \
    --argjson activity "$ACTIVITY" \
    '{sleep: $sleep, readiness: $readiness, activity: $activity}'
  exit 0
fi

# Extract key metrics — use jq selectors directly on the raw JSON
if [[ $WAKE_CHECK -eq 1 ]]; then
  WAKE_TIME=$(echo "$SLEEP" | jq -r '[.data[] | select(.type == "long_sleep")] | sort_by(.bedtime_end) | last | .bedtime_end // empty' 2>/dev/null)
  if [[ -n "$WAKE_TIME" && "$WAKE_TIME" != "null" ]]; then
    echo "wake_confirmed: $WAKE_TIME"
    exit 0
  else
    echo "not_awake_yet"
    exit 1
  fi
fi

# Sleep metrics (pull from most recent long_sleep in window)
SLEEP_SCORE=$(echo "$SLEEP" | jq -r '[.data[] | select(.type == "long_sleep")] | sort_by(.bedtime_end) | last | .score // "N/A"' 2>/dev/null)
[[ -z "$SLEEP_SCORE" || "$SLEEP_SCORE" == "null" ]] && SLEEP_SCORE="N/A"

TOTAL_SLEEP_SEC=$(echo "$SLEEP" | jq -r '[.data[] | select(.type == "long_sleep")] | sort_by(.bedtime_end) | last | .total_sleep_duration // 0' 2>/dev/null)
TOTAL_H=$((TOTAL_SLEEP_SEC / 3600))
TOTAL_M=$(( (TOTAL_SLEEP_SEC % 3600) / 60 ))

EFFICIENCY=$(echo "$SLEEP" | jq -r '[.data[] | select(.type == "long_sleep")] | sort_by(.bedtime_end) | last | .efficiency // "N/A"' 2>/dev/null)
REM_SEC=$(echo "$SLEEP" | jq -r '[.data[] | select(.type == "long_sleep")] | sort_by(.bedtime_end) | last | .rem_sleep_duration // 0' 2>/dev/null)
DEEP_SEC=$(echo "$SLEEP" | jq -r '[.data[] | select(.type == "long_sleep")] | sort_by(.bedtime_end) | last | .deep_sleep_duration // 0' 2>/dev/null)
REM_H=$((REM_SEC / 3600)); REM_M=$(( (REM_SEC % 3600) / 60 ))
DEEP_H=$((DEEP_SEC / 3600)); DEEP_M=$(( (DEEP_SEC % 3600) / 60 ))

BEDTIME_START=$(echo "$SLEEP" | jq -r '[.data[] | select(.type == "long_sleep")] | sort_by(.bedtime_end) | last | .bedtime_start // "N/A"' 2>/dev/null | sed 's/T/ /' | sed 's/\.[0-9]*//' | sed 's/-0[45]:00//')
BEDTIME_END=$(echo "$SLEEP" | jq -r '[.data[] | select(.type == "long_sleep")] | sort_by(.bedtime_end) | last | .bedtime_end // "N/A"' 2>/dev/null | sed 's/T/ /' | sed 's/\.[0-9]*//' | sed 's/-0[45]:00//')
HRV_AVG=$(echo "$SLEEP" | jq -r '[.data[] | select(.type == "long_sleep")] | sort_by(.bedtime_end) | last | .average_hrv // "N/A"' 2>/dev/null)
RESTING_HR=$(echo "$SLEEP" | jq -r '[.data[] | select(.type == "long_sleep")] | sort_by(.bedtime_end) | last | .lowest_heart_rate // "N/A"' 2>/dev/null)

# Readiness metrics
READINESS_SCORE=$(echo "$READINESS" | jq -r '.data[0].score // "N/A"' 2>/dev/null)
HRV_BALANCE=$(echo "$READINESS" | jq -r '.data[0].contributors.hrv_balance // "N/A"' 2>/dev/null)
BODY_TEMP=$(echo "$READINESS" | jq -r '.data[0].temperature_deviation // "N/A"' 2>/dev/null)

# Activity metrics
ACTIVITY_SCORE=$(echo "$ACTIVITY" | jq -r '.data[0].score // "N/A"' 2>/dev/null)
STEPS=$(echo "$ACTIVITY" | jq -r '.data[0].steps // "N/A"' 2>/dev/null)
ACTIVE_CAL=$(echo "$ACTIVITY" | jq -r '.data[0].active_calories // "N/A"' 2>/dev/null)

# Print briefing
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌙 OURA BRIEFING — $DATE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💤 SLEEP"
echo "  Score:      ${SLEEP_SCORE}/100"
echo "  Total:      ${TOTAL_H}h ${TOTAL_M}m"
echo "  Efficiency: ${EFFICIENCY}%"
echo "  REM:        ${REM_H}h ${REM_M}m"
echo "  Deep:       ${DEEP_H}h ${DEEP_M}m"
echo "  Bedtime:    ${BEDTIME_START} → ${BEDTIME_END}"
echo "  HRV avg:    ${HRV_AVG} ms"
echo "  Resting HR: ${RESTING_HR} bpm"
echo ""
echo "⚡ READINESS"
echo "  Score:      ${READINESS_SCORE}/100"
echo "  HRV bal:    ${HRV_BALANCE}/100"
echo "  Body temp:  ${BODY_TEMP}°C deviation"
echo ""
echo "🏃 ACTIVITY"
echo "  Score:      ${ACTIVITY_SCORE}/100"
echo "  Steps:      ${STEPS}"
echo "  Active cal: ${ACTIVE_CAL} kcal"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
