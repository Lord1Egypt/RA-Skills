#!/usr/bin/env python3
"""
香港天氣 API 查詢腳本

用法:
    python3 fetch_weather.py --type current                    # 全港即時天氣
    python3 fetch_weather.py --type forecast --days 9         # 九天預報
    python3 fetch_weather.py --type hourly                     # 本地天氣預報 (每小時)
    python3 fetch_weather.py --type warnings                   # 天氣警告

參數:
    --type: current, forecast, hourly, warnings
    --days: 預報天數 (僅 forecast 類型需要，默认 9)
    --lang: en, tc (默认 tc)
"""

import argparse
import json
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from datetime import datetime

# API 基址
BASE_URL = "https://data.weather.gov.hk/weatherAPI/opendata/weather.php"

# 天氣警告類型映射 (繁體中文)
WARNING_NAMES = {
    "RAINSTM": "暴雨警告",
    "TYHOON": "颱風警告",
    "HEAT": "高溫天氣",
    "COLD": "寒冷天氣",
    "FIRE": "火災危險警告",
    "FLOOD": "山洪暴發警告",
    "LANDSLP": "山泥傾瀉警告",
    "WIND": "強烈季候風信號",
    "TSTORM": "雷暴提示",
    "UV": "紫外線指數",
    "RS": "暴雨警告",  # Rainstorm
    "TC": "颱風警告",  # Tropical Cyclone
}

# 分區名稱映射
REGION_NAMES = {
    "Central": "中環",
    "Wan Chai": "灣仔",
    "Causeway Bay": "銅鑼灣",
    "Victoria Park": "維多利亞公園",
    "Tsim Sha Tsui": "尖沙咀",
    "Kowloon City": "九龍城",
    "Sha Tin": "沙田",
    "Tai Po": "大埔",
    "Tuen Mun": "屯門",
    "Yuen Long": "元朗",
    "Tsuen Wan": "荃灣",
    "Disneyland Resort": "迪士尼樂園",
    "Chek Lap Kok": "赤鱲角",
    "Stanley": "赤柱",
}


def fetch_api_data(data_type, lang="tc"):
    """獲取 API 數據"""
    params = f"dataType={data_type}&lang={lang}"
    url = f"{BASE_URL}?{params}"
    
    try:
        req = Request(url, headers={"User-Agent": "HKO-Weather-Skill/1.0"})
        with urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        print(f"❌ HTTP 錯誤：{e.code}", file=sys.stderr)
        return None
    except URLError as e:
        print(f"❌ 網絡錯誤：{e.reason}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析錯誤：{e}", file=sys.stderr)
        return None


def format_current_weather(data):
    """格式化即時天氣 (rhrread)"""
    if not data:
        return "❌ 無法獲取天氣數據"
    
    lines = ["🌡️ 香港即時天氣"]
    
    # 獲取温度 (嵌套在 temperature.data 陣列中)
    if "temperature" in data and "data" in data["temperature"]:
        temp_data = data["temperature"]["data"]
        if temp_data and len(temp_data) > 0:
            # 找香港天文台的數據
            hko_temp = None
            for item in temp_data:
                if "香港天文台" in item.get("place", ""):
                    hko_temp = item.get("value")
                    break
            if hko_temp is None and len(temp_data) > 0:
                hko_temp = temp_data[0].get("value")
            lines.append(f"   溫度：{hko_temp}°C")
        else:
            lines.append("   溫度：N/A")
    else:
        lines.append("   溫度：N/A")
    
    # 獲取濕度 (嵌套在 humidity.data 陣列中)
    if "humidity" in data and "data" in data["humidity"]:
        humidity_data = data["humidity"]["data"]
        if humidity_data and len(humidity_data) > 0:
            humidity_val = humidity_data[0].get("value", "N/A")
            lines.append(f"   濕度：{humidity_val}%")
        else:
            lines.append("   濕度：N/A")
    else:
        lines.append("   濕度：N/A")
    
    # 分區氣溫
    if "temperature" in data and "data" in data["temperature"]:
        temp_data = data["temperature"]["data"]
        if temp_data:
            lines.append("")
            lines.append("📍 分區氣溫:")
            for region in temp_data[:8]:  # 顯示前 8 個
                place = region.get("place", "未知")
                temp = region.get("value", "N/A")
                lines.append(f"   {place}: {temp}°C")
    
    # 紫外線指數
    if "uvindex" in data and data["uvindex"]:
        lines.append(f"   紫外線：{data['uvindex']}")
    
    # 圖標
    if "icon" in data:
        lines.append(f"   天氣圖標代碼：{data['icon']}")
    
    return "\n".join(lines)


def format_forecast(data, days=9):
    """格式化九天天氣預報 (fnd)"""
    if not data or "weatherForecast" not in data:
        return "❌ 無法獲取預報數據"

    forecasts = data["weatherForecast"][:days]
    title = "📅 九天天氣預報" if days >= 9 else f"📅 {days} 天氣預報"
    lines = [title]

    for fc in forecasts:
        date = fc.get("forecastDate", "N/A")
        # 處理日期格式 (YYYYMMDD -> YYYY-MM-DD)
        if len(date) == 8:
            date = f"{date[:4]}-{date[4:6]}-{date[6:8]}"

        # 處理嵌套的溫度數據
        temp_min_obj = fc.get("forecastMintemp", {})
        temp_max_obj = fc.get("forecastMaxtemp", {})
        temp_min = temp_min_obj.get("value", "N/A") if isinstance(temp_min_obj, dict) else temp_min_obj
        temp_max = temp_max_obj.get("value", "N/A") if isinstance(temp_max_obj, dict) else temp_max_obj

        # 處理嵌套的濕度數據
        rh_min_obj = fc.get("forecastMinrh", {})
        rh_max_obj = fc.get("forecastMaxrh", {})
        humidity_min = rh_min_obj.get("value", "N/A") if isinstance(rh_min_obj, dict) else rh_min_obj
        humidity_max = rh_max_obj.get("value", "N/A") if isinstance(rh_max_obj, dict) else rh_max_obj

        # 天氣概況
        weather = fc.get("forecastWeather", "")
        wind = fc.get("forecastWind", "")

        lines.append(f"   {date}")
        if weather:
            lines.append(f"      天氣：{weather}")
        if wind:
            lines.append(f"      風：{wind}")
        lines.append(f"      溫度：{temp_min}-{temp_max}°C")
        lines.append(f"      濕度：{humidity_min}-{humidity_max}%")

    return "\n".join(lines)


def format_hourly(data):
    """格式化本地天氣預報 (flw)

    HKO `flw` 主要提供概況式的本地天氣預報文字（唔係逐小時數值）。
    """
    if not data:
        return "❌ 無法獲取本地天氣預報"

    lines = ["🕒 本地天氣預報"]

    forecast_desc = data.get("forecastDesc") or data.get("forecastdesc")
    if forecast_desc:
        lines.append(f"   {forecast_desc}")

    outlook = data.get("outlook")
    if outlook:
        lines.append("")
        lines.append(f"🔭 展望：{outlook}")

    update_time = data.get("updateTime")
    if update_time:
        # 2026-03-22T08:45:00+08:00 -> 2026-03-22 08:45:00
        if "T" in update_time:
            update_time = update_time.replace("T", " ").split("+")[0]
        lines.append("")
        lines.append(f"⏱️ 更新時間：{update_time}")

    # 兼容顯示其他常見欄位（如果存在）
    general_situation = data.get("generalSituation")
    if general_situation:
        lines.append("")
        lines.append(f"🌤️ 概況：{general_situation}")

    return "\n".join(lines)


def format_regional_weather(data, location=None):
    """格式化分區天氣 (rhrread)"""
    if not data:
        return "❌ 無法獲取天氣數據"
    
    lines = ["📍 分區天氣"]
    
    # 獲取溫度數據
    if "temperature" in data and "data" in data["temperature"]:
        temp_data = data["temperature"]["data"]
        
        if location:
            # 查找指定地區
            found = False
            for station in temp_data:
                place = station.get("place", "")
                if location in place or place in location:
                    temp = station.get("value", "N/A")
                    lines.append(f"   {place}: {temp}°C")
                    found = True
            
            if not found:
                # 嘗試模糊匹配
                for station in temp_data:
                    place = station.get("place", "")
                    if location in place or place in location:
                        temp = station.get("value", "N/A")
                        lines.append(f"   {place}: {temp}°C")
                        found = True
                
                if not found:
                    return f"❌ 找不到地區 \"{location}\"，可用監測站包括：{', '.join([s.get('place', '') for s in temp_data[:10]])}..."
        else:
            # 顯示所有地區
            lines.append("")
            lines.append("🌡️ 各監測站氣溫:")
            for station in temp_data:
                place = station.get("place", "未知")
                temp = station.get("value", "N/A")
                lines.append(f"   {place}: {temp}°C")
    
    # 如果有指定地區，同時顯示該區降雨
    if location and "rainfall" in data and "data" in data["rainfall"]:
        rainfall_data = data["rainfall"]["data"]
        for area in rainfall_data:
            place = area.get("place", "")
            if location in place or place in location:
                rain = area.get("max", 0)
                if rain > 0:
                    lines.append(f"   🌧️ 過去一小時降雨：{rain}mm")
                else:
                    lines.append(f"   💧 過去一小時無降雨")
                break
    
    return "\n".join(lines)


def format_rainfall(data):
    """格式化降雨資訊 (rhrread)"""
    if not data:
        return "❌ 無法獲取降雨數據"
    
    lines = ["🌧️ 降雨資訊"]
    
    # 過去一小時降雨量 (分區)
    if "rainfall" in data and "data" in data["rainfall"]:
        rainfall_data = data["rainfall"]["data"]
        if rainfall_data:
            lines.append("")
            lines.append("📍 過去一小時降雨量:")
            
            # 整理有雨的地區
            rainy_areas = []
            dry_areas = []
            for area in rainfall_data:
                place = area.get("place", "未知")
                max_rain = area.get("max", 0)
                if max_rain > 0:
                    rainy_areas.append((place, max_rain))
                else:
                    dry_areas.append(place)
            
            if rainy_areas:
                lines.append("   ⛈️ 有降雨地區:")
                for place, rain in sorted(rainy_areas, key=lambda x: -x[1])[:10]:
                    lines.append(f"      {place}: {rain}mm")
            else:
                lines.append("   ✅ 全港乾燥，無降雨")
            
            # 顯示總站數
            lines.append(f"   監測站總數：{len(rainfall_data)}")
    
    # startTime 和 endTime
    if "rainfall" in data:
        start = data["rainfall"].get("startTime", "")
        end = data["rainfall"].get("endTime", "")
        if start and end:
            start = start.replace("T", " ").split("+")[0]
            end = end.replace("T", " ").split("+")[0]
            lines.append(f"   統計時段：{start} 至 {end}")
    
    return "\n".join(lines)


def format_rainfall_forecast(data, days=9):
    """格式化降雨預報 (fnd)"""
    if not data or "weatherForecast" not in data:
        return "❌ 無法獲取預報數據"
    
    forecasts = data["weatherForecast"][:days]
    lines = ["🌦️ 降雨預報"]
    
    rainy_days = []
    dry_days = []
    
    for fc in forecasts:
        date = fc.get("forecastDate", "N/A")
        if len(date) == 8:
            date = f"{date[:4]}-{date[4:6]}-{date[6:8]}"
        
        weather = fc.get("forecastWeather", "")
        psr = fc.get("PSR", "")  # 降水機率
        
        # 判斷會唔會落雨
        will_rain = False
        rain_keywords = ["雨", "驟雨", "大雨", "暴雨", "雷暴", "短暫時間有雨", "有雨"]
        for keyword in rain_keywords:
            if keyword in weather:
                will_rain = True
                break
        
        if will_rain or psr == "高":
            rainy_days.append((date, weather, psr))
        else:
            dry_days.append(date)
    
    # 顯示會落雨的日子
    if rainy_days:
        lines.append("")
        lines.append("⛈️ 會落雨的日子:")
        for date, weather, psr in rainy_days:
            psr_text = f" (降水機率：{psr})" if psr else ""
            lines.append(f"   {date}: {weather}{psr_text}")
    else:
        lines.append("   ✅ 未來幾日無雨")
    
    # 顯示乾燥日子
    if dry_days:
        lines.append("")
        lines.append("☀️ 乾燥日子:")
        lines.append(f"   {', '.join(dry_days[:5])}" + ("..." if len(dry_days) > 5 else ""))
    
    return "\n".join(lines)


def format_warnings(data):
    """格式化天氣警告 (warnsum)"""
    if not data:
        return "❌ 無法獲取警告數據"
    
    # 處理不同格式的回應
    warnings = []
    if isinstance(data, dict):
        if "warningSummary" in data:
            warnings = data["warningSummary"]
        elif "warnings" in data:
            warnings = data["warnings"]
        elif "warningType" in data:
            warnings = [data]
    
    if not warnings:
        return "✅ 目前無生效中天氣警告"
    
    lines = ["⚠️ 生效中天氣警告"]
    for w in warnings:
        w_type = w.get("warningType", "")
        w_name = w.get("name", WARNING_NAMES.get(w_type, w_type))
        status = w.get("status", "")
        effective = w.get("effectiveTime", "")
        
        # 檢查是否為中文名稱
        if isinstance(w_name, dict):
            w_name = w_name.get("tc", w_name.get("en", w_type))
        
        status_text = "🟢 生效中" if status == "ISSUED" else f"狀態：{status}"
        lines.append(f"   {w_name}")
        lines.append(f"      {status_text}")
        if effective:
            # 格式化時間
            if "T" in effective:
                effective = effective.replace("T", " ").split("+")[0]
            lines.append(f"      生效時間：{effective}")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="香港天氣 API 查詢工具")
    parser.add_argument("--type", required=True, 
                        choices=["current", "regional", "forecast", "hourly", "warnings", "rainfall", "rainfall-forecast"],
                        help="數據類型")
    parser.add_argument("--location", type=str, default=None,
                        help="指定地區 (僅 regional 類型需要，例如：沙田、香港天文台)")
    parser.add_argument("--days", type=int, default=9,
                        help="預報天數 (僅 forecast/rainfall-forecast 類型需要)")
    parser.add_argument("--lang", choices=["en", "tc"], default="tc",
                        help="語言 (默认：tc)")
    parser.add_argument("--json", action="store_true",
                        help="輸出原始 JSON")
    
    args = parser.parse_args()
    
    # 映射數據類型到 API dataType
    type_map = {
        "current": "rhrread",
        "regional": "rhrread",         # 使用 rhrread 的分區數據
        "forecast": "fnd",
        "hourly": "flw",
        "warnings": "warnsum",
        "rainfall": "rhrread",
        "rainfall-forecast": "fnd"
    }
    
    data_type = type_map[args.type]
    
    # 獲取數據
    data = fetch_api_data(data_type, lang=args.lang)
    
    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return
    
    # 格式化輸出
    if args.type == "current":
        output = format_current_weather(data)
    elif args.type == "regional":
        output = format_regional_weather(data, location=args.location)
    elif args.type == "forecast":
        output = format_forecast(data, days=args.days)
    elif args.type == "hourly":
        output = format_hourly(data)
    elif args.type == "warnings":
        output = format_warnings(data)
    elif args.type == "rainfall":
        output = format_rainfall(data)
    elif args.type == "rainfall-forecast":
        output = format_rainfall_forecast(data, days=args.days)
    else:
        output = "❌ 未知的數據類型"
    
    print(output)


if __name__ == "__main__":
    main()
