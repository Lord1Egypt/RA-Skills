#!/usr/bin/env python3
"""Simple internet speed test (download/upload) using Cloudflare endpoints.

Download: GET https://speed.cloudflare.com/__down?bytes=N
Upload:   POST https://speed.cloudflare.com/__up

We measure wall-clock time and compute Mbps.
"""

import argparse
import os
import time
import urllib.request

DOWN_URL = "https://speed.cloudflare.com/__down"
UP_URL = "https://speed.cloudflare.com/__up"


def mbps(num_bytes: int, seconds: float) -> float:
    if seconds <= 0:
        return 0.0
    return (num_bytes * 8) / seconds / 1_000_000


def download_test(n: int, timeout: int = 120) -> float:
    url = f"{DOWN_URL}?bytes={n}"
    t0 = time.perf_counter()
    req = urllib.request.Request(url, method="GET")
    req.add_header("User-Agent", "neomano-internet-speed/1.0")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        # read all
        _ = resp.read()
    t1 = time.perf_counter()
    return mbps(n, t1 - t0)


def upload_test(n: int, timeout: int = 120) -> float:
    data = b"0" * n
    req = urllib.request.Request(UP_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/octet-stream")
    req.add_header("User-Agent", "neomano-internet-speed/1.0")
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        _ = resp.read()
    t1 = time.perf_counter()
    return mbps(n, t1 - t0)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--download-bytes", type=int, default=25_000_000)
    ap.add_argument("--upload-bytes", type=int, default=5_000_000)
    args = ap.parse_args()

    dl = download_test(args.download_bytes)
    ul = upload_test(args.upload_bytes)

    print(f"Download: {dl:.2f} Mbps")
    print(f"Upload:   {ul:.2f} Mbps")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
