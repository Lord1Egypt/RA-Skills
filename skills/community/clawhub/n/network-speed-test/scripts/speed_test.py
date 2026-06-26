#!/usr/bin/env python3
"""Network Speed Test — measure download/upload speed and latency using public endpoints.

No external dependencies required. Uses standard library only.

Usage:
  python3 speed_test.py [--download] [--upload] [--latency] [--all] [--json] [--size <MB>]
  python3 speed_test.py --all
  python3 speed_test.py --latency --json
"""

import argparse
import json
import socket
import sys
import time
import urllib.request
import urllib.error
import io
import statistics


# Public download test endpoints (large static files)
DOWNLOAD_URLS = [
    ("Cloudflare", "https://speed.cloudflare.com/__down?bytes=10000000"),
    ("Google (gstatic)", "https://www.gstatic.com/generate_204"),
]

# Upload test endpoint
UPLOAD_URL = "https://speed.cloudflare.com/__up"

# Latency test hosts
LATENCY_HOSTS = [
    ("Cloudflare DNS", "1.1.1.1", 443),
    ("Google DNS", "8.8.8.8", 443),
    ("Quad9 DNS", "9.9.9.9", 443),
]


def measure_latency(host, port, count=5, timeout=5):
    """Measure TCP connection latency to a host:port."""
    latencies = []
    for _ in range(count):
        try:
            start = time.monotonic()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            elapsed = (time.monotonic() - start) * 1000  # ms
            latencies.append(elapsed)
            sock.close()
        except (socket.timeout, OSError):
            pass
        time.sleep(0.1)
    return latencies


def measure_download(size_bytes=10_000_000, timeout=30):
    """Measure download speed using Cloudflare speed test endpoint."""
    url = f"https://speed.cloudflare.com/__down?bytes={size_bytes}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "SpeedTest/1.0"})
        start = time.monotonic()
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            total = 0
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                total += len(chunk)
        elapsed = time.monotonic() - start
        if elapsed <= 0:
            return None, None, None
        speed_bps = (total * 8) / elapsed
        speed_mbps = speed_bps / 1_000_000
        return total, elapsed, speed_mbps
    except (urllib.error.URLError, OSError, Exception) as e:
        print(f"  Download test failed: {e}", file=sys.stderr)
        return None, None, None


def measure_upload(size_bytes=5_000_000, timeout=30):
    """Measure upload speed using Cloudflare speed test endpoint."""
    data = b"0" * size_bytes
    try:
        req = urllib.request.Request(
            UPLOAD_URL,
            data=data,
            headers={
                "User-Agent": "SpeedTest/1.0",
                "Content-Type": "application/octet-stream",
                "Content-Length": str(size_bytes),
            },
            method="POST",
        )
        start = time.monotonic()
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            resp.read()
        elapsed = time.monotonic() - start
        if elapsed <= 0:
            return None, None, None
        speed_bps = (size_bytes * 8) / elapsed
        speed_mbps = speed_bps / 1_000_000
        return size_bytes, elapsed, speed_mbps
    except (urllib.error.URLError, OSError, Exception) as e:
        print(f"  Upload test failed: {e}", file=sys.stderr)
        return None, None, None


def format_speed(mbps):
    """Format speed value."""
    if mbps is None:
        return "N/A"
    if mbps >= 1000:
        return f"{mbps/1000:.2f} Gbps"
    return f"{mbps:.2f} Mbps"


def format_bytes(b):
    """Format byte count."""
    if b is None:
        return "N/A"
    if b >= 1_000_000_000:
        return f"{b/1_000_000_000:.2f} GB"
    if b >= 1_000_000:
        return f"{b/1_000_000:.2f} MB"
    if b >= 1_000:
        return f"{b/1_000:.1f} KB"
    return f"{b} B"


def run_latency_test(as_json=False):
    """Run latency tests against multiple hosts."""
    results = []
    if not as_json:
        print("\n📡 Latency Test")
        print("─" * 50)

    for name, host, port in LATENCY_HOSTS:
        latencies = measure_latency(host, port)
        if latencies:
            avg = statistics.mean(latencies)
            mn = min(latencies)
            mx = max(latencies)
            jitter = statistics.stdev(latencies) if len(latencies) > 1 else 0
            results.append({
                "host": name,
                "ip": host,
                "avg_ms": round(avg, 2),
                "min_ms": round(mn, 2),
                "max_ms": round(mx, 2),
                "jitter_ms": round(jitter, 2),
                "samples": len(latencies),
            })
            if not as_json:
                print(f"  {name} ({host}): avg={avg:.1f}ms  min={mn:.1f}ms  max={mx:.1f}ms  jitter={jitter:.1f}ms")
        else:
            results.append({"host": name, "ip": host, "error": "timeout"})
            if not as_json:
                print(f"  {name} ({host}): ❌ timed out")

    return results


def run_download_test(size_mb=10, as_json=False):
    """Run download speed test."""
    size_bytes = int(size_mb * 1_000_000)
    if not as_json:
        print(f"\n⬇️  Download Test ({size_mb} MB)")
        print("─" * 50)
        print("  Testing...")

    total, elapsed, speed = measure_download(size_bytes)
    result = {}
    if speed is not None:
        result = {
            "bytes": total,
            "elapsed_s": round(elapsed, 2),
            "speed_mbps": round(speed, 2),
        }
        if not as_json:
            print(f"  Downloaded: {format_bytes(total)} in {elapsed:.2f}s")
            print(f"  Speed: {format_speed(speed)}")
    else:
        result = {"error": "download test failed"}
        if not as_json:
            print("  ❌ Download test failed")

    return result


def run_upload_test(size_mb=5, as_json=False):
    """Run upload speed test."""
    size_bytes = int(size_mb * 1_000_000)
    if not as_json:
        print(f"\n⬆️  Upload Test ({size_mb} MB)")
        print("─" * 50)
        print("  Testing...")

    total, elapsed, speed = measure_upload(size_bytes)
    result = {}
    if speed is not None:
        result = {
            "bytes": total,
            "elapsed_s": round(elapsed, 2),
            "speed_mbps": round(speed, 2),
        }
        if not as_json:
            print(f"  Uploaded: {format_bytes(total)} in {elapsed:.2f}s")
            print(f"  Speed: {format_speed(speed)}")
    else:
        result = {"error": "upload test failed"}
        if not as_json:
            print("  ❌ Upload test failed")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Network Speed Test — measure download, upload, and latency",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s --all                  Run all tests
  %(prog)s --download             Download speed only
  %(prog)s --upload               Upload speed only
  %(prog)s --latency              Latency only
  %(prog)s --all --json           JSON output
  %(prog)s --download --size 25   Download with 25 MB test file
"""
    )
    parser.add_argument("--download", action="store_true", help="Run download speed test")
    parser.add_argument("--upload", action="store_true", help="Run upload speed test")
    parser.add_argument("--latency", action="store_true", help="Run latency test")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--size", type=float, default=10, help="Test file size in MB (default: 10)")

    args = parser.parse_args()

    # Default to --all if nothing specified
    if not (args.download or args.upload or args.latency or args.all):
        args.all = True

    do_download = args.all or args.download
    do_upload = args.all or args.upload
    do_latency = args.all or args.latency

    if not args.json:
        print("🚀 Network Speed Test")
        print("=" * 50)

    results = {"timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z")}

    if do_latency:
        results["latency"] = run_latency_test(args.json)

    if do_download:
        results["download"] = run_download_test(args.size, args.json)

    if do_upload:
        results["upload"] = run_upload_test(max(args.size / 2, 1), args.json)

    if args.json:
        print(json.dumps(results, indent=2))
    elif not args.json:
        print("\n" + "=" * 50)
        print("✅ Tests complete")


if __name__ == "__main__":
    main()
