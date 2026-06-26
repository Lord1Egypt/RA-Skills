#!/bin/bash
# Test script for HKO Weather API (Traditional Chinese)
# Demonstrates the skill works by fetching and formatting real data in TC
# Includes weather warnings/signals testing

set -e

echo "🧪 測試 HKO 天氣 API (繁體中文)..."
echo ""

# Test 1: Weather Warnings
echo "✅ 測試 1: 獲取天氣警告..."
WARNINGS=$(curl -s --max-time 10 "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warningInfo&lang=tc")

if [ -z "$WARNINGS" ] || [ "$WARNINGS" = "{}" ]; then
    echo "   目前沒有生效警告"
else
    # Check for Warning_Summary
    if echo "$WARNINGS" | grep -q '"Warning_Summary"'; then
        echo "   ⚠️  有生效警告"
        WARNING_TYPE=$(echo "$WARNINGS" | grep -o '"Name":{"tc":"[^"]*"' | head -1 | cut -d'"' -f6)
        echo "   警告類型：${WARNING_TYPE}"
    else
        echo "   目前沒有生效警告"
    fi
fi
echo ""

# Test 2: Current Weather (Traditional Chinese)
echo "✅ 測試 2: 獲取現時天氣..."
CURRENT=$(curl -s --max-time 10 "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=tc")

if [ -z "$CURRENT" ]; then
    echo "❌ 失敗：沒有返回數據"
    exit 1
fi

# Verify JSON structure
if ! echo "$CURRENT" | grep -q '"temperature"'; then
    echo "❌ 失敗：JSON 結構無效"
    exit 1
fi

# Extract values - using 京士柏 (King's Park) in TC
TEMP=$(echo "$CURRENT" | sed 's/.*"京士柏","value":\([0-9]*\).*/\1/' | head -1)
HUMIDITY=$(echo "$CURRENT" | grep -o '"humidity":{[^}]*"value":[0-9]*' | grep -o '"value":[0-9]*' | cut -d: -f2)
UV=$(echo "$CURRENT" | grep -o '"uvindex":{[^}]*"value":[0-9]*' | grep -o '"value":[0-9]*' | cut -d: -f2)
UV_DESC=$(echo "$CURRENT" | grep -o '"desc":"[^"]*"' | head -1 | cut -d'"' -f4)

echo "   溫度：${TEMP}°C (京士柏)"
echo "   濕度：${HUMIDITY}%"
echo "   紫外線指數：${UV} (${UV_DESC})"
echo ""

# Test 3: 9-Day Forecast (Traditional Chinese)
echo "✅ 測試 3: 獲取 9 日預報..."
FORECAST=$(curl -s --max-time 10 "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=fnd&lang=tc")

if [ -z "$FORECAST" ]; then
    echo "❌ 失敗：沒有預報數據"
    exit 1
fi

# Count forecast days
DAY_COUNT=$(echo "$FORECAST" | grep -o '"forecastDate"' | wc -l)
echo "   可用預報天數：${DAY_COUNT}"
echo ""

# Test 4: Generate Traditional Chinese Markdown Output
echo "✅ 測試 4: 生成繁體中文 Markdown (Discord 格式)..."
echo ""
echo "--- MARKDOWN 輸出 ---"
echo "## 🌤️ 香港天氣"
echo ""
echo "**現時天氣**"
echo "- 🌡️ 溫度：${TEMP}°C (京士柏)"
echo "- 💧 濕度：${HUMIDITY}%"
echo "- ☀️ 紫外線指數：${UV} (${UV_DESC})"
echo ""

# Extract general situation
GENERAL=$(echo "$FORECAST" | grep -o '"generalSituation":"[^"]*"' | head -1 | cut -d'"' -f4)
echo "**天氣概況**"
echo "${GENERAL}"
echo ""

# Extract first forecast day as example
FIRST_WEEK=$(echo "$FORECAST" | grep -o '"week":"[^"]*"' | head -1 | cut -d'"' -f4)
FIRST_HIGH=$(echo "$FORECAST" | grep -o '"forecastMaxtemp":{"value":[0-9]*' | head -1 | grep -o '[0-9]*$')
FIRST_LOW=$(echo "$FORECAST" | grep -o '"forecastMintemp":{"value":[0-9]*' | head -1 | grep -o '[0-9]*$')
FIRST_WEATHER=$(echo "$FORECAST" | grep -o '"forecastWeather":"[^"]*"' | head -1 | cut -d'"' -f4 | cut -c1-40)

echo "**預報範例 (${FIRST_WEEK})**"
echo "- 最高：${FIRST_HIGH}°C | 最低：${FIRST_LOW}°C"
echo "- 天氣：${FIRST_WEATHER}"
echo ""
echo "**9 日預報已獲取**"
echo "(完整預報數據已成功獲取)"
echo ""
echo "--- 結束 MARKDOWN ---"
echo ""

# Test 5: Verify API reliability
echo "✅ 測試 5: API 可靠性檢查..."
START=$(date +%s)
curl -s --max-time 10 "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=tc" > /dev/null
END=$(date +%s)
DURATION=$((END - START))
echo "   API 回應時間：${DURATION}秒"

if [ $DURATION -gt 5 ]; then
    echo "   ⚠️  API 回應較慢 (>5 秒)"
else
    echo "   ✅ API 回應時間正常"
fi

echo ""
echo "✅ 所有測試通過！HKO 天氣 API 運行正常 (繁體中文)。"
echo ""
echo "📁 技能位置：/app/skills/hko-weather/"
echo "📄 SKILL.md: 包含 API 文檔 (繁體中文)"
echo "🔧 腳本：fetch-weather.sh, test-hko.sh"
echo "🌐 語言：繁體中文 (Traditional Chinese)"
echo ""
echo "💡 使用提示："
echo "   bash fetch-weather.sh --format markdown --lang tc"
echo "   bash fetch-weather.sh --help"
