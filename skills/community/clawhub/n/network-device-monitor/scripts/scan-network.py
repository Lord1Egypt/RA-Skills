#!/usr/bin/env python3
"""
Network Device Monitor
Scans network for devices, tracks state, alerts on unknown connections.
Works with any subnet — no router-specific dependencies.
"""

import argparse
import json
import os
import subprocess
import sys
import re
from datetime import datetime


def arp_scan(subnet):
    """Fast ARP-based scan (requires root)."""
    try:
        result = subprocess.run(["arp-scan", "--localnet"], capture_output=True, text=True, timeout=30)
        devices = []
        for line in result.stdout.splitlines():
            match = re.match(r'(\d+\.\d+\.\d+\.\d+)\s+([0-9a-f:]{17})\s+(.*)', line, re.IGNORECASE)
            if match:
                devices.append({
                    "ip": match.group(1),
                    "mac": match.group(2).upper(),
                    "hostname": match.group(3).strip()
                })
        return devices
    except FileNotFoundError:
        print("arp-scan not found, falling back to nmap", file=sys.stderr)
        return nmap_scan(subnet)


def nmap_scan(subnet):
    """Nmap-based scan (no root required)."""
    try:
        result = subprocess.run(
            ["nmap", "-sn", "-oG", "-", subnet],
            capture_output=True, text=True, timeout=120
        )
        devices = []
        for line in result.stdout.splitlines():
            if "Host:" in line and "Up" in line:
                ip_match = re.search(r'Host:\s+(\d+\.\d+\.\d+\.\d+)', line)
                mac_match = re.search(r'MAC:\s+([0-9A-F:]{17})', line, re.IGNORECASE)
                host_match = re.search(r'\(([^)]+)\)', line)
                if ip_match:
                    devices.append({
                        "ip": ip_match.group(1),
                        "mac": mac_match.group(1).upper() if mac_match else "Unknown",
                        "hostname": host_match.group(1) if host_match else ""
                    })
        return devices
    except FileNotFoundError:
        print("nmap not found. Install nmap or arp-scan.", file=sys.stderr)
        sys.exit(1)


def load_state(state_file):
    if os.path.exists(state_file):
        with open(state_file) as f:
            return json.load(f)
    return {"last_scan": None, "devices": {}, "unknown_devices": []}


def save_state(state, state_file):
    os.makedirs(os.path.dirname(state_file) or ".", exist_ok=True)
    with open(state_file, "w") as f:
        json.dump(state, f, indent=2)


def load_known(known_file):
    if known_file and os.path.exists(known_file):
        with open(known_file) as f:
            return json.load(f)
    return {}


def detect_changes(devices, known, state):
    now = datetime.now().isoformat()
    new_devices = []
    unknown = []
    gone_offline = []

    current_macs = {d["mac"] for d in devices}

    # Check for new / updated devices
    for dev in devices:
        mac = dev["mac"]
        if mac not in state["devices"]:
            new_devices.append(dev)
        state["devices"][mac] = {
            "ip": dev["ip"],
            "hostname": dev.get("hostname", ""),
            "first_seen": state["devices"].get(mac, {}).get("first_seen", now),
            "last_seen": now,
            "status": "online"
        }
        if mac not in known:
            unknown.append(dev)

    # Check for gone offline
    for mac, info in state["devices"].items():
        if mac not in current_macs and info.get("status") == "online":
            info["status"] = "offline"
            gone_offline.append({"mac": mac, **info})

    state["last_scan"] = now
    state["unknown_devices"] = [d["mac"] for d in unknown]

    return new_devices, unknown, gone_offline


def print_table(devices, known):
    print(f"{'IP':<16} {'MAC':<20} {'Name':<25} {'Status':<10}")
    print("-" * 75)
    for d in sorted(devices, key=lambda x: x["ip"]):
        name = known.get(d["mac"], d.get("hostname", "Unknown"))
        print(f"{d['ip']:<16} {d['mac']:<20} {name:<25} {'Online':<10}")


def main():
    parser = argparse.ArgumentParser(description="Network Device Monitor")
    parser.add_argument("--subnet", required=True, help="Network CIDR (e.g., 192.168.1.0/24)")
    parser.add_argument("--arp", action="store_true", help="Use ARP scan (faster, needs root)")
    parser.add_argument("--known", help="Known devices JSON file")
    parser.add_argument("--state", default=os.path.expanduser("~/.network-state.json"), help="State file")
    parser.add_argument("--alerts", action="store_true", help="Only output if unknown devices found")
    parser.add_argument("--json", action="store_true", dest="json_out", help="JSON output")
    parser.add_argument("--table", action="store_true", help="Table output")
    args = parser.parse_args()

    known = load_known(args.known)
    state = load_state(args.state)

    print(f"Scanning {args.subnet}...", file=sys.stderr)
    devices = arp_scan(args.subnet) if args.arp else nmap_scan(args.subnet)

    new_devices, unknown, gone = detect_changes(devices, known, state)
    save_state(state, args.state)

    if args.alerts and not unknown:
        return  # Silent when no unknown devices

    if args.json_out:
        output = {
            "scan_time": state["last_scan"],
            "total_devices": len(devices),
            "devices": devices,
            "new_devices": new_devices,
            "unknown_devices": unknown,
            "gone_offline": gone
        }
        print(json.dumps(output, indent=2))
    elif args.table:
        print_table(devices, known)
    else:
        print(f"\n=== Scan Results ({len(devices)} devices) ===")
        if new_devices:
            print(f"\n🆕 NEW DEVICES ({len(new_devices)}):")
            for d in new_devices:
                name = known.get(d["mac"], "UNKNOWN")
                print(f"  {d['ip']} — {d['mac']} — {name}")
        if unknown:
            print(f"\n⚠️  UNKNOWN DEVICES ({len(unknown)}):")
            for d in unknown:
                print(f"  {d['ip']} — {d['mac']} — {d.get('hostname', '')}")
        if gone:
            print(f"\n🔴 GONE OFFLINE ({len(gone)}):")
            for d in gone:
                print(f"  {d['mac']} — {d.get('hostname', '')}")
        if not new_devices and not unknown and not gone:
            print("All clear — no changes detected.")


if __name__ == "__main__":
    main()
