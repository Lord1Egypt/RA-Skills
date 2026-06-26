#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
jisu-travel: 同程旅行信息聚合 + 极速数据火车查询

- flight: 航班入口与相关链接
- scenery: 景点入口与相关链接
- train_station2s / train_line / train_ticket: 使用极速数据火车接口
"""

from __future__ import annotations

import argparse
import json
import os
import re
import urllib.parse
from typing import Dict, List

import requests
from bs4 import BeautifulSoup

LY_HOME = "https://www.ly.com/"
TRAIN_STATION2S_URL = "https://api.jisuapi.com/train/station2s"
TRAIN_LINE_URL = "https://api.jisuapi.com/train/line"
TRAIN_TICKET_URL = "https://api.jisuapi.com/train/ticket"
DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
_AIRPORT_CODE_BY_CITY: Dict[str, str] = {}

# 对常见多机场城市给默认优先值（只在 city->code 自动补全时生效）
CITY_CODE_PREFERRED = {
    "北京": "PEK",
    "上海": "SHA",
    "成都": "TFU",
    "广州": "CAN",
    "深圳": "SZX",
    "杭州": "HGH",
    "重庆": "CKG",
    "西安": "XIY",
    "南京": "NKG",
    "昆明": "KMG",
    "武汉": "WUH",
}


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())


def _safe_get(url: str, timeout: float, ua: str) -> str:
    headers = {"User-Agent": ua or DEFAULT_UA}
    r = requests.get(url, headers=headers, timeout=timeout)
    r.raise_for_status()
    return r.text


def _load_airport_city_code_map() -> Dict[str, str]:
    global _AIRPORT_CODE_BY_CITY
    if _AIRPORT_CODE_BY_CITY:
        return _AIRPORT_CODE_BY_CITY

    md_path = os.path.join(os.path.dirname(__file__), "airport.md")
    m: Dict[str, str] = {}
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line or "\t" not in line:
                    continue
                if line.startswith("代码\t"):
                    continue
                parts = line.split("\t")
                if len(parts) < 3:
                    continue
                code = _norm(parts[0]).upper()
                city = _norm(parts[2])
                if not code or not city:
                    continue
                if not re.fullmatch(r"[A-Z]{3}", code):
                    continue
                # 已有映射时保留先到先得，后续通过 CITY_CODE_PREFERRED 覆盖
                if city not in m:
                    m[city] = code
    except Exception:
        m = {}

    for c, preferred in CITY_CODE_PREFERRED.items():
        if re.fullmatch(r"[A-Z]{3}", preferred):
            m[c] = preferred
    _AIRPORT_CODE_BY_CITY = m
    return _AIRPORT_CODE_BY_CITY


def _city_to_airport_code(city: str) -> str:
    c = _norm(city)
    if not c:
        return ""
    m = _load_airport_city_code_map()
    return _norm(m.get(c, "")).upper()


def _extract_flights_from_itinerary(html: str, limit: int = 30) -> List[Dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text("\n", strip=True)
    lines = [_norm(x) for x in text.splitlines() if _norm(x)]
    out: List[Dict[str, str]] = []
    seen = set()

    for i, line in enumerate(lines):
        m = re.search(r"([A-Z]{2}\d{3,4})", line)
        if not m:
            continue
        flight_no = m.group(1)
        airline = _norm(line.replace(flight_no, "").replace("｜", " ").replace("|", " "))
        if not airline:
            continue

        depart_time = ""
        depart_airport = ""
        arrive_time = ""
        arrive_airport = ""
        duration = ""
        price_from = ""
        cabin = ""

        window = lines[i + 1 : i + 20]
        wi = 0
        while wi < len(window):
            w = window[wi]
            nxt = window[wi + 1] if wi + 1 < len(window) else ""

            if not depart_time and re.match(r"^\d{1,2}:\d{2}$", w):
                depart_time = w
                if "机场" in nxt:
                    depart_airport = nxt
                    wi += 2
                    continue

            if depart_time and not duration and re.match(r"^\d+h\d+m$", w):
                duration = w
                wi += 1
                continue

            if depart_time and not arrive_time and re.match(r"^\d{1,2}:\d{2}$", w):
                if w != depart_time:
                    arrive_time = w
                    if "机场" in nxt:
                        arrive_airport = nxt
                        wi += 2
                        continue

            if not price_from:
                pm = re.search(r"¥\s*([0-9]+)", w)
                if pm:
                    price_from = pm.group(1)
                    # 常见结构：¥2540 / 起 / 8折经济舱
                    if nxt == "起" and wi + 2 < len(window):
                        maybe_cabin = _norm(window[wi + 2])
                        if maybe_cabin and maybe_cabin not in ("选择", "立减0"):
                            cabin = maybe_cabin
                    wi += 1
                    continue

            wi += 1

        key = (flight_no, depart_time, arrive_time)
        if key in seen:
            continue
        seen.add(key)
        out.append(
            {
                "flight_no": flight_no,
                "airline": airline or "无",
                "depart_time": depart_time or "无",
                "depart_airport": depart_airport or "无",
                "arrive_time": arrive_time or "无",
                "arrive_airport": arrive_airport or "无",
                "duration": duration or "无",
                "price_from": price_from or "",
                "cabin": cabin or "无",
            }
        )
        if len(out) >= max(1, min(int(limit), 100)):
            break

    return out


def _flight_time_to_minutes(s: str) -> int:
    t = _norm(s)
    m = re.match(r"^(\d{1,2}):(\d{2})$", t)
    if not m:
        return 99_999
    return int(m.group(1)) * 60 + int(m.group(2))


def _flight_price_to_int(s: str) -> int:
    t = _norm(s)
    m = re.search(r"(\d+)", t)
    if not m:
        return 9_999_999
    return int(m.group(1))


def _sort_flights(
    flights: List[Dict[str, str]],
    sort_by: str,
    sort_order: str,
) -> List[Dict[str, str]]:
    sb = _norm(sort_by).lower()
    so = _norm(sort_order).lower()
    reverse = so in ("desc", "down", "reverse")

    if sb in ("price", "fare"):
        return sorted(
            flights,
            key=lambda x: (
                _flight_price_to_int(str(x.get("price_from", ""))),
                _flight_time_to_minutes(str(x.get("depart_time", ""))),
            ),
            reverse=reverse,
        )
    if sb in ("time", "depart_time", "departure"):
        return sorted(
            flights,
            key=lambda x: (
                _flight_time_to_minutes(str(x.get("depart_time", ""))),
                _flight_price_to_int(str(x.get("price_from", ""))),
            ),
            reverse=reverse,
        )
    return flights


def _to_abs_url(url: str) -> str:
    u = _norm(url)
    if not u:
        return ""
    if u.startswith("//"):
        return "https:" + u
    if u.startswith("/"):
        return "https://www.ly.com" + u
    return u


def _extract_sceneries_from_search(html: str, limit: int = 20) -> List[Dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    out: List[Dict[str, str]] = []
    seen = set()

    cards = soup.select("#sceneryListInfo .scenery_list")
    for card in cards:
        name_tag = card.select_one("a.sce_name")
        if not name_tag:
            continue

        name = _norm(name_tag.get_text(strip=True))
        if not name:
            continue

        detail_url = _to_abs_url(str(name_tag.get("href", "")))
        level = _norm(card.select_one(".s_level").get_text(strip=True) if card.select_one(".s_level") else "")

        city = ""
        city_tag = card.select_one(".sce_address a")
        if city_tag:
            city = _norm(city_tag.get_text(strip=True))

        address = ""
        for p in card.select("dd p"):
            txt = _norm(p.get_text(" ", strip=True))
            if txt.startswith("地址："):
                address = _norm(txt.replace("地址：", "", 1))
                break

        feature = ""
        for p in card.select("dd p"):
            txt = _norm(p.get_text(" ", strip=True))
            if txt.startswith("特色："):
                feature = _norm(txt.replace("特色：", "", 1))
                break

        price_val = ""
        price_b = card.select_one(".price_b b")
        if price_b:
            price_val = _norm(price_b.get_text(strip=True))
        if not price_val:
            pb = card.select_one(".price_b")
            if pb:
                m = re.search(r"¥\s*([0-9]+)", _norm(pb.get_text(" ", strip=True)))
                if m:
                    price_val = m.group(1)
        price_from = ("¥" + price_val) if price_val else ""

        key = (name, detail_url)
        if key in seen:
            continue
        seen.add(key)

        out.append(
            {
                "name": name,
                "city": city or "无",
                "level": level or "无",
                "address": address or "无",
                "feature": feature or "无",
                "price_from": price_from or "",
                "url": detail_url or "",
            }
        )
        if len(out) >= max(1, min(int(limit), 100)):
            break

    return out


def _scenery_sort_to_code(v: str) -> str:
    s = _norm(v).lower()
    if s in ("", "recommend", "recommended", "default", "tuijian", "推荐"):
        return "0"
    if s in ("popular", "hot", "renqi", "人气"):
        return "4"
    if s in ("level", "grade", "jibie", "级别"):
        return "2"
    return "0"


def _scenery_sort_to_name(code: str) -> str:
    c = _norm(code)
    if c == "4":
        return "人气"
    if c == "2":
        return "级别"
    return "推荐"


def _build_search_url(channel: str, req: Dict[str, object]) -> str:
    if channel == "flight":
        from_city = _norm(str(req.get("from_city", "")))
        to_city = _norm(str(req.get("to_city", "")))
        depart_date = _norm(str(req.get("depart_date", ""))) or _norm(str(req.get("date", "")))
        return_date = _norm(str(req.get("return_date", "")))
        trip_type = _norm(str(req.get("trip_type", ""))) or "oneway"
        from_code = _norm(str(req.get("from_code", ""))).upper() or _city_to_airport_code(from_city)
        to_code = _norm(str(req.get("to_code", ""))).upper() or _city_to_airport_code(to_city)

        if from_code and to_code and depart_date:
            path = "https://www.ly.com/flights/itinerary/%s/%s-%s" % (
                "round" if trip_type == "round" else "oneway",
                from_code,
                to_code,
            )
            qs = [
                "from=%s" % urllib.parse.quote(from_city, safe=""),
                "to=%s" % urllib.parse.quote(to_city, safe=""),
                "date=%s" % urllib.parse.quote(depart_date, safe="-"),
                "fromairport=%s" % urllib.parse.quote(_norm(str(req.get("from_airport", ""))), safe=""),
                "toairport=%s" % urllib.parse.quote(_norm(str(req.get("to_airport", ""))), safe=""),
            ]
            if return_date and trip_type == "round":
                qs.append("returndate=%s" % urllib.parse.quote(return_date, safe="-"))
            return path + "?" + "&".join(qs)

        qs = []
        if from_city:
            qs.append("fromCity=%s" % from_city)
        if to_city:
            qs.append("toCity=%s" % to_city)
        if depart_date:
            qs.append("fromDate=%s" % depart_date)
        if return_date:
            qs.append("backDate=%s" % return_date)
        if trip_type:
            qs.append("tripType=%s" % trip_type)
        base = "https://www.ly.com/flights/home"
        return base + (("?" + "&".join(qs)) if qs else "")

    if channel == "scenery":
        city = _norm(str(req.get("city", "")))
        keyword = _norm(str(req.get("keyword", "")))
        q = _norm("%s %s" % (city, keyword))
        if not q:
            q = "热门景点"
        sort_code = _scenery_sort_to_code(str(req.get("scenery_sort", "")))
        return "https://so.ly.com/scenery?q=%s&sort=%s" % (
            urllib.parse.quote(q, safe=""),
            urllib.parse.quote(sort_code, safe=""),
        )

    return LY_HOME


def _ly_channel(channel: str, req: Dict[str, object], timeout: float, ua: str) -> Dict[str, object]:
    entry = {
        "flight": "https://www.ly.com/flights/",
        "scenery": "https://www.ly.com/scenery/",
    }.get(channel, LY_HOME)
    search_url = _build_search_url(channel, req)
    result = {
        "ok": True,
        "provider": "ly.com",
        "channel": channel,
        "entry_url": entry,
        "search_url": search_url,
        "request": req,
        "source": LY_HOME,
    }

    if channel == "flight" and "/flights/itinerary/" in search_url:
        try:
            html2 = _safe_get(search_url, timeout=timeout, ua=ua)
            limit_flights = max(1, min(int(req.get("limit_flights", 20) or 20), 100))
            # 先全量候选排序，再按 limit 截断，确保最低价/最早时间不会被提前截掉
            flights_all = _extract_flights_from_itinerary(html2, limit=100)
            sort_by = _norm(str(req.get("sort_by", ""))) or "price"
            sort_order = _norm(str(req.get("sort_order", ""))) or "asc"
            flights_all = _sort_flights(flights_all, sort_by=sort_by, sort_order=sort_order)
            flights = flights_all[:limit_flights]
            result["flight_count"] = len(flights)
            result["flights"] = flights
            result["flight_sort"] = {"sort_by": sort_by, "sort_order": sort_order}
        except Exception as e:
            result["flight_count"] = 0
            result["flights"] = []
            result["flight_error"] = str(e)

    if channel == "scenery":
        try:
            html2 = _safe_get(search_url, timeout=timeout, ua=ua)
            limit_sceneries = max(1, min(int(req.get("limit_sceneries", 20) or 20), 100))
            sceneries = _extract_sceneries_from_search(html2, limit=limit_sceneries)
            result["scenery_count"] = len(sceneries)
            result["sceneries"] = sceneries
            sort_code = _scenery_sort_to_code(str(req.get("scenery_sort", "")))
            result["scenery_sort"] = {"sort": _scenery_sort_to_name(sort_code), "sort_code": sort_code}
        except Exception as e:
            result["scenery_count"] = 0
            result["sceneries"] = []
            result["scenery_error"] = str(e)

    return result


def _train_station2s(appkey: str, req: Dict[str, object]) -> Dict[str, object]:
    start = req.get("start")
    end = req.get("end")
    if not start:
        return {"error": "missing_param", "message": "start is required"}
    if not end:
        return {"error": "missing_param", "message": "end is required"}
    params = {"appkey": appkey, "start": start, "end": end}
    if req.get("ishigh") is not None and req.get("ishigh") != "":
        params["ishigh"] = req.get("ishigh")
    if req.get("date"):
        params["date"] = req.get("date")
    r = requests.get(TRAIN_STATION2S_URL, params=params, timeout=12)
    r.raise_for_status()
    data = r.json()
    if data.get("status") != 0:
        return {"error": "api_error", "code": data.get("status"), "message": data.get("msg")}
    return {"ok": True, "channel": "train_station2s", "data": data.get("result", [])}


def _train_line(appkey: str, req: Dict[str, object]) -> Dict[str, object]:
    trainno = req.get("trainno")
    if not trainno:
        return {"error": "missing_param", "message": "trainno is required"}
    params = {"appkey": appkey, "trainno": trainno}
    if req.get("date"):
        params["date"] = req.get("date")
    r = requests.get(TRAIN_LINE_URL, params=params, timeout=12)
    r.raise_for_status()
    data = r.json()
    if data.get("status") != 0:
        return {"error": "api_error", "code": data.get("status"), "message": data.get("msg")}
    return {"ok": True, "channel": "train_line", "data": data.get("result", {})}


def _train_ticket(appkey: str, req: Dict[str, object]) -> Dict[str, object]:
    start = req.get("start")
    end = req.get("end")
    date = req.get("date")
    if not start:
        return {"error": "missing_param", "message": "start is required"}
    if not end:
        return {"error": "missing_param", "message": "end is required"}
    if not date:
        return {"error": "missing_param", "message": "date is required"}
    params = {"appkey": appkey, "start": start, "end": end, "date": date}
    r = requests.get(TRAIN_TICKET_URL, params=params, timeout=12)
    r.raise_for_status()
    data = r.json()
    if data.get("status") != 0:
        return {"error": "api_error", "code": data.get("status"), "message": data.get("msg")}
    return {"ok": True, "channel": "train_ticket", "data": data.get("result", [])}


def main() -> None:
    ap = argparse.ArgumentParser(description="jisu-travel: 同程(航班/景点) + 极速火车")
    ap.add_argument(
        "command",
        choices=("flight", "scenery", "train_station2s", "train_line", "train_ticket"),
        help="子命令",
    )
    ap.add_argument("json_body", nargs="?", default="{}", help="请求 JSON（可选）")
    ap.add_argument("--timeout", type=float, default=15.0, help="请求超时秒数，默认 15")
    ap.add_argument("--ua", default="", help="自定义 User-Agent")
    args = ap.parse_args()

    try:
        req = json.loads(args.json_body or "{}")
        if not isinstance(req, dict):
            raise ValueError("json_body must be object")
    except Exception as e:
        print(json.dumps({"ok": False, "error": "invalid_json", "message": str(e)}, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    try:
        if args.command in ("flight", "scenery"):
            result = _ly_channel(args.command, req=req, timeout=float(args.timeout), ua=args.ua.strip())
        else:
            appkey = os.getenv("JISU_API_KEY", "").strip()
            if not appkey:
                print(
                    json.dumps(
                        {"ok": False, "error": "missing_env", "message": "JISU_API_KEY is required for train commands"},
                        ensure_ascii=False,
                        indent=2,
                    )
                )
                raise SystemExit(1)
            if args.command == "train_station2s":
                result = _train_station2s(appkey, req)
            elif args.command == "train_line":
                result = _train_line(appkey, req)
            else:
                result = _train_ticket(appkey, req)
    except Exception as e:
        result = {"ok": False, "error": "request_failed", "message": str(e)}

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

