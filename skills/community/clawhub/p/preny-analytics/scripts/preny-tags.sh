#!/bin/bash
# Preny Analytics - Tag Statistics
# Usage: preny-tags [period]

set -e

API_URL="${PRENY_API_URL:-https://api-production.prenychatbot.ai/api/v1/statistics/tag-attributes}"
TOKEN="${PRENY_TOKEN}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check token
if [ -z "$TOKEN" ]; then
    echo -e "${RED}Lỗi: Chưa cấu hình PRENY_TOKEN${NC}"
    exit 1
fi

# Date helpers
get_today_range() {
    local today=$(date -u +"%Y-%m-%d")
    echo "${today}T00:00:00.000Z ${today}T23:59:59.000Z"
}

get_week_range() {
    local to=$(date -u +"%Y-%m-%dT23:59:59.000Z")
    local from=$(date -u -d "7 days ago" +"%Y-%m-%dT00:00:00.000Z")
    echo "$from $to"
}

get_month_range() {
    local to=$(date -u +"%Y-%m-%dT23:59:59.000Z")
    local from=$(date -u -d "30 days ago" +"%Y-%m-%dT00:00:00.000Z")
    echo "$from $to"
}

# Call API
call_api() {
    local from="$1"
    local to="$2"
    
    curl -s "${API_URL}?from=${from}&to=${to}&skip=0&limit=50&sort=-1&type=status" \
        -H 'Accept: application/json' \
        -H "Authorization: Bearer ${TOKEN}"
}

# Format number
fmt() {
    printf "%'d" "$1" 2>/dev/null || echo "$1"
}

# Display tags
display_tags() {
    local response="$1"
    local period="$2"
    
    if echo "$response" | jq -e '.systemCode != "ACC_0000"' > /dev/null 2>&1; then
        echo -e "${RED}Lỗi API${NC}"
        return 1
    fi
    
    local list=$(echo "$response" | jq '.data.listData')
    local total=$(echo "$response" | jq '.data.total')
    
    echo ""
    echo -e "${BLUE}🏷️ THỐNG KÊ TAG KHÁCH HÀNG - ${period}${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Sort by totalConversation descending
    echo "$list" | jq -r 'sort_by(-.totalConversation) | .[] | "\(.name)|\(.totalConversation)|\(.color)"' | \
    while IFS='|' read name count color; do
        local bar=""
        local num=$((count / 10))
        for ((i=0; i<num && i<20; i++)); do bar+="█"; done
        printf "   %-20s %5s  %s\n" "$name" "$(fmt $count)" "$bar"
    done
    
    echo ""
    echo "   Tổng: $total tags"
    echo ""
}

# Main
PERIOD="${1:-week}"

case "$PERIOD" in
    today)
        read FROM TO <<< $(get_today_range)
        display_tags "$(call_api "$FROM" "$TO")" "HÔM NAY"
        ;;
    week)
        read FROM TO <<< $(get_week_range)
        display_tags "$(call_api "$FROM" "$TO")" "7 NGÀY QUA"
        ;;
    month)
        read FROM TO <<< $(get_month_range)
        display_tags "$(call_api "$FROM" "$TO")" "30 NGÀY QUA"
        ;;
    *)
        echo "Usage: preny-tags [today|week|month]"
        ;;
esac
