#!/usr/bin/env bash
set -euo pipefail

# Habit Tracker Pro — Weekly Report Generator
# Generates a weekly habit summary with completion stats and patterns.

DATA_DIR="${HOME}/.normieclaw/habit-tracker-pro"

# Check dependencies
if ! command -v jq &> /dev/null; then
  echo "❌ jq is required. Install: brew install jq (macOS) or apt install jq (Linux)"
  exit 1
fi

if [[ ! -f "${DATA_DIR}/completions.json" ]] || [[ ! -f "${DATA_DIR}/habits.json" ]]; then
  echo "❌ Data files not found. Run setup.sh first."
  exit 1
fi

# Date calculations — last 7 days
if [[ "$(uname)" == "Darwin" ]]; then
  WEEK_START=$(date -v-7d +"%Y-%m-%d")
  WEEK_END=$(date -v-1d +"%Y-%m-%d")
  TODAY=$(date +"%Y-%m-%d")
else
  WEEK_START=$(date -d "7 days ago" +"%Y-%m-%d")
  WEEK_END=$(date -d "yesterday" +"%Y-%m-%d")
  TODAY=$(date +"%Y-%m-%d")
fi

echo "📊 Weekly Habit Report — ${WEEK_START} to ${WEEK_END}"
echo "=================================================="
echo ""

# Get active habits
ACTIVE_HABITS=$(jq -r '.habits[] | select(.active == true) | .id' "${DATA_DIR}/habits.json")
HABIT_COUNT=$(echo "$ACTIVE_HABITS" | grep -c . || true)

if [[ "$HABIT_COUNT" -eq 0 ]]; then
  echo "No active habits found. Add some habits first!"
  exit 0
fi

# Calculate overall completion rate
TOTAL_COMPLETED=0
TOTAL_SCHEDULED=0

echo "**Per-Habit Breakdown:**"
echo ""

while IFS= read -r HABIT_ID; do
  [[ -z "$HABIT_ID" ]] && continue

  HABIT_NAME=$(jq -r --arg id "$HABIT_ID" '.habits[] | select(.id == $id) | .name' "${DATA_DIR}/habits.json")

  # Count completions in the last 7 days
  COMPLETED=$(jq --arg start "$WEEK_START" --arg end "$WEEK_END" --arg id "$HABIT_ID" \
    '[.completions[] | select(.date >= $start and .date <= $end) | .entries[] | select(.habit_id == $id and .completed == true)] | length' \
    "${DATA_DIR}/completions.json" 2>/dev/null || echo "0")

  SCHEDULED=$(jq --arg start "$WEEK_START" --arg end "$WEEK_END" --arg id "$HABIT_ID" \
    '[.completions[] | select(.date >= $start and .date <= $end) | .entries[] | select(.habit_id == $id)] | length' \
    "${DATA_DIR}/completions.json" 2>/dev/null || echo "0")

  # Fallback: if no entries logged, assume 7 scheduled days
  if [[ "$SCHEDULED" -eq 0 ]]; then
    SCHEDULED=7
  fi

  if [[ "$SCHEDULED" -gt 0 ]]; then
    RATE=$(( (COMPLETED * 100) / SCHEDULED ))
  else
    RATE=0
  fi

  TOTAL_COMPLETED=$((TOTAL_COMPLETED + COMPLETED))
  TOTAL_SCHEDULED=$((TOTAL_SCHEDULED + SCHEDULED))

  # Current streak
  CURRENT_STREAK=$(jq -r --arg id "$HABIT_ID" \
    '.habits[] | select(.id == $id) | .streak.current // 0' \
    "${DATA_DIR}/habits.json" 2>/dev/null || echo "0")

  # Status indicator
  if [[ "$RATE" -ge 80 ]]; then
    INDICATOR="🟢"
  elif [[ "$RATE" -ge 50 ]]; then
    INDICATOR="🟡"
  else
    INDICATOR="🔴"
  fi

  echo "${INDICATOR} ${HABIT_NAME}: ${COMPLETED}/${SCHEDULED} (${RATE}%) — streak: ${CURRENT_STREAK} days"

done <<< "$ACTIVE_HABITS"

echo ""

# Overall rate
if [[ "$TOTAL_SCHEDULED" -gt 0 ]]; then
  OVERALL_RATE=$(( (TOTAL_COMPLETED * 100) / TOTAL_SCHEDULED ))
else
  OVERALL_RATE=0
fi

echo "**Overall: ${OVERALL_RATE}% (${TOTAL_COMPLETED}/${TOTAL_SCHEDULED} completions)**"
echo ""

# Skip reason summary
echo "**Skip Reasons This Week:**"
jq --arg start "$WEEK_START" --arg end "$WEEK_END" \
  '[.completions[] | select(.date >= $start and .date <= $end) | .entries[] | select(.completed == false and .skip_reason != null) | .skip_reason] | group_by(.) | map({reason: .[0], count: length}) | sort_by(-.count) | .[] | "  \(.reason): \(.count)"' \
  "${DATA_DIR}/completions.json" 2>/dev/null || echo "  No skip data recorded."

echo ""

# Pattern insights (if available)
if [[ -f "${DATA_DIR}/patterns.json" ]]; then
  INSIGHTS=$(jq -r '.patterns | to_entries[] | .value.insights // [] | .[]' "${DATA_DIR}/patterns.json" 2>/dev/null || true)
  if [[ -n "$INSIGHTS" ]]; then
    echo "**Pattern Insights:**"
    echo "$INSIGHTS" | while IFS= read -r insight; do
      echo "  💡 ${insight}"
    done
    echo ""
  fi
fi

echo "---"
echo "Generated: $(date +"%Y-%m-%d %H:%M %Z")"
echo "Data: ${DATA_DIR}"
