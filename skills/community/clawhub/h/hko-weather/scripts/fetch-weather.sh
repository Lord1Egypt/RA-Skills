#!/bin/bash
# HKO Weather Fetcher (Traditional Chinese / Cantonese)
# Fetches current weather, 9-day forecast, and weather warnings from Hong Kong Observatory
# Output: Formatted JSON or Markdown in Traditional Chinese

set -e

HKO_BASE="https://data.weather.gov.hk/weatherAPI/opendata/weather.php"
TIMEOUT=10
LANG="tc"

# Parse arguments
FORMAT="json"
FETCH="both"

while [[ $# -gt 0 ]]; do
    case $1 in
        --format|-f)
            FORMAT="$2"
            shift 2
            ;;
        --fetch|-t)
            FETCH="$2"
            shift 2
            ;;
        --lang|-l)
            LANG="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [--format json|markdown] [--fetch current|forecast|both|warnings] [--lang tc|en]"
            echo "  --lang: tc (Traditional Chinese) or en (English)"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

fetch_current() {
    curl -s --max-time $TIMEOUT "${HKO_BASE}?dataType=rhrread&lang=${LANG}"
}

fetch_forecast() {
    curl -s --max-time $TIMEOUT "${HKO_BASE}?dataType=fnd&lang=${LANG}"
}

fetch_warnings() {
    curl -s --max-time $TIMEOUT "${HKO_BASE}?dataType=warningInfo&lang=${LANG}"
}

format_warnings_markdown() {
    local warnings_data="$1"
    
    # Check if warnings_data is empty or just {}
    if [ -z "$warnings_data" ] || [ "$warnings_data" = "{}" ]; then
        echo "## ⚠️ 天氣警告及信號"
        echo ""
        echo "目前沒有生效警告"
        echo ""
        return
    fi
    
    # Check for Warning_Summary array
    local has_warnings=$(echo "$warnings_data" | grep -o '"Warning_Summary"\s*:\s*\[' | head -1)
    
    if [ -z "$has_warnings" ]; then
        echo "## ⚠️ 天氣警告及信號"
        echo ""
        echo "目前沒有生效警告"
        echo ""
        return
    fi
    
    # Check if Warning_Summary is empty array
    local warning_count=$(echo "$warnings_data" | grep -o '"Warning_Summary"\s*:\s*\[\]' | wc -l)
    if [ "$warning_count" -gt 0 ]; then
        echo "## ⚠️ 天氣警告及信號"
        echo ""
        echo "目前沒有生效警告"
        echo ""
        return
    fi
    
    echo "## ⚠️ 天氣警告及信號"
    echo ""
    
    # Extract warning type
    local warning_type=$(echo "$warnings_data" | grep -o '"WarningType":{"Code":"[^"]*"' | head -1 | cut -d'"' -f6)
    local warning_name=$(echo "$warnings_data" | grep -o '"Name":{"tc":"[^"]*"' | head -1 | cut -d'"' -f6)
    local warning_code=$(echo "$warnings_data" | grep -o '"Code":"[^"]*"' | head -1 | cut -d'"' -f4)
    
    # Extract signal number if applicable (for tropical cyclone or rainstorm)
    local signal=""
    local emoji=""
    
    case "$warning_code" in
        TCWS)
            # Tropical Cyclone Warning Signal
            signal=$(echo "$warnings_data" | grep -o '"Signal":{"Value":"[^"]*"' | head -1 | cut -d'"' -f6)
            emoji="🌀"
            ;;
        RAINSTORM)
            # Rainstorm Warning Signal
            signal=$(echo "$warnings_data" | grep -o '"Signal":{"Value":"[^"]*"' | head -1 | cut -d'"' -f6)
            emoji="🌧️"
            ;;
        COLD)
            emoji="❄️"
            ;;
        STRONGWIND)
            emoji="💨"
            ;;
        LIGHTNING)
            emoji="⚡"
            ;;
        FIRESHRISK)
            emoji="🔥"
            ;;
        FLOOD)
            emoji="🌊"
            ;;
        LANDSLIP)
            emoji="🏔️"
            ;;
        *)
            emoji="⚠️"
            ;;
    esac
    
    # Extract issue time
    local issue_time=$(echo "$warnings_data" | grep -o '"IssueTime":"[^"]*"' | head -1 | cut -d'"' -f4)
    local issue_time_formatted=$(echo "$issue_time" | grep -o 'T[0-9][0-9]:[0-9][0-9]' | cut -c2-)
    
    # Display warning
    if [ -n "$signal" ] && [ "$signal" != "0" ]; then
        echo "- ${emoji} **${warning_name} ${signal}號**"
    else
        echo "- ${emoji} **${warning_name}**"
    fi
    
    if [ -n "$issue_time_formatted" ]; then
        echo "  - 發出時間：${issue_time_formatted} HKT"
    fi
    
    # Extract and display additional warnings if present
    local special_warnings=$(echo "$warnings_data" | grep -o '"Special_Warning"\s*:\s*\[' | head -1)
    if [ -n "$special_warnings" ]; then
        # Check if Special_Warning array is not empty
        local special_empty=$(echo "$warnings_data" | grep -o '"Special_Warning"\s*:\s*\[\]' | wc -l)
        if [ "$special_empty" -eq 0 ]; then
            echo ""
            echo "**特別提示**"
            local special_desc=$(echo "$warnings_data" | grep -o '"desc":"[^"]*"' | tail -1 | cut -d'"' -f4)
            if [ -n "$special_desc" ]; then
                echo "- ${special_desc}"
            fi
        fi
    fi
    
    echo ""
}

format_markdown() {
    local current_data="$1"
    local forecast_data="$2"
    local warnings_data="$3"
    
    # Display warnings FIRST (at the top)
    format_warnings_markdown "$warnings_data"
    
    # Extract current weather
    local temp=$(echo "$current_data" | sed 's/.*"京士柏","value":\([0-9]*\).*/\1/' | head -1)
    local humidity=$(echo "$current_data" | grep -o '"humidity":{[^}]*"value":[0-9]*' | grep -o '"value":[0-9]*' | cut -d: -f2)
    local uv=$(echo "$current_data" | grep -o '"uvindex":{[^}]*"value":[0-9]*' | grep -o '"value":[0-9]*' | cut -d: -f2)
    local uv_desc=$(echo "$current_data" | grep -o '"desc":"[^"]*"' | head -1 | cut -d'"' -f4)
    local record_time=$(echo "$current_data" | grep -o '"recordTime":"[^"]*"' | head -1 | cut -d'"' -f4)
    local time_only=$(echo "$record_time" | grep -o 'T[0-9][0-9]:[0-9][0-9]' | cut -c2-)
    
    # Extract general situation
    local general=$(echo "$forecast_data" | grep -o '"generalSituation":"[^"]*"' | cut -d'"' -f4)
    
    echo "## 🌤️ 香港天氣"
    echo ""
    echo "**現時天氣** (更新時間：${time_only} HKT)"
    echo "- 🌡️ 溫度：${temp}°C (京士柏)"
    echo "- 💧 濕度：${humidity}%"
    echo "- ☀️ 紫外線指數：${uv} (${uv_desc})"
    echo ""
    echo "**天氣概況**"
    echo "${general}"
    echo ""
    echo "**9 日預報**"
    
    # Get today's date for comparison
    local today=$(date +%Y%m%d)
    
    # Extract all forecast dates, weeks, temps, and weather separately, then combine
    local dates=$(echo "$forecast_data" | grep -o '"forecastDate":"[0-9]*"' | cut -d'"' -f4 | head -9)
    local weeks=$(echo "$forecast_data" | grep -o '"week":"[^"]*"' | cut -d'"' -f4 | head -9)
    local maxtemps=$(echo "$forecast_data" | grep -o '"forecastMaxtemp":{"value":[0-9]*' | grep -o '[0-9]*$' | head -9)
    local mintemps=$(echo "$forecast_data" | grep -o '"forecastMintemp":{"value":[0-9]*' | grep -o '[0-9]*$' | head -9)
    local weathers=$(echo "$forecast_data" | grep -o '"forecastWeather":"[^"]*"' | cut -d'"' -f4 | head -9)
    
    # Convert to arrays
    IFS=$'\n' read -r -d '' -a date_arr <<< "$dates" || true
    IFS=$'\n' read -r -d '' -a week_arr <<< "$weeks" || true
    IFS=$'\n' read -r -d '' -a max_arr <<< "$maxtemps" || true
    IFS=$'\n' read -r -d '' -a min_arr <<< "$mintemps" || true
    IFS=$'\n' read -r -d '' -a weather_arr <<< "$weathers" || true
    
    # Loop through and print each day
    for i in "${!date_arr[@]}"; do
        local fdate="${date_arr[$i]}"
        local week="${week_arr[$i]}"
        local maxtemp="${max_arr[$i]}"
        local mintemp="${min_arr[$i]}"
        local weather="${weather_arr[$i]}"
        
        # Truncate weather if too long
        weather="${weather:0:45}"
        
        # Determine day label
        local day_label="$week"
        if [ "$fdate" = "$today" ]; then
            day_label="今天"
        fi
        
        echo "• $day_label ($week)：高 ${maxtemp}° / 低 ${mintemp}° - ${weather}"
    done
    
    echo ""
    echo "---"
    echo "資料來源：香港天文台 (https://www.hko.gov.hk)"
    echo ""
    echo "*免責聲明：香港天文台所提供的天氣預報及氣候預測僅供參考，天文台不就該等天氣預報及氣候預測的準確性或完整性作出任何明示或暗示的保證。*"
}

case $FETCH in
    current)
        fetch_current
        ;;
    forecast)
        fetch_forecast
        ;;
    warnings)
        fetch_warnings
        ;;
    both)
        current=$(fetch_current)
        forecast=$(fetch_forecast)
        warnings=$(fetch_warnings)
        
        if [ "$FORMAT" = "markdown" ]; then
            format_markdown "$current" "$forecast" "$warnings"
        else
            echo "{\"current\":$current,\"forecast\":$forecast,\"warnings\":$warnings}"
        fi
        ;;
    *)
        echo "Invalid fetch type: $FETCH"
        exit 1
        ;;
esac
