#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
show_history.py - Detailed playback history viewer with filters and export.

Usage:
    python show_history.py                          # all history
    python show_history.py -d 2026-05-26             # filter by date
    python show_history.py -g jazz                   # filter by genre
    python show_history.py -d 2026-05-26 -g jazz     # date + genre
    python show_history.py --today                   # today only
    python show_history.py --export csv              # export to CSV
    python show_history.py --export html             # export to HTML

Options:
    -d, --date DATE         Filter by date (YYYY-MM-DD or YYYY-MM or YYYY)
    -g, --genre GENRE       Filter by genre (partial match)
    -n, --limit N           Limit output to N newest entries
    -e, --export FORMAT     Export: csv, html, json
    -o, --output FILE       Output file (default: print to stdout)
    --today                 Shortcut for today's date
    -v, --verbose           Show URL and Note columns
    --stats                 Show statistics summary
"""

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, date
from io import StringIO

# Fix encoding for Windows console
if hasattr(sys.stdout, 'encoding') and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Determine paths: try env vars first, then auto-detect
_SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_FILE = os.path.join(_SKILL_DIR, "state.json")
_MUSIC_DB_SKILL = os.path.join(os.path.expanduser("~"), ".openclaw", "skills", "internet-radio-music-db")
_MUSIC_DB_SIBLING_OLD = os.path.join(os.path.dirname(_SKILL_DIR), "music-db")
_MUSIC_DB_SIBLING_NEW = os.path.join(os.path.dirname(_SKILL_DIR), "internet-radio-music-db")
if os.environ.get("MUSIC_DB_PATH"):
    MUSIC_DB_STATE = os.environ["MUSIC_DB_PATH"]
elif os.path.exists(os.path.join(_MUSIC_DB_SKILL, "state.json")):
    MUSIC_DB_STATE = os.path.join(_MUSIC_DB_SKILL, "state.json")
elif os.path.exists(os.path.join(_MUSIC_DB_SIBLING_NEW, "state.json")):
    MUSIC_DB_STATE = os.path.join(_MUSIC_DB_SIBLING_NEW, "state.json")
elif os.path.exists(os.path.join(_MUSIC_DB_SIBLING_OLD, "state.json")):
    MUSIC_DB_STATE = os.path.join(_MUSIC_DB_SIBLING_OLD, "state.json")
else:
    MUSIC_DB_STATE = os.path.join(_MUSIC_DB_SKILL, "state.json")


def load_history():
    if not os.path.exists(STATE_FILE):
        print("Error: state.json not found. Has any music been played?", file=sys.stderr)
        sys.exit(1)
    with open(STATE_FILE, "r", encoding="utf-8-sig") as f:
        return json.load(f).get("History", [])


def load_db_stats():
    """Load stream count per genre from DB."""
    if not os.path.exists(MUSIC_DB_STATE):
        return {}
    with open(MUSIC_DB_STATE, "r", encoding="utf-8") as f:
        db = json.load(f).get("streams", [])
    stats = Counter(s["genre"] for s in db if s.get("available"))
    return dict(stats.most_common())


def parse_args():
    parser = argparse.ArgumentParser(
        description="Detailed playback history viewer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python show_history.py                          Show all history
  python show_history.py --today                  Show today's history
  python show_history.py -d 2026-05-26            Show specific date
  python show_history.py -g jazz                  Filter by genre
  python show_history.py -d 2026-05 --limit 10    Last 10 entries in May
  python show_history.py --export csv -o out.csv  Export to CSV
  python show_history.py --stats                  Show statistics only
        """
    )
    parser.add_argument("-d", "--date", default=None,
                        help="Filter by date (YYYY-MM-DD, YYYY-MM, or YYYY)")
    parser.add_argument("-g", "--genre", default=None,
                        help="Filter by genre (partial match)")
    parser.add_argument("-n", "--limit", type=int, default=None,
                        help="Limit to N newest entries")
    parser.add_argument("--today", action="store_true",
                        help="Show only today's entries")
    parser.add_argument("--export", choices=["csv", "html", "json"], default=None,
                        help="Export format")
    parser.add_argument("-o", "--output", default=None,
                        help="Output file (default: stdout)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Show URL and Note columns")
    parser.add_argument("--stats", action="store_true",
                        help="Show statistics summary")
    return parser.parse_args()


def filter_history(history, args):
    filtered = []

    # Date filter
    date_prefix = None
    if args.today:
        date_prefix = date.today().strftime("%Y-%m-%d")
    elif args.date:
        date_prefix = args.date

    for h in history:
        # Date filter
        if date_prefix and not h["Time"].startswith(date_prefix):
            continue
        # Genre filter
        if args.genre and args.genre.lower() not in h.get("Genre", "").lower():
            continue
        filtered.append(h)

    # Limit (from the end = newest)
    if args.limit and args.limit > 0:
        filtered = filtered[-args.limit:]

    return filtered


def format_duration(dur_str):
    if not dur_str:
        return "-"
    return dur_str


def show_table(history, verbose=False):
    if not history:
        print("No matching entries found.")
        return

    if verbose:
        header = "{:<4} {:<22} {:<10} {:>8}  {:<40} {:<55} {}".format(
            "#", "Time", "Genre", "Duration", "Stream", "URL", "Note")
        print(header)
        print("=" * 200)
        for i, h in enumerate(history, 1):
            dur = format_duration(h.get("Duration"))
            note = h.get("Note", "") or ""
            url = h.get("Url", "")[:54]
            name = h["Name"][:39]
            line = "{:<4} {:<22} {:<10} {:>8}  {:<40} {:<55} {}".format(
                i, h["Time"], h["Genre"], dur, name, url, note)
            print(line)
    else:
        header = "{:<4} {:<22} {:<10} {:>8}  {:<50} {}".format(
            "#", "Time", "Genre", "Duration", "Stream", "Note")
        print(header)
        print("-" * 120)
        for i, h in enumerate(history, 1):
            dur = format_duration(h.get("Duration"))
            note = h.get("Note", "") or ""
            name = h["Name"][:49]
            line = "{:<4} {:<22} {:<10} {:>8}  {:<50} {}".format(
                i, h["Time"], h["Genre"], dur, name, note)
            print(line)

    print(f"\nShowing {len(history)} entries")


def show_stats(history, db_stats=None):
    if not history:
        print("No history entries to analyze.")
        return

    total = len(history)
    genres = Counter(h["Genre"] for h in history)
    total_seconds = 0
    for h in history:
        dur = h.get("Duration")
        if dur:
            parts = dur.split(":")
            if len(parts) == 3:
                total_seconds += int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])

    h = total_seconds // 3600
    m = (total_seconds // 60) % 60
    s = total_seconds % 60

    # Date range
    dates = sorted(set(h["Time"][:10] for h in history))

    print("=" * 50)
    print("PLAYBACK STATISTICS")
    print("=" * 50)
    print(f"Total entries:    {total}")
    print(f"Total listening: {h:02d}:{m:02d}:{s:02d}")
    print(f"Date range:       {dates[0] if dates else 'N/A'} .. {dates[-1] if dates else 'N/A'}")
    print(f"Unique genres:    {len(genres)}")
    print()
    print(f"{'Genre':<15} {'Count':>6} {'%':>6}  Bar")
    print("-" * 50)
    for g, cnt in genres.most_common():
        pct = cnt / total * 100
        bar = "#" * int(pct / 2) + "-" * (50 - int(pct / 2))
        print(f"{g:<15} {cnt:>6} {pct:>5.1f}%  {bar[:40]}")
    print("-" * 50)

    if db_stats:
        print()
        print("Available streams in DB:")
        print("-" * 50)
        for g, cnt in list(db_stats.items())[:10]:
            played = genres.get(g, 0)
            print(f"  {g:<15} DB: {cnt:>3}  Played: {played:>3}")


def export_csv(history, output=None):
    import csv
    buf = StringIO()
    writer = csv.writer(buf)
    writer.writerow(["#", "Time", "Genre", "Duration", "Stream", "URL", "Note"])
    for i, h in enumerate(history, 1):
        writer.writerow([
            i, h["Time"], h["Genre"],
            h.get("Duration") or "",
            h["Name"],
            h.get("Url", ""),
            h.get("Note", "")
        ])
    content = buf.getvalue()
    if output:
        with open(output, "w", encoding="utf-8", newline="") as f:
            f.write(content)
        print(f"Exported {len(history)} entries to {output}")
    else:
        print(content)


def export_html(history, output=None):
    html_parts = [
        "<!DOCTYPE html>",
        "<html><head><meta charset='utf-8'><title>Playback History</title>",
        "<style>",
        "body{font-family:Arial,sans-serif;margin:20px}",
        "table{border-collapse:collapse;width:100%}",
        "th,td{border:1px solid #ddd;padding:8px;text-align:left}",
        "th{background:#4CAF50;color:white}",
        "tr:nth-child(even){background:#f2f2f2}",
        "tr:hover{background:#ddd}",
        "</style></head><body>",
        "<h1>Playback History ({count} entries)</h1>".format(count=len(history)),
        "<table><tr><th>#</th><th>Time</th><th>Genre</th><th>Duration</th><th>Stream</th><th>URL</th><th>Note</th></tr>",
    ]
    for i, h in enumerate(history, 1):
        dur = h.get("Duration") or "-"
        note = h.get("Note", "") or ""
        url = h.get("Url", "")
        html_parts.append(
            "<tr><td>{i}</td><td>{t}</td><td>{g}</td><td>{d}</td><td>{nm}</td><td>{u}</td><td>{no}</td></tr>".format(
                i=i, t=h["Time"], g=h["Genre"], d=dur, nm=h["Name"], u=url, no=note
            )
        )
    html_parts.append("</table></body></html>")
    content = "\n".join(html_parts)

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Exported {len(history)} entries to {output}")
    else:
        print(content)


def export_json(history, output=None):
    data = []
    for i, h in enumerate(history, 1):
        entry = {
            "index": i,
            "time": h["Time"],
            "genre": h["Genre"],
            "name": h["Name"],
            "duration": h.get("Duration"),
            "url": h.get("Url"),
            "note": h.get("Note"),
        }
        data.append(entry)
    content = json.dumps(data, ensure_ascii=False, indent=2)
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Exported {len(history)} entries to {output}")
    else:
        print(content)


def main():
    args = parse_args()
    history = load_history()

    if not history:
        print("No playback history found.")
        show_stats(history)
        sys.exit(0)

    db_stats = load_db_stats()

    if args.stats:
        show_stats(history, db_stats)
        sys.exit(0)

    filtered = filter_history(history, args)

    if args.export == "csv":
        export_csv(filtered, args.output)
    elif args.export == "html":
        export_html(filtered, args.output)
    elif args.export == "json":
        export_json(filtered, args.output)
    else:
        show_table(filtered, args.verbose)
        if not args.export:
            show_stats(filtered, db_stats)


if __name__ == "__main__":
    main()
