#!/bin/bash
# Preny Analytics - Main CLI
# Usage: preny-cli <command> [options]

set -e

API_URL="${PRENY_API_URL:-https://api.preny.ai/v1}"
API_KEY="${PRENY_API_KEY}"
WORKSPACE_ID="${PRENY_WORKSPACE_ID}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check config
check_config() {
    if [ -z "$API_KEY" ] || [ -z "$WORKSPACE_ID" ]; then
        echo -e "${RED}Error: Missing configuration${NC}"
        echo "Please set PRENY_API_KEY and PRENY_WORKSPACE_ID"
        exit 1
    fi
}

# API Call helper
api_call() {
    local method="$1"
    local endpoint="$2"
    local data="$3"
    
    local url="${API_URL}${endpoint}"
    local args=(-s -X "$method" -H "Authorization: Bearer ${API_KEY}" -H "X-Workspace-ID: ${WORKSPACE_ID}" -H "Content-Type: application/json")
    
    if [ -n "$data" ]; then
        args+=(-d "$data")
    fi
    
    curl "${args[@]}" "$url"
}

# ===== STATS COMMANDS =====

# Thống kê hôm nay
stats_today() {
    echo -e "${BLUE}📊 THỐNG KÊ HÔM NAY${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    local response=$(api_call GET "/analytics/summary?period=today")
    
    if echo "$response" | jq -e '.success == false' > /dev/null 2>&1; then
        echo -e "${RED}Lỗi: $(echo "$response" | jq -r '.error.message')${NC}"
        return 1
    fi
    
    local data=$(echo "$response" | jq '.data')
    local metrics=$(echo "$data" | jq '.metrics')
    
    echo ""
    echo -e "${GREEN}👥 Khách hàng${NC}"
    echo "   Tổng:        $(echo "$metrics" | jq -r '.totalCustomers')"
    echo "   Mới:         $(echo "$metrics" | jq -r '.newCustomers')"
    echo "   Quay lại:    $(echo "$metrics" | jq -r '.returningCustomers')"
    echo ""
    echo -e "${GREEN}💬 Tin nhắn${NC}"
    echo "   Hội thoại:   $(echo "$metrics" | jq -r '.totalConversations')"
    echo "   Tổng tin:    $(echo "$metrics" | jq -r '.totalMessages')"
    echo "   Nhận:        $(echo "$metrics" | jq -r '.messagesReceived')"
    echo "   Gửi:         $(echo "$metrics" | jq -r '.messagesSent')"
    echo ""
    echo -e "${GREEN}📈 Hiệu suất${NC}"
    echo "   T/g phản hồi: $(echo "$metrics" | jq -r '.avgResponseTime')s"
    echo "   Tỷ lệ chốt:   $(echo "$metrics" | jq -r '.conversionRate | . * 100 | floor')%"
    echo ""
    echo -e "${GREEN}💰 Kinh doanh${NC}"
    echo "   Đơn hàng:    $(echo "$metrics" | jq -r '.ordersCreated')"
    echo "   Doanh thu:   $(echo "$metrics" | jq -r '.revenue') VND"
    echo ""
}

# Thống kê tuần
stats_week() {
    echo -e "${BLUE}📊 THỐNG KÊ TUẦN NAY${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    local response=$(api_call GET "/analytics/summary?period=week")
    
    if echo "$response" | jq -e '.success == false' > /dev/null 2>&1; then
        echo -e "${RED}Lỗi: $(echo "$response" | jq -r '.error.message')${NC}"
        return 1
    fi
    
    local metrics=$(echo "$response" | jq '.data.metrics')
    
    echo ""
    echo -e "👥 Khách: $(echo "$metrics" | jq -r '.totalCustomers') (Mới: $(echo "$metrics" | jq -r '.newCustomers'))"
    echo -e "💬 Hội thoại: $(echo "$metrics" | jq -r '.totalConversations')"
    echo -e "💰 Doanh thu: $(echo "$metrics" | jq -r '.revenue') VND"
    echo -e "📈 Tỷ lệ chốt: $(echo "$metrics" | jq -r '.conversionRate | . * 100 | floor')%"
    echo ""
}

# Thống kê tháng
stats_month() {
    echo -e "${BLUE}📊 THỐNG KÊ THÁNG NAY${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    local response=$(api_call GET "/analytics/summary?period=month")
    
    if echo "$response" | jq -e '.success == false' > /dev/null 2>&1; then
        echo -e "${RED}Lỗi: $(echo "$response" | jq -r '.error.message')${NC}"
        return 1
    fi
    
    local metrics=$(echo "$response" | jq '.data.metrics')
    
    echo ""
    echo -e "👥 Khách: $(echo "$metrics" | jq -r '.totalCustomers') (Mới: $(echo "$metrics" | jq -r '.newCustomers'))"
    echo -e "💬 Hội thoại: $(echo "$metrics" | jq -r '.totalConversations')"
    echo -e "💰 Doanh thu: $(echo "$metrics" | jq -r '.revenue') VND"
    echo -e "📈 Tỷ lệ chốt: $(echo "$metrics" | jq -r '.conversionRate | . * 100 | floor')%"
    echo ""
}

# ===== CONVERSATION COMMANDS =====

# Danh sách hội thoại chờ
conversations_pending() {
    echo -e "${YELLOW}⏳ HỘI THOẠI CHỜ XỬ LÝ${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    local response=$(api_call GET "/conversations?status=pending&limit=20")
    
    if echo "$response" | jq -e '.success == false' > /dev/null 2>&1; then
        echo -e "${RED}Lỗi: $(echo "$response" | jq -r '.error.message')${NC}"
        return 1
    fi
    
    local count=$(echo "$response" | jq '.data.conversations | length')
    
    if [ "$count" -eq 0 ]; then
        echo ""
        echo "   ✅ Không có hội thoại chờ xử lý"
        echo ""
        return 0
    fi
    
    echo ""
    echo "$response" | jq -r '.data.conversations[] | 
        "   📨 \(.customerName) | \(.channel) | \(.lastMessage[:40])..."'
    echo ""
    echo "   Tổng: $count hội thoại"
    echo ""
}

# ===== COMPARISON =====

# So sánh
compare_weeks() {
    echo -e "${BLUE}📊 SO SÁNH TUẦN NAY VS TUẦN TRƯỚC${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    local this_week=$(api_call GET "/analytics/summary?period=week")
    local last_week=$(api_call GET "/analytics/summary?period=last_week")
    
    local tw_customers=$(echo "$this_week" | jq -r '.data.metrics.totalCustomers')
    local lw_customers=$(echo "$last_week" | jq -r '.data.metrics.totalCustomers')
    local tw_revenue=$(echo "$this_week" | jq -r '.data.metrics.revenue')
    local lw_revenue=$(echo "$last_week" | jq -r '.data.metrics.revenue')
    
    echo ""
    printf "%-20s %15s %15s %15s\n" "Chỉ số" "Tuần này" "Tuần trước" "Thay đổi"
    echo "─────────────────────────────────────────────────────────"
    printf "%-20s %15s %15s %15s\n" "Khách hàng" "$tw_customers" "$lw_customers" "$((tw_customers - lw_customers))"
    printf "%-20s %15s %15s %15s\n" "Doanh thu" "$tw_revenue" "$lw_revenue" "$((tw_revenue - lw_revenue))"
    echo ""
}

# ===== HELP =====

show_help() {
    echo ""
    echo -e "${BLUE}Preny Analytics CLI${NC}"
    echo ""
    echo "Commands:"
    echo ""
    echo "  Thống kê:"
    echo "    today          Thống kê hôm nay"
    echo "    week           Thống kê tuần này"
    echo "    month          Thống kê tháng này"
    echo ""
    echo "  Hội thoại:"
    echo "    pending        Hội thoại chờ xử lý"
    echo "    list [status]  Danh sách hội thoại"
    echo ""
    echo "  So sánh:"
    echo "    compare        So sánh tuần này vs tuần trước"
    echo ""
    echo "Examples:"
    echo "    preny-cli today"
    echo "    preny-cli pending"
    echo "    preny-cli compare"
    echo ""
}

# ===== MAIN =====

check_config

COMMAND="${1:-help}"

case "$COMMAND" in
    today)
        stats_today
        ;;
    week)
        stats_week
        ;;
    month)
        stats_month
        ;;
    pending)
        conversations_pending
        ;;
    list)
        conversations_pending
        ;;
    compare)
        compare_weeks
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "Unknown command: $COMMAND"
        show_help
        exit 1
        ;;
esac
