#!/bin/bash
# Weekly report script
# Usage: ./weekly_report.sh

MEMORY_DIR="/root/.openclaw/workspace/memory"
TARGET=2100
DAYS="${1:-7}"
YEAR="${2:-$(date +%Y)}"

if ! [[ "$DAYS" =~ ^[0-9]+$ ]] || [ "$DAYS" -lt 1 ]; then
  echo "Usage: $0 <days(>=1)> [year]"
  exit 1
fi

echo "📊 Calorie tracking for the last ${DAYS} days"
echo "═══════════════════════════════"
echo "Target: ${TARGET} kcal/day"
echo ""

for i in $(seq 0 $((DAYS - 1))); do
    DATE=$(date -d "$i days ago" +"%m-%d")
    FILE="${MEMORY_DIR}/${YEAR}-${DATE}.md"
    
    if [ -f "$FILE" ]; then
        # Extract lunch and dinner data
        LUNCH=$(grep -A20 "午餐" "$FILE" | grep "小计" | awk '{print $3}' | tr -d '~' | tr -d 'kcal')
        DINNER=$(grep -A10 "晚餐" "$FILE" | grep -E "^[|]" | tail -1 | awk -F'|' '{print $4}' | tr -d ' ')
        
        # Show "Missing" if records are absent
        [ -z "$LUNCH" ] && LUNCH="Missing"
        [ -z "$DINNER" ] && DINNER="Missing"
        
        echo "$DATE  Lunch $LUNCH  Dinner $DINNER"
    else
        echo "$DATE  No record"
    fi
done
