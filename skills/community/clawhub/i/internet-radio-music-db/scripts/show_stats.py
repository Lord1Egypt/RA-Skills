#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
show_stats.py - Internet Radio Music DB statistics viewer.

Usage:
    python show_stats.py                    # full statistics
    python show_stats.py --genres           # genres breakdown only
    python show_stats.py --top N            # top N genres
    python show_stats.py --lang             # language breakdown
    python show_stats.py --speed            # speed distribution
    python show_stats.py --top-speed N      # top N fastest streams
    python show_stats.py --effective        # efficiency report (speed vs bitrate)
"""

import argparse
import json
import os
import sys
from collections import Counter

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_FILE = os.path.join(SKILL_DIR, "state.json")

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def load_db():
    if not os.path.exists(STATE_FILE):
        print("Error: state.json not found. Run build_db.py first.", file=sys.stderr)
        sys.exit(1)
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def bar(pct, width=30):
    filled = int(width * pct / 100)
    return "X" * filled + "-" * (width - filled)


def show_genres(streams, top_n=None):
    gc = Counter(s["genre"] for s in streams)
    ga = Counter(s["genre"] for s in streams if s.get("available"))
    items = gc.most_common(top_n) if top_n else gc.most_common()

    print(f"\n{'Genre':<15} {'Total':>6} {'Avail':>6} {'%':>5}  {'Bar'}")
    print("-" * 75)
    for g, c in items:
        a = ga.get(g, 0)
        p = a * 100 // c if c else 0
        print(f"{g:<15} {c:>6} {a:>6} {p:>4}%  {bar(p)}")


def show_languages(streams):
    lc = Counter(s.get("language", "unknown") for s in streams)
    la = Counter(s.get("language", "unknown") for s in streams if s.get("available"))

    print(f"\n{'Language':<10} {'Total':>6} {'Avail':>6} {'%':>5}")
    print("-" * 35)
    for lang, c in lc.most_common():
        a = la.get(lang, 0)
        p = a * 100 // c if c else 0
        print(f"{lang:<10} {c:>6} {a:>6} {p:>4}%")


def show_speed(streams):
    speeds = [s.get("last_speed_bps", 0) or 0 for s in streams if s.get("available")]
    if not speeds:
        print("\nNo speed data available.")
        return

    speeds_kb = [s / 1024 for s in speeds]

    print(f"\nSpeed Statistics (available streams):")
    print(f"  Count:    {len(speeds_kb)}")
    print(f"  Min:      {min(speeds_kb):.1f} KB/s")
    print(f"  Max:      {max(speeds_kb):.1f} KB/s")
    print(f"  Avg:      {sum(speeds_kb)/len(speeds_kb):.1f} KB/s")

    buckets = [
        (0, 20, "< 20 KB/s"),
        (20, 50, "20-50 KB/s"),
        (50, 100, "50-100 KB/s"),
        (100, 200, "100-200 KB/s"),
        (200, float("inf"), "> 200 KB/s"),
    ]
    print(f"\n  Speed Distribution:")
    for lo, hi, label in buckets:
        cnt = sum(1 for s in speeds_kb if lo <= s < hi)
        p = cnt * 100 // len(speeds_kb) if speeds_kb else 0
        print(f"    {label:<15} {cnt:>5} ({p}%)  {bar(p)}")


def calc_efficiency(speed_kbs, bitrate_kbps):
    """Calculate stream efficiency: actual speed / nominal bitrate speed."""
    if not bitrate_kbps or bitrate_kbps <= 0:
        return None
    nominal_kbs = bitrate_kbps / 8.0
    return (speed_kbs / nominal_kbs) * 100.0


def show_top_speed(streams, n=10):
    avail = [s for s in streams if s.get("available") and s.get("last_speed_bps")]
    if not avail:
        print("\nNo speed data available.")
        return

    top = sorted(avail, key=lambda s: s.get("last_speed_bps", 0), reverse=True)[:n]

    print(f"\nTop {n} Fastest Streams:")
    print(f"  {'#':<4} {'Speed':>10} {'Bitrate':>8} {'Efficiency':>10} {'Genre':<12} {'Name'}")
    print("  " + "-" * 85)
    for i, s in enumerate(top, 1):
        speed_kbs = s.get("last_speed_bps", 0) / 1024
        bitrate = s.get("bitrate", 0) or 0
        eff = calc_efficiency(speed_kbs, bitrate)
        eff_str = f"{eff:.0f}%" if eff is not None else "?"
        name = s["name"][:38] + ".." if len(s["name"]) > 38 else s["name"]
        print(f"  {i:<4} {speed_kbs:>8.1f} KB/s  {bitrate:>5}k  {eff_str:>9}  {s['genre']:<12} {name}")


def show_effective(streams):
    """Show efficiency report: actual speed / nominal bitrate per stream."""
    avail = [s for s in streams if s.get("available") and s.get("last_speed_bps") and s.get("bitrate")]
    if not avail:
        print("\nNo streams with bitrate data available.")
        return

    print(f"\nStream Efficiency Report (actual speed / nominal bitrate speed):")
    print(f"  {'Name':<35} {'Bitrate':>7} {'Speed':>9} {'Efficiency':>10} {'Status':<10}")
    print("  " + "-" * 75)

    # Sort by efficiency
    for s in sorted(avail, key=lambda x: calc_efficiency(
        (x.get("last_speed_bps", 0) or 0) / 1024,
        x.get("bitrate", 0) or 0
    ) or 0, reverse=True):
        speed_kbs = (s.get("last_speed_bps", 0) or 0) / 1024
        bitrate = s.get("bitrate", 0) or 0
        eff = calc_efficiency(speed_kbs, bitrate)
        nominal_kbs = bitrate / 8.0

        if eff is None:
            status = "unknown"
        elif eff >= 90:
            status = "excellent"
        elif eff >= 75:
            status = "good"
        elif eff >= 50:
            status = "fair"
        elif eff >= 25:
            status = "poor"
        else:
            status = "bad"

        name = s["name"][:34] + ".." if len(s["name"]) > 34 else s["name"]
        print(f"  {name:<35} {bitrate:>5}k  {speed_kbs:>7.1f} KB/s  {eff:>8.1f}%  {status}")

    # Efficiency distribution
    effs = []
    for s in avail:
        speed_kbs = (s.get("last_speed_bps", 0) or 0) / 1024
        bitrate = s.get("bitrate", 0) or 0
        e = calc_efficiency(speed_kbs, bitrate)
        if e is not None:
            effs.append(e)

    if effs:
        print(f"\n  Efficiency Distribution:")
        for lo, hi, label in [(90, 999, "excellent (>=90%)"), (75, 90, "good (75-89%)"),
                              (50, 75, "fair (50-74%)"), (25, 50, "poor (24-49%)"),
                              (0, 25, "bad (<25%)")]:
            cnt = sum(1 for e in effs if lo <= e < hi)
            if cnt > 0:
                pct = cnt * 100 // len(effs)
                print(f"    {label:<20} {cnt:>4} ({pct}%)")


def show_summary(streams):
    total = len(streams)
    avail = sum(1 for s in streams if s.get("available"))
    failed = sum(1 for s in streams if s.get("failed_checks", 0) > 0)
    never_checked = sum(1 for s in streams if not s.get("last_checked"))
    genres = len(set(s["genre"] for s in streams))
    langs = len(set(s.get("language", "unknown") for s in streams))

    # Count streams with bitrate info
    with_bitrate = sum(1 for s in streams if s.get("bitrate"))

    print("=" * 50)
    print("  Internet Radio Music DB - Statistics")
    print("=" * 50)
    print(f"  Total streams:      {total}")
    if total:
        print(f"  Available:          {avail} ({avail*100//total}%)")
    else:
        print(f"  Available:          0")
    print(f"  Unavailable:        {total - avail}")
    print(f"  Failed checks:      {failed}")
    print(f"  Never checked:      {never_checked}")
    print(f"  Genres:             {genres}")
    print(f"  Languages:          {langs}")
    print(f"  With bitrate info:  {with_bitrate}")

    if os.path.exists(STATE_FILE):
        size_mb = os.path.getsize(STATE_FILE) / (1024 * 1024)
        print(f"  DB file size:       {size_mb:.1f} MB")

    mtime = os.path.getmtime(STATE_FILE)
    from datetime import datetime
    print(f"  Last modified:      {datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="Internet Radio Music DB statistics")
    parser.add_argument("--genres", action="store_true", help="Genres breakdown only")
    parser.add_argument("--lang", action="store_true", help="Language breakdown only")
    parser.add_argument("--speed", action="store_true", help="Speed distribution only")
    parser.add_argument("--top", type=int, metavar="N", help="Top N genres")
    parser.add_argument("--top-speed", type=int, metavar="N", help="Top N fastest streams")
    parser.add_argument("--effective", action="store_true", help="Efficiency report (speed vs bitrate)")
    args = parser.parse_args()

    data = load_db()
    streams = data.get("streams", [])

    if not streams:
        print("Database is empty. Run build_db.py first.")
        sys.exit(0)

    show_summary(streams)

    if args.genres:
        show_genres(streams, top_n=args.top)
    elif args.lang:
        show_languages(streams)
    elif args.speed:
        show_speed(streams)
    elif args.top_speed:
        show_top_speed(streams, n=args.top_speed)
    elif args.effective:
        show_effective(streams)
    else:
        show_genres(streams)
        show_languages(streams)
        show_speed(streams)
        show_top_speed(streams, n=10)


if __name__ == "__main__":
    main()
