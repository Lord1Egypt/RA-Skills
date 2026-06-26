#!/bin/bash
# Preny Analytics - Real API Integration
# Usage: preny-stats [today|yesterday|week|month|from to]

set -e

API_URL="${PRENY_API_URL:-https://api-production.prenychatbot.ai/api/v1/statistics/stats}"
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
    echo ""
    echo "Cách lấy token:"
    echo "1. Đăng nhập https://app.preny.ai"
    echo "2. Mở DevTools (F12) → Network"
    echo "3. Copy token từ header Authorization: Bearer xxx"
    echo "4. export PRENY_TOKEN=\"your-token\""
    exit 1
fi

# Date helpers
get_today_range() {
    local today=$(date -u +"%Y-%m-%d")
    local from="${today}T00:00:00.000Z"
    local to="${today}T23:59:59.000Z"
    echo "$from $to"
}

get_yesterday_range() {
    local yesterday=$(date -u -d "yesterday" +"%Y-%m-%d")
    local from="${yesterday}T00:00:00.000Z"
    local to="${yesterday}T23:59:59.000Z"
    echo "$from $to"
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

# Call Preny API
call_api() {
    local from="$1"
    local to="$2"
    local limit="${3:-30}"
    
    curl -s "${API_URL}?from=${from}&to=${to}&skip=0&limit=${limit}&sort=-1&type=interact" \
        -H 'Accept: application/json' \
        -H "Authorization: Bearer ${TOKEN}" \
        -H 'Content-Type: application/json'
}

# Format number
fmt() {
    printf "%'d" "$1" 2>/dev/null || echo "$1"
}

# Display stats
display_stats() {
    local response="$1"
    local period="$2"
    
    # Check error
    if echo "$response" | jq -e '.systemCode != "ACC_0000"' > /dev/null 2>&1; then
        echo -e "${RED}Lỗi API: $(echo "$response" | jq -r '.message // .systemCode')${NC}"
        return 1
    fi
    
    local data=$(echo "$response" | jq '.data')
    local list=$(echo "$data" | jq '.listData')
    local count=$(echo "$list" | jq 'length')
    
    echo ""
    echo -e "${BLUE}📊 THỐNG KÊ PRENY - ${period}${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Summary
    local total_accounts=$(echo "$list" | jq '[.[].countNewAccounts] | add // 0')
    local total_phones=$(echo "$list" | jq '[.[].countNewPhoneNumber] | add // 0')
    local total_messages=$(echo "$list" | jq '[.[].messageByFanpage] | add // 0')
    local total_comments=$(echo "$list" | jq '[.[].userCommentPage] | add // 0')
    local total_old=$(echo "$list" | jq '[.[].countOldCustomer] | add // 0')
    
    echo -e "${GREEN}👥 KHÁCH HÀNG${NC}"
    echo "   Tài khoản mới:     $(fmt $total_accounts)"
    echo "   SĐT mới:           $(fmt $total_phones)"
    echo "   Khách quay lại:    $(fmt $total_old)"
    echo ""
    echo -e "${GREEN}💬 TƯƠNG TÁC${NC}"
    echo "   Tin nhắn Fanpage:  $(fmt $total_messages)"
    echo "   Comment khách:     $(fmt $total_comments)"
    echo ""
    
    # Daily breakdown
    if [ "$count" -gt 1 ]; then
        echo -e "${GREEN}📅 CHI TIẾT THEO NGÀY${NC}"
        echo "────────────────────────────────────────────────"
        printf "%-12s %10s %10s %12s\n" "Ngày" "TK mới" "SĐT mới" "Tin nhắn"
        echo "────────────────────────────────────────────────"
        echo "$list" | jq -r '.[] | "\(.date) \(.countNewAccounts) \(.countNewPhoneNumber) \(.messageByFanpage)"' | \
        while read date acc phone msg; do
            printf "%-12s %10s %10s %12s\n" "$date" "$(fmt $acc)" "$(fmt $phone)" "$(fmt $msg)"
        done
        echo ""
    fi
}

# Main
PERIOD="${1:-today}"
FROM="$2"
TO="$3"

case "$PERIOD" in
    today)
        read FROM TO <<< $(get_today_range)
        display_stats "$(call_api "$FROM" "$TO" 1)" "HÔM NAY"
        ;;
    yesterday)
        read FROM TO <<< $(get_yesterday_range)
        display_stats "$(call_api "$FROM" "$TO" 1)" "HÔM QUA"
        ;;
    week)
        read FROM TO <<< $(get_week_range)
        display_stats "$(call_api "$FROM" "$TO" 7)" "7 NGÀY QUA"
        ;;
    month)
        read FROM TO <<< $(get_month_range)
        display_stats "$(call_api "$FROM" "$TO" 30)" "30 NGÀY QUA"
        ;;
    *)
        # Custom date range: preny-stats 2026-04-01 2026-04-03
        if [ -n "$FROM" ] && [ -n "$TO" ]; then
            FROM="${FROM}T00:00:00.000Z"
            TO="${TO}T23:59:59.000Z"
            display_stats "$(call_api "$FROM" "$TO" 30)" "TÙY CHỈN"
        else
            echo "Usage: preny-stats [today|yesterday|week|month|from_date to_date]"
            echo ""
            echo "Examples:"
            echo "  preny-stats today"
            echo "  preny-stats week"
            echo "  preny-stats 2026-04-01 2026-04-03"
        fi
        ;;
esac
