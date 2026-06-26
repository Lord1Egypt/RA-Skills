#!/usr/bin/env python3
"""
Hong Kong Weather - HKO Open Data API Client
Fetches current weather, warnings, and forecast from Hong Kong Observatory.
No API key required.
"""

import json
import sys
import urllib.request
from datetime import datetime

BASE_URL = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php"

# Weather icon mapping (simplified)
ICON_DESC_TC = {
    50: "陽光充沛", 51: "部分時間有陽光", 52: "部分時間有陽光", 53: "部分時間有陽光",
    54: "部分時間有陽光", 60: "多雲", 61: "多雲", 62: "多雲",
    63: "多雲", 64: "雨", 65: "大雨", 70: "雷暴",
    71: "雷暴", 72: "雷暴", 73: "雷暴", 74: "雷暴",
    75: "雷暴", 76: "雷暴", 77: "雷暴", 80: "陣風",
    81: "陣風", 82: "陣風", 83: "陣風", 84: "陣風",
    85: "陣風", 90: "熱帶氣旋", 91: "熱帶氣旋", 92: "熱帶氣旋",
    93: "熱帶氣旋",
}

ICON_DESC_EN = {
    50: "Sunny", 51: "Sunny Periods", 52: "Sunny Periods", 53: "Sunny Periods",
    54: "Sunny Periods", 60: "Cloudy", 61: "Cloudy", 62: "Cloudy",
    63: "Cloudy", 64: "Rain", 65: "Heavy Rain", 70: "Thunderstorms",
    71: "Thunderstorms", 72: "Thunderstorms", 73: "Thunderstorms", 74: "Thunderstorms",
    75: "Thunderstorms", 76: "Thunderstorms", 77: "Thunderstorms", 80: "Squally",
    81: "Squally", 82: "Squally", 83: "Squally", 84: "Squally",
    85: "Squally", 90: "Tropical Cyclone", 91: "Tropical Cyclone", 92: "Tropical Cyclone",
    93: "Tropical Cyclone",
}


def fetch_json(data_type, lang):
    """Fetch data from HKO API."""
    url = f"{BASE_URL}?dataType={data_type}&lang={lang}"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}


def format_current(data, lang):
    """Format current weather report."""
    if "error" in data:
        return f"[ERROR] Failed to fetch weather: {data['error']}"

    temp_data = data.get("temperature", {}).get("data", [])
    humidity_data = data.get("humidity", {}).get("data", [])
    uv_data = data.get("uvindex", {}).get("data", [])
    rainfall_data = data.get("rainfall", {}).get("data", [])
    icons = data.get("icon", [])

    if lang == "tc":
        lines = ["🌤️ 香港天文台實時天氣", "━━━━━━━━━━━━━━━━━━━━━━"]
    else:
        lines = ["🌤️ HKO Current Weather", "━━━━━━━━━━━━━━━━━━━━━━"]

    # Temperature (prioritize King's Park / 京士柏 as main station)
    main_temp = None
    for t in temp_data:
        place = t.get("place", "")
        if place in ("京士柏", "King's Park"):
            main_temp = t
            break
    if not main_temp and temp_data:
        main_temp = temp_data[0]

    if main_temp:
        val = main_temp.get("value", "N/A")
        unit = main_temp.get("unit", "C")
        if lang == "tc":
            lines.append(f"🌡️ 氣溫：{val}°{unit}")
        else:
            lines.append(f"🌡️ Temperature: {val}°{unit}")

    # Humidity
    if humidity_data:
        h = humidity_data[0]
        val = h.get("value", "N/A")
        if lang == "tc":
            lines.append(f"💧 相對濕度：{val}%")
        else:
            lines.append(f"💧 Humidity: {val}%")

    # Rainfall - show max from all districts
    max_rain = 0
    for r in rainfall_data:
        try:
            max_rain = max(max_rain, r.get("max", 0))
        except:
            pass
    if lang == "tc":
        lines.append(f"🌧️ 過去一小時雨量：{max_rain} mm（全港最大）")
    else:
        lines.append(f"🌧️ Rainfall (past hr): {max_rain} mm (max across HK)")

    # UV Index
    if uv_data:
        uv = uv_data[0]
        val = uv.get("value", "N/A")
        desc = uv.get("desc", "")
        if lang == "tc":
            lines.append(f"☀️ 紫外線指數：{val}（{desc}）")
        else:
            lines.append(f"☀️ UV Index: {val} ({desc})")

    # Weather icon description
    if icons:
        icon = icons[0]
        desc = ICON_DESC_TC.get(icon, "") if lang == "tc" else ICON_DESC_EN.get(icon, "")
        if desc:
            if lang == "tc":
                lines.append(f"📝 天氣概況：{desc}")
            else:
                lines.append(f"📝 Conditions: {desc}")

    lines.append("━━━━━━━━━━━━━━━━━━━━━━")
    return "\n".join(lines)


def format_warnings(data, lang):
    """Format weather warnings."""
    if "error" in data:
        return f"[ERROR] Failed to fetch warnings: {data['error']}"

    # warnsum returns empty {} when no warnings
    if not data:
        if lang == "tc":
            return "✅ 現時無生效天氣警告"
        return "✅ No active weather warnings"

    # If there are warnings, format them
    lines = []
    if lang == "tc":
        lines.append("⚠️ 天氣警告")
        lines.append("━━━━━━━━━━━━━━━━━━━━━━")
    else:
        lines.append("⚠️ Weather Warnings")
        lines.append("━━━━━━━━━━━━━━━━━━━━━━")

    for key, value in data.items():
        if isinstance(value, dict):
            name = value.get("name", key)
            code = value.get("code", "")
            action_code = value.get("actionCode", "")
            status = "生效中" if action_code == "ISSU" else "取消" if action_code == "CANCEL" else action_code
            if lang == "en":
                status = "In effect" if action_code == "ISSU" else "Cancelled" if action_code == "CANCEL" else action_code
            lines.append(f"• {name}: {status}")

    lines.append("━━━━━━━━━━━━━━━━━━━━━━")
    return "\n".join(lines)


def format_forecast(data, lang, days=3):
    """Format weather forecast."""
    if "error" in data:
        return f"[ERROR] Failed to fetch forecast: {data['error']}"

    forecast = data.get("weatherForecast", [])
    general = data.get("generalSituation", "")

    if not forecast:
        if lang == "tc":
            return "[ERROR] 無法取得預報資料"
        return "[ERROR] Unable to retrieve forecast data"

    lines = []
    if lang == "tc":
        lines.append(f"📅 九天氣象預報（顯示首{days}日）")
        lines.append("━━━━━━━━━━━━━━━━━━━━━━")
        if general:
            lines.append(f"📋 天氣概況：{general}")
            lines.append("")
    else:
        lines.append(f"📅 9-Day Forecast (showing first {days} days)")
        lines.append("━━━━━━━━━━━━━━━━━━━━━━")
        if general:
            lines.append(f"📋 General Situation: {general}")
            lines.append("")

    for i, day in enumerate(forecast[:days]):
        date_str = day.get("forecastDate", "")
        week = day.get("week", "")
        weather = day.get("forecastWeather", "")
        max_temp = day.get("forecastMaxtemp", {}).get("value", "N/A")
        min_temp = day.get("forecastMintemp", {}).get("value", "N/A")
        max_rh = day.get("forecastMaxrh", {}).get("value", "N/A")
        min_rh = day.get("forecastMinrh", {}).get("value", "N/A")
        psr = day.get("PSR", "")

        # Format date
        try:
            dt = datetime.strptime(date_str, "%Y%m%d")
            date_fmt = dt.strftime("%m/%d") if lang == "en" else f"{dt.month}月{dt.day}日"
        except:
            date_fmt = date_str

        if lang == "tc":
            lines.append(f"📆 {date_fmt}（{week}）")
            lines.append(f"   {weather}")
            lines.append(f"   🌡️ {min_temp}°C - {max_temp}°C  💧 {min_rh}% - {max_rh}%")
            if psr:
                lines.append(f"   🌧️ 降雨概率：{psr}")
        else:
            lines.append(f"📆 {date_fmt} ({week})")
            lines.append(f"   {weather}")
            lines.append(f"   🌡️ {min_temp}°C - {max_temp}°C  💧 {min_rh}% - {max_rh}%")
            if psr:
                lines.append(f"   🌧️ Rain probability: {psr}")
        lines.append("")

    lines.append("━━━━━━━━━━━━━━━━━━━━━━")
    return "\n".join(lines)


def format_all(current, warn, forecast, lang):
    """Combine all reports."""
    parts = []
    parts.append(format_current(current, lang))
    parts.append("")
    parts.append(format_warnings(warn, lang))
    parts.append("")
    parts.append(format_forecast(forecast, lang, days=3))
    return "\n".join(parts)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 hk_weather.py <current|warning|forecast|all> [tc|en]", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1].lower()
    lang = sys.argv[2].lower() if len(sys.argv) > 2 else "tc"
    if lang not in ("tc", "en"):
        lang = "tc"

    if command == "current":
        data = fetch_json("rhrread", lang)
        print(format_current(data, lang))
    elif command == "warning":
        data = fetch_json("warnsum", lang)
        print(format_warnings(data, lang))
    elif command == "forecast":
        data = fetch_json("fnd", lang)
        print(format_forecast(data, lang, days=9))
    elif command == "all":
        current = fetch_json("rhrread", lang)
        warn = fetch_json("warnsum", lang)
        forecast = fetch_json("fnd", lang)
        print(format_all(current, warn, forecast, lang))
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print("Usage: python3 hk_weather.py <current|warning|forecast|all> [tc|en]", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
