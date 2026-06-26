#!/usr/bin/env python3
import argparse
import csv
import io
import json
import re
import sys
from collections import defaultdict
from datetime import datetime
from functools import lru_cache
from zoneinfo import ZoneInfo
from urllib.parse import quote
from urllib.request import Request, urlopen

KMB_BASE = "https://data.etabus.gov.hk/v1/transport/kmb"
CITYBUS_BASE = "https://rt.data.gov.hk/v2/transport/citybus"
MTR_SCHEDULE_URL = "https://rt.data.gov.hk/v1/transport/mtr/getSchedule.php?line={line}&sta={station}"
MTR_LINES_CSV_URL = "https://opendata.mtr.com.hk/data/mtr_lines_and_stations.csv"
TZ = ZoneInfo("Asia/Hong_Kong")

KMB_LIKE_OPERATORS = {"kmb", "lwb"}
CITYBUS_OPERATORS = {"citybus", "ctb"}
HEAVY_RAIL_LINE_CODES = {"AEL", "TCL", "TML", "TKL", "TWL", "ISL", "KTL", "EAL", "DRL", "SIL"}
MTR_LINE_HINTS = {
    "airport express": "AEL",
    "ael": "AEL",
    "東涌線": "TCL",
    "tcl": "TCL",
    "屯馬線": "TML",
    "tml": "TML",
    "將軍澳線": "TKL",
    "tkl": "TKL",
    "荃灣線": "TWL",
    "twl": "TWL",
    "港島線": "ISL",
    "isl": "ISL",
    "觀塘線": "KTL",
    "ktl": "KTL",
    "東鐵線": "EAL",
    "eal": "EAL",
    "迪士尼線": "DRL",
    "drl": "DRL",
    "南港島線": "SIL",
    "sil": "SIL",
}


def fetch_text(url: str):
    req = Request(url, headers={"User-Agent": "OpenClaw hk-bus-eta skill"})
    with urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8-sig")


def fetch_json(url: str):
    return json.loads(fetch_text(url))


@lru_cache(maxsize=1)
def load_mtr_rows():
    text = fetch_text(MTR_LINES_CSV_URL)
    rows = []
    for row in csv.DictReader(io.StringIO(text)):
        line = row["Line Code"].strip().upper()
        if line not in HEAVY_RAIL_LINE_CODES:
            continue
        rows.append(
            {
                "line": line,
                "direction": row["Direction"].strip().upper(),
                "station_code": row["Station Code"].strip().upper(),
                "station_id": row["Station ID"].strip(),
                "name_tc": row["Chinese Name"].strip(),
                "name_en": row["English Name"].strip(),
                "sequence": float(row["Sequence"]),
            }
        )
    return rows


@lru_cache(maxsize=1)
def mtr_station_index():
    by_station = defaultdict(list)
    by_line_direction = defaultdict(dict)
    for row in load_mtr_rows():
        by_station[row["station_code"]].append(row)
        by_line_direction[(row["line"], row["direction"])][row["station_code"]] = row
    return by_station, by_line_direction


@lru_cache(maxsize=1)
def mtr_station_catalog():
    stations = {}
    for row in load_mtr_rows():
        code = row["station_code"]
        entry = stations.setdefault(
            code,
            {
                "station_code": code,
                "name_tc": row["name_tc"],
                "name_en": row["name_en"],
                "lines": set(),
            },
        )
        entry["lines"].add(row["line"])
    for entry in stations.values():
        entry["lines"] = sorted(entry["lines"])
    return list(stations.values())


@lru_cache(maxsize=128)
def get_mtr_schedule(line: str, station_code: str):
    line = line.upper()
    station_code = station_code.upper()
    data = fetch_json(MTR_SCHEDULE_URL.format(line=quote(line), station=quote(station_code)))
    if str(data.get("status")) != "1":
        raise RuntimeError(data.get("message") or f"MTR API status={data.get('status')}")
    key = f"{line}-{station_code}"
    return data["data"].get(key, {})


def normalize_operator(operator: str) -> str:
    op = (operator or "kmb").strip().lower()
    if op in KMB_LIKE_OPERATORS:
        return op
    if op in CITYBUS_OPERATORS:
        return "citybus"
    raise ValueError(f"Unsupported operator: {operator}")


def normalize_direction(direction: str, operator: str) -> str:
    direction = (direction or "both").strip().lower()
    if direction not in {"inbound", "outbound", "both"}:
        raise ValueError(f"Unsupported direction: {direction}")
    if direction == "both":
        return direction
    if operator == "citybus":
        return "inbound" if direction == "inbound" else "outbound"
    return direction


def get_route_stops(operator: str, route: str, direction: str, service_type: str):
    if operator in KMB_LIKE_OPERATORS:
        url = f"{KMB_BASE}/route-stop/{quote(route)}/{direction}/{service_type}"
        return fetch_json(url)["data"]

    url = f"{CITYBUS_BASE}/route-stop/CTB/{quote(route)}/{direction}"
    return fetch_json(url)["data"]


def get_stop(operator: str, stop_id: str):
    if operator in KMB_LIKE_OPERATORS:
        return fetch_json(f"{KMB_BASE}/stop/{stop_id}")["data"]
    return fetch_json(f"{CITYBUS_BASE}/stop/{stop_id}")["data"]


def get_eta(operator: str, stop_id: str, route: str, service_type: str):
    if operator in KMB_LIKE_OPERATORS:
        return fetch_json(f"{KMB_BASE}/eta/{stop_id}/{quote(route)}/{service_type}")["data"]
    return fetch_json(f"{CITYBUS_BASE}/eta/CTB/{stop_id}/{quote(route)}")["data"]


def normalize_text(s: str) -> str:
    cleaned = (s or "").strip().lower()
    for ch in "()[]{}.,，。／/\\-_:;：'\"":
        cleaned = cleaned.replace(ch, " ")
    return " ".join(cleaned.split())


def matches(stop_name: str, query: str) -> bool:
    stop = normalize_text(stop_name)
    q = normalize_text(query)
    if not q:
        return False
    if q in stop:
        return True
    return all(token in stop for token in q.split())


def minutes_until(eta_iso: str):
    eta_dt = datetime.fromisoformat(eta_iso)
    if eta_dt.tzinfo is None:
        eta_dt = eta_dt.replace(tzinfo=TZ)
    now = datetime.now(TZ)
    return max(0, round((eta_dt - now).total_seconds() / 60))


def build_eta_entry(row: dict):
    if not row.get("eta"):
        return None
    return {
        "eta": row["eta"],
        "minutes": minutes_until(row["eta"]),
        "destination_tc": row.get("dest_tc", ""),
        "destination_en": row.get("dest_en", ""),
        "remark_tc": row.get("rmk_tc", ""),
        "remark_en": row.get("rmk_en", ""),
    }


def format_match_line(match: dict) -> str:
    operator = match["operator"].upper()
    stop_name_tc = match.get("stop_name_tc") or match.get("stop_name_en") or match["stop_id"]
    dest = match.get("route_destination_tc") or match.get("route_destination_en") or ""
    suffix = f" → {dest}" if dest else ""
    return (
        f"- [{operator}] {stop_name_tc}{suffix} "
        f"[{match['direction']}, seq {match['sequence']}, stop {match['stop_id']}]"
    )


def run_bus_query(args):
    operator = normalize_operator(args.operator)
    directions = [args.direction] if args.direction != "both" else ["outbound", "inbound"]
    out = {
        "mode": "bus",
        "operator": operator,
        "route": args.route,
        "stop_query": args.stop_query,
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "matches": [],
    }

    for direction in directions:
        try:
            route_stops = get_route_stops(operator, args.route, normalize_direction(direction, operator), args.service_type)
        except Exception as e:
            out.setdefault("errors", []).append({"direction": direction, "error": str(e)})
            continue

        for rs in route_stops:
            stop = get_stop(operator, rs["stop"])
            if not any(
                matches(stop.get(name, ""), args.stop_query)
                for name in ["name_tc", "name_en", "name_sc"]
            ):
                continue

            eta_rows = get_eta(operator, rs["stop"], args.route, args.service_type)
            if operator in KMB_LIKE_OPERATORS:
                eta_rows = [
                    row for row in eta_rows
                    if row.get("dir") == rs.get("bound") and int(row.get("seq", -1)) == int(rs.get("seq", -1))
                ]
                route_destination_tc = ""
                route_destination_en = ""
            else:
                dir_code = "O" if direction == "outbound" else "I"
                eta_rows = [
                    row for row in eta_rows
                    if row.get("dir") == dir_code and int(row.get("seq", -1)) == int(rs.get("seq", -1))
                ]
                first = eta_rows[0] if eta_rows else {}
                route_destination_tc = first.get("dest_tc", "")
                route_destination_en = first.get("dest_en", "")

            etas = [entry for entry in (build_eta_entry(row) for row in eta_rows[: args.limit]) if entry]
            out["matches"].append(
                {
                    "operator": operator,
                    "direction": direction,
                    "sequence": int(rs["seq"]),
                    "service_type": rs.get("service_type", args.service_type),
                    "stop_id": rs["stop"],
                    "stop_name_tc": stop.get("name_tc", ""),
                    "stop_name_en": stop.get("name_en", ""),
                    "route_destination_tc": route_destination_tc,
                    "route_destination_en": route_destination_en,
                    "etas": etas,
                }
            )

    out["matches"].sort(key=lambda m: (m["direction"], m["sequence"]))
    return out


def line_hint_from_text(text: str):
    t = normalize_text(text)
    for key, line in sorted(MTR_LINE_HINTS.items(), key=lambda item: -len(item[0])):
        if normalize_text(key) in t:
            return line
    return None


def find_mtr_station_candidates(query: str, line_hint: str | None = None):
    q = normalize_text(query).replace(" station", "").replace("站", "").strip()
    candidates = []
    for station in mtr_station_catalog():
        haystacks = [station["name_tc"], station["name_en"], station["station_code"]]
        if any(matches(name, q) for name in haystacks):
            if line_hint and line_hint not in station["lines"]:
                continue
            score = 0
            if normalize_text(station["name_tc"]).replace("站", "") == q:
                score += 5
            if normalize_text(station["name_en"]) == q:
                score += 5
            if q in normalize_text(station["name_tc"]):
                score += 2
            if q in normalize_text(station["name_en"]):
                score += 2
            if station["station_code"].lower() == q:
                score += 3
            if line_hint and line_hint in station["lines"]:
                score += 1
            candidates.append((score, station))
    candidates.sort(key=lambda item: (-item[0], item[1]["station_code"]))
    return [station for _, station in candidates]


def find_journey_options(origin_code: str, target_code: str, line_hint: str | None = None):
    _, by_line_direction = mtr_station_index()
    options = []
    seen = set()
    for (line, direction), mapping in by_line_direction.items():
        if line_hint and line != line_hint:
            continue
        if origin_code not in mapping or target_code not in mapping:
            continue
        origin_seq = mapping[origin_code]["sequence"]
        target_seq = mapping[target_code]["sequence"]
        if origin_seq == target_seq:
            continue
        step = "increasing" if target_seq > origin_seq else "decreasing"
        key = (line, step)
        if key in seen:
            continue
        options.append(
            {
                "line": line,
                "direction_table": direction,
                "origin_seq": origin_seq,
                "target_seq": target_seq,
                "step": step,
            }
        )
        seen.add(key)
    return options


def train_passes_target(line: str, origin_code: str, target_code: str, dest_code: str):
    _, by_line_direction = mtr_station_index()
    for (ln, _direction), mapping in by_line_direction.items():
        if ln != line:
            continue
        if origin_code not in mapping or target_code not in mapping or dest_code not in mapping:
            continue
        origin_seq = mapping[origin_code]["sequence"]
        target_seq = mapping[target_code]["sequence"]
        dest_seq = mapping[dest_code]["sequence"]
        if origin_seq <= target_seq <= dest_seq:
            return True
        if origin_seq >= target_seq >= dest_seq:
            return True
    return False


def station_name_by_code(station_code: str):
    for station in mtr_station_catalog():
        if station["station_code"] == station_code:
            return station
    return {"station_code": station_code, "name_tc": station_code, "name_en": station_code, "lines": []}


def build_mtr_eta_entry(row: dict, line: str, origin_code: str, target_code: str):
    dest_code = (row.get("dest") or "").upper()
    if not row.get("time") or not dest_code:
        return None
    if not train_passes_target(line, origin_code, target_code, dest_code):
        return None
    dest_station = station_name_by_code(dest_code)
    return {
        "eta": row["time"],
        "minutes": int(row.get("ttnt", minutes_until(row["time"]))),
        "destination_code": dest_code,
        "destination_tc": dest_station.get("name_tc", dest_code),
        "destination_en": dest_station.get("name_en", dest_code),
        "platform": row.get("plat", ""),
        "route": row.get("route", ""),
        "time_type": row.get("timeType", ""),
    }


def run_mtr_query(origin_query: str, destination_query: str, line: str | None = None, limit: int = 3):
    line = line.upper() if line else None
    origin_candidates = find_mtr_station_candidates(origin_query, line)
    destination_candidates = find_mtr_station_candidates(destination_query, line)
    out = {
        "mode": "mtr",
        "origin_query": origin_query,
        "destination_query": destination_query,
        "line_hint": line,
        "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
        "origin_candidates": origin_candidates[:5],
        "destination_candidates": destination_candidates[:5],
        "matches": [],
    }
    if not origin_candidates or not destination_candidates:
        return out

    for origin in origin_candidates[:3]:
        for destination in destination_candidates[:3]:
            if origin["station_code"] == destination["station_code"]:
                continue
            for option in find_journey_options(origin["station_code"], destination["station_code"], line):
                schedule = get_mtr_schedule(option["line"], origin["station_code"])
                for api_direction in ["UP", "DOWN"]:
                    rows = schedule.get(api_direction, [])
                    etas = [
                        entry
                        for entry in (
                            build_mtr_eta_entry(row, option["line"], origin["station_code"], destination["station_code"])
                            for row in rows[: max(limit * 3, 6)]
                        )
                        if entry
                    ][:limit]
                    if not etas:
                        continue
                    out["matches"].append(
                        {
                            "operator": "mtr",
                            "line": option["line"],
                            "api_direction": api_direction,
                            "origin_station_code": origin["station_code"],
                            "origin_station_tc": origin["name_tc"],
                            "origin_station_en": origin["name_en"],
                            "target_station_code": destination["station_code"],
                            "target_station_tc": destination["name_tc"],
                            "target_station_en": destination["name_en"],
                            "etas": etas,
                        }
                    )
    deduped = []
    seen = set()
    for match in out["matches"]:
        key = (match["line"], match["origin_station_code"], match["target_station_code"], tuple(e["eta"] for e in match["etas"]))
        if key in seen:
            continue
        deduped.append(match)
        seen.add(key)
    out["matches"] = deduped
    return out


def parse_mtr_text(text: str):
    cleaned = re.sub(r"[？?]", "", text.strip())
    line = line_hint_from_text(cleaned)
    reduced = cleaned
    for noise in ["下一班", "幾點有車", "有冇車", "幾耐到", "幾時到", "到站", "班車", "列車"]:
        reduced = reduced.replace(noise, "")
    reduced = re.sub(r"\s+", "", reduced)
    patterns = [
        r"(?P<origin>.+?)(?:站)?(?:去|往)(?P<destination>.+?)(?:方向|站)?$",
        r"(?P<origin>.+?)(?:站)?(?:去|往)(?P<destination>.+?)(?:方向|站)?",
        r"(?P<origin>.+?)(?:站)?(?P<destination>.+?)方向$",
    ]
    for pattern in patterns:
        m = re.match(pattern, reduced)
        if m:
            origin = m.group("origin").strip()
            destination = m.group("destination").strip()
            origin = re.sub(r"(站)+$", "", origin)
            destination = re.sub(r"(方向|站)+$", "", destination)
            if origin and destination:
                return {"origin": origin, "destination": destination, "line": line}
    raise ValueError(f"Could not parse MTR prompt: {text}")


def format_mtr_match(match: dict) -> str:
    return (
        f"- [MTR {match['line']}] {match['origin_station_tc']} → {match['target_station_tc']} "
        f"[{match['origin_station_code']}→{match['target_station_code']}]"
    )


def print_bus_output(out, as_json=False):
    if as_json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return
    print(f"Operator {out['operator'].upper()} | Route {out['route']} @ {out['generated_at']}")
    if not out["matches"]:
        print(f"No stop matched query: {out['stop_query']}")
        if out.get("errors"):
            for err in out["errors"]:
                print(f"  {err['direction']}: {err['error']}")
        return
    for match in out["matches"]:
        print(format_match_line(match))
        if not match["etas"]:
            print("  No ETA available")
            continue
        for eta in match["etas"]:
            remark = f" ({eta['remark_tc']})" if eta["remark_tc"] else ""
            destination = eta["destination_tc"] or eta["destination_en"]
            print(f"  {eta['minutes']} 分鐘後 → {destination} @ {eta['eta']}{remark}")


def print_mtr_output(out, as_json=False):
    if as_json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return
    hint = f" | line hint {out['line_hint']}" if out.get("line_hint") else ""
    print(f"Operator MTR | {out['origin_query']} → {out['destination_query']} @ {out['generated_at']}{hint}")
    if not out["matches"]:
        print("No MTR match found")
        if out.get("origin_candidates"):
            print("  Origin candidates:")
            for station in out["origin_candidates"]:
                print(f"  - {station['name_tc']} ({station['station_code']}) [{'/'.join(station['lines'])}]")
        if out.get("destination_candidates"):
            print("  Destination candidates:")
            for station in out["destination_candidates"]:
                print(f"  - {station['name_tc']} ({station['station_code']}) [{'/'.join(station['lines'])}]")
        return
    for match in out["matches"]:
        print(format_mtr_match(match))
        for eta in match["etas"]:
            print(
                f"  {eta['minutes']} 分鐘後 → {eta['destination_tc']} "
                f"@ {eta['eta']} (月台 {eta['platform'] or '?'})"
            )


def build_parser():
    parser = argparse.ArgumentParser(description="Query Hong Kong bus ETA or MTR heavy rail ETA")
    sub = parser.add_subparsers(dest="mode")

    bus = sub.add_parser("bus", help="query bus ETA by route + stop keyword")
    bus.add_argument("route")
    bus.add_argument("stop_query")
    bus.add_argument("--operator", choices=["kmb", "lwb", "citybus", "ctb"], default="kmb")
    bus.add_argument("--direction", choices=["inbound", "outbound", "both"], default="both")
    bus.add_argument("--service-type", default="1")
    bus.add_argument("--limit", type=int, default=3)
    bus.add_argument("--json", action="store_true")

    mtr = sub.add_parser("mtr", help="query MTR heavy rail ETA by origin + destination station")
    mtr.add_argument("origin_query")
    mtr.add_argument("destination_query")
    mtr.add_argument("--line", choices=sorted(HEAVY_RAIL_LINE_CODES))
    mtr.add_argument("--limit", type=int, default=3)
    mtr.add_argument("--json", action="store_true")

    mtr_text = sub.add_parser("mtr-text", help="parse a natural-language MTR prompt and query ETA")
    mtr_text.add_argument("text")
    mtr_text.add_argument("--line", choices=sorted(HEAVY_RAIL_LINE_CODES))
    mtr_text.add_argument("--limit", type=int, default=3)
    mtr_text.add_argument("--json", action="store_true")
    return parser


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] not in {"bus", "mtr", "mtr-text", "-h", "--help"}:
        argv = ["bus", *argv]
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.mode == "bus":
        out = run_bus_query(args)
        print_bus_output(out, args.json)
        return

    if args.mode == "mtr":
        out = run_mtr_query(args.origin_query, args.destination_query, args.line, args.limit)
        print_mtr_output(out, args.json)
        return

    if args.mode == "mtr-text":
        parsed = parse_mtr_text(args.text)
        line = args.line or parsed.get("line")
        out = run_mtr_query(parsed["origin"], parsed["destination"], line, args.limit)
        out["parsed_prompt"] = parsed
        print_mtr_output(out, args.json)
        return

    parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
