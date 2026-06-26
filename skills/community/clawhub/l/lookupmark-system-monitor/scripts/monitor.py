#!/usr/bin/env python3
"""System health monitor for Raspberry Pi / ARM devices.

Reads /proc, /sys, ps, df, vcgencmd for system stats.
Zero external dependencies — stdlib only.

Usage:
    monitor.py                    # Full status report
    monitor.py --json             # JSON output
    monitor.py --check-alerts     # Compare thresholds, return alerts
    monitor.py --top N            # Top N processes by CPU/MEM
"""

import json
import os
import re
import subprocess
import sys
import time


def get_cpu():
    try:
        with open("/proc/stat") as f:
            line = f.readline()
        vals = list(map(int, line.split()[1:]))
        idle = vals[3]
        total = sum(vals)
        time.sleep(0.1)
        with open("/proc/stat") as f:
            line = f.readline()
        vals2 = list(map(int, line.split()[1:]))
        idle2 = vals2[3]
        total2 = sum(vals2)
        usage = 1 - (idle2 - idle) / (total2 - total) if total2 != total else 0
        return round(usage * 100, 1)
    except Exception:
        return None


def get_ram():
    try:
        info = {}
        with open("/proc/meminfo") as f:
            for line in f:
                parts = line.split()
                if "MemTotal" in line:
                    info["total_mb"] = int(parts[1]) / 1024
                elif "MemAvailable" in line:
                    info["available_mb"] = int(parts[1]) / 1024
                elif "SwapTotal" in line:
                    info["swap_total_mb"] = int(parts[1]) / 1024
                elif "SwapFree" in line:
                    info["swap_free_mb"] = int(parts[1]) / 1024
        info["used_mb"] = info["total_mb"] - info["available_mb"]
        info["used_pct"] = round(info["used_mb"] / info["total_mb"] * 100, 1) if info["total_mb"] > 0 else 0
        info["swap_used_mb"] = info["swap_total_mb"] - info["swap_free_mb"]
        return info
    except Exception:
        return None


def get_disk():
    try:
        result = subprocess.run(["df", "-h", "-x", "tmpfs", "-x", "devtmpfs"],
                                capture_output=True, text=True, timeout=5)
        disks = []
        for line in result.stdout.strip().splitlines()[1:]:
            parts = line.split()
            if len(parts) >= 6 and parts[5].startswith("/"):
                disks.append({
                    "mount": parts[5],
                    "size": parts[1],
                    "used": parts[2],
                    "avail": parts[3],
                    "pct": parts[4].rstrip("%"),
                })
        return disks
    except Exception:
        return None


def get_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return round(int(f.read().strip()) / 1000, 1)
    except Exception:
        return None


def get_uptime():
    try:
        with open("/proc/uptime") as f:
            secs = float(f.read().split()[0])
        days = int(secs // 86400)
        hours = int((secs % 86400) // 3600)
        mins = int((secs % 3600) // 60)
        return f"{days}d {hours}h {mins}m"
    except Exception:
        return None


def get_load():
    try:
        with open("/proc/loadavg") as f:
            parts = f.read().split()[:3]
        return {"1m": float(parts[0]), "5m": float(parts[1]), "15m": float(parts[2])}
    except Exception:
        return None


def sanitize_cmdline(cmdline: str) -> str:
    """Redact sensitive patterns from command lines."""
    cmdline = re.sub(r'((?:token|key|secret|password|apikey|api_key|access_token)=)\S+', r'\1***', cmdline, flags=re.IGNORECASE)
    cmdline = re.sub(r'(--(?:token|key|password|secret|api-key))\s+\S+', r'\1 ***', cmdline, flags=re.IGNORECASE)
    return cmdline


def get_top_processes(n=5):
    try:
        result = subprocess.run(
            ["ps", "aux", "--sort=-pcpu"],
            capture_output=True, text=True, timeout=5
        )
        procs = []
        for line in result.stdout.strip().splitlines()[1:n+1]:
            parts = line.split(None, 10)
            if len(parts) >= 11:
                cmd = sanitize_cmdline(parts[10])
                procs.append({
                    "user": parts[0],
                    "pid": parts[1],
                    "cpu": parts[2],
                    "mem": parts[3],
                    "rss_mb": round(int(parts[5]) / 1024, 1),
                    "command": cmd[:60],
                })
        return procs
    except Exception:
        return None


def get_full_status():
    return {
        "cpu_pct": get_cpu(),
        "ram": get_ram(),
        "disk": get_disk(),
        "temp_c": get_temp(),
        "uptime": get_uptime(),
        "load": get_load(),
        "top": get_top_processes(5),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }


CONFIG_PATH = os.path.expanduser("~/.config/system-monitor/config.json")
DEFAULT_THRESHOLDS = {"ram_pct": 90, "disk_pct": 90, "temp_c": 75, "swap_mb": 500}


def load_thresholds() -> dict:
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as f:
                cfg = json.load(f)
            return {**DEFAULT_THRESHOLDS, **cfg.get("thresholds", {})}
        except Exception:
            pass
    return DEFAULT_THRESHOLDS


def check_alerts(thresholds=None):
    thresholds = thresholds or load_thresholds()
    alerts = []
    ram = get_ram()
    if ram and ram["used_pct"] > thresholds["ram_pct"]:
        alerts.append(f"🔴 RAM: {ram['used_pct']}% (threshold: {thresholds['ram_pct']}%)")
    if ram and ram["swap_used_mb"] > thresholds["swap_mb"]:
        alerts.append(f"🔴 Swap: {ram['swap_used_mb']:.0f}MB used (threshold: {thresholds['swap_mb']}MB)")
    temp = get_temp()
    if temp and temp > thresholds["temp_c"]:
        alerts.append(f"🔴 CPU temp: {temp}°C (threshold: {thresholds['temp_c']}°C)")
    disks = get_disk()
    if disks:
        for d in disks:
            if int(d["pct"]) > thresholds["disk_pct"]:
                alerts.append(f"🔴 Disk {d['mount']}: {d['pct']}% full (threshold: {thresholds['disk_pct']}%)")
    if not alerts:
        alerts.append("✅ All systems normal")
    return alerts


def format_status(data):
    lines = []
    lines.append("📊 System Status")
    lines.append(f"  Uptime: {data['uptime']}")
    if data["cpu_pct"] is not None:
        lines.append(f"  CPU: {data['cpu_pct']}%")
    if data["temp_c"] is not None:
        lines.append(f"  Temp: {data['temp_c']}°C")
    if data["load"]:
        lines.append(f"  Load: {data['load']['1m']:.2f} / {data['load']['5m']:.2f} / {data['load']['15m']:.2f}")
    if data["ram"]:
        r = data["ram"]
        lines.append(f"  RAM: {r['used_mb']:.0f}/{r['total_mb']:.0f}MB ({r['used_pct']}%)")
        lines.append(f"  Swap: {r['swap_used_mb']:.0f}/{r['swap_total_mb']:.0f}MB")
    if data["disk"]:
        for d in data["disk"]:
            lines.append(f"  Disk {d['mount']}: {d['used']}/{d['size']} ({d['pct']}%)")
    if data["top"]:
        lines.append("  Top processes:")
        for p in data["top"]:
            lines.append(f"    {p['command'][:40]}  CPU:{p['cpu']}%  MEM:{p['rss_mb']}MB")
    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="System health monitor")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--check-alerts", action="store_true")
    parser.add_argument("--top", type=int, default=5)
    args = parser.parse_args()

    if args.check_alerts:
        for a in check_alerts():
            print(a)
    else:
        data = get_full_status()
        data["top"] = get_top_processes(args.top)
        if args.json:
            print(json.dumps(data, indent=2))
        else:
            print(format_status(data))


if __name__ == "__main__":
    main()
