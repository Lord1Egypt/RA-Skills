#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_availability.py - Stream availability check with adaptive speed measurement.

Criteria for "available":
  1. HTTP status 2xx/3xx
  2. Received enough bytes within TEST_DURATION seconds
  3. Average speed >= adaptive threshold (based on stream bitrate)

The speed threshold is adaptive per stream:
  threshold = max(FLOOR, min((bitrate_kbps / 8) * RATIO, CEILING))
  Default: RATIO=0.75, FLOOR=5 KB/s, CEILING=50 KB/s

  Examples:
    320 kbps -> 30 KB/s threshold
    128 kbps -> 12 KB/s threshold
     64 kbps ->  6 KB/s threshold
     32 kbps ->  5 KB/s threshold (floor)
    unknown  ->  5 KB/s threshold (floor)

Streams are NOT deleted immediately — only marked available=false with failed_checks++.
Streams with failed_checks >= 3 are auto-removed.
"""

import json, os, sys, time, urllib.request
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import shared check module
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from check_stream import check_stream, get_threshold_kbs, format_result

SKILL_DIR = os.path.dirname(SCRIPT_DIR)
STATE_FILE = os.path.join(SKILL_DIR, "state.json")

MAX_WORKERS = 120


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"streams": []}

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def check_stream_adaptive(url, bitrate=None):
    """
    Check stream availability with bitrate-based adaptive threshold.
    Returns a result dict compatible with the main loop.
    """
    ok, speed_kbs, threshold_kbs, bytes_read, elapsed = check_stream(url, bitrate_kbps=bitrate)

    return {
        "available": ok,
        "speed_bps": round(speed_kbs * 1024, 2),
        "speed_kbs": round(speed_kbs, 2),
        "threshold_kbs": round(threshold_kbs, 2),
        "bytes_received": bytes_read,
        "duration": round(elapsed, 2),
        "error": None if ok else "Too slow: {:.1f} KB/s (threshold: {:.1f} KB/s)".format(speed_kbs, threshold_kbs),
    }


def main():
    state = load_state()
    streams = state.get("streams", [])

    if not streams:
        print("Database is empty.")
        return

    now = datetime.now(timezone.utc).isoformat()
    total = len(streams)

    # Select streams to check: prioritize unchecked, then slow, then rest
    check_indices = []

    # Priority 1: streams never checked
    for i, s in enumerate(streams):
        if s.get("last_speed_bps") is None and s.get("available", True):
            check_indices.append(i)

    # Priority 2: slow/failing streams
    for i, s in enumerate(streams):
        if i not in check_indices and (s.get("last_speed_bps") or 0) < 20 * 1024:
            check_indices.append(i)

    # Priority 3: others (periodic re-check)
    for i, s in enumerate(streams):
        if i not in check_indices:
            check_indices.append(i)

    print("Checking {} of {} streams (priority: unchecked > slow > rest)".format(
        len(check_indices), total))
    print("(adaptive thresholds based on stream bitrate)")
    print()

    # Parallel check
    results = {}
    check_map = {i: streams[i] for i in check_indices}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_idx = {
            executor.submit(
                check_stream_adaptive,
                s["url"],
                s.get("bitrate")
            ): i
            for i, s in check_map.items()
        }
        done = 0
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            try:
                results[idx] = future.result()
            except Exception as e:
                results[idx] = {
                    "available": False,
                    "speed_bps": 0, "speed_kbs": 0,
                    "threshold_kbs": 0,
                    "bytes_received": 0, "duration": 0,
                    "error": str(e),
                }
            done += 1
            if done % 10 == 0:
                print("  ... checked {}/{}".format(done, len(check_indices)))

    # Update records
    checked = 0
    available_count = 0
    unavailable_count = 0
    slow_count = 0
    dead_count = 0

    for i, s in enumerate(streams):
        r = results.get(i)
        if r is None:
            if s.get("available", True):
                available_count += 1
            else:
                unavailable_count += 1
            continue

        checked += 1
        is_ok = r.get("available", False)
        s["last_checked"] = now
        s["check_speed_bps"] = r.get("speed_bps", 0)
        s["check_bytes_received"] = r.get("bytes_received", 0)
        s["check_duration"] = r.get("duration", 0)
        s["check_threshold_kbs"] = r.get("threshold_kbs", 0)

        if is_ok:
            s["available"] = True
            s["failed_checks"] = 0
            s["last_speed_bps"] = r.get("speed_bps", 0)
            available_count += 1
        else:
            s["available"] = False
            s["failed_checks"] = s.get("failed_checks", 0) + 1
            s["last_error"] = r.get("error", "unknown")
            s["last_speed_bps"] = r.get("speed_bps", 0)
            unavailable_count += 1

            speed_kbs = r.get("speed_kbs", 0)
            threshold_kbs = r.get("threshold_kbs", 0)
            if speed_kbs > 0 and threshold_kbs > 0:
                slow_count += 1
            if not r.get("bytes_received"):
                dead_count += 1

    state["last_checked"] = now

    # Auto-remove streams with failed_checks >= 3
    before_removal = len(state["streams"])
    state["streams"] = [s for s in state["streams"] if s.get("failed_checks", 0) < 3]
    removed = before_removal - len(state["streams"])

    save_state(state)

    # Recount after removal
    total = len(state["streams"])
    available_count = sum(1 for s in state["streams"] if s.get("available", True))
    unavailable_count = total - available_count

    print()
    print("=" * 60)
    print("RESULTS: checked={}, {} OK | {} FAIL (slow:{}, dead:{}) | total:{}".format(
        checked, available_count, unavailable_count, slow_count, dead_count, total))
    if removed > 0:
        print("AUTO-REMOVED: {} streams with failed_checks >= 3".format(removed))
    print("=" * 60)

    # Show problem streams
    problem = [s for s in state["streams"] if not s.get("available", True)]
    if problem:
        problem.sort(key=lambda s: s.get("last_speed_bps") or 0)
        print("\nProblem streams ({}):".format(len(problem)))
        for s in problem[:15]:
            speed_kbs = (s.get("last_speed_bps") or 0) / 1024
            threshold = s.get("check_threshold_kbs", 0)
            fails = s.get("failed_checks", 0)
            bitrate = s.get("bitrate", 0) or 0
            err = (s.get("last_error", "") or "")[:45]
            print("  [{:>2}x] {:<30} {:5.1f} KB/s (thr:{:.1f}, br:{:>3}k)  {}".format(
                fails, s.get("name", "?")[:30], speed_kbs, threshold,
                bitrate, err))

    # Show fastest
    fast = sorted(
        [s for s in state["streams"] if s.get("available", True)],
        key=lambda s: s.get("last_speed_bps") or 0,
        reverse=True
    )[:5]
    if fast:
        print("\nFastest streams:")
        for s in fast:
            speed_kbs = (s.get("last_speed_bps") or 0) / 1024
            print("  {:<40} {:.1f} KB/s".format(
                s.get("name", "?")[:40], speed_kbs))


if __name__ == "__main__":
    main()
