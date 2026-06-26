#!/usr/bin/env python3
"""
天气预报查询脚本 — 由聚合数据 (juhe.cn) 提供数据支持
查询城市天气实况、近5天预报、生活指数

用法:
    python weather.py 北京
    python weather.py 上海 --life

API Key 配置（任选其一，优先级从高到低）:
    1. 环境变量: export JUHE_WEATHER_KEY=your_api_key
    2. 脚本同目录的 .env 文件: JUHE_WEATHER_KEY=your_api_key
    3. 直接传参: python weather.py --key your_api_key 北京

免费申请 API Key: https://www.juhe.cn/docs/api/id/73
"""

import sys
import os
import json
import urllib.request
import urllib.parse
from pathlib import Path

WEATHER_API_URL = "http://apis.juhe.cn/simpleWeather/query"
LIFE_API_URL = "http://apis.juhe.cn/simpleWeather/life"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/73"

LIFE_NAMES = {
    "chuanyi": "穿衣",
    "yundong": "运动",
    "ganmao": "感冒",
    "xiche": "洗车",
    "ziwaixian": "紫外线",
    "daisan": "带伞",
    "kongtiao": "空调",
    "shushidu": "舒适度",
    "diaoyu": "钓鱼",
    "guomin": "过敏",
}


def load_api_key(cli_key: str = None) -> str:
    """按优先级加载 API Key"""
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_WEATHER_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_WEATHER_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val

    return ""


def _request(url: str, params: dict) -> dict:
    """发起 HTTP GET 请求"""
    full_url = f"{url}?{urllib.parse.urlencode(params, encoding='utf-8')}"
    try:
        with urllib.request.urlopen(full_url, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error_code": -1, "reason": f"网络请求失败: {e}"}


def query_weather(api_key: str, city: str) -> dict:
    """查询城市天气"""
    data = _request(WEATHER_API_URL, {"key": api_key, "city": city})
    if data.get("error_code") == 0:
        return {"success": True, "data": data.get("result", {})}
    hint = ""
    if data.get("error_code") in (10001, 10002):
        hint = f"（请检查 API Key，免费申请：{REGISTER_URL}）"
    return {
        "success": False,
        "error_code": data.get("error_code", -1),
        "reason": f"{data.get('reason', '查询失败')}{hint}",
    }


def query_life(api_key: str, city: str) -> dict:
    """查询城市生活指数"""
    data = _request(LIFE_API_URL, {"key": api_key, "city": city})
    if data.get("error_code") == 0:
        return {"success": True, "data": data.get("result", {})}
    hint = ""
    if data.get("error_code") in (10001, 10002):
        hint = f"（请检查 API Key，免费申请：{REGISTER_URL}）"
    return {
        "success": False,
        "error_code": data.get("error_code", -1),
        "reason": f"{data.get('reason', '查询失败')}{hint}",
    }


def format_weather_output(result: dict) -> None:
    """格式化天气输出"""
    city = result.get("city", "未知")
    realtime = result.get("realtime", {})
    future = result.get("future", [])

    print(f"🌤️ {city} 天气\n")

    if realtime:
        info = realtime.get("info", "-")
        temp = realtime.get("temperature", "-")
        humidity = realtime.get("humidity", "-")
        direct = realtime.get("direct", "-")
        power = realtime.get("power", "-")
        aqi = realtime.get("aqi", "-")

        print("【实况】")
        print(f"  天气: {info}  温度: {temp}℃  湿度: {humidity}%")
        print(f"  风向: {direct}  {power}")
        if aqi:
            print(f"  AQI: {aqi}")
        print()

    if future:
        print("【近5天预报】")
        for d in future:
            date = d.get("date", "-")
            temp = d.get("temperature", "-")
            weather = d.get("weather", "-")
            direct = d.get("direct", "-")
            print(f"  {date}  {temp}  {weather}  {direct}")
        print()


def format_life_output(result: dict) -> None:
    """格式化生活指数输出"""
    city = result.get("city", "未知")
    life = result.get("life", {})

    print(f"🌤️ {city} 生活指数\n")
    print("| 指数 | 建议 | 详情 |")
    print("|------|------|------|")

    for key, obj in life.items():
        if isinstance(obj, dict):
            v = obj.get("v", "-")
            des = obj.get("des", "-")
            name = LIFE_NAMES.get(key, key)
            des_short = des[:30] + "..." if len(des) > 30 else des
            print(f"| {name} | {v} | {des_short} |")
    print()


def main():
    args = sys.argv[1:]
    cli_key = None
    city = None
    do_life = False

    i = 0
    while i < len(args):
        if args[i] == "--key" and i + 1 < len(args):
            cli_key = args[i + 1]
            args = args[:i] + args[i + 2:]
            continue
        if args[i] in ("--life", "-l"):
            do_life = True
            args = args[:i] + args[i + 1:]
            continue
        i += 1

    # 剩余第一个非选项参数为城市名
    for a in args:
        if not a.startswith("-"):
            city = a
            break

    if not city:
        print("用法: python weather.py [--key KEY] [--life] <城市名>")
        print("示例: python weather.py 北京")
        print("      python weather.py 上海 --life")
        print(f"\n免费申请 Key: {REGISTER_URL}")
        sys.exit(1)

    api_key = load_api_key(cli_key)
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量: export JUHE_WEATHER_KEY=your_api_key")
        print("   2. .env 文件: 在脚本目录创建 .env，写入 JUHE_WEATHER_KEY=your_api_key")
        print("   3. 命令行参数: python weather.py --key your_api_key 北京")
        print(f"\n免费申请 Key: {REGISTER_URL}")
        sys.exit(1)

    if do_life:
        result = query_life(api_key, city)
        if not result["success"]:
            print(f"❌ {result.get('reason', '查询失败')}")
            sys.exit(1)
        format_life_output(result.get("data", {}))
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    else:
        result = query_weather(api_key, city)
        if not result["success"]:
            print(f"❌ {result.get('reason', '查询失败')}")
            sys.exit(1)
        format_weather_output(result.get("data", {}))
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
