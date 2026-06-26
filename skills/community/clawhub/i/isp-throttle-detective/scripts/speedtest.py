#!/usr/bin/env python3
"""
speedtest.py - Run download and upload speed tests to multiple endpoints.
Outputs a JSON result object to stdout.

Usage: python3 speedtest.py [--config /path/to/config.json]
"""

import json
import os
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone

ENDPOINTS = {
    "cloudflare": {
        "url": "https://speed.cloudflare.com/__down?bytes=25000000",
        "label": "Cloudflare",
        "category": "general",
    },
    "fastly_npm": {
        "url": "https://registry.npmjs.org/typescript/-/typescript-5.4.5.tgz",
        "label": "Fastly CDN (npm registry)",
        "category": "cdn",
    },
    "github_releases": {
        "url": "https://github.com/git/git/archive/refs/tags/v2.44.0.tar.gz",
        "label": "GitHub Releases (Fastly)",
        "category": "cdn",
    },
}

UPLOAD_ENDPOINT = "https://speed.cloudflare.com/__up"
UPLOAD_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


def load_config(config_path: str | None) -> dict:
    if config_path and os.path.exists(config_path):
        with open(config_path) as f:
            return json.load(f)
    return {}


def measure_download_urllib(url: str, max_bytes: int = 25_000_000, timeout: int = 30) -> dict:
    """Download from url, return speed_mbps and bytes_received."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 isp-throttle-detective/1.0"})
        start = time.monotonic()
        bytes_received = 0
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                bytes_received += len(chunk)
                if bytes_received >= max_bytes:
                    break
        elapsed = time.monotonic() - start
        if elapsed < 0.1:
            return {"speed_mbps": None, "bytes": bytes_received, "error": "Too fast to measure"}
        speed_mbps = round((bytes_received * 8) / (elapsed * 1_000_000), 2)
        return {"speed_mbps": speed_mbps, "bytes": bytes_received, "elapsed_s": round(elapsed, 2)}
    except Exception as e:
        return {"speed_mbps": None, "error": str(e)}


def measure_download_curl(url: str, max_bytes: int = 25_000_000, timeout: int = 30) -> dict:
    """Use curl for download measurement (more accurate for large transfers)."""
    try:
        cmd = [
            "curl", "-s", "-o", "/dev/null",
            "--max-filesize", str(max_bytes),
            "--max-time", str(timeout),
            "-w", "%{size_download} %{time_total} %{speed_download}",
            "-L", "--compressed",
            "-A", "isp-throttle-detective/1.0",
            url
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
        if result.returncode not in (0, 63):  # 63 = max-filesize exceeded (expected)
            return {"speed_mbps": None, "error": result.stderr.strip() or f"curl exit {result.returncode}"}
        parts = result.stdout.strip().split()
        if len(parts) < 3:
            return {"speed_mbps": None, "error": "Unexpected curl output"}
        size_bytes = int(float(parts[0]))
        elapsed_s = float(parts[1])
        speed_bytes_s = float(parts[2])
        speed_mbps = round((speed_bytes_s * 8) / 1_000_000, 2)
        return {"speed_mbps": speed_mbps, "bytes": size_bytes, "elapsed_s": round(elapsed_s, 2)}
    except Exception as e:
        return {"speed_mbps": None, "error": str(e)}


def curl_available() -> bool:
    try:
        subprocess.run(["curl", "--version"], capture_output=True, timeout=5)
        return True
    except Exception:
        return False


def measure_upload_cloudflare(timeout: int = 20) -> dict:
    """Upload random data to Cloudflare speed test endpoint."""
    try:
        data = bytes(UPLOAD_SIZE_BYTES)
        req = urllib.request.Request(
            UPLOAD_ENDPOINT,
            data=data,
            method="POST",
            headers={
                "Content-Type": "application/octet-stream",
                "User-Agent": "isp-throttle-detective/1.0",
            }
        )
        start = time.monotonic()
        with urllib.request.urlopen(req, timeout=timeout):
            pass
        elapsed = time.monotonic() - start
        if elapsed < 0.1:
            return {"speed_mbps": None, "error": "Too fast to measure"}
        speed_mbps = round((UPLOAD_SIZE_BYTES * 8) / (elapsed * 1_000_000), 2)
        return {"speed_mbps": speed_mbps, "bytes": UPLOAD_SIZE_BYTES, "elapsed_s": round(elapsed, 2)}
    except Exception as e:
        return {"speed_mbps": None, "error": str(e)}


def run_tests(config: dict) -> dict:
    use_curl = curl_available()
    endpoints = config.get("endpoints", ENDPOINTS)
    timeout = config.get("timeout_seconds", 30)
    max_bytes = config.get("max_download_bytes", 25_000_000)

    results = {}
    for key, ep in endpoints.items():
        url = ep["url"] if isinstance(ep, dict) else ep
        label = ep.get("label", key) if isinstance(ep, dict) else key
        category = ep.get("category", "general") if isinstance(ep, dict) else "general"

        print(f"  Testing {label}...", file=sys.stderr)
        if use_curl:
            r = measure_download_curl(url, max_bytes=max_bytes, timeout=timeout)
        else:
            r = measure_download_urllib(url, max_bytes=max_bytes, timeout=timeout)

        results[key] = {
            "label": label,
            "category": category,
            "url": url,
            **r,
        }

    print("  Testing upload (Cloudflare)...", file=sys.stderr)
    upload_result = measure_upload_cloudflare(timeout=config.get("upload_timeout_seconds", 20))
    results["upload_cloudflare"] = {
        "label": "Upload (Cloudflare)",
        "category": "upload",
        **upload_result,
    }

    now = datetime.now(timezone.utc)
    return {
        "timestamp_utc": now.isoformat(),
        "timestamp_local": datetime.now().isoformat(),
        "results": results,
    }


def main():
    config_path = None
    args = sys.argv[1:]
    if "--config" in args:
        idx = args.index("--config")
        if idx + 1 < len(args):
            config_path = args[idx + 1]

    # Also check default config location
    if not config_path:
        default_cfg = os.path.expanduser("~/.isp-throttle-detective/config.json")
        if os.path.exists(default_cfg):
            config_path = default_cfg

    config = load_config(config_path)
    print("Running speed tests...", file=sys.stderr)
    output = run_tests(config)
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
