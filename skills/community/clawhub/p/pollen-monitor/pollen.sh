#!/bin/bash
# 花粉浓度查询脚本
# 用法：./pollen.sh [城市拼音] [城市中文名]
# 示例：./pollen.sh beijing 北京

set -e

CITY_EN="${1:-beijing}"
CITY_CN="${2:-北京}"

# 计算日期（7 天前到今天）
START=$(date -d '-7 days' +%Y-%m-%d 2>/dev/null || date -v-7d +%Y-%m-%d)
END=$(date +%Y-%m-%d)

# 调用 API
API_URL="https://graph.weatherdt.com/ty/pollen/v2/hfindex.html?eletype=1&city=${CITY_EN}&start=${START}&end=${END}&predictFlag=true"

RESPONSE=$(curl -s "$API_URL")

# 检查是否获取到数据
if [ -z "$RESPONSE" ] || echo "$RESPONSE" | grep -q "error"; then
    echo "❌ 获取花粉数据失败"
    exit 1
fi

# 解析数据
SEASON_NAME=$(echo "$RESPONSE" | jq -r '.seasonLevelName // "花粉季"')

# 获取今天的数据（倒数第二个，因为最后一个是预报）
TODAY_DATA=$(echo "$RESPONSE" | jq -r '.dataList | sort_by(.addTime) | .[-2]')
TOMORROW_DATA=$(echo "$RESPONSE" | jq -r '.dataList | sort_by(.addTime) | .[-1]')

# 提取今天的信息
TODAY_LEVEL=$(echo "$TODAY_DATA" | jq -r '.level // "未知"')
TODAY_LEVELCODE=$(echo "$TODAY_DATA" | jq -r '.levelCode // "0"')
TODAY_MSG=$(echo "$TODAY_DATA" | jq -r '.levelMsg // "无数据"')
TODAY_DATE=$(echo "$TODAY_DATA" | jq -r '.addTime // "未知"')
TODAY_WEEK=$(echo "$TODAY_DATA" | jq -r '.week // "未知"')

# 提取明天的信息
TOMORROW_LEVEL=$(echo "$TOMORROW_DATA" | jq -r '.level // "未知"')
TOMORROW_MSG=$(echo "$TOMORROW_DATA" | jq -r '.levelMsg // "无数据"')
TOMORROW_DATE=$(echo "$TOMORROW_DATA" | jq -r '.addTime // "未知"')
TOMORROW_WEEK=$(echo "$TOMORROW_DATA" | jq -r '.week // "未知"')

# 根据等级代码设置 emoji
get_emoji() {
    case "$1" in
        "0") echo "⚪" ;;
        "1") echo "🟢" ;;
        "2") echo "🟡" ;;
        "3") echo "🟠" ;;
        "4") echo "🔴" ;;
        "5") echo "🔴🔴" ;;
        *) echo "⚪" ;;
    esac
}

TODAY_EMOJI=$(get_emoji "$TODAY_LEVELCODE")
TOMORROW_LEVELCODE=$(echo "$TOMORROW_DATA" | jq -r '.levelCode // "0"')
TOMORROW_EMOJI=$(get_emoji "$TOMORROW_LEVELCODE")

# 输出结果
echo "🌸 ${CITY_CN} 花粉浓度报告"
echo "━━━━━━━━━━━━━━━━━━━━━━"
echo "季节：${SEASON_NAME}花粉季"
echo ""
echo "📅 ${TODAY_WEEK} (${TODAY_DATE})"
echo "   等级：${TODAY_EMOJI} ${TODAY_LEVEL}"
echo "   建议：${TODAY_MSG}"
echo ""
echo "📅 ${TOMORROW_WEEK} (${TOMORROW_DATE}) 预报"
echo "   等级：${TOMORROW_EMOJI} ${TOMORROW_LEVEL}"
echo "   建议：${TOMORROW_MSG}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━"
echo "💡 数据来源：中国天气网 & 全国医院联合发布"
echo "🕐 更新时间：每日 08:00"
