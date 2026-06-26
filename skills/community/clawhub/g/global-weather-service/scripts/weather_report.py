#!/usr/bin/env python3
import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime
from urllib.error import HTTPError, URLError

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
FETCH_RETRIES = 3
FETCH_RETRY_DELAY_SECONDS = 1.2

WMO_TEXT = {
    0: ("☀️", "晴"),
    1: ("🌤️", "晴间多云"),
    2: ("⛅", "多云"),
    3: ("⛅", "多云"),
    45: ("🌫️", "雾"),
    48: ("🌫️", "冻雾"),
    51: ("🌦️", "小毛毛雨"),
    53: ("🌦️", "毛毛雨"),
    55: ("🌧️", "浓毛毛雨"),
    56: ("🌨️", "冻毛毛雨"),
    57: ("🌨️", "强冻毛毛雨"),
    61: ("🌧️", "中雨"),
    63: ("🌧️", "中到大雨"),
    65: ("🌧️", "大雨"),
    66: ("🌨️", "冻雨"),
    67: ("🌨️", "强冻雨"),
    71: ("🌨️", "小雪"),
    73: ("🌨️", "中雪"),
    75: ("❄️", "大雪"),
    77: ("🌨️", "冰粒"),
    80: ("🌦️", "阵雨"),
    81: ("🌧️", "较强阵雨"),
    82: ("⛈️", "强阵雨"),
    85: ("🌨️", "阵雪"),
    86: ("❄️", "强阵雪"),
    95: ("⛈️", "雷暴"),
    96: ("⛈️", "雷暴伴小冰雹"),
    99: ("⛈️", "雷暴伴冰雹"),
}


def fetch_json(url: str, params: dict) -> dict:
    query = urllib.parse.urlencode(params)
    last_error = None
    for attempt in range(1, FETCH_RETRIES + 1):
        try:
            req = urllib.request.Request(
                f"{url}?{query}",
                headers={
                    "User-Agent": "OpenClaw weather skill",
                    "Accept": "application/json",
                },
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt < FETCH_RETRIES:
                time.sleep(FETCH_RETRY_DELAY_SECONDS * attempt)
            else:
                raise SystemExit(f"天气数据获取失败: {exc}") from exc
    raise SystemExit(f"天气数据获取失败: {last_error}")


def geocode(place: str, language: str) -> dict:
    data = fetch_json(GEOCODE_URL, {
        "name": place,
        "count": 5,
        "language": language,
        "format": "json",
    })
    results = data.get("results") or []
    if not results:
        raise SystemExit(f"未找到地点: {place}")
    return results[0]


def classify_cold_risk(tmax: float, tmin: float, rain_prob: float, wind: float) -> str:
    if tmin <= 8 or (rain_prob >= 80 and tmax <= 16):
        return "极易发"
    if tmin <= 12 or rain_prob >= 60 or wind >= 25:
        return "易发"
    if tmin <= 16 or rain_prob >= 30:
        return "较易发"
    return "较少发"


def classify_sport(rain_prob: float, precip: float, tmax: float, wind: float) -> str:
    if rain_prob >= 80 or precip >= 8 or wind >= 35:
        return "不适宜"
    if rain_prob >= 50 or precip >= 3 or tmax >= 32:
        return "不太适宜"
    if tmax >= 24 and rain_prob <= 20 and wind <= 25:
        return "很适宜"
    if rain_prob <= 40 and wind <= 30:
        return "适宜"
    return "较适宜"


def clothing_advice(tmax: float, tmin: float, rain_prob: float) -> str:
    if tmax <= 12:
        return "毛衣 / 厚外套 / 长裤"
    if tmax <= 18:
        return "长袖衬衫 / 薄卫衣 / 薄外套"
    if tmax <= 24 and tmin <= 12:
        return "长袖衬衫 / 薄外套 / 早晚加一件针织衫"
    if tmax <= 24:
        return "T恤 / 薄长袖 / 轻薄外套"
    if rain_prob >= 50:
        return "短袖 / 透气长袖 / 轻薄防雨外套"
    if tmax <= 28:
        return "T恤 / 薄衬衫 / 轻薄防晒外套"
    return "短袖 / 速干衣 / 轻薄防晒外套"


def uv_level(uv: float) -> str:
    if uv >= 8:
        return "强"
    if uv >= 6:
        return "较强"
    if uv >= 3:
        return "中等"
    return "弱"


def extra_advice(rain_prob: float, precip: float, tmax: float, tmin: float, uv: float) -> str:
    notes = []
    if rain_prob >= 60 or precip >= 3:
        notes.append("建议带伞")
    if uv >= 6:
        notes.append("建议涂防晒霜")
    if tmax - tmin >= 10:
        notes.append("昼夜温差较大")
    if tmax >= 28:
        notes.append("注意补水")
    if tmin <= 10:
        notes.append("早晚注意保暖")
    if not notes:
        notes.append("天气较平稳，按常规出行即可")
    return "，".join(notes)


def normalize_chinese_name(text: str) -> str:
    replacements = {
        "倫敦": "伦敦",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def build_title(place_data: dict, days: int) -> str:
    country = normalize_chinese_name(place_data.get("country", ""))
    admin1 = normalize_chinese_name(place_data.get("admin1", ""))
    name = normalize_chinese_name(place_data.get("name", ""))
    if country == "美国":
        location = f"{country}{name}"
    elif country == "中国":
        location = f"{country}{admin1}{name}" if admin1 else f"{country}{name}"
    else:
        location = f"{country}{name}" if country else name
    day_text = {7: "七", 1: "一", 2: "二"}.get(days, str(days))
    return f"#{location}近{day_text}日天气"


def format_date(iso_date: str) -> str:
    dt = datetime.strptime(iso_date, "%Y-%m-%d")
    return dt.strftime("%Y年%m月%d日")


def generate_report(place: str, days: int, language: str) -> str:
    place_data = geocode(place, language)
    forecast = fetch_json(FORECAST_URL, {
        "latitude": place_data["latitude"],
        "longitude": place_data["longitude"],
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,uv_index_max",
        "timezone": place_data.get("timezone", "auto"),
        "forecast_days": days,
    })
    daily = forecast["daily"]
    lines = [build_title(place_data, days)]
    for i, iso_date in enumerate(daily["time"]):
        code = daily["weather_code"][i]
        emoji, text = WMO_TEXT.get(code, ("🌤️", f"天气代码{code}"))
        tmax = daily["temperature_2m_max"][i]
        tmin = daily["temperature_2m_min"][i]
        precip = daily.get("precipitation_sum", [0] * len(daily["time"]))[i]
        rain_prob = daily.get("precipitation_probability_max", [0] * len(daily["time"]))[i]
        wind = daily.get("wind_speed_10m_max", [0] * len(daily["time"]))[i]
        uv = daily.get("uv_index_max", [0] * len(daily["time"]))[i]
        lines.extend([
            "",
            f"📍 {format_date(iso_date)}天气",
            f"{emoji} {text} | 温度：{tmax:.1f}/{tmin:.1f}℃",
            "",
            "📊 生活指数",
            f"🤧 感冒：{classify_cold_risk(tmax, tmin, rain_prob, wind)}",
            f"🏃 运动：{classify_sport(rain_prob, precip, tmax, wind)}",
            f"👔 穿衣：{clothing_advice(tmax, tmin, rain_prob)}",
            f"☀️ 紫外线：{uv_level(uv)}",
            f"❗ 其他建议：{extra_advice(rain_prob, precip, tmax, tmin, uv)}",
        ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a weather report from Open-Meteo.")
    parser.add_argument("place", help="City or place name, e.g. 洛杉矶 or Los Angeles")
    parser.add_argument("--days", type=int, default=7, help="Forecast days, default 7")
    parser.add_argument("--language", default="zh", help="Geocoding language, default zh")
    args = parser.parse_args()
    if not 1 <= args.days <= 16:
        raise SystemExit("days 必须在 1 到 16 之间")
    report = generate_report(args.place, args.days, args.language)
    sys.stdout.write(report + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
