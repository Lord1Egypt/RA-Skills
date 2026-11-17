# -*- coding: utf-8 -*-
"""
env_tools.py —— 环境查询：地理编码 / 日出日落 / 天气（Open-Meteo，免 key，国内可直连）。
纯 Python 标准库。

子命令:
    geocode 地名                    地名 -> 坐标（+ 开放时间，高德源才有）
    sun    lat lon 日期             某地某天日出日落
    weather lat lon 日期 [起-止]    某地某天天气（可选只看某几个小时，如 16-20）
    trip   地名 日期                geocode + sun + weather 一次打包 —— 规划时优先用这个，
                                    一次调用拿全，省得 agent 来回跑三轮

设计要点:
  日落是天文计算，给定坐标和日期就是确定值，不需要"智能"；agent 的价值不在
  算出 18:42，而在推出"所以你 16:50 必须出门"。
  失败原因必须如实带回去：之前把所有失败吞成「找不到这个地方」，结果分不清
  是名字写错了还是数据源挂了，排查全靠猜。
"""

import datetime
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

TIMEOUT = 12
PROFILE_PATH = Path(__file__).resolve().parent.parent / "data" / "profile.json"

WMO = {
    0: "晴", 1: "晴间多云", 2: "多云", 3: "阴",
    45: "雾", 48: "雾凇",
    51: "小毛毛雨", 53: "毛毛雨", 55: "大毛毛雨",
    56: "冻毛毛雨", 57: "强冻毛毛雨",
    61: "小雨", 63: "中雨", 65: "大雨",
    66: "冻雨", 67: "强冻雨",
    71: "小雪", 73: "中雪", 75: "大雪", 77: "雪粒",
    80: "阵雨", 81: "强阵雨", 82: "暴雨",
    85: "阵雪", 86: "强阵雪",
    95: "雷阵雨", 96: "雷阵雨伴冰雹", 99: "强雷阵雨伴冰雹",
}


def die(msg, hint=""):
    print("[错误] " + msg, file=sys.stderr)
    if hint:
        print("       " + hint, file=sys.stderr)
    sys.exit(1)


def load_profile():
    try:
        with open(PROFILE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        die("找不到 %s" % PROFILE_PATH)


def http_json(url, params, timeout=TIMEOUT):
    q = urllib.parse.urlencode(params)
    r = urllib.request.Request(url + "?" + q,
                               headers={"User-Agent": "apple-calpal/1.0"})
    with urllib.request.urlopen(r, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ---------------------------------------------------------------- 地理编码
def geocode(name):
    """
    地名 -> 坐标。三个源依次降级，失败时把各源的情况如实带回：
      高德        国内 POI 最准，坐标是 GCJ-02，和路径规划同一坐标系。需要 key。
      Open-Meteo  快，但中文 POI 覆盖极窄，连「颐和园」都查不到。
      Nominatim   中文覆盖不错但国内访问不稳定，实测整片超时，只配当最后兜底。
    """
    problems = []
    for label, fn in (("高德", _geocode_amap), ("Open-Meteo", _geocode_openmeteo),
                      ("Nominatim", _geocode_nominatim)):
        try:
            r = fn(name)
            if r:
                return r
            problems.append("%s 无结果" % label)
        except OSError as e:
            problems.append("%s 超时/网络(%s)" % (label, type(e).__name__))
        except Exception as e:
            problems.append("%s 异常(%s)" % (label, type(e).__name__))
    return {"error": "查不到「%s」。各源情况：%s" % (name, "；".join(problems))}


def _geocode_amap(name):
    prof = load_profile()
    if not prof.get("amap_key"):
        return None
    # 必须先限定城市再全国搜：不限定的话「沙河」会命中河北沙河市，
    # 几百公里的偏差而且不报错。有些 POI 没有 location 字段，要往后翻。
    key = prof["amap_key"]
    for extra in ({"city": prof.get("city_code") or "010"}, {}):
        d = http_json("https://restapi.amap.com/v3/place/text", dict({
            "keywords": name, "key": key, "offset": 10, "page": 1,
            "extensions": "all",        # 只有 all 才带 biz_ext（开放时间在里面）
        }, **extra))
        if d.get("status") != "1":
            raise RuntimeError("高德：%s（%s）" % (d.get("info"), d.get("infocode")))
        for p in (d.get("pois") or [])[:8]:
            loc = p.get("location") or ""
            if "," not in loc:
                continue
            try:
                lon, lat = (float(x) for x in loc.split(","))
            except ValueError:
                continue
            return {
                "name": p.get("name") or name, "lat": lat, "lon": lon,
                "admin": p.get("cityname") or "", "country": "中国",
                "source": "amap", "open_hours": _open_hours(p),
            }
    return None


def _open_hours(p):
    """营业/开放时间。取不到就返回 None，别编 —— 这是「到了发现进不去」的唯一防线。"""
    biz = p.get("biz_ext")
    if not isinstance(biz, dict):       # 高德有时返回空列表而不是对象
        return None
    for k in ("opentime2", "opentime_today", "opentime_week"):
        v = biz.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()[:400]      # 有的描述极长，截断免得撑爆上下文
    return None


def _geocode_openmeteo(name):
    hits = http_json("https://geocoding-api.open-meteo.com/v1/search",
                     {"name": name, "count": 1, "language": "zh", "format": "json"}).get("results") or []
    if not hits:
        return None
    h = hits[0]
    return {"name": h.get("name"), "lat": h["latitude"], "lon": h["longitude"],
            "admin": h.get("admin1") or "", "country": h.get("country") or "",
            "source": "open-meteo"}


def _geocode_nominatim(name):
    try:
        hits = http_json("https://nominatim.openstreetmap.org/search",
                         {"q": name, "format": "json", "limit": 1, "accept-language": "zh"})
    except (OSError, ValueError):
        return None
    if not hits:
        return None
    h = hits[0]
    parts = [p.strip() for p in (h.get("display_name") or "").split(",") if p.strip()]
    return {"name": parts[0] if parts else name, "lat": float(h["lat"]),
            "lon": float(h["lon"]), "admin": parts[3] if len(parts) > 3 else "",
            "country": parts[-1] if parts else "", "source": "nominatim"}


# ---------------------------------------------------------------- 日出日落 / 天气
def sun_times(lat, lon, date):
    d = http_json("https://api.open-meteo.com/v1/forecast", {
        "latitude": lat, "longitude": lon,
        "daily": "sunrise,sunset,daylight_duration",
        "timezone": "Asia/Shanghai", "start_date": date, "end_date": date,
    })["daily"]
    if not d.get("sunrise") or not d["sunrise"][0]:
        return None
    return {"date": date,
            "sunrise": d["sunrise"][0][-5:], "sunset": d["sunset"][0][-5:],
            "daylight_hours": round((d.get("daylight_duration") or [0])[0] / 3600, 1)}


def weather(lat, lon, date, hours=None):
    j = http_json("https://api.open-meteo.com/v1/forecast", {
        "latitude": lat, "longitude": lon,
        "hourly": "temperature_2m,precipitation_probability,weathercode",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weathercode",
        "timezone": "Asia/Shanghai", "start_date": date, "end_date": date,
    })
    hourly = []
    h = j["hourly"]
    for i, t in enumerate(h["time"]):
        hh = int(t[11:13])
        if hours is not None and hh not in hours:
            continue
        hourly.append({"time": t[-5:], "temp": h["temperature_2m"][i],
                       "rain_prob": h["precipitation_probability"][i],
                       "sky": WMO.get(h["weathercode"][i], "未知")})
    d = j["daily"]
    return {"date": date, "temp_min": d["temperature_2m_min"][0],
            "temp_max": d["temperature_2m_max"][0],
            "rain_prob_max": d["precipitation_probability_max"][0],
            "sky": WMO.get(d["weathercode"][0], "未知"), "hourly": hourly}


# ---------------------------------------------------------------- 入口
def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return
    cmd = a[0]

    if cmd == "geocode":
        if len(a) < 2:
            die("geocode 需要地名")
        print(json.dumps(geocode(a[1]), ensure_ascii=False, indent=2))
        return

    if cmd == "sun":
        if len(a) < 4:
            die("sun 需要 lat lon 日期")
        print(json.dumps(sun_times(float(a[1]), float(a[2]), a[3]), ensure_ascii=False))
        return

    if cmd == "weather":
        if len(a) < 4:
            die("weather 需要 lat lon 日期")
        hours = None
        if len(a) > 4 and "-" in a[4]:
            lo, hi = a[4].split("-")
            hours = set(range(int(lo), int(hi) + 1))
        print(json.dumps(weather(float(a[1]), float(a[2]), a[3], hours),
                         ensure_ascii=False, indent=2))
        return

    if cmd == "trip":
        if len(a) < 3:
            die("trip 需要地名 日期（YYYY-MM-DD）")
        place, date = a[1], a[2]
        loc = geocode(place)
        if loc.get("error"):
            print(json.dumps(loc, ensure_ascii=False, indent=2))
            sys.exit(1)
        out = {"place": loc}
        try:
            out["sun"] = sun_times(loc["lat"], loc["lon"], date)
            out["weather"] = weather(loc["lat"], loc["lon"], date)
        except OSError as e:
            out["error"] = "天气/日落查询失败：%s" % e
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    die("未知子命令 %r" % cmd, "可用：geocode / sun / weather / trip")


if __name__ == "__main__":
    main()
