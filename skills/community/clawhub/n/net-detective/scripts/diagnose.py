#!/usr/bin/env python3
"""
Net Detective — full diagnostic orchestrator.
Runs DNS checks, ping tests, traceroute, MTU detection, and optional speed test.
Outputs unified JSON to stdout.
"""

import json
import os
import platform
import re
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone

PING_HOSTS = [
    "google.com",
    "cloudflare.com",
    "1.1.1.1",
    "8.8.8.8",
    "fastly.net",
]

TRACEROUTE_HOST = "google.com"
IS_MAC = platform.system() == "Darwin"


# ---------------------------------------------------------------------------
# Ping
# ---------------------------------------------------------------------------

PING_BIN = None  # resolved on first use


def get_ping_bin():
    global PING_BIN
    if PING_BIN is None:
        for path in ["/sbin/ping", "/bin/ping", "/usr/bin/ping", "ping"]:
            try:
                subprocess.run([path, "-c", "1", "-W", "500", "127.0.0.1"],
                               capture_output=True, timeout=2)
                PING_BIN = path
                break
            except FileNotFoundError:
                continue
            except Exception:
                PING_BIN = path
                break
        if PING_BIN is None:
            PING_BIN = "ping"
    return PING_BIN


def run_ping(host, count=5):
    ping_bin = get_ping_bin()
    if IS_MAC:
        cmd = [ping_bin, "-c", str(count), "-W", "2000", host]
    else:
        cmd = [ping_bin, "-c", str(count), "-W", "2", host]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=20
        )
        output = result.stdout + result.stderr

        # Parse packet loss
        loss_match = re.search(r"(\d+(?:\.\d+)?)%\s+packet loss", output)
        loss = float(loss_match.group(1)) if loss_match else None

        # Parse RTT stats (min/avg/max/stddev or mdev)
        rtt_match = re.search(
            r"(?:rtt|round-trip)\s+min/avg/max/(?:stddev|mdev)\s*=\s*([\d.]+)/([\d.]+)/([\d.]+)",
            output,
        )
        if rtt_match:
            min_ms = float(rtt_match.group(1))
            avg_ms = float(rtt_match.group(2))
            max_ms = float(rtt_match.group(3))
        else:
            min_ms = avg_ms = max_ms = None

        reachable = result.returncode == 0 or (loss is not None and loss < 100)
        return {
            "host": host,
            "reachable": reachable,
            "packet_loss_pct": loss,
            "min_ms": min_ms,
            "avg_ms": avg_ms,
            "max_ms": max_ms,
        }
    except subprocess.TimeoutExpired:
        return {"host": host, "reachable": False, "error": "timeout"}
    except FileNotFoundError:
        return {"host": host, "reachable": False, "error": "ping not found"}
    except Exception as e:
        return {"host": host, "reachable": False, "error": str(e)}


# ---------------------------------------------------------------------------
# Traceroute
# ---------------------------------------------------------------------------

def find_traceroute():
    for path in ["/usr/sbin/traceroute", "/sbin/traceroute", "/usr/bin/traceroute", "traceroute"]:
        try:
            subprocess.run([path, "--help"], capture_output=True, timeout=2)
            return path
        except FileNotFoundError:
            continue
        except Exception:
            return path
    return "traceroute"


def run_traceroute(host, max_hops=20):
    tr_bin = find_traceroute()
    if IS_MAC:
        cmd = [tr_bin, "-m", str(max_hops), "-w", "2", host]
    else:
        cmd = [tr_bin, "-m", str(max_hops), "-w", "2", "--", host]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60
        )
        output = result.stdout
        hops = []
        for line in output.splitlines():
            line = line.strip()
            hop_match = re.match(r"^\s*(\d+)\s+(.+)$", line)
            if not hop_match:
                continue
            hop_num = int(hop_match.group(1))
            rest = hop_match.group(2).strip()

            if rest.startswith("* * *"):
                hops.append({"hop": hop_num, "host": "*", "latencies_ms": [], "timeout": True})
                continue

            # Extract hostname/IP
            host_match = re.match(r"([^\s(]+)\s*(?:\(([^)]+)\))?", rest)
            hop_host = host_match.group(1) if host_match else "*"
            hop_ip = host_match.group(2) if host_match and host_match.group(2) else hop_host

            # Extract latencies
            latencies = [float(m) for m in re.findall(r"([\d.]+)\s*ms", rest)]
            hops.append({
                "hop": hop_num,
                "host": hop_host,
                "ip": hop_ip,
                "latencies_ms": latencies,
                "avg_ms": round(sum(latencies) / len(latencies), 2) if latencies else None,
                "timeout": False,
            })

        # Detect first timeout hop (potential loss point)
        first_loss_hop = None
        for h in hops:
            if h.get("timeout"):
                first_loss_hop = h["hop"]
                break

        return {
            "host": host,
            "hops": hops,
            "total_hops": len(hops),
            "first_timeout_hop": first_loss_hop,
            "raw": output,
        }
    except subprocess.TimeoutExpired:
        return {"host": host, "hops": [], "error": "traceroute timed out"}
    except FileNotFoundError:
        return {"host": host, "hops": [], "error": "traceroute not found"}
    except Exception as e:
        return {"host": host, "hops": [], "error": str(e)}


# ---------------------------------------------------------------------------
# MTU detection
# ---------------------------------------------------------------------------

def detect_mtu(host="8.8.8.8"):
    """
    Binary-search for the largest ping payload that passes without fragmentation.
    macOS: uses regular ping (no DF flag needed — macOS doesn't fragment ICMP by default).
    Linux: uses ping -M do to set DF bit.
    Returns estimated path MTU = payload_size + 28 (IP+ICMP headers).
    """
    ping_bin = get_ping_bin()

    if IS_MAC:
        # macOS ping doesn't have a user-facing DF control, but ICMP probes
        # travel unfragmented by default in most paths. We use regular ping
        # to find max working payload size.
        def probe(size):
            try:
                result = subprocess.run(
                    [ping_bin, "-c", "1", "-W", "2000", "-s", str(size), host],
                    capture_output=True, text=True, timeout=5
                )
                return result.returncode == 0
            except Exception:
                return False
    else:
        # Linux: ping -M do sets DF bit; returns non-zero if packet too large
        def probe(size):
            try:
                result = subprocess.run(
                    [ping_bin, "-c", "1", "-W", "2", "-M", "do", "-s", str(size), host],
                    capture_output=True, text=True, timeout=5
                )
                return result.returncode == 0
            except Exception:
                return False

    # Binary search between 576 and 1472 bytes payload
    lo, hi = 576, 1472
    best = lo
    for _ in range(10):
        mid = (lo + hi) // 2
        if probe(mid):
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
        if lo > hi:
            break

    mtu = best + 28  # IP(20) + ICMP(8)
    fragmentation_likely = mtu < 1492  # 1492 = PPPoE; 1500 = standard Ethernet
    return {
        "estimated_path_mtu": mtu,
        "max_payload_bytes": best,
        "fragmentation_likely": fragmentation_likely,
        "note": "Path MTU < 1492 suggests fragmentation along the route." if fragmentation_likely else "Path MTU looks normal (standard Ethernet or PPPoE).",
    }


# ---------------------------------------------------------------------------
# Local interface info
# ---------------------------------------------------------------------------

def get_local_info():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        hostname = "unknown"
        local_ip = "unknown"

    gateway = None
    try:
        if IS_MAC:
            r = subprocess.run(["route", "-n", "get", "default"], capture_output=True, text=True, timeout=5)
            m = re.search(r"gateway:\s+([\d.]+)", r.stdout)
            if m:
                gateway = m.group(1)
        else:
            r = subprocess.run(["ip", "route", "show", "default"], capture_output=True, text=True, timeout=5)
            m = re.search(r"default\s+via\s+([\d.]+)", r.stdout)
            if m:
                gateway = m.group(1)
    except Exception:
        pass

    return {"hostname": hostname, "local_ip": local_ip, "gateway": gateway}


# ---------------------------------------------------------------------------
# DNS (import sibling module)
# ---------------------------------------------------------------------------

def run_dns():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dns_script = os.path.join(script_dir, "dns_check.py")
    try:
        result = subprocess.run(
            [sys.executable, dns_script],
            capture_output=True, text=True, timeout=30
        )
        return json.loads(result.stdout)
    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------------------------------
# Speed test (optional)
# ---------------------------------------------------------------------------

def run_speed(quick=True):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    speed_script = os.path.join(script_dir, "speedtest.py")
    args = [sys.executable, speed_script]
    if quick:
        args.append("--quick")
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=60)
        return json.loads(result.stdout)
    except Exception as e:
        return {"error": str(e)}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    include_speed = "--speed" in sys.argv
    include_traceroute = "--no-traceroute" not in sys.argv
    include_mtu = "--no-mtu" not in sys.argv

    print("Running net-detective diagnostics...", file=sys.stderr)

    diag = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "platform": platform.system(),
        "local": get_local_info(),
    }

    # Ping all endpoints
    print("  → Ping tests...", file=sys.stderr)
    diag["ping"] = {}
    for host in PING_HOSTS:
        diag["ping"][host] = run_ping(host)

    # DNS checks
    print("  → DNS checks...", file=sys.stderr)
    diag["dns"] = run_dns()

    # Traceroute
    if include_traceroute:
        print(f"  → Traceroute to {TRACEROUTE_HOST}...", file=sys.stderr)
        diag["traceroute"] = run_traceroute(TRACEROUTE_HOST)

    # MTU detection
    if include_mtu:
        print("  → MTU detection...", file=sys.stderr)
        diag["mtu"] = detect_mtu()

    # Speed test (optional)
    if include_speed:
        print("  → Speed test...", file=sys.stderr)
        diag["speed"] = run_speed(quick=True)

    print("Done.", file=sys.stderr)
    print(json.dumps(diag, indent=2))


if __name__ == "__main__":
    main()
