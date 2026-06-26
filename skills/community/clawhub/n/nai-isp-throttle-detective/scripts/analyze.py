#!/usr/bin/env python3
"""
analyze.py - Analyze speed test history for throttling patterns.

Usage:
  python3 analyze.py
  python3 analyze.py --log /path/to/speed_log.jsonl
  python3 analyze.py --days 30
  python3 analyze.py --json   (machine-readable output)
"""

import json
import os
import statistics
import sys
from datetime import datetime, timedelta

DEFAULT_LOG_FILE = os.path.expanduser("~/.isp-throttle-detective/speed_log.jsonl")
ANOMALY_STDDEV_THRESHOLD = 2.0   # flag if speed is > N stddevs below mean
THROTTLE_CDN_RATIO = 0.75        # flag if CDN speed < 75% of general internet speed


def load_log(log_path: str, days: int = 90) -> list[dict]:
    if not os.path.exists(log_path):
        return []
    cutoff = datetime.now() - timedelta(days=days)
    entries = []
    with open(log_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
                date_str = e.get("date", "")
                if date_str:
                    try:
                        if datetime.strptime(date_str, "%Y-%m-%d") >= cutoff:
                            entries.append(e)
                    except ValueError:
                        entries.append(e)
                else:
                    entries.append(e)
            except json.JSONDecodeError:
                continue
    return entries


def extract_speeds(entries: list[dict], category_filter: str | None = None) -> list[dict]:
    """Flatten entries into per-endpoint speed records."""
    records = []
    for entry in entries:
        for key, v in entry.get("results", {}).items():
            if v.get("speed_mbps") is None:
                continue
            cat = v.get("category", "general")
            if category_filter and cat != category_filter:
                continue
            records.append({
                "endpoint": key,
                "label": v.get("label", key),
                "category": cat,
                "speed_mbps": v["speed_mbps"],
                "hour": entry.get("hour", 0),
                "day_of_week": entry.get("day_of_week", "Unknown"),
                "day_num": entry.get("day_num", 0),
                "date": entry.get("date", ""),
                "timestamp": entry.get("timestamp_local", ""),
            })
    return records


def avg(values: list[float]) -> float:
    return round(statistics.mean(values), 2) if values else 0.0


def stdev(values: list[float]) -> float:
    return round(statistics.stdev(values), 2) if len(values) >= 2 else 0.0


def group_by(records: list[dict], key: str) -> dict[str, list[float]]:
    groups: dict[str, list[float]] = {}
    for r in records:
        k = str(r.get(key, "unknown"))
        groups.setdefault(k, []).append(r["speed_mbps"])
    return groups


def analyze_by_hour(records: list[dict]) -> dict:
    groups = group_by(records, "hour")
    return {h: {"avg_mbps": avg(v), "count": len(v)} for h, v in sorted(groups.items(), key=lambda x: int(x[0]))}


def analyze_by_day(records: list[dict]) -> dict:
    groups = group_by(records, "day_of_week")
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return {d: {"avg_mbps": avg(groups[d]), "count": len(groups[d])} for d in day_order if d in groups}


def analyze_by_endpoint(records: list[dict]) -> dict:
    groups: dict[str, list] = {}
    for r in records:
        key = r["endpoint"]
        groups.setdefault(key, {"label": r["label"], "category": r["category"], "speeds": []})
        groups[key]["speeds"].append(r["speed_mbps"])
    return {
        k: {
            "label": v["label"],
            "category": v["category"],
            "avg_mbps": avg(v["speeds"]),
            "min_mbps": round(min(v["speeds"]), 2),
            "max_mbps": round(max(v["speeds"]), 2),
            "stdev": stdev(v["speeds"]),
            "count": len(v["speeds"]),
        }
        for k, v in groups.items()
    }


def peak_vs_offpeak(records: list[dict], peak_hours: list[int] | None = None) -> dict:
    if peak_hours is None:
        peak_hours = list(range(18, 24)) + list(range(0, 1))  # 6pm-midnight
    peak = [r["speed_mbps"] for r in records if r["hour"] in peak_hours]
    offpeak = [r["speed_mbps"] for r in records if r["hour"] not in peak_hours]
    return {
        "peak": {"avg_mbps": avg(peak), "count": len(peak)},
        "off_peak": {"avg_mbps": avg(offpeak), "count": len(offpeak)},
        "difference_mbps": round(avg(offpeak) - avg(peak), 2) if peak and offpeak else None,
        "peak_hours": peak_hours,
    }


def trend_analysis(entries: list[dict]) -> dict:
    """Simple linear regression on overall average speed over time."""
    daily_avg: dict[str, list[float]] = {}
    for entry in entries:
        date = entry.get("date", "")
        if not date:
            continue
        speeds = [
            v["speed_mbps"]
            for v in entry.get("results", {}).values()
            if v.get("speed_mbps") is not None and v.get("category") not in ("upload",)
        ]
        if speeds:
            daily_avg.setdefault(date, []).extend(speeds)

    if len(daily_avg) < 3:
        return {"status": "insufficient_data", "days_sampled": len(daily_avg)}

    sorted_days = sorted(daily_avg.keys())
    y = [avg(daily_avg[d]) for d in sorted_days]
    n = len(y)
    x = list(range(n))
    x_mean = sum(x) / n
    y_mean = sum(y) / n
    slope_num = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
    slope_den = sum((x[i] - x_mean) ** 2 for i in range(n))
    slope = round(slope_num / slope_den, 4) if slope_den != 0 else 0.0

    return {
        "days_sampled": n,
        "first_day": sorted_days[0],
        "last_day": sorted_days[-1],
        "slope_mbps_per_day": slope,
        "trend": "declining" if slope < -0.5 else "stable" if abs(slope) <= 0.5 else "improving",
        "first_week_avg": avg(y[:7]),
        "last_week_avg": avg(y[-7:]),
    }


def detect_anomalies(records: list[dict]) -> list[dict]:
    endpoint_groups: dict[str, list] = {}
    for r in records:
        endpoint_groups.setdefault(r["endpoint"], []).append(r)

    anomalies = []
    for ep, ep_records in endpoint_groups.items():
        speeds = [r["speed_mbps"] for r in ep_records]
        if len(speeds) < 5:
            continue
        mean = statistics.mean(speeds)
        sd = statistics.stdev(speeds)
        if sd == 0:
            continue
        for r in ep_records:
            z = (r["speed_mbps"] - mean) / sd
            if z < -ANOMALY_STDDEV_THRESHOLD:
                anomalies.append({
                    "endpoint": r["label"],
                    "date": r["date"],
                    "hour": r["hour"],
                    "speed_mbps": r["speed_mbps"],
                    "z_score": round(z, 2),
                    "mean_mbps": round(mean, 2),
                })
    return sorted(anomalies, key=lambda x: x["z_score"])


def detect_cdn_discrimination(by_endpoint: dict) -> dict:
    general = [v["avg_mbps"] for v in by_endpoint.values() if v["category"] == "general" and v["avg_mbps"] > 0]
    cdn = [v["avg_mbps"] for v in by_endpoint.values() if v["category"] == "cdn" and v["avg_mbps"] > 0]
    upload = [v["avg_mbps"] for v in by_endpoint.values() if v["category"] == "upload" and v["avg_mbps"] > 0]

    result: dict = {}
    if general and cdn:
        gen_avg = avg(general)
        cdn_avg = avg(cdn)
        ratio = round(cdn_avg / gen_avg, 3) if gen_avg > 0 else None
        result["cdn_vs_general_ratio"] = ratio
        result["cdn_avg_mbps"] = cdn_avg
        result["general_avg_mbps"] = gen_avg
        result["cdn_throttling_suspected"] = ratio is not None and ratio < THROTTLE_CDN_RATIO
    if upload:
        result["upload_avg_mbps"] = avg(upload)

    return result


def main():
    args = sys.argv[1:]
    log_path = DEFAULT_LOG_FILE
    days = 90
    json_output = False

    i = 0
    while i < len(args):
        if args[i] == "--log" and i + 1 < len(args):
            log_path = os.path.expanduser(args[i + 1])
            i += 2
        elif args[i] == "--days" and i + 1 < len(args):
            days = int(args[i + 1])
            i += 2
        elif args[i] == "--config" and i + 1 < len(args):
            config_path = args[i + 1]
            if os.path.exists(config_path):
                with open(config_path) as f:
                    cfg = json.load(f)
                log_path = os.path.expanduser(cfg.get("log_file", log_path))
            i += 2
        elif args[i] == "--json":
            json_output = True
            i += 1
        else:
            i += 1

    entries = load_log(log_path, days=days)
    if not entries:
        msg = {"error": f"No data found in {log_path}"}
        print(json.dumps(msg) if json_output else f"No data found in {log_path}")
        sys.exit(0)

    dl_records = [r for r in extract_speeds(entries) if r["category"] != "upload"]
    by_endpoint = analyze_by_endpoint(dl_records)
    cdn_disc = detect_cdn_discrimination(by_endpoint)
    peak = peak_vs_offpeak(dl_records)
    by_hour = analyze_by_hour(dl_records)
    by_day = analyze_by_day(dl_records)
    trend = trend_analysis(entries)
    anomalies = detect_anomalies(dl_records)

    analysis = {
        "summary": {
            "total_tests": len(entries),
            "date_range_days": days,
            "log_file": log_path,
        },
        "by_endpoint": by_endpoint,
        "cdn_discrimination": cdn_disc,
        "peak_vs_offpeak": peak,
        "by_hour": by_hour,
        "by_day_of_week": by_day,
        "trend": trend,
        "anomalies": anomalies[:20],  # top 20 worst
    }

    if json_output:
        print(json.dumps(analysis, indent=2))
    else:
        # Human-readable summary
        print(f"\n=== ISP Throttle Detective — Analysis ===")
        print(f"Log: {log_path}")
        print(f"Total tests: {len(entries)} | Range: last {days} days")

        print("\n--- Speed by Endpoint ---")
        for k, v in by_endpoint.items():
            print(f"  {v['label']:35s}  avg={v['avg_mbps']:6.1f} Mbps  "
                  f"min={v['min_mbps']:5.1f}  max={v['max_mbps']:5.1f}  n={v['count']}")

        print("\n--- Peak vs Off-Peak ---")
        p = peak
        print(f"  Peak hours {p['peak_hours'][0]}-{p['peak_hours'][-1]}:  {p['peak']['avg_mbps']} Mbps  (n={p['peak']['count']})")
        print(f"  Off-peak:                    {p['off_peak']['avg_mbps']} Mbps  (n={p['off_peak']['count']})")
        if p["difference_mbps"] is not None:
            print(f"  Difference: {p['difference_mbps']} Mbps slower at peak")

        if cdn_disc:
            print("\n--- CDN Discrimination ---")
            for k, v in cdn_disc.items():
                print(f"  {k}: {v}")

        print("\n--- Trend ---")
        for k, v in trend.items():
            print(f"  {k}: {v}")

        if anomalies:
            print(f"\n--- Anomalies ({len(anomalies)} detected) ---")
            for a in anomalies[:5]:
                print(f"  {a['date']} {a['hour']:02d}:00  {a['endpoint']:30s}  "
                      f"{a['speed_mbps']} Mbps  (z={a['z_score']}, mean={a['mean_mbps']} Mbps)")

        print()


if __name__ == "__main__":
    main()
