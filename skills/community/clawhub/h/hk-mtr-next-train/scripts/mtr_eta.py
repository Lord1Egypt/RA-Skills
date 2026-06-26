#!/usr/bin/env python3
"""
Hong Kong MTR Next Train ETA Query Script
Version: 1.0.0
Created: 2026-03-18

Changelog:
v1.0.0 - 2026-03-18 (Initial version)
- Fast station/line matching with local CSV cache
- Bilingual output (TC/EN)
- Supports station-only / line+station queries
- Optional travel-time estimate between two stations (same line only)
"""

import csv
import json
import os
import re
import sys
import time
import math
from datetime import datetime
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIONS_CSV = os.path.join(BASE_DIR, "mtr_lines_and_stations.csv")

MTR_CSV_URL = "https://opendata.mtr.com.hk/data/mtr_lines_and_stations.csv"
API_URL = "https://rt.data.gov.hk/v1/transport/mtr/getSchedule.php"

MAX_WORKERS = 8
HTTP_TIMEOUT = 2.2

FALLBACK_TC = "尾班車已過或未有班次資料"
FALLBACK_EN = "Service hours have passed / No information found"

LINE_LABELS = {
    "AEL": {"tc": "機場快線", "en": "Airport Express"},
    "TCL": {"tc": "東涌線", "en": "Tung Chung Line"},
    "TML": {"tc": "屯馬線", "en": "Tuen Ma Line"},
    "TKL": {"tc": "將軍澳線", "en": "Tseung Kwan O Line"},
    "EAL": {"tc": "東鐵線", "en": "East Rail Line"},
    "SIL": {"tc": "南港島線", "en": "South Island Line"},
    "TWL": {"tc": "荃灣線", "en": "Tsuen Wan Line"},
    "ISL": {"tc": "港島線", "en": "Island Line"},
    "KTL": {"tc": "觀塘線", "en": "Kwun Tong Line"},
    "DRL": {"tc": "迪士尼線", "en": "Disneyland Resort Line"},
}

LINE_ALIASES = {
    "ael": "AEL", "airport express": "AEL", "機場快線": "AEL", "機場快綫": "AEL",
    "tcl": "TCL", "tung chung line": "TCL", "東涌線": "TCL", "東涌綫": "TCL",
    "tml": "TML", "tuen ma line": "TML", "屯馬線": "TML", "屯馬綫": "TML",
    "tkl": "TKL", "tseung kwan o line": "TKL", "將軍澳線": "TKL", "將軍澳綫": "TKL",
    "eal": "EAL", "east rail line": "EAL", "東鐵線": "EAL", "東鐵綫": "EAL",
    "sil": "SIL", "south island line": "SIL", "南港島線": "SIL", "南港島綫": "SIL",
    "twl": "TWL", "tsuen wan line": "TWL", "荃灣線": "TWL", "荃灣綫": "TWL",
    "isl": "ISL", "island line": "ISL", "港島線": "ISL", "港島綫": "ISL",
    "ktl": "KTL", "kwun tong line": "KTL", "觀塘線": "KTL", "觀塘綫": "KTL",
    "drl": "DRL", "disneyland resort line": "DRL", "迪士尼線": "DRL", "迪士尼綫": "DRL",
}


def normalize_text(s: str) -> str:
    s = (s or "").strip().lower()
    s = s.replace(" ", " ")
    s = re.sub(r"[()\-_/,.]", " ", s)
    for token in ["港鐵", "地鐵", "mtr", "station", "站", "綫", "線", "line", "rail"]:
        s = s.replace(token, "")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def http_get_json(url: str):
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=HTTP_TIMEOUT) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception:
        return None


def ensure_csv():
    if os.path.exists(STATIONS_CSV):
        return True
    try:
        req = Request(MTR_CSV_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=8) as r:
            data = r.read()
        with open(STATIONS_CSV, "wb") as f:
            f.write(data)
        return True
    except Exception:
        return False


def load_station_index():
    if not ensure_csv():
        return {}, {}, {}

    stations = {}  # station_code -> station info
    station_to_lines = {}  # station_code -> set(lines)
    line_to_stations = {}  # line -> [{code,name_tc,name_en,seq}]

    with open(STATIONS_CSV, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            line = (row.get("Line Code") or "").strip().upper()
            sta = (row.get("Station Code") or "").strip().upper()
            sid = (row.get("Station ID") or "").strip()
            name_tc = (row.get("Chinese Name") or "").strip()
            name_en = (row.get("English Name") or "").strip()
            try:
                seq = float(row.get("Sequence") or 0)
            except Exception:
                seq = 0

            if line not in LINE_LABELS:
                continue

            if sta not in stations:
                stations[sta] = {
                    "code": sta,
                    "id": sid,
                    "name_tc": name_tc,
                    "name_en": name_en,
                    "norm_tc": normalize_text(name_tc),
                    "norm_en": normalize_text(name_en),
                }

            station_to_lines.setdefault(sta, set()).add(line)
            line_to_stations.setdefault(line, []).append({
                "code": sta,
                "name_tc": name_tc,
                "name_en": name_en,
                "seq": seq,
            })

    # dedupe + sort stations within each line
    for line, arr in list(line_to_stations.items()):
        seen = {}
        for x in arr:
            c = x["code"]
            if c not in seen or x["seq"] < seen[c]["seq"]:
                seen[c] = x
        line_to_stations[line] = sorted(seen.values(), key=lambda x: x["seq"])

    return stations, station_to_lines, line_to_stations


def has_cjk(text: str) -> bool:
    t = text or ""
    for ch in t:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def pick_lang(user_lang: str, station_query: str = "", line_query: str = "", to_station_query: str = "") -> str:
    l = (user_lang or "").strip().upper()
    if l in ("TC", "EN"):
        return l
    sample = f"{station_query} {line_query} {to_station_query}".strip()
    return "TC" if has_cjk(sample) else "EN"


def find_line(line_query: str):
    if not line_query:
        return None
    q = normalize_text(line_query)
    if not q:
        return None
    if q in LINE_ALIASES:
        return LINE_ALIASES[q]

    # fallback contains
    for k, v in LINE_ALIASES.items():
        if q == k or q in k or k in q:
            return v
    return None


def find_station(stations: dict, station_query: str):
    q_raw = (station_query or "").strip()
    q = normalize_text(q_raw)
    if not q:
        return []

    matches = []
    for sta, info in stations.items():
        n_tc = info["norm_tc"]
        n_en = info["norm_en"]
        score = 0
        if q == n_tc or q == n_en:
            score = 100
        elif q and (q in n_tc or q in n_en):
            score = 80
        elif n_tc and n_tc in q:
            score = 70
        elif n_en and n_en in q:
            score = 70

        if score > 0:
            matches.append((score, sta, info))

    matches.sort(key=lambda x: (-x[0], x[2]["name_en"]))
    # unique station code
    out = []
    seen = set()
    for _, sta, info in matches:
        if sta in seen:
            continue
        seen.add(sta)
        out.append(info)
    return out


def call_schedule(line: str, sta: str, lang: str):
    qs = urlencode({"line": line, "sta": sta, "lang": lang})
    data = http_get_json(f"{API_URL}?{qs}")
    if not data or data.get("status") != 1:
        return None
    node = data.get("data", {}).get(f"{line}-{sta}")
    if not isinstance(node, dict):
        return None
    return node


def parse_time_str(ts: str):
    try:
        return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
    except Exception:
        return None


def fmt_dir_label(lang: str, dir_key: str):
    if lang == "TC":
        return "上行" if dir_key == "UP" else "下行"
    return "UP" if dir_key == "UP" else "DOWN"


def station_display(info: dict, lang: str):
    name = info["name_tc"] if lang == "TC" else info["name_en"]
    if lang == "TC" and name and not name.endswith("站"):
        name = f"{name}站"
    return name


def line_display(line: str, lang: str):
    return LINE_LABELS.get(line, {}).get("tc" if lang == "TC" else "en", line)


def join_line_labels(lines, lang: str):
    sep = "/" if lang == "TC" else " / "
    return sep.join([line_display(x, lang) for x in lines])


def format_schedule(line: str, sta_info: dict, node: dict, lang: str, stations: dict):
    out = []
    sta_name = station_display(sta_info, lang)
    out.append(f"{sta_name}｜{line_display(line, lang)}")

    now = datetime.now()
    rows = 0

    def eta_text_and_keep(delta_sec: float, ttnt_min: int):
        # departed >2 min => skip
        if delta_sec < -120:
            return None, False
        # departed within 0~2 min
        if delta_sec < 0:
            return ("已離開" if lang == "TC" else "Departed"), True
        # now / 0 min
        if ttnt_min <= 0:
            return ("即將離開" if lang == "TC" else "Departing"), True
        # within 1 minute
        if delta_sec < 60 or ttnt_min == 1:
            return ("即將到達" if lang == "TC" else "Arriving"), True
        # normal minute display
        return (f"{ttnt_min}分" if lang == "TC" else f"{ttnt_min}m"), True

    for dir_key in ["UP", "DOWN"]:
        arr = node.get(dir_key, [])
        if not isinstance(arr, list) or not arr:
            continue

        valid = []
        for x in arr:
            t = parse_time_str(x.get("time", ""))
            if not t:
                continue

            delta_sec = (t - now).total_seconds()

            ttnt_raw = x.get("ttnt", "")
            try:
                ttnt_min = int(str(ttnt_raw).strip())
            except Exception:
                ttnt_min = max(0, int(math.ceil(max(0.0, delta_sec) / 60.0)))

            eta_text, keep = eta_text_and_keep(delta_sec, ttnt_min)
            if not keep:
                continue

            valid.append({
                "time": t,
                "eta_text": eta_text,
                "dest_code": x.get("dest", "-"),
                "plat": str(x.get("plat", "-")).strip() or "-",
            })

        if not valid:
            continue

        valid.sort(key=lambda z: z["time"])

        by_dest = {}
        for item in valid:
            by_dest.setdefault(item["dest_code"], []).append(item)

        groups = sorted(by_dest.items(), key=lambda kv: kv[1][0]["time"] if kv[1] else datetime.max)

        for dest_code, items in groups:
            dest_info = stations.get(dest_code, {}) if isinstance(stations, dict) else {}
            dest = station_display(dest_info, lang) if dest_info else dest_code

            # direction-level platform unless mixed
            plats = sorted({it.get("plat", "-") for it in items if it.get("plat", "-") != "-"})
            single_plat = plats[0] if len(plats) == 1 else None

            vals = []
            for it in items[:4]:
                t = it["time"]
                eta = it["eta_text"]
                plat = it.get("plat", "-")
                if single_plat:
                    vals.append(f"{t.strftime('%H:%M')}({eta})")
                else:
                    if lang == "TC":
                        vals.append(f"{t.strftime('%H:%M')}({eta}, {plat}號月台)")
                    else:
                        vals.append(f"{t.strftime('%H:%M')}({eta}, Platform {plat})")

            if vals:
                rows += 1
                if lang == "TC":
                    if single_plat:
                        out.append(f"- {fmt_dir_label(lang, dir_key)}｜{single_plat}號月台｜往{dest}｜" + "、".join(vals))
                    else:
                        out.append(f"- {fmt_dir_label(lang, dir_key)}｜往{dest}｜" + "、".join(vals))
                else:
                    if single_plat:
                        out.append(f"- {fmt_dir_label(lang, dir_key)} | Platform {single_plat} | to {dest} | " + ", ".join(vals))
                    else:
                        out.append(f"- {fmt_dir_label(lang, dir_key)} | to {dest} | " + ", ".join(vals))

    if rows == 0:
        return []
    return out


def suggest_line_stations(line_to_stations: dict, line: str, lang: str):
    arr = line_to_stations.get(line, [])[:2]
    names = [x["name_tc"] if lang == "TC" else x["name_en"] for x in arr]
    return names


def estimate_travel_minutes(line_to_stations: dict, line: str, src_code: str, dst_code: str):
    arr = line_to_stations.get(line, [])
    idx = {x["code"]: i for i, x in enumerate(arr)}
    if src_code not in idx or dst_code not in idx:
        return None
    hops = abs(idx[src_code] - idx[dst_code])
    # rough heuristic: avg 2.3 min per stop + 2 min buffer
    return int(round(hops * 2.3 + 2))


def main(station_query: str = "", line_query: str = "", lang: str = "", to_station_query: str = ""):
    lang = pick_lang(lang, station_query, line_query, to_station_query)

    stations, station_to_lines, line_to_stations = load_station_index()
    if not stations:
        print(FALLBACK_TC if lang == "TC" else FALLBACK_EN)
        return

    line = find_line(line_query) if line_query else None
    station_matches = find_station(stations, station_query) if station_query else []

    # Case 4: no line and no station
    if not line and not station_matches:
        print("查詢哪一個港鐵站？" if lang == "TC" else "Which MTR station do you want to check?")
        return

    # Case 3: line only
    if line and not station_matches:
        sugg = suggest_line_stations(line_to_stations, line, lang)
        if lang == "TC":
            if sugg:
                print(f"查詢哪一個港鐵站？例如：{sugg[0]}、{sugg[1] if len(sugg)>1 else sugg[0]}")
            else:
                print("查詢哪一個港鐵站？")
        else:
            if sugg:
                print(f"Which station on {line_display(line, lang)}? e.g. {sugg[0]}, {sugg[1] if len(sugg)>1 else sugg[0]}")
            else:
                print("Which MTR station do you want to check?")
        return

    # pick best station
    sta = station_matches[0]
    sta_code = sta["code"]
    lines_of_station = sorted(station_to_lines.get(sta_code, []))

    # Case 1 & 5: line provided
    target_lines = []
    conflict_msg = None
    if line:
        if line in lines_of_station:
            target_lines = [line]
        else:
            # conflict: fallback to all lines at station
            target_lines = lines_of_station
            if lang == "TC":
                conflict_msg = f"你指定嘅綫路 ({line_display(line, lang)}) 並不經過 {station_display(sta, lang)}，以下改為顯示該站所有可用綫路。"
            else:
                conflict_msg = f"The specified line ({line_display(line, lang)}) does not serve {station_display(sta, lang)}. Showing all available lines at this station."
    else:
        # Case 2: station only => all lines
        target_lines = lines_of_station

    # fetch schedules in parallel
    reqs = [(ln, sta_code) for ln in target_lines]
    schedules = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futs = {ex.submit(call_schedule, ln, sc, lang): (ln, sc) for ln, sc in reqs}
        for f in as_completed(futs):
            ln, sc = futs[f]
            try:
                schedules[(ln, sc)] = f.result()
            except Exception:
                schedules[(ln, sc)] = None

    out = []
    if conflict_msg:
        out.append(conflict_msg)

    has_any = False
    for ln in target_lines:
        node = schedules.get((ln, sta_code))
        if not node:
            continue
        block = format_schedule(ln, sta, node, lang, stations)
        if block:
            has_any = True
            out.extend(block)
            out.append("")

    # optional travel-time estimate
    if to_station_query:
        dst_matches = find_station(stations, to_station_query)
        if dst_matches:
            dst = dst_matches[0]
            common_lines = sorted(set(lines_of_station) & set(station_to_lines.get(dst["code"], [])))
            if common_lines:
                best_line = common_lines[0]
                mins = estimate_travel_minutes(line_to_stations, best_line, sta_code, dst["code"])
                if mins is not None:
                    if lang == "TC":
                        out.append(f"⏱️ 由 {station_display(sta, lang)} 去 {station_display(dst, lang)}（{line_display(best_line, lang)}）估計約 {mins} 分鐘（未計等車／轉綫）。")
                    else:
                        out.append(f"⏱️ Estimated {mins} min from {station_display(sta, lang)} to {station_display(dst, lang)} on {line_display(best_line, lang)} (excluding wait/transfer time).")

    if not has_any:
        # fallback with [Station] @ [Line(s)] format
        sta_label = station_display(sta, lang) if sta else ("(Unknown Station)" if lang != "TC" else "（未知車站）")
        line_label = ""
        if line:
            line_label = line_display(line, lang)
        elif target_lines:
            line_label = join_line_labels(target_lines, lang)

        if line_label:
            if lang == "TC":
                print(f"{sta_label} @ {line_label} ：{FALLBACK_TC}")
            else:
                print(f"{sta_label} @ {line_label} : {FALLBACK_EN}")
        else:
            print(FALLBACK_TC if lang == "TC" else FALLBACK_EN)
        return

    # trim duplicate blank lines
    cleaned = []
    prev_blank = False
    for line_out in out:
        is_blank = (line_out.strip() == "")
        if is_blank and prev_blank:
            continue
        cleaned.append(line_out)
        prev_blank = is_blank

    print("\n".join(cleaned).strip())


if __name__ == "__main__":
    # args: station [line] [lang] [to_station]
    args = sys.argv[1:]
    station = args[0] if len(args) >= 1 else ""
    line = args[1] if len(args) >= 2 else ""
    lang = args[2] if len(args) >= 3 else "EN"
    to_sta = args[3] if len(args) >= 4 else ""
    main(station, line, lang, to_sta)
