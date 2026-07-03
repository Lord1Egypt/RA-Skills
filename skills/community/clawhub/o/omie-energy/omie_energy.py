#!/usr/bin/env python3
import argparse
import json
import math
import os
import subprocess
import sys
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
from OMIEData.DataImport.omie_marginalprice_importer import OMIEMarginalPriceFileImporter

IBERIAN_TZ = ZoneInfo("Europe/Lisbon")
AREA_TO_CONCEPT = {"PT": "PRICE_PT", "ES": "PRICE_SP"}
AREA_LABELS = {"PT": "Portugal", "ES": "Spain"}
HOUR_COLUMNS = [f"H{i}" for i in range(1, 26)]
VALID_AREAS = frozenset(AREA_TO_CONCEPT)


def load_local_env_file() -> None:
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if not key:
            continue
        os.environ.setdefault(key, value.strip())


def load_home_config(config_dirname: str) -> dict:
    cfg_path = Path.home() / ".config" / config_dirname / "config.json"
    if not cfg_path.exists():
        return {}
    try:
        data = json.loads(cfg_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON in {cfg_path}: {exc}") from exc
    if not isinstance(data, dict):
        raise RuntimeError(f"Expected object JSON in {cfg_path}.")
    return data


def config_get_str(cfg: dict, *keys: str) -> str | None:
    for k in keys:
        v = cfg.get(k)
        if v is None:
            continue
        if isinstance(v, str):
            v = v.strip()
        else:
            v = str(v).strip()
        if v:
            return v
    return None


def env_nonempty(name: str, default: str | None = None) -> str | None:
    value = os.environ.get(name)
    if value is None:
        return default
    value = value.strip()
    return value if value else default


def resolve_area(config: dict) -> str:
    area = env_nonempty("OMIE_AREA") or config_get_str(config, "area", "OMIE_AREA") or "PT"
    area = area.upper()
    if area not in VALID_AREAS:
        raise RuntimeError(f"Invalid area '{area}'. Use PT (Portugal) or ES (Spain).")
    return area


def parse_dt(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=IBERIAN_TZ)
    return dt


def fetch_raw_prices(start: date, end: date) -> pd.DataFrame:
    importer = OMIEMarginalPriceFileImporter(
        date_ini=datetime.combine(start, time.min),
        date_end=datetime.combine(end, time.min),
    )
    frame = importer.read_to_dataframe(verbose=False)
    if frame is None or frame.empty:
        return pd.DataFrame()
    frame = frame.copy()
    frame["DATE"] = pd.to_datetime(frame["DATE"])
    return frame


def fetch_area_prices(area: str, start: date, end: date) -> list[dict]:
    concept = AREA_TO_CONCEPT[area]
    raw = fetch_raw_prices(start, end)
    if raw.empty:
        return []

    subset = raw[raw["CONCEPT"] == concept].copy()
    if subset.empty:
        return []

    value_columns = [c for c in HOUR_COLUMNS if c in subset.columns]
    long = subset.melt(
        id_vars=["DATE", "CONCEPT"],
        value_vars=value_columns,
        var_name="hour_label",
        value_name="price_eur_mwh",
    )
    long.dropna(subset=["price_eur_mwh"], inplace=True)
    long["price_eur_mwh"] = pd.to_numeric(long["price_eur_mwh"], errors="coerce")
    long.dropna(subset=["price_eur_mwh"], inplace=True)
    long["delivery_hour"] = long["hour_label"].str.extract(r"(\d+)").astype(int)
    long["starts_at"] = long["DATE"] + pd.to_timedelta(long["delivery_hour"] - 1, unit="h")
    long.sort_values("starts_at", inplace=True)

    points = []
    for _, row in long.iterrows():
        ts = row["starts_at"].to_pydatetime()
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=IBERIAN_TZ)
        price_mwh = float(row["price_eur_mwh"])
        points.append(
            {
                "startsAt": ts.isoformat(),
                "market_date": str(row["DATE"].date()),
                "delivery_hour": int(row["delivery_hour"]),
                "area": area,
                "price_eur_mwh": price_mwh,
                "price_eur_kwh": price_mwh / 1000.0,
            }
        )
    return points


def default_fetch_window() -> tuple[date, date]:
    today = datetime.now(IBERIAN_TZ).date()
    return today - timedelta(days=1), today + timedelta(days=2)


def best_window(points, window_start, window_end, duration_hours):
    scoped = []
    for p in points:
        ts = parse_dt(p["startsAt"])
        if window_start and ts < window_start:
            continue
        if window_end and ts >= window_end:
            continue
        scoped.append({"ts": ts, **p})
    if len(scoped) < duration_hours:
        raise RuntimeError("Not enough hourly points in selected window.")

    best = None
    for i in range(0, len(scoped) - duration_hours + 1):
        chunk = scoped[i : i + duration_hours]
        contiguous = True
        for j in range(1, len(chunk)):
            if int((chunk[j]["ts"] - chunk[j - 1]["ts"]).total_seconds()) != 3600:
                contiguous = False
                break
        if not contiguous:
            continue
        total = sum(x["price_eur_kwh"] for x in chunk)
        if best is None or total < best["total"]:
            best = {"total": total, "chunk": chunk}
    if best is None:
        raise RuntimeError("No contiguous price window found.")
    return best


def command_prices(args, default_area: str):
    area = (args.area or default_area).upper()
    if area not in VALID_AREAS:
        raise RuntimeError(f"Invalid area '{area}'. Use PT or ES.")

    start = date.fromisoformat(args.start) if args.start else None
    end = date.fromisoformat(args.end) if args.end else None
    if start is None or end is None:
        ds, de = default_fetch_window()
        start = start or ds
        end = end or de

    points = fetch_area_prices(area, start, end)
    now = datetime.now(IBERIAN_TZ)
    future = [p for p in points if parse_dt(p["startsAt"]) >= now]
    limited = future[: args.hours]

    print(f"Area: {area} ({AREA_LABELS[area]})")
    print(f"Source: OMIE day-ahead marginal prices ({start} to {end})")
    print(f"Upcoming prices (next {len(limited)}h):")
    for p in limited:
        print(
            f"- {p['startsAt']}  "
            f"{p['price_eur_mwh']:.2f} EUR/MWh  "
            f"({p['price_eur_kwh']:.4f} EUR/kWh)"
        )


def command_optimize(args, default_area: str):
    area = (args.area or default_area).upper()
    if area not in VALID_AREAS:
        raise RuntimeError(f"Invalid area '{area}'. Use PT or ES.")

    start = date.fromisoformat(args.start) if args.start else None
    end = date.fromisoformat(args.end) if args.end else None
    if start is None or end is None:
        ds, de = default_fetch_window()
        start = start or ds
        end = end or de

    points = fetch_area_prices(area, start, end)

    if args.duration_hours:
        duration = args.duration_hours
    else:
        if not args.kwh or not args.power_kw:
            raise RuntimeError("Provide either --duration-hours or both --kwh and --power-kw.")
        duration = math.ceil(args.kwh / args.power_kw)
        duration = max(duration, 1)

    ws = parse_dt(args.window_start) if args.window_start else None
    we = parse_dt(args.window_end) if args.window_end else None
    best = best_window(points, ws, we, duration)
    chunk = best["chunk"]
    avg_kwh = best["total"] / len(chunk)
    avg_mwh = avg_kwh * 1000.0
    est_cost = (args.kwh * avg_kwh) if args.kwh else None

    print(f"Area: {area} ({AREA_LABELS[area]})")
    print(f"Optimal {duration}h window:")
    print(f"- Start: {chunk[0]['startsAt']}")
    print(f"- End:   {chunk[-1]['startsAt']} +1h")
    print(f"- Avg price: {avg_mwh:.2f} EUR/MWh ({avg_kwh:.4f} EUR/kWh)")
    if est_cost is not None:
        print(f"- Estimated energy cost ({args.kwh} kWh): {est_cost:.2f} EUR")
    print("Window details:")
    for p in chunk:
        print(
            f"  * {p['startsAt']} -> "
            f"{p['price_eur_mwh']:.2f} EUR/MWh ({p['price_eur_kwh']:.4f} EUR/kWh)"
        )


def command_compare(args):
    start = date.fromisoformat(args.start) if args.start else None
    end = date.fromisoformat(args.end) if args.end else None
    if start is None or end is None:
        ds, de = default_fetch_window()
        start = start or ds
        end = end or de

    pt_points = fetch_area_prices("PT", start, end)
    es_points = fetch_area_prices("ES", start, end)
    now = datetime.now(IBERIAN_TZ)

    pt_by_ts = {p["startsAt"]: p for p in pt_points if parse_dt(p["startsAt"]) >= now}
    es_by_ts = {p["startsAt"]: p for p in es_points if parse_dt(p["startsAt"]) >= now}
    shared_ts = sorted(set(pt_by_ts) & set(es_by_ts))[: args.hours]

    print(f"Portugal vs Spain — next {len(shared_ts)} shared hours ({start} to {end})")
    print(f"{'Hour':<26} {'PT EUR/MWh':>12} {'ES EUR/MWh':>12} {'Diff':>10}")
    for ts in shared_ts:
        pt = pt_by_ts[ts]["price_eur_mwh"]
        es = es_by_ts[ts]["price_eur_mwh"]
        diff = pt - es
        print(f"{ts:<26} {pt:>12.2f} {es:>12.2f} {diff:>+10.2f}")


def run_cmd(label: str, cmd: str, execute: bool):
    print(f"{label}: {cmd}")
    if execute:
        subprocess.run(cmd, shell=True, check=True)


def command_control(args, default_area: str):
    area = (args.area or default_area).upper()
    if area not in VALID_AREAS:
        raise RuntimeError(f"Invalid area '{area}'. Use PT or ES.")

    start = date.fromisoformat(args.start) if args.start else None
    end = date.fromisoformat(args.end) if args.end else None
    if start is None or end is None:
        ds, de = default_fetch_window()
        start = start or ds
        end = end or de

    points = fetch_area_prices(area, start, end)
    now = datetime.now(IBERIAN_TZ)
    current_candidates = [
        p for p in points if parse_dt(p["startsAt"]) <= now < parse_dt(p["startsAt"]) + timedelta(hours=1)
    ]
    if not current_candidates:
        past = [p for p in points if parse_dt(p["startsAt"]) <= now]
        if not past:
            raise RuntimeError("No current/near-current price available.")
        current = past[-1]
    else:
        current = current_candidates[0]

    price_kwh = float(current["price_eur_kwh"])
    price_mwh = float(current["price_eur_mwh"])
    print(f"Area: {area} ({AREA_LABELS[area]})")
    print(
        f"Current price: {price_mwh:.2f} EUR/MWh ({price_kwh:.4f} EUR/kWh) "
        f"at {current['startsAt']}"
    )
    execute = args.execute
    if not execute:
        print("Mode: dry-run (add --execute to run commands).")
    action_taken = False
    if args.price_below is not None and price_kwh <= args.price_below:
        if args.on_command:
            run_cmd("Price is below threshold -> ON command", args.on_command, execute)
            action_taken = True
    if args.price_above is not None and price_kwh >= args.price_above:
        if args.off_command:
            run_cmd("Price is above threshold -> OFF command", args.off_command, execute)
            action_taken = True
    if not action_taken:
        print("No threshold condition matched; no command executed.")


def build_parser():
    p = argparse.ArgumentParser(
        description="OMIE Iberian market helper for Portugal/Spain day-ahead prices."
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    s1 = sub.add_parser("prices", help="Show upcoming hourly day-ahead prices.")
    s1.add_argument("--area", choices=sorted(VALID_AREAS), help="PT or ES (default: OMIE_AREA or PT).")
    s1.add_argument("--hours", type=int, default=24)
    s1.add_argument("--start", help="Fetch window start YYYY-MM-DD.")
    s1.add_argument("--end", help="Fetch window end YYYY-MM-DD.")

    s2 = sub.add_parser("optimize", help="Find cheapest contiguous time window.")
    s2.add_argument("--area", choices=sorted(VALID_AREAS), help="PT or ES (default: OMIE_AREA or PT).")
    s2.add_argument("--duration-hours", type=int)
    s2.add_argument("--kwh", type=float)
    s2.add_argument("--power-kw", type=float)
    s2.add_argument("--window-start")
    s2.add_argument("--window-end")
    s2.add_argument("--start", help="Fetch window start YYYY-MM-DD.")
    s2.add_argument("--end", help="Fetch window end YYYY-MM-DD.")

    s3 = sub.add_parser("compare", help="Compare Portugal vs Spain prices hour by hour.")
    s3.add_argument("--hours", type=int, default=24)
    s3.add_argument("--start", help="Fetch window start YYYY-MM-DD.")
    s3.add_argument("--end", help="Fetch window end YYYY-MM-DD.")

    s4 = sub.add_parser("control", help="Trigger commands from current price thresholds.")
    s4.add_argument("--area", choices=sorted(VALID_AREAS), help="PT or ES (default: OMIE_AREA or PT).")
    s4.add_argument("--price-below", type=float, help="Threshold in EUR/kWh.")
    s4.add_argument("--price-above", type=float, help="Threshold in EUR/kWh.")
    s4.add_argument("--on-command")
    s4.add_argument("--off-command")
    s4.add_argument("--execute", action="store_true")
    s4.add_argument("--start", help="Fetch window start YYYY-MM-DD.")
    s4.add_argument("--end", help="Fetch window end YYYY-MM-DD.")

    return p


def main():
    load_local_env_file()
    parser = build_parser()
    args = parser.parse_args()
    config = load_home_config("omie-energy")
    default_area = resolve_area(config)

    if args.cmd == "prices":
        command_prices(args, default_area)
    elif args.cmd == "optimize":
        command_optimize(args, default_area)
    elif args.cmd == "compare":
        command_compare(args)
    elif args.cmd == "control":
        command_control(args, default_area)
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
