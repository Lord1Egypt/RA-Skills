#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
12306 高铁/火车票余票查询工具
数据源：12306 官方公开接口（kyfw.12306.cn），免费、权威、无需登录
"""
import json
import re
import sys
import os
import time
import urllib.request
import urllib.parse
import http.cookiejar

TIMEOUT = 20
BASE = "https://kyfw.12306.cn"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

# 车站代码表（首次运行自动拉取官方 station_name.js，本地缓存）
STATION_CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "station_codes.json")


def _fetch(url, cj, referer=None, data=None):
    """带超时的 HTTP 请求，失败立即返回 None"""
    req = urllib.request.Request(url, data=data)
    req.add_header("User-Agent", UA)
    if referer:
        req.add_header("Referer", referer)
    if data:
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    try:
        with opener.open(req, timeout=TIMEOUT) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception:
        return None


def _load_stations():
    """加载车站代码表：优先本地缓存，否则拉取官方 station_name.js"""
    if os.path.exists(STATION_CACHE):
        try:
            with open(STATION_CACHE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    raw = _fetch(BASE + "/otn/resources/js/framework/station_name.js?station_version=1.9300", http.cookiejar.CookieJar())
    if not raw:
        return None
    stations = {}
    for m in re.finditer(r"@([a-z]+)\|([^|]+)\|([A-Z]+)\|", raw):
        stations[m.group(2)] = m.group(3)
    if stations:
        try:
            with open(STATION_CACHE, "w", encoding="utf-8") as f:
                json.dump(stations, f, ensure_ascii=False)
        except Exception:
            pass
    return stations


def resolve_station(name, stations):
    """站名/拼音/代码模糊匹配，返回 (代码, 展示名) 列表"""
    if not stations:
        return []
    name = name.strip()
    # 1. 精确代码
    for n, c in stations.items():
        if c == name.upper():
            return [(c, n)]
    # 2. 精确站名
    if name in stations:
        return [(stations[name], name)]
    # 3. 模糊包含（站名包含关键词）
    hits = [(c, n) for n, c in stations.items() if name in n]
    if hits:
        return hits
    # 4. 拼音匹配（官方 station_name.js 第4段是拼音）
    raw = ""
    cache_file = STATION_CACHE
    if os.path.exists(cache_file):
        raw = open(cache_file, encoding="utf-8").read()
    if not raw:
        raw = _fetch(BASE + "/otn/resources/js/framework/station_name.js?station_version=1.9300", http.cookiejar.CookieJar()) or ""
    for m in re.finditer(r"@([a-z]+)\|([^|]+)\|([A-Z]+)\|([a-z]+)\|", raw):
        if m.group(4).startswith(name.lower()) or m.group(1) == name.lower():
            hits.append((m.group(3), m.group(2)))
    return hits


def query_tickets(from_name, to_name, date):
    """查询余票，返回格式化文本"""
    stations = _load_stations()
    if not stations:
        return "查询失败：无法获取车站代码表（网络异常），请稍后重试"

    from_hits = resolve_station(from_name, stations)
    to_hits = resolve_station(to_name, stations)
    if not from_hits:
        return "未找到车站：" + from_name + "，请检查站名（如：深圳北、邯郸东）"
    if not to_hits:
        return "未找到车站：" + to_name + "，请检查站名（如：深圳北、邯郸东）"

    # 多个匹配时按名称排序取第一个（如"深圳"→深圳站），提示用户可用更精确站名
    from_code, from_label = from_hits[0]
    to_code, to_label = to_hits[0]
    hint = ""
    if len(from_hits) > 1:
        hint = "（" + from_name + " 匹配多站：" + ", ".join(n for c, n in from_hits) + "，默认取 " + from_label + "）"
    if len(to_hits) > 1:
        hint += "（" + to_name + " 匹配多站：" + ", ".join(n for c, n in to_hits) + "，默认取 " + to_label + "）"

    # 建立 cookie 会话（12306 需要先访问 init 页面拿 cookie）
    cj = http.cookiejar.CookieJar()
    _fetch(BASE + "/otn/leftTicket/init?linktypeid=dc", cj, referer=BASE + "/otn/index/init")

    # 代码→站名反向映射（显示用）
    code2name = {c: n for n, c in stations.items()}

    params = urllib.parse.urlencode({
        "leftTicketDTO.train_date": date,
        "leftTicketDTO.from_station": from_code,
        "leftTicketDTO.to_station": to_code,
        "purpose_codes": "ADULT",
    })
    url = BASE + "/otn/leftTicket/queryG?" + params
    raw = _fetch(url, cj, referer=BASE + "/otn/leftTicket/init")
    if raw is None:
        return "查询失败：请求 12306 超时，请稍后重试"
    if raw.lstrip().startswith("<!DOCTYPE") or "<html" in raw[:200]:
        return (f"查询失败：{date} 可能超出预售期（12306 一般提前 15 天放票）或请求被限流，请换个日期或稍后重试")
    try:
        data = json.loads(raw)
    except Exception:
        return "查询失败：12306 返回异常，请稍后重试"

    if not data.get("status"):
        return "查询失败：12306 接口未返回数据（可能被限流），请稍后重试"

    result = data.get("data", {}).get("result", [])
    if not result:
        return f"未查询到 {from_label} -> {to_label} {date} 的车次（可能日期超出预售期或当日无车）"

    lines = [f"🚄 {from_label} → {to_label}（{date}）共 {len(result)} 个车次：" + (hint or ""), ""]
    seat_headers = [("商务座", 32), ("特等座", 20), ("一等座", 31), ("二等座", 30),
                    ("软卧", 23), ("动卧", 27), ("硬卧", 29), ("硬座", 26), ("无座", 22)]

    for i, item in enumerate(result, 1):
        p = item.split("|")
        if len(p) < 33:
            continue
        no = p[3]
        dep_code, dep_t = p[6], p[8]
        arr_code, arr_t = p[7], p[9]
        dur = p[10]
        can_book = p[11]

        dep_name = code2name.get(dep_code, dep_code)
        arr_name = code2name.get(arr_code, arr_code)

        seats = []
        for label, idx in seat_headers:
            if idx < len(p):
                v = p[idx]
                if v in ("", "无"):
                    continue
                if v == "*":
                    v = "候补"
                seats.append(f"{label}:{v}")
        seat_str = " | ".join(seats) if seats else "暂无余票"

        book_flag = "✅可订" if can_book == "Y" else "❌不可订"
        lines.append(f"{i}. {no} {dep_name}{dep_t} → {arr_name}{arr_t}（历时{dur}）{book_flag}")
        lines.append(f"   余票：{seat_str}")
        lines.append("")

    lines.append("数据来源：12306 官方（kyfw.12306.cn）｜余票实时变动，以 12306 为准")
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    if len(args) < 3:
        print("用法：python3 train_query.py <出发站> <到达站> <日期YYYY-MM-DD>")
        print("示例：python3 train_query.py 深圳北 邯郸东 2026-09-03")
        print("       python3 train_query.py 深圳 邯郸 2026-09-03,2026-09-05 （多日期）")
        return
    frm, to = args[0], args[1]
    dates = args[2].split(",")
    for i, d in enumerate(dates):
        if i > 0:
            print("")
        print(query_tickets(frm, to, d.strip()))


if __name__ == "__main__":
    main()
