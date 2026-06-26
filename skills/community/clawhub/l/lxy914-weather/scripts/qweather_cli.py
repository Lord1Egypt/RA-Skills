#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
和风天气 API 查询工具
支持实时天气、7 天预报、小时预报等
"""

import os
import sys
import json
import urllib.request
import urllib.error
import urllib.parse
import gzip
from typing import Dict, Any, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except:
        pass


class QWeatherAPI:
    """和风天气 API 客户端"""

    def __init__(self):
        self.api_key = os.environ.get("QWEATHER_API_KEY")
        self.base_url = os.environ.get("QWEATHER_BASE_URL")
        if not self.base_url:
            raise ValueError("请设置环境变量QWEATHER_BASE_URL")
        if not self.api_key:
            raise ValueError("请设置环境变量QWEATHER_API_KEY")

    def _make_request(self, endpoint: str, params: Dict[str, str]) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"

        query_params = "&".join(
            [f"{k}={urllib.parse.quote(str(v), safe='')}" for k, v in params.items()]
        )
        full_url = f"{url}?{query_params}"

        # 构建请求头 - 使用 X-QW-Api-Key 方式
        headers = {
            "X-QW-Api-Key": self.api_key,
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate",
        }

        try:
            request = urllib.request.Request(full_url, headers=headers)
            with urllib.request.urlopen(request, timeout=10) as response:
                data = response.read()
                encoding = response.getheader("Content-Encoding", "")

                if encoding == "gzip":
                    data = gzip.decompress(data)

                data = data.decode("utf-8")
                return json.loads(data)
        except urllib.error.HTTPError as e:
            error_data = e.read()
            try:
                error_data = error_data.decode("utf-8")
            except:
                try:
                    error_data = error_data.decode("gbk")
                except:
                    error_data = str(error_data)
            try:
                error_data = json.loads(error_data)
                raise Exception(
                    f"API 请求失败：{error_data.get('status', '未知错误')} - {error_data.get('detail', error_data.get('msg', ''))}"
                )
            except json.JSONDecodeError:
                raise Exception(f"API 请求失败：HTTP {e.code} - {error_data}")
        except Exception as e:
            raise Exception(f"请求失败：{str(e)}")

    def get_now(self, location: str) -> Dict[str, Any]:
        return self._make_request("/v7/weather/now", {"location": location})

    def get_daily(self, location: str, days: int = 7) -> Dict[str, Any]:
        days_map = {3: "3d", 7: "7d", 10: "10d", 15: "15d", 30: "30d"}
        if days not in days_map:
            days = 7
        days_param = days_map.get(days, "7d")
        return self._make_request(f"/v7/weather/{days_param}", {"location": location})

    def get_hourly(self, location: str, hours: int = 24) -> Dict[str, Any]:
        hours_map = {24: "24h", 72: "72h", 168: "168h"}
        if hours not in hours_map:
            hours = 24
        hours_param = hours_map.get(hours, "24h")
        return self._make_request(f"/v7/weather/{hours_param}", {"location": location})

    def get_location_id(self, city_name: str) -> Optional[str]:
        try:
            data = self._make_request("/geo/v2/city/lookup", {"location": city_name})
            if data.get("code") == "200" and data.get("location"):
                return data["location"][0]["id"]
        except:
            pass
        return None


def format_weather(data: Dict[str, Any], use_emoji: bool = True) -> str:
    """
    格式化天气数据为可读文本

    Args:
        data: API 返回的数据
        use_emoji: 是否使用 emoji 表情符号

    Returns:
        格式化后的天气信息
    """
    now = data.get("now", {})

    if use_emoji:
        lines = [
            "🌤️ 实时天气",
            "",
            f"🌡️ 温度：{now.get('temp', 'N/A')}°C",
            f"🤔 体感温度：{now.get('feelsLike', 'N/A')}°C",
            f"☁️ 天气：{now.get('text', 'N/A')}",
            f"💨 风向：{now.get('windDir', 'N/A')} {now.get('windScale', 'N/A')}级",
            f"💧 湿度：{now.get('humidity', 'N/A')}%",
            f"👁️ 能见度：{now.get('vis', 'N/A')}公里",
            f"🌡️ 气压：{now.get('pressure', 'N/A')}hPa",
        ]
    else:
        lines = [
            "实时天气",
            "",
            f"温度：{now.get('temp', 'N/A')}°C",
            f"体感温度：{now.get('feelsLike', 'N/A')}°C",
            f"天气：{now.get('text', 'N/A')}",
            f"风向：{now.get('windDir', 'N/A')} {now.get('windScale', 'N/A')}级",
            f"湿度：{now.get('humidity', 'N/A')}%",
            f"能见度：{now.get('vis', 'N/A')}公里",
            f"气压：{now.get('pressure', 'N/A')}hPa",
        ]

    return "\n".join(lines)


def format_daily_forecast(data: Dict[str, Any]) -> str:
    """
    格式化天气预报数据为可读文本

    Args:
        data: API 返回的数据

    Returns:
        格式化后的天气预报
    """
    daily = data.get("daily", [])

    lines = [
        "📅 天气预报",
        "",
    ]

    for day in daily:
        lines.append(f"📆 {day.get('fxDate', 'N/A')}")
        lines.append(
            f"   天气：{day.get('textDay', 'N/A')} / {day.get('textNight', 'N/A')}"
        )
        lines.append(
            f"   温度：{day.get('tempMax', 'N/A')}°C / {day.get('tempMin', 'N/A')}°C"
        )
        lines.append(
            f"   风向：{day.get('windDirDay', 'N/A')} {day.get('windScaleDay', 'N/A')}级"
        )
        lines.append("")

    return "\n".join(lines)


def format_hourly_forecast(data: Dict[str, Any], use_emoji: bool = True) -> str:
    """
    格式化小时预报数据为可读文本

    Args:
        data: API 返回的数据
        use_emoji: 是否使用 emoji

    Returns:
        格式化后的小时预报
    """
    hourly = data.get("hourly", [])

    if use_emoji:
        lines = [
            "⏰ 小时预报",
            "",
        ]
    else:
        lines = [
            "小时预报",
            "",
        ]

    for hour in hourly:
        time = hour.get("fxTime", "N/A")
        if "+08:00" in time:
            time = time.replace("+08:00", "").replace("T", " ")

        if use_emoji:
            lines.append(
                f"🕐 {time} | 🌡️ {hour.get('temp', 'N/A')}°C | ☁️ {hour.get('text', 'N/A')} | "
                f"💨 {hour.get('windDir', 'N/A')} {hour.get('windScale', 'N/A')}级 | 💧 {hour.get('humidity', 'N/A')}%"
            )
        else:
            lines.append(
                f"{time} | 温度: {hour.get('temp', 'N/A')}°C | 天气: {hour.get('text', 'N/A')} | "
                f"风向: {hour.get('windDir', 'N/A')} {hour.get('windScale', 'N/A')}级 | 湿度: {hour.get('humidity', 'N/A')}%"
            )

    return "\n".join(lines)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python qweather_cli.py <命令> [地点]")
        print("")
        print("命令:")
        print("  now <地点>      - 查询实时天气 (地点可以是城市名称或ID)")
        print("  daily <地点> [天数] - 查询天气预报")
        print("  hourly <地点> [小时] - 查询小时预报")
        print("")
        print("选项:")
        print("  --json         - 输出 JSON 格式")
        print("  --plain        - 纯文本模式（不使用 emoji）")
        print("")
        print("示例:")
        print("  python qweather_cli.py now 太原")
        print("  python qweather_cli.py now 101010100")
        print("  python qweather_cli.py daily 上海 3")
        print("  python qweather_cli.py hourly 北京 24")
        return

    command = sys.argv[1].lower()

    use_json = "--json" in sys.argv
    use_plain = "--plain" in sys.argv

    try:
        api = QWeatherAPI()
    except ValueError as e:
        print(f"错误：{e}")
        print("请设置环境变量 QWEATHER_API_KEY 和 QWEATHER_BASE_URL")
        return

    def resolve_location(location: str) -> str:
        if location.isdigit():
            return location
        loc_id = api.get_location_id(location)
        if loc_id:
            return loc_id
        raise Exception(f"未找到地点: {location}")

    if command == "now":
        if len(sys.argv) < 3:
            print("错误：请提供地点")
            return
        location = resolve_location(sys.argv[2])
        try:
            data = api.get_now(location)
            if use_json:
                print(json.dumps(data, ensure_ascii=False, indent=2))
            else:
                print(format_weather(data, use_emoji=not use_plain))
        except Exception as e:
            print(f"错误：{e}")

    elif command == "daily":
        if len(sys.argv) < 3:
            print("错误：请提供地点")
            return
        location = resolve_location(sys.argv[2])
        days = int(sys.argv[3]) if len(sys.argv) > 3 else 7
        try:
            data = api.get_daily(location, days)
            if use_json:
                print(json.dumps(data, ensure_ascii=False, indent=2))
            else:
                print(format_daily_forecast(data))
        except Exception as e:
            print(f"错误：{e}")

    elif command == "hourly":
        if len(sys.argv) < 3:
            print("错误：请提供地点")
            return
        location = resolve_location(sys.argv[2])
        hours = int(sys.argv[3]) if len(sys.argv) > 3 else 24
        try:
            data = api.get_hourly(location, hours)
            if use_json:
                print(json.dumps(data, ensure_ascii=False, indent=2))
            else:
                print(format_hourly_forecast(data, use_emoji=not use_plain))
        except Exception as e:
            print(f"错误：{e}")

    else:
        print(f"错误：未知命令 '{command}'")


if __name__ == "__main__":
    main()
