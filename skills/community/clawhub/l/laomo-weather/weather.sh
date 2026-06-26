#!/bin/bash
# Weather Skill - Bilingual Helper Script
# 天气技能 - 双语辅助脚本
# Note: This is a reference implementation. Full implementation should be done in JavaScript/TypeScript.

set -e

# Detect language from query
# 从查询检测语言
detect_language() {
    local query="$1"
    local explicit_lang="$2"
    
    # Check explicit language parameter first
    if [[ -n "$explicit_lang" ]]; then
        case "$explicit_lang" in
            zh|zh-CN|zh-TW|chinese|中文)
                echo "zh"
                return
                ;;
            en|en-US|en-GB|english|英文)
                echo "en"
                return
                ;;
            auto|automatic|自动)
                # Fall through to auto-detection
                ;;
            *)
                echo "en"  # Default to English for unknown
                return
                ;;
        esac
    fi
    
    # Auto-detect: check for Chinese characters (Unicode range CJK Unified Ideographs)
    # Use LC_ALL=C to avoid locale issues and check for common Chinese character range
    if echo "$query" | LC_ALL=C grep -qE $'[\xe4\xb8\x80-\xe9\xbf\xbf]' 2>/dev/null; then
        echo "zh"
    else
        echo "en"
    fi
}

# Get weather emoji based on condition
# 根据天气状况获取表情符号
get_weather_emoji() {
    local condition="$1"
    
    case "$condition" in
        *Sunny*|*Clear*|*晴*)
            echo "☀️"
            ;;
        *Partly*cloudy*|*多云*)
            echo "⛅"
            ;;
        *Cloudy*|*Overcast*|*阴天*)
            echo "☁️"
            ;;
        *Light*rain*|*小雨*)
            echo "🌧️"
            ;;
        *Rain*|*雨*)
            echo "🌧️"
            ;;
        *Thunder*|*雷*)
            echo "⛈️"
            ;;
        *Snow*|*雪*)
            echo "❄️"
            ;;
        *Fog*|*雾*)
            echo "🌫️"
            ;;
        *Wind*|*风*)
            echo "💨"
            ;;
        *)
            echo "🌡️"
            ;;
    esac
}

# Get error message in specified language
# 获取指定语言的错误信息
get_error_message() {
    local lang="$1"
    local error_type="$2"
    
    case "$error_type" in
        city_not_found)
            if [[ "$lang" == "zh" ]]; then
                echo "❌ 未找到城市：请检查城市名称或尝试使用英文名称"
            else
                echo "❌ City not found: Please check the city name or try using the English name"
            fi
            ;;
        fetch_failed)
            if [[ "$lang" == "zh" ]]; then
                echo "❌ 无法获取天气数据：请稍后重试或检查网络连接"
            else
                echo "❌ Unable to fetch weather data: Please try again later or check your internet connection"
            fi
            ;;
        ambiguous_location)
            if [[ "$lang" == "zh" ]]; then
                echo "❌ 位置不明确：请提供更具体的城市名（例如：北京，中国）"
            else
                echo "❌ Ambiguous location: Please provide a more specific city name (e.g., Beijing, China)"
            fi
            ;;
        *)
            if [[ "$lang" == "zh" ]]; then
                echo "❌ 发生错误：请稍后重试"
            else
                echo "❌ An error occurred: Please try again later"
            fi
            ;;
    esac
}

# Simple city name mapping using case statement
# 使用 case 语句的简单城市名映射
translate_city() {
    local city="$1"
    
    case "$city" in
        北京)
            echo "Beijing"
            ;;
        上海)
            echo "Shanghai"
            ;;
        广州)
            echo "Guangzhou"
            ;;
        深圳)
            echo "Shenzhen"
            ;;
        纽约)
            echo "New York"
            ;;
        伦敦)
            echo "London"
            ;;
        东京)
            echo "Tokyo"
            ;;
        巴黎)
            echo "Paris"
            ;;
        悉尼)
            echo "Sydney"
            ;;
        多伦多)
            echo "Toronto"
            ;;
        柏林)
            echo "Berlin"
            ;;
        莫斯科)
            echo "Moscow"
            ;;
        新加坡)
            echo "Singapore"
            ;;
        首尔)
            echo "Seoul"
            ;;
        曼谷)
            echo "Bangkok"
            ;;
        *)
            # Return as-is (assume it's already in correct format or unknown city)
            echo "$city"
            ;;
    esac
}

# Translate weather condition to Chinese
# 翻译天气状况为中文
translate_condition_zh() {
    local condition="$1"
    
    case "$condition" in
        *Sunny*|*Clear*)
            echo "晴"
            ;;
        *Partly*cloudy*)
            echo "多云"
            ;;
        *Cloudy*|*Overcast*)
            echo "阴天"
            ;;
        *Light*rain*)
            echo "小雨"
            ;;
        *Rain*)
            echo "雨"
            ;;
        *Thunder*)
            echo "雷阵雨"
            ;;
        *Snow*)
            echo "雪"
            ;;
        *Fog*|*Mist*)
            echo "雾"
            ;;
        *Wind*)
            echo "风"
            ;;
        *)
            echo "$condition"
            ;;
    esac
}

# Format weather output
# 格式化天气输出
format_weather() {
    local lang="$1"
    local location="$2"
    local temp="$3"
    local condition="$4"
    local humidity="$5"
    local wind="$6"
    
    local emoji=$(get_weather_emoji "$condition")
    
    if [[ "$lang" == "zh" ]]; then
        local condition_zh=$(translate_condition_zh "$condition")
        echo "${location}: ${emoji} ${temp}°C，${condition_zh}，湿度 ${humidity}%"
        if [[ -n "$wind" ]]; then
            echo "   风：${wind}"
        fi
    else
        echo "${location}: ${emoji} ${temp}°C, ${condition}, ${humidity}% humidity"
        if [[ -n "$wind" ]]; then
            echo "   Wind: ${wind}"
        fi
    fi
}

# Main weather function
# 主天气函数
get_weather() {
    local query="$1"
    local lang_flag="$2"
    
    # Detect language
    local lang=$(detect_language "$query" "$lang_flag")
    
    # Extract city name from query (simple extraction)
    local city=$(echo "$query" | sed -E 's/^(天气|weather|--lang[= ][^ ]+)//g' | xargs)
    
    if [[ -z "$city" ]]; then
        get_error_message "$lang" "ambiguous_location"
        return 1
    fi
    
    # Translate city to English for API call
    local city_en=$(translate_city "$city")
    local city_display="$city"
    
    # If city was Chinese, use English for display in English mode
    if [[ "$lang" == "en" && "$city" != "$city_en" ]]; then
        city_display="$city_en"
    fi
    
    # Fetch weather data from wttr.in
    local weather_data
    weather_data=$(curl -s "wttr.in/${city_en}?format=j1" 2>/dev/null) || {
        get_error_message "$lang" "fetch_failed"
        return 1
    }
    
    if [[ -z "$weather_data" ]]; then
        get_error_message "$lang" "city_not_found"
        return 1
    fi
    
    # For now, use simple format
    local result
    result=$(curl -s "wttr.in/${city_en}?format=3" 2>/dev/null) || {
        get_error_message "$lang" "fetch_failed"
        return 1
    }
    
    # Output based on language
    if [[ "$lang" == "zh" ]]; then
        # Parse and translate the result
        # Note: This is simplified. Full implementation should parse JSON.
        echo "$result" | sed -E \
            -e 's/Sunny/晴/g' \
            -e 's/Partly cloudy/多云/g' \
            -e 's/Cloudy/阴天/g' \
            -e 's/Light rain/小雨/g' \
            -e 's/Rain/雨/g' \
            -e 's/Thunderstorm/雷阵雨/g' \
            -e 's/Snow/雪/g' \
            -e 's/Fog/雾/g' \
            -e 's/humidity/湿度/g'
    else
        echo "$result"
    fi
}

# Usage
show_usage() {
    cat << EOF
Weather Skill - Bilingual Support
天气技能 - 双语支持

Usage / 用法:
  $0 <city> [--lang zh|en|auto]
  $0 <城市> [--lang zh|en|auto]

Examples / 示例:
  $0 Beijing
  $0 北京
  $0 Beijing --lang zh
  $0 北京 --lang en
  $0 "New York" --lang auto

EOF
}

# Main entry point
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    case "${1}" in
        -h|--help|help)
            show_usage
            ;;
        "")
            show_usage
            exit 1
            ;;
        *)
            get_weather "$@"
            ;;
    esac
fi
