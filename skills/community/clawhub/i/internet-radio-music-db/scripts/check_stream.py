#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_stream.py — Shared stream health check module.

Provides unified availability checking for both build_db.py and check_availability.py.
The speed threshold is adaptive: based on the stream's bitrate.

Threshold formula:
    min_speed_kbs = max(floor, (bitrate_kbps / 8) * RATIO)

Where:
    bitrate_kbps — stream bitrate from database (kbps), or None if unknown
    RATIO = 0.75 — stream is healthy if download speed >= 75% of nominal bitrate
    floor = 5.0 KB/s — absolute minimum to avoid rejecting very low bitrate streams
    ceiling = 50.0 KB/s — absolute maximum threshold (for unknown/corrPUTed high bitrates)

Test parameters:
    test_duration — seconds to download (default 4)
    min_bytes     — minimum bytes to read (derived from threshold if not set)
    timeout       — HTTP connection timeout (default 8 sec)
"""

import time
import urllib.request

# --- Configuration ---

RATIO = 0.75          # healthy stream: download >= 75% of nominal bitrate speed
FLOOR_KBS = 5.0       # absolute minimum threshold (KB/s)
CEILING_KBS = 50.0    # absolute maximum threshold (KB/s)
TEST_DURATION = 4     # seconds to download
HTTP_TIMEOUT = 8      # HTTP connection timeout


def get_threshold_kbs(bitrate_kbps=None):
    """Calculate minimum speed threshold based on stream bitrate.

    Args:
        bitrate_kbps: Stream bitrate in kbps (e.g. 128, 320). None if unknown.

    Returns:
        tuple: (threshold_kbs, is_adaptive)
            threshold_kbs — minimum download speed in KB/s
            is_adaptive — True if based on bitrate, False if fallback
    """
    if bitrate_kbps and bitrate_kbps > 0:
        # nominal_speed = bitrate_kbps / 8 (convert kbps to KB/s)
        # threshold = nominal_speed * RATIO
        nominal_kbs = bitrate_kbps / 8.0
        threshold = nominal_kbs * RATIO
        # Apply floor and ceiling
        threshold = max(FLOOR_KBS, min(threshold, CEILING_KBS))
        return (threshold, True)
    else:
        # Unknown bitrate — use default
        return (FLOOR_KBS, False)


def get_min_bytes(threshold_kbs):
    """Calculate minimum bytes to read during test.

    Based on threshold speed × test duration.
    """
    return int(threshold_kbs * 1024 * TEST_DURATION * 0.5)


def check_stream(url, bitrate_kbps=None, test_duration=None, timeout=None):
    """Check if a stream is available and meets its bitrate-based speed threshold.

    Args:
        url: Stream URL to check
        bitrate_kbps: Stream bitrate in kbps (None for unknown)
        test_duration: Override default test duration (seconds)
        timeout: Override default HTTP timeout (seconds)

    Returns:
        tuple: (ok, speed_kbs, threshold_kbs, bytes_read, elapsed)
            ok — True if stream is available and meets threshold
            speed_kbs — actual download speed in KB/s
            threshold_kbs — applied threshold in KB/s
            bytes_read — total bytes downloaded
            elapsed — actual test duration in seconds
    """
    if test_duration is None:
        test_duration = TEST_DURATION
    if timeout is None:
        timeout = HTTP_TIMEOUT

    threshold_kbs, is_adaptive = get_threshold_kbs(bitrate_kbps)
    min_bytes = get_min_bytes(threshold_kbs)

    headers = {
        "User-Agent": "Foobar2000",
        "Icy-MetaData": "0",
    }

    total_bytes = 0
    start_time = time.time()

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            while True:
                elapsed = time.time() - start_time
                if elapsed >= test_duration:
                    break
                chunk = resp.read(4096)
                if not chunk:
                    break
                total_bytes += len(chunk)
    except Exception:
        elapsed = time.time() - start_time
        return (False, 0.0, threshold_kbs, total_bytes, elapsed)

    elapsed = time.time() - start_time
    speed_kbs = (total_bytes / 1024.0) / max(elapsed, 0.01)

    ok = (total_bytes >= min_bytes) and (speed_kbs >= threshold_kbs)

    return (ok, speed_kbs, threshold_kbs, total_bytes, elapsed)


def format_result(name, ok, speed_kbs, threshold_kbs, bitrate_kbps, bytes_read, elapsed):
    """Format check result for display."""
    status = "OK" if ok else "FAIL"
    bitrate_str = f"{bitrate_kbps}k" if bitrate_kbps else "?"
    adap = "adaptive" if bitrate_kbps else "default"
    return (
        f"  {status} {name} | "
        f"{speed_kbs:.1f} KB/s (threshold: {threshold_kbs:.1f} KB/s, "
        f"bitrate={bitrate_str}, {adap}) | "
        f"{bytes_read} bytes in {elapsed:.1f}s"
    )


if __name__ == "__main__":
    # Quick self-test
    print("check_stream.py — self test")
    print("-" * 60)
    for bitrate in [32, 64, 128, 192, 256, 320, None]:
        threshold, adaptive = get_threshold_kbs(bitrate)
        bt_str = f"{bitrate}k" if bitrate else "unknown"
        mode = "adaptive" if adaptive else "default/fallback"
        print(f"  bitrate={bt_str:<10} → threshold={threshold:.1f} KB/s ({mode})")
    print("-" * 60)
    print(f"  RATIO={RATIO}, FLOOR={FLOOR_KBS} KB/s, CEILING={CEILING_KBS} KB/s")
    print(f"  TEST_DURATION={TEST_DURATION}s, HTTP_TIMEOUT={HTTP_TIMEOUT}s")
