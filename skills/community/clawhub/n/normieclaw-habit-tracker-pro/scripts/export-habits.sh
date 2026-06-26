#!/usr/bin/env bash
set -euo pipefail

# Habit Tracker Pro — Export Script
# Exports habit data to CSV and markdown formats.

DATA_DIR="${HOME}/.normieclaw/habit-tracker-pro"
EXPORTS_DIR="${DATA_DIR}/exports"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Check dependencies
if ! command -v jq &> /dev/null; then
  echo "❌ jq is required. Install: brew install jq (macOS) or apt install jq (Linux)"
  exit 1
fi

# Check data directory
if [[ ! -d "$DATA_DIR" ]]; then
  echo "❌ Data directory not found: ${DATA_DIR}"
  echo "   Run setup.sh first."
  exit 1
fi

mkdir -p "$EXPORTS_DIR"

echo "🦬 Habit Tracker Pro — Export"
echo "----------------------------"

# --- Export habits to CSV ---
HABITS_CSV="${EXPORTS_DIR}/habits_${TIMESTAMP}.csv"
echo "id,name,category,frequency_type,time_preference,current_streak,longest_streak,active,created_at" > "$HABITS_CSV"

if [[ -f "${DATA_DIR}/habits.json" ]]; then
  jq -r '.habits[] | [
    .id,
    .name,
    .category,
    .frequency.type,
    .time_preference,
    (.streak.current // 0),
    (.streak.longest // 0),
    .active,
    .created_at
  ] | @csv' "${DATA_DIR}/habits.json" >> "$HABITS_CSV" 2>/dev/null || true
fi

HABIT_COUNT=$(tail -n +2 "$HABITS_CSV" | wc -l | tr -d ' ')
echo "✅ Exported ${HABIT_COUNT} habits → ${HABITS_CSV}"

# --- Export completions to CSV ---
COMPLETIONS_CSV="${EXPORTS_DIR}/completions_${TIMESTAMP}.csv"
echo "date,habit_id,completed,source,skip_reason,note,logged_at" > "$COMPLETIONS_CSV"

if [[ -f "${DATA_DIR}/completions.json" ]]; then
  jq -r '.completions[] | .date as $date | .entries[] | [
    $date,
    .habit_id,
    .completed,
    (.source // ""),
    (.skip_reason // ""),
    (.note // "" | gsub("\n"; " ")),
    (.logged_at // "")
  ] | @csv' "${DATA_DIR}/completions.json" >> "$COMPLETIONS_CSV" 2>/dev/null || true
fi

COMPLETION_COUNT=$(tail -n +2 "$COMPLETIONS_CSV" | wc -l | tr -d ' ')
echo "✅ Exported ${COMPLETION_COUNT} completion entries → ${COMPLETIONS_CSV}"

# --- Export summary as markdown ---
SUMMARY_MD="${EXPORTS_DIR}/summary_${TIMESTAMP}.md"

cat > "$SUMMARY_MD" << EOF
# Habit Tracker Pro — Data Export
**Exported:** $(date +"%Y-%m-%d %H:%M:%S %Z")

## Habits (${HABIT_COUNT})

EOF

if [[ -f "${DATA_DIR}/habits.json" ]]; then
  jq -r '.habits[] | "### \(.name)\n- **ID:** \(.id)\n- **Category:** \(.category)\n- **Frequency:** \(.frequency.type)\n- **Time:** \(.time_preference)\n- **Current Streak:** \(.streak.current // 0) days\n- **Longest Streak:** \(.streak.longest // 0) days\n- **Active:** \(.active)\n- **Created:** \(.created_at)\n"' \
    "${DATA_DIR}/habits.json" >> "$SUMMARY_MD" 2>/dev/null || true
fi

# Add streaks section
if [[ -f "${DATA_DIR}/streaks.json" ]]; then
  echo "## Streak Data" >> "$SUMMARY_MD"
  echo "" >> "$SUMMARY_MD"
  jq -r 'to_entries[] | select(.key != "version") | "- **\(.key):** \(.value | tostring)"' \
    "${DATA_DIR}/streaks.json" >> "$SUMMARY_MD" 2>/dev/null || true
  echo "" >> "$SUMMARY_MD"
fi

# Add patterns section
if [[ -f "${DATA_DIR}/patterns.json" ]]; then
  PATTERN_COUNT=$(jq '.patterns | keys | length' "${DATA_DIR}/patterns.json" 2>/dev/null || echo "0")
  if [[ "$PATTERN_COUNT" -gt 0 ]]; then
    echo "## Pattern Insights" >> "$SUMMARY_MD"
    echo "" >> "$SUMMARY_MD"
    jq -r '.patterns | to_entries[] | "### \(.key)\n\(.value.insights // [] | map("- \(.)") | join("\n"))\n"' \
      "${DATA_DIR}/patterns.json" >> "$SUMMARY_MD" 2>/dev/null || true
  fi
fi

echo "✅ Exported summary → ${SUMMARY_MD}"

echo ""
echo "📁 All exports in: ${EXPORTS_DIR}"
echo "   habits_${TIMESTAMP}.csv"
echo "   completions_${TIMESTAMP}.csv"
echo "   summary_${TIMESTAMP}.md"
