#!/usr/bin/env python3
"""
status.py — Show current streaks and today's completion status.

Usage:
  python status.py                    # Human-readable table
  python status.py --json             # JSON output
  python status.py --date 2024-01-15  # Status as of a specific date
  python status.py --data-dir /path   # Override data directory
"""

import json
import sys
import os
import argparse
from datetime import date, timedelta
from pathlib import Path


DEFAULT_DATA_DIR = Path.home() / ".openclaw" / "workspace" / "habits"


def get_data_dir(override=None):
    if override:
        return Path(override)
    env = os.environ.get("HABIT_DATA_DIR")
    if env:
        return Path(env)
    return DEFAULT_DATA_DIR


def load_json(path, default):
    if not path.exists():
        return default
    with open(path) as f:
        return json.load(f)


def is_expected_day(habit, check_date):
    """Return True if this habit is expected on the given date."""
    freq = habit.get("frequency", "daily")
    if freq == "daily":
        return True
    if freq == "weekday":
        return check_date.weekday() < 5  # Mon=0 ... Fri=4
    if freq == "weekly":
        return True  # counted per 7-day window, not per day
    return True


def calc_current_streak(habit, log_data, as_of):
    """Count consecutive days (or weeks) the habit was completed up to as_of."""
    habit_id = habit["id"]
    freq = habit.get("frequency", "daily")

    # Floor: earliest date any log exists for this habit (or 365 days back as safety)
    min_floor = as_of - timedelta(days=365)

    if freq == "weekly":
        # Count consecutive 7-day windows going backwards from as_of
        streak = 0
        week_end = as_of
        while week_end >= min_floor:
            week_start = week_end - timedelta(days=6)
            done_in_window = False
            for offset in range(7):
                d = week_start + timedelta(days=offset)
                if d > as_of:
                    continue
                if log_data.get(d.isoformat(), {}).get(habit_id, {}).get("done"):
                    done_in_window = True
                    break
            if not done_in_window:
                break
            streak += 1
            week_end = week_start - timedelta(days=1)
        return streak

    # daily / weekday: walk backwards day by day
    streak = 0
    current = as_of

    # If not done today (and today is an expected day), streak starts from yesterday
    today_done = log_data.get(as_of.isoformat(), {}).get(habit_id, {}).get("done", False)
    if not today_done and is_expected_day(habit, as_of):
        current = as_of - timedelta(days=1)

    while current >= min_floor:
        if is_expected_day(habit, current):
            done = log_data.get(current.isoformat(), {}).get(habit_id, {}).get("done", False)
            if done:
                streak += 1
            else:
                break
        current -= timedelta(days=1)

    return streak


def calc_longest_streak(habit, log_data):
    """Calculate the all-time longest streak."""
    habit_id = habit["id"]
    today = date.today()
    freq = habit.get("frequency", "daily")
    # Start from the earliest logged date or 365 days ago
    all_dates = sorted(log_data.keys())
    if all_dates:
        created = date.fromisoformat(all_dates[0])
    else:
        created = today

    if freq == "weekly":
        # Walk week windows forward
        best = 0
        current_streak = 0
        week_start = created
        while week_start <= today:
            week_end = week_start + timedelta(days=6)
            done_in_window = any(
                log_data.get((week_start + timedelta(days=i)).isoformat(), {})
                         .get(habit_id, {}).get("done", False)
                for i in range(7)
            )
            if done_in_window:
                current_streak += 1
                best = max(best, current_streak)
            else:
                current_streak = 0
            week_start = week_end + timedelta(days=1)
        return best

    best = 0
    current_streak = 0
    cursor = created
    while cursor <= today:
        if is_expected_day(habit, cursor):
            done = log_data.get(cursor.isoformat(), {}).get(habit_id, {}).get("done", False)
            if done:
                current_streak += 1
                best = max(best, current_streak)
            else:
                current_streak = 0
        cursor += timedelta(days=1)
    return best


def calc_completion_rate(habit, log_data, as_of, window_days):
    """Completion rate over the last N days (respects frequency)."""
    habit_id = habit["id"]
    created = date.fromisoformat(habit.get("created", "2000-01-01"))
    freq = habit.get("frequency", "daily")

    if freq == "weekly":
        # Count weeks in window
        expected = window_days // 7
        if expected == 0:
            return 0.0
        done = 0
        for week_offset in range(expected):
            week_end = as_of - timedelta(days=week_offset * 7)
            week_start = week_end - timedelta(days=6)
            if any(
                log_data.get((week_start + timedelta(days=i)).isoformat(), {})
                         .get(habit_id, {}).get("done", False)
                for i in range(7)
            ):
                done += 1
        return round(done / expected * 100, 1)

    expected = 0
    done = 0
    for offset in range(window_days):
        d = as_of - timedelta(days=offset)
        if d < created:
            continue
        if is_expected_day(habit, d):
            expected += 1
            if log_data.get(d.isoformat(), {}).get(habit_id, {}).get("done", False):
                done += 1

    if expected == 0:
        return 0.0
    return round(done / expected * 100, 1)


def compute_status(habits_data, log_data, as_of):
    active_habits = [h for h in habits_data.get("habits", []) if h.get("active", True)]
    results = []

    for habit in active_habits:
        habit_id = habit["id"]
        today_done = log_data.get(as_of.isoformat(), {}).get(habit_id, {}).get("done", False)
        expected_today = is_expected_day(habit, as_of)

        results.append({
            "id": habit_id,
            "name": habit["name"],
            "emoji": habit.get("emoji", "•"),
            "frequency": habit.get("frequency", "daily"),
            "today_done": today_done,
            "expected_today": expected_today,
            "current_streak": calc_current_streak(habit, log_data, as_of),
            "longest_streak": calc_longest_streak(habit, log_data),
            "completion_7d": calc_completion_rate(habit, log_data, as_of, 7),
            "completion_30d": calc_completion_rate(habit, log_data, as_of, 30),
        })

    return results


def print_table(results, as_of):
    done_today = sum(1 for r in results if r["today_done"])
    expected_today = sum(1 for r in results if r["expected_today"])

    print(f"\n{'═'*60}")
    print(f"  HABIT STATUS — {as_of.strftime('%A, %B %d %Y')}")
    print(f"  Today: {done_today}/{expected_today} complete")
    print(f"{'═'*60}\n")

    for r in results:
        emoji = r["emoji"]
        name = r["name"]
        if not r["expected_today"]:
            status = "─ rest day"
        elif r["today_done"]:
            status = "✅ done"
        else:
            status = "⬜ pending"

        streak = r["current_streak"]
        streak_label = f"{streak}🔥" if streak > 0 else "0"
        rate_7 = r["completion_7d"]
        rate_30 = r["completion_30d"]

        print(f"  {emoji}  {name:<22} {status:<14}  streak: {streak_label:<6}  7d: {rate_7:5.1f}%  30d: {rate_30:5.1f}%")

    print()


def main():
    parser = argparse.ArgumentParser(description="Show habit status and streaks.")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--date", dest="as_of", metavar="YYYY-MM-DD",
                        help="Status as of date (default: today)")
    parser.add_argument("--data-dir", help="Override data directory")

    args = parser.parse_args()
    data_dir = get_data_dir(args.data_dir)

    if args.as_of:
        try:
            as_of = date.fromisoformat(args.as_of)
        except ValueError:
            print(f"Error: invalid date '{args.as_of}'", file=sys.stderr)
            sys.exit(1)
    else:
        as_of = date.today()

    habits_file = data_dir / "habits.json"
    if not habits_file.exists():
        if args.json:
            print(json.dumps([]))
        else:
            print("No habits configured. Run setup_habits.py --add to get started.")
        return

    habits_data = load_json(habits_file, {"habits": []})
    log_data = load_json(data_dir / "log.json", {})

    results = compute_status(habits_data, log_data, as_of)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_table(results, as_of)


if __name__ == "__main__":
    main()
