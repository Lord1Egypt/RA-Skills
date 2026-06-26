#!/bin/bash
# 兰泰式按摩预约 API 测试脚本 (Shell 版本)
#
# 使用方法:
#   chmod +x test_booking.sh
#   ./test_booking.sh

API_ENDPOINT="https://open.lannlife.com/mcp/book/create"

# 测试数据
TEST_MOBILE="13812345678"
TEST_STORE="淮海店"
TEST_SERVICE="传统古法全身按摩-90分钟"
TEST_COUNT=2
# 生成明天的时间（ISO 8601 格式）
TEST_TIME=$(date -d "+1 day 14:00:00" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -v+1d -v14H -v0M -v0S +"%Y-%m-%dT%H:%M:%S")

print_separator() {
    echo ""
    echo "============================================================"
    if [ -n "$1" ]; then
        echo "  $1"
        echo "============================================================"
    fi
}

create_booking() {
    local mobile=$1
    local store_name=$2
    local service_name=$3
    local count=$4
    local book_time=$5
    local test_name=$6

    echo ""
    echo "测试: $test_name"
    echo "请求参数:"
    cat <<EOF
{
  "mobile": "$mobile",
  "storeName": "$store_name",
  "serviceName": "$service_name",
  "count": $count,
  "bookTime": "$book_time"
}
EOF

    response=$(curl -s -w "\n%{http_code}" -X POST "$API_ENDPOINT" \
        -H "Content-Type: application/json" \
        -d "{
            \"mobile\": \"$mobile\",
            \"storeName\": \"$store_name\",
            \"serviceName\": \"$service_name\",
            \"count\": $count,
            \"bookTime\": \"$book_time\"
        }" 2>&1)

    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    echo "状态码: $http_code"
    echo "响应内容:"
    echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"

    success=$(echo "$body" | grep -o '"success":[^,}]*' | cut -d':' -f2 | tr -d ' ')
    if [ "$success" = "true" ]; then
        echo "✅ 测试通过"
    else
        echo "❌ 测试失败"
    fi
}

# 主测试流程
echo "============================================================"
echo "  兰泰式按摩预约 API 测试套件 (Shell 版本)"
echo "============================================================"
echo ""
echo "API Endpoint: $API_ENDPOINT"
echo "测试时间: $(date '+%Y-%m-%d %H:%M:%S')"

read -p "按 Enter 键开始测试..."

# 测试 1: 有效的预约请求
print_separator "测试 1: 有效的预约请求"
create_booking "$TEST_MOBILE" "$TEST_STORE" "$TEST_SERVICE" "$TEST_COUNT" "$TEST_TIME" "有效预约"

# 测试 2: 无效的手机号
print_separator "测试 2: 无效的手机号"
create_booking "12345" "$TEST_STORE" "$TEST_SERVICE" "$TEST_COUNT" "$TEST_TIME" "无效手机号"

# 测试 3: 不存在的门店
print_separator "测试 3: 不存在的门店"
create_booking "$TEST_MOBILE" "不存在的门店" "$TEST_SERVICE" "$TEST_COUNT" "$TEST_TIME" "不存在的门店"

# 测试 4: 不存在的服务
print_separator "测试 4: 不存在的服务"
create_booking "$TEST_MOBILE" "$TEST_STORE" "不存在的服务" "$TEST_COUNT" "$TEST_TIME" "不存在的服务"

# 测试 5: 无效的人数
print_separator "测试 5: 无效的人数"
create_booking "$TEST_MOBILE" "$TEST_STORE" "$TEST_SERVICE" 25 "$TEST_TIME" "无效人数（超过限制）"

# 测试 6: 过去的时间
print_separator "测试 6: 过去的时间"
PAST_TIME=$(date -d "-1 day" +"%Y-%m-%dT%H:%M:%S" 2>/dev/null || date -v-1d +"%Y-%m-%dT%H:%M:%S")
create_booking "$TEST_MOBILE" "$TEST_STORE" "$TEST_SERVICE" "$TEST_COUNT" "$PAST_TIME" "过去的时间"

print_separator "测试完成"
echo ""
echo "所有测试已执行完毕。"
