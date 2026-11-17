#!/usr/bin/env python3
"""
trends.py — aggregate the journal index into gentle, factual trends.

Reads journal/index.jsonl (one JSON object per entry) and reports mood average,
current logging streak, recurring tags/themes and recent mood direction. These
are DESCRIPTIVE facts about what the user wrote — not predictions and not
judgments. "Streaks" are surfaced without guilt (a gap is just a gap).

Usage:
  python3 trends.py [--home ~/.companion] [--days 30]
  # or import: from trends import aggregate
"""
import argparse
import datetime
import json
import os
from collections import Counter


def _home(explicit=None):
    return explicit or os.environ.get("COMPANION_HOME") or os.path.expanduser("~/.companion")


def _load(index_path):
    rows = []
    if not os.path.exists(index_path):
        return rows
    with open(index_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def _streak(dates):
    """Consecutive-day logging streak ending today or yesterday (guilt-free)."""
    if not dates:
        return 0
    days = sorted({datetime.date.fromisoformat(d) for d in dates}, reverse=True)
    today = datetime.date.today()
    if (today - days[0]).days > 1:
        return 0  # streak ended; not a failure, just information
    streak = 1
    for prev, cur in zip(days, days[1:]):
        if (prev - cur).days == 1:
            streak += 1
        else:
            break
    return streak


LOW_MOOD_MAX = 3          # on the 0–10 scale, a day averaging 3 or lower counts as low
LOW_WINDOW_DAYS = 14
LOW_MIN_DAYS = 5
LOW_RECENT_DAYS = 3       # a low day among the last three logged, or the stretch has lifted


def _sustained_low(rows, today=None):
    """Two weeks of mostly low days: moods logged on at least LOW_MIN_DAYS days of the last
    LOW_WINDOW_DAYS, more than half of those days averaging LOW_MOOD_MAX or lower, and a low
    day among the last LOW_RECENT_DAYS logged. Counting entries let one bad afternoon typed
    in five times read as two weeks, and a stretch that had already lifted still asked.
    A reason to ask how someone is doing — not a diagnosis, and not a crisis flag."""
    today = today or datetime.date.today()
    start = today - datetime.timedelta(days=LOW_WINDOW_DAYS - 1)
    by_day, entries = {}, 0
    for r in rows:
        if not isinstance(r.get("mood"), (int, float)) or not r.get("date"):
            continue
        try:
            d = datetime.date.fromisoformat(str(r["date"])[:10])
        except ValueError:
            continue
        if start <= d <= today:
            by_day.setdefault(d, []).append(r["mood"])
            entries += 1
    days = sorted(by_day)
    low_days = {d for d in days if sum(by_day[d]) / len(by_day[d]) <= LOW_MOOD_MAX}
    recent_low = any(d in low_days for d in days[-LOW_RECENT_DAYS:])
    return {"window_days": LOW_WINDOW_DAYS, "days": len(days), "entries": entries,
            "low": len(low_days), "low_max": LOW_MOOD_MAX,
            "triggered": (len(days) >= LOW_MIN_DAYS and len(low_days) * 2 > len(days)
                          and recent_low)}


def aggregate(home=None, days=30):
    home = _home(home)
    index_path = os.path.join(home, "journal", "index.jsonl")
    rows = _load(index_path)
    if not rows:
        return {"entries": 0, "note": "No journal entries yet."}

    cutoff = datetime.date.today() - datetime.timedelta(days=days)
    recent = [r for r in rows
              if r.get("date") and datetime.date.fromisoformat(r["date"]) >= cutoff]

    # Consent-gated categories are withheld here too. A trend is shown to the person as a
    # computed FACT, so an average over moods they asked us to stop using is exactly what
    # revoking consent has to stop.
    consent = {}
    consent_path = os.path.join(home, "consent.yaml")
    if os.path.exists(consent_path):
        import sys
        if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from _deps import ensure
        with open(consent_path, encoding="utf-8") as f:
            consent = ensure("PyYAML", "yaml").safe_load(f) or {}
    if not isinstance(consent, dict):       # a hand-edited file grants nothing, and doesn't crash
        consent = {}
    withheld = [c for c in ("mood", "relationships")
                if not (isinstance(consent.get(c), dict) and consent[c].get("granted") is True)]

    moods = ([r["mood"] for r in recent if isinstance(r.get("mood"), (int, float))]
             if "mood" not in withheld else [])
    tags = Counter(t for r in recent for t in (r.get("tags") or []))
    themes = Counter(t for r in recent for t in (r.get("themes") or []))
    people = (Counter(p for r in recent for p in (r.get("people") or []))
              if "relationships" not in withheld else Counter())
    sustained = None if "mood" in withheld else _sustained_low(rows)

    # mood direction: compare first vs second half of the window
    direction = None
    if len(moods) >= 4:
        half = len(moods) // 2
        first = sum(moods[:half]) / half
        second = sum(moods[half:]) / (len(moods) - half)
        delta = second - first
        direction = ("improving" if delta > 0.5 else
                     "declining" if delta < -0.5 else "steady")

    return {
        "window_days": days,
        "entries": len(rows),
        "entries_in_window": len(recent),
        "streak_days": _streak([r["date"] for r in rows if r.get("date")]),
        "mood_avg": round(sum(moods) / len(moods), 1) if moods else None,
        "mood_direction": direction,
        "crisis_flags_in_window": sum(1 for r in recent if r.get("crisis_flag")),
        "top_tags": tags.most_common(6),
        "top_themes": themes.most_common(6),
        "recurring_people": [p for p, c in people.most_common(6) if c > 1],
        "sustained_low": sustained,
        "withheld_without_consent": withheld,
        "_note": "Descriptive summary of what was logged. Not a prediction.",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--home", default=None)
    ap.add_argument("--days", type=int, default=30)
    args = ap.parse_args()
    print(json.dumps(aggregate(args.home, args.days), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
