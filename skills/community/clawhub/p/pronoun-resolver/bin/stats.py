#!/usr/bin/env python3
"""Display pronoun-resolver analytics summary."""

import json
import sys
import os
from collections import Counter
from datetime import datetime

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    analytics_file = os.path.join(script_dir, "..", ".claude", "pronoun-resolver-analytics.jsonl")

    if not os.path.exists(analytics_file):
        print("No analytics data yet. The hook will start logging on your next message.")
        return

    entries = []
    with open(analytics_file) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    if not entries:
        print("Analytics file exists but is empty.")
        return

    total = len(entries)
    flagged = sum(1 for e in entries if e.get("flagged"))
    clean = total - flagged

    type_counts = Counter()
    for e in entries:
        if e.get("types"):
            for t in e["types"].split(","):
                if t:
                    type_counts[t] += 1

    flag_rate = (flagged / total * 100) if total > 0 else 0

    first_ts = entries[0].get("ts", "?")
    last_ts = entries[-1].get("ts", "?")

    print(f"Pronoun Resolver Analytics")
    print(f"{'=' * 40}")
    print(f"Messages scanned:  {total}")
    print(f"Messages flagged:  {flagged} ({flag_rate:.1f}%)")
    print(f"Messages clean:    {clean} ({100-flag_rate:.1f}%)")
    print()
    print(f"Flags by type:")
    for t, count in type_counts.most_common():
        print(f"  {t:20s} {count}")
    print()
    print(f"Period: {first_ts[:10]} → {last_ts[:10]}")
    print(f"File: {analytics_file}")


if __name__ == "__main__":
    main()
