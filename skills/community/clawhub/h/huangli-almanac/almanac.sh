#!/bin/bash
# 黄历万年历查询脚本
# 使用 tiax.cn 的黄历 API 接口

set -e

# 默认 API 地址
API_BASE="https://api.tiax.cn/almanac/"

# 解析参数
YEAR=""
MONTH=""
DAY=""

# 检查参数
if [ $# -eq 0 ]; then
    echo "用法：almanac.sh <年> <月> <日>"
    echo "示例：almanac.sh 2024 05 20"
    echo "或者：almanac.sh today"
    echo "或者：almanac.sh tomorrow"
    exit 1
fi

# 处理特殊参数
if [ "$1" == "today" ]; then
    YEAR=$(date +%Y)
    MONTH=$(date +%m)
    DAY=$(date +%d)
elif [ "$1" == "tomorrow" ]; then
    NEXT_DATE=$(date -d "+1 day" +%Y-%m-%d)
    YEAR=$(echo $NEXT_DATE | cut -d'-' -f1)
    MONTH=$(echo $NEXT_DATE | cut -d'-' -f2)
    DAY=$(echo $NEXT_DATE | cut -d'-' -f3)
else
    YEAR=$1
    MONTH=$2
    DAY=$3
fi

# 格式自适应为两位数字（补零）
MONTH=$(printf "%02d" "$((10#$MONTH))")
DAY=$(printf "%02d" "$((10#$DAY))")

# 验证日期格式
if ! [[ "$YEAR" =~ ^[0-9]{4}$ ]] || ! [[ "$MONTH" =~ ^[0-9]{2}$ ]] || ! [[ "$DAY" =~ ^[0-9]{2}$ ]]; then
    echo "❌ 日期格式错误，请使用：年 (4 位) 月 (2 位) 日 (2 位)"
    echo "示例：almanac.sh 2024 05 20"
    exit 1
fi

# 调用 API
echo "📅 查询黄历：${YEAR}-${MONTH}-${DAY}"
echo ""

RESPONSE=$(curl -s "${API_BASE}?year=${YEAR}&month=${MONTH}&day=${DAY}")

# 检查响应
if [ -z "$RESPONSE" ]; then
    echo "❌ 请求失败，请检查网络连接"
    exit 1
fi

# 使用 Python 解析 JSON 并格式化输出
echo "$RESPONSE" | python3 -c '
import sys, json
try:
    data = json.load(sys.stdin)
    print("公历日期：" + data.get("公历日期", ""))
    print("农历日期：" + data.get("农历日期", ""))
    print("干支日期：" + data.get("干支日期", ""))
    print("五行纳音：" + data.get("五行纳音", ""))
    print("值日星神：" + data.get("值日星神", ""))
    print()
    print("宜：" + data.get("宜", ""))
    print("忌：" + data.get("忌", ""))
except json.JSONDecodeError:
    print("❌ API 响应不是合法的 JSON")
    sys.exit(1)
'
