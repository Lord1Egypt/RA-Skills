#!/usr/bin/env python3
"""
Speed test using curl to download a known file from Cloudflare's speed endpoint.
No external packages — stdlib + curl only.
"""

import json
import subprocess
import sys
import time

# Cloudflare's dedicated speed test endpoint
TEST_SIZES = [
    ("100kb",  "https://speed.cloudflare.com/__down?bytes=102400"),
    ("1mb",    "https://speed.cloudflare.com/__down?bytes=1048576"),
    ("10mb",   "https://speed.cloudflare.com/__down?bytes=10485760"),
]

TIMEOUT_SECS = 20


def run_curl_download(url, label):
    """Download URL via curl and measure throughput."""
    cmd = [
        "curl",
        "--silent",
        "--output", "/dev/null",
        "--write-out", "%{time_total},%{size_download},%{speed_download}",
        "--max-time", str(TIMEOUT_SECS),
        "--connect-timeout", "5",
        url,
    ]
    start = time.monotonic()
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECS + 5,
        )
        elapsed = time.monotonic() - start
        if result.returncode != 0:
            return {
                "label": label,
                "success": False,
                "error": f"curl exit {result.returncode}: {result.stderr.strip()}",
            }
        parts = result.stdout.strip().split(",")
        if len(parts) != 3:
            return {"label": label, "success": False, "error": "unexpected curl output"}
        time_total = float(parts[0])
        bytes_downloaded = int(float(parts[1]))
        speed_bps = float(parts[2])  # bytes/sec from curl
        mbps = round((speed_bps * 8) / 1_000_000, 2)
        return {
            "label": label,
            "success": True,
            "bytes_downloaded": bytes_downloaded,
            "time_total_s": round(time_total, 3),
            "speed_mbps": mbps,
            "speed_bytes_sec": round(speed_bps, 0),
        }
    except subprocess.TimeoutExpired:
        return {"label": label, "success": False, "error": "timeout"}
    except FileNotFoundError:
        return {"label": label, "success": False, "error": "curl not found"}
    except Exception as e:
        return {"label": label, "success": False, "error": str(e)}


def run_speedtest(quick=False):
    """Run speed tests. If quick=True, only test 100kb and 1mb."""
    sizes = TEST_SIZES[:2] if quick else TEST_SIZES
    results = []
    for label, url in sizes:
        r = run_curl_download(url, label)
        results.append(r)

    # Summary: use largest successful result as headline speed
    successful = [r for r in results if r.get("success")]
    if successful:
        best = max(successful, key=lambda r: r.get("bytes_downloaded", 0))
        headline_mbps = best["speed_mbps"]
        quality = (
            "excellent" if headline_mbps > 100
            else "good" if headline_mbps > 25
            else "fair" if headline_mbps > 5
            else "slow"
        )
    else:
        headline_mbps = None
        quality = "unavailable"

    return {
        "tests": results,
        "summary": {
            "headline_mbps": headline_mbps,
            "quality": quality,
            "successful_tests": len(successful),
            "total_tests": len(results),
        },
    }


if __name__ == "__main__":
    quick = "--quick" in sys.argv
    data = run_speedtest(quick=quick)
    print(json.dumps(data, indent=2))
