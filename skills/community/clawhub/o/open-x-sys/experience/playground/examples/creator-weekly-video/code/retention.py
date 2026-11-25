"""Recompute the weekly figures for the episode practice.

Constructed example for the OpenXSys Playground.

Reads ../data/episodes.csv (one row per episode) and prints the averages
before and after the practice changed, then checks the watch condition
recorded in SYSTEM.md. Standard library only.

    python retention.py            # uses ../data/episodes.csv
    python retention.py other.csv
"""

import csv
import os
import sys

CHANGE_AT_EPISODE = 5      # first episode made with "decide the promise first"
WATCH_MAX_HOURS = 11.0     # two weeks running above this: look again
WATCH_MAX_GAP_DAYS = 1.0   # any recent week above this: look again


def load(path):
    with open(path, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        row["episode"] = int(row["episode"])
        row["hours_total"] = float(row["hours_total"])
        row["gap"] = float(row["gap_days_finish_to_publish"])
        row["retention"] = float(row["retention_30s_percent"])
        row["thursday"] = row["published_on_thursday"].strip().lower() == "yes"
    return rows


def mean(values):
    values = list(values)
    return sum(values) / len(values) if values else float("nan")


def summarize(label, rows):
    print(label)
    print("  episodes                  : %d" % len(rows))
    print("  finish-to-publish gap     : %.1f days" % mean(r["gap"] for r in rows))
    print("  published on Thursday     : %d of %d" % (sum(r["thursday"] for r in rows), len(rows)))
    print("  retention at 30 seconds   : %.0f%%" % mean(r["retention"] for r in rows))
    print("  hours per episode         : %.1f" % mean(r["hours_total"] for r in rows))


def check_watch(rows):
    last_two = rows[-2:]
    over_hours = len(last_two) == 2 and all(r["hours_total"] > WATCH_MAX_HOURS for r in last_two)
    over_gap = bool(rows) and rows[-1]["gap"] > WATCH_MAX_GAP_DAYS
    print("Watch condition")
    if over_hours or over_gap:
        if over_hours:
            print("  FIRED: hours per episode above %.0f for two weeks running" % WATCH_MAX_HOURS)
        if over_gap:
            print("  FIRED: finish-to-publish gap above %.0f day" % WATCH_MAX_GAP_DAYS)
    else:
        print("  not fired")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "data", "episodes.csv")
    rows = load(path)
    summarize("Before the change", [r for r in rows if r["episode"] < CHANGE_AT_EPISODE])
    summarize("After the change", [r for r in rows if r["episode"] >= CHANGE_AT_EPISODE])
    check_watch(rows)


if __name__ == "__main__":
    main()
