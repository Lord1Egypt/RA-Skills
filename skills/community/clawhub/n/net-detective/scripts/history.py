#!/usr/bin/env python3
"""
Maintain a rolling baseline of diagnostic results.
Supports --record <json_file> and --compare <json_file>.
"""

import json
import os
import sys
import statistics
from datetime import datetime, timezone

HISTORY_FILE = os.path.expanduser(
    "~/.openclaw/workspace/skills/net-detective/data/history.json"
)
MAX_RECORDS = 30  # keep up to 30 runs for baseline


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_history(records):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(records[-MAX_RECORDS:], f, indent=2)


def extract_metrics(diag):
    """Pull key scalar metrics from a diagnostic JSON blob."""
    metrics = {}

    # Ping latency
    ping = diag.get("ping", {})
    latencies = []
    packet_loss_total = 0
    ping_count = 0
    for host, data in ping.items():
        if isinstance(data, dict):
            if data.get("avg_ms") is not None:
                latencies.append(data["avg_ms"])
            if data.get("packet_loss_pct") is not None:
                packet_loss_total += data["packet_loss_pct"]
                ping_count += 1
    if latencies:
        metrics["avg_ping_ms"] = round(statistics.mean(latencies), 2)
        metrics["max_ping_ms"] = round(max(latencies), 2)
    if ping_count > 0:
        metrics["avg_packet_loss_pct"] = round(packet_loss_total / ping_count, 2)

    # DNS latency
    dns = diag.get("dns", {}).get("summary", {}).get("server_avg_ms", {})
    if dns:
        all_dns = list(dns.values())
        metrics["avg_dns_ms"] = round(statistics.mean(all_dns), 2)
        metrics["system_dns_ms"] = dns.get("system")
        metrics["cloudflare_dns_ms"] = dns.get("cloudflare")
        metrics["google_dns_ms"] = dns.get("google")

    # Speed
    speed = diag.get("speed", {}).get("summary", {})
    if speed.get("headline_mbps") is not None:
        metrics["speed_mbps"] = speed["headline_mbps"]

    return metrics


def compute_baseline(records):
    """Compute mean and stdev for each metric across historical records."""
    if not records:
        return {}
    all_metrics = [r.get("metrics", {}) for r in records]
    keys = set()
    for m in all_metrics:
        keys.update(m.keys())
    baseline = {}
    for key in keys:
        values = [m[key] for m in all_metrics if key in m and m[key] is not None]
        if len(values) >= 2:
            baseline[key] = {
                "mean": round(statistics.mean(values), 2),
                "stdev": round(statistics.stdev(values), 2),
                "samples": len(values),
            }
        elif len(values) == 1:
            baseline[key] = {"mean": values[0], "stdev": 0, "samples": 1}
    return baseline


def detect_anomalies(current_metrics, baseline):
    """Flag metrics that deviate significantly from baseline."""
    anomalies = []
    THRESHOLDS = {
        "avg_ping_ms": (2.0, "Latency is {val}ms vs baseline {mean}ms — significant spike detected."),
        "max_ping_ms": (2.0, "Max ping {val}ms vs baseline {mean}ms — high jitter."),
        "avg_packet_loss_pct": (None, "Packet loss at {val}% — baseline was {mean}%."),
        "avg_dns_ms": (3.0, "DNS response time {val}ms vs baseline {mean}ms — DNS may be struggling."),
        "system_dns_ms": (3.0, "System DNS {val}ms vs baseline {mean}ms — local resolver slow."),
        "speed_mbps": (None, "Download speed {val} Mbps vs baseline {mean} Mbps — speed drop."),
    }
    for key, (sigma_threshold, msg_template) in THRESHOLDS.items():
        if key not in current_metrics or key not in baseline:
            continue
        val = current_metrics[key]
        b = baseline[key]
        mean = b["mean"]
        stdev = b["stdev"]
        if val is None:
            continue

        if key in ("avg_packet_loss_pct",):
            # Flag any packet loss if baseline was near 0
            if val > 1 and mean < 1:
                anomalies.append({
                    "metric": key,
                    "current": val,
                    "baseline_mean": mean,
                    "severity": "high" if val > 5 else "medium",
                    "message": msg_template.format(val=val, mean=mean),
                })
        elif key == "speed_mbps":
            # Flag if speed dropped by more than 50%
            if mean > 0 and val < mean * 0.5:
                anomalies.append({
                    "metric": key,
                    "current": val,
                    "baseline_mean": mean,
                    "severity": "medium",
                    "message": msg_template.format(val=val, mean=mean),
                })
        else:
            if stdev > 0 and sigma_threshold:
                z = (val - mean) / stdev
                if z > sigma_threshold:
                    severity = "high" if z > 4 else "medium"
                    anomalies.append({
                        "metric": key,
                        "current": val,
                        "baseline_mean": mean,
                        "z_score": round(z, 2),
                        "severity": severity,
                        "message": msg_template.format(val=val, mean=round(mean, 1)),
                    })
            elif stdev == 0 and mean > 0 and val > mean * 2:
                anomalies.append({
                    "metric": key,
                    "current": val,
                    "baseline_mean": mean,
                    "severity": "medium",
                    "message": msg_template.format(val=val, mean=mean),
                })
    return anomalies


def cmd_record(diag_file):
    with open(diag_file) as f:
        diag = json.load(f)
    metrics = extract_metrics(diag)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metrics": metrics,
    }
    history = load_history()
    history.append(record)
    save_history(history)
    print(json.dumps({"status": "recorded", "metrics": metrics, "total_records": len(history)}, indent=2))


def cmd_compare(diag_file):
    with open(diag_file) as f:
        diag = json.load(f)
    current_metrics = extract_metrics(diag)
    history = load_history()
    baseline = compute_baseline(history)
    anomalies = detect_anomalies(current_metrics, baseline)
    print(json.dumps({
        "current_metrics": current_metrics,
        "baseline": baseline,
        "anomalies": anomalies,
        "history_samples": len(history),
    }, indent=2))


def cmd_show():
    history = load_history()
    baseline = compute_baseline(history)
    print(json.dumps({"baseline": baseline, "history_samples": len(history)}, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: history.py --record <diag.json> | --compare <diag.json> | --show", file=sys.stderr)
        sys.exit(1)

    mode = sys.argv[1]
    if mode == "--record":
        if len(sys.argv) < 3:
            print("--record requires a JSON file path", file=sys.stderr)
            sys.exit(1)
        cmd_record(sys.argv[2])
    elif mode == "--compare":
        if len(sys.argv) < 3:
            print("--compare requires a JSON file path", file=sys.stderr)
            sys.exit(1)
        cmd_compare(sys.argv[2])
    elif mode == "--show":
        cmd_show()
    else:
        print(f"Unknown mode: {mode}", file=sys.stderr)
        sys.exit(1)
