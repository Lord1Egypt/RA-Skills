#!/usr/bin/env python3
"""
weekly_review.py — Generate a weekly review markdown report.

Usage:
  python weekly_review.py                    # Current week (Mon–today)
  python weekly_review.py --week 2024-01-15  # Week containing this date
  python weekly_review.py --output file.md   # Write to file instead of stdout
  python weekly_review.py --obsidian         # Save to Obsidian vault
  python weekly_review.py --data-dir /path
"""

import json
import sys
import os
import argparse
from datetime import date, timedelta, datetime
from pathlib import Path


DEFAULT_DATA_DIR = Path.home() / ".openclaw" / "workspace" / "habits"
DEFAULT_VAULT_DIR = Path.home() / ".openclaw" / "workspace" / "vault"


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


def get_week_range(anchor):
    """Return (monday, sunday) for the week containing anchor."""
    monday = anchor - timedelta(days=anchor.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday


def is_expected_day(habit, d):
    freq = habit.get("frequency", "daily")
    if freq == "daily":
        return True
    if freq == "weekday":
        return d.weekday() < 5
    if freq == "weekly":
        return True
    return True


def progress_bar(pct, width=20):
    """ASCII progress bar. e.g. [████████████░░░░░░░░] 60%"""
    filled = round(pct / 100 * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {pct:.0f}%"


def get_week_stats(habit, log_data, week_start, week_end, today):
    """Compute per-habit stats for the given week."""
    habit_id = habit["id"]
    freq = habit.get("frequency", "daily")

    days_done = []
    days_expected = []

    if freq == "weekly":
        # Weekly habits: did it happen at all this week?
        done_any = False
        for offset in range(7):
            d = week_start + timedelta(days=offset)
            if d > today or d > week_end:
                break
            if log_data.get(d.isoformat(), {}).get(habit_id, {}).get("done", False):
                done_any = True
                days_done.append(d)
        expected = 1
        done_count = 1 if done_any else 0
    else:
        for offset in range(7):
            d = week_start + timedelta(days=offset)
            if d > today or d > week_end:
                break
            if is_expected_day(habit, d):
                days_expected.append(d)
                if log_data.get(d.isoformat(), {}).get(habit_id, {}).get("done", False):
                    days_done.append(d)
        expected = len(days_expected)
        done_count = len(days_done)

    pct = round(done_count / expected * 100, 1) if expected > 0 else 0.0
    return {
        "done_count": done_count,
        "expected": expected,
        "pct": pct,
        "days_done": [d.isoformat() for d in days_done],
    }


def calc_current_streak(habit, log_data, as_of):
    habit_id = habit["id"]
    freq = habit.get("frequency", "daily")
    min_floor = as_of - timedelta(days=365)

    if freq == "weekly":
        streak = 0
        week_end = as_of
        while week_end >= min_floor:
            week_start = week_end - timedelta(days=6)
            done = any(
                log_data.get((week_start + timedelta(days=i)).isoformat(), {})
                         .get(habit_id, {}).get("done", False)
                for i in range(7)
            )
            if not done:
                break
            streak += 1
            week_end = week_start - timedelta(days=1)
        return streak

    streak = 0
    current = as_of
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


def motivation_line(overall_pct, best_habit, worst_habit):
    if overall_pct == 100:
        return "🏆 Perfect week. Every single habit done. Keep that energy going."
    elif overall_pct >= 80:
        return f"🔥 Strong week — {overall_pct:.0f}% overall. {best_habit['name']} was on fire. A few more days of this and those streaks get serious."
    elif overall_pct >= 60:
        return f"📈 Solid progress at {overall_pct:.0f}%. {best_habit['name']} led the way. {worst_habit['name']} needs more attention next week."
    elif overall_pct >= 40:
        return f"⚡ Rough week at {overall_pct:.0f}%. That's fine — the point is showing back up. {best_habit['name']} still showed up. Build on that."
    else:
        return f"🌱 Tough week. {overall_pct:.0f}% completion. Pick one habit — just one — and make it non-negotiable next week."


def generate_report(habits_data, log_data, week_start, week_end, today):
    active_habits = [h for h in habits_data.get("habits", []) if h.get("active", True)]
    if not active_habits:
        return "# Weekly Habit Review\n\nNo active habits configured.\n"

    # Compute stats
    stats = {}
    for habit in active_habits:
        stats[habit["id"]] = get_week_stats(habit, log_data, week_start, week_end, today)

    # Overall completion
    total_done = sum(s["done_count"] for s in stats.values())
    total_expected = sum(s["expected"] for s in stats.values())
    overall_pct = round(total_done / total_expected * 100, 1) if total_expected > 0 else 0.0

    # Best/worst
    sortable = sorted(active_habits, key=lambda h: stats[h["id"]]["pct"], reverse=True)
    best = sortable[0]
    worst = sortable[-1]

    # Streaks as of week_end (or today if week_end is in the future)
    streak_date = min(week_end, today)
    streaks = {h["id"]: calc_current_streak(h, log_data, streak_date) for h in active_habits}

    lines = []
    lines.append("---")
    lines.append(f"date: {today.isoformat()}")
    lines.append(f"week_start: {week_start.isoformat()}")
    lines.append(f"week_end: {week_end.isoformat()}")
    lines.append("type: habit-weekly-review")
    lines.append("tags: [habits, weekly-review, self-improvement]")
    lines.append("---")
    lines.append("")
    lines.append(f"# 📊 Weekly Habit Review")
    lines.append(f"### {week_start.strftime('%B %d')} – {week_end.strftime('%B %d, %Y')}")
    lines.append("")

    # Summary bar
    lines.append("## Overview")
    lines.append("")
    lines.append(f"**Overall completion: {progress_bar(overall_pct)}**")
    lines.append(f"*{total_done} of {total_expected} expected completions*")
    lines.append("")

    # Day-by-day grid header
    day_labels = []
    for offset in range(7):
        d = week_start + timedelta(days=offset)
        label = d.strftime("%a")
        day_labels.append(label)

    lines.append("## Habit Log")
    lines.append("")

    col_w = 5
    header = f"{'Habit':<24}" + "".join(f"{d:^{col_w}}" for d in day_labels) + f"  {'Rate':>6}  {'Streak':>7}"
    lines.append(f"```")
    lines.append(header)
    lines.append("─" * len(header))

    for habit in active_habits:
        habit_id = habit["id"]
        emoji = habit.get("emoji", "•")
        name = f"{emoji} {habit['name']}"
        row = f"{name:<24}"
        for offset in range(7):
            d = week_start + timedelta(days=offset)
            if d > today:
                cell = "·"
            elif not is_expected_day(habit, d):
                cell = "─"
            elif log_data.get(d.isoformat(), {}).get(habit_id, {}).get("done", False):
                cell = "✓"
            else:
                cell = "✗"
            row += f"{cell:^{col_w}}"
        s = stats[habit_id]
        streak = streaks[habit_id]
        streak_str = f"{streak}🔥" if streak > 0 else "0"
        row += f"  {s['pct']:5.0f}%  {streak_str:>7}"
        lines.append(row)

    lines.append("─" * len(header))
    lines.append(f"{'TOTAL':<24}" + " " * (col_w * 7) + f"  {overall_pct:5.0f}%")
    lines.append("```")
    lines.append("")

    # Per-habit breakdown
    lines.append("## Breakdown")
    lines.append("")
    for habit in active_habits:
        habit_id = habit["id"]
        s = stats[habit_id]
        emoji = habit.get("emoji", "•")
        streak = streaks[habit_id]
        lines.append(f"### {emoji} {habit['name']}")
        lines.append(f"- **This week:** {s['done_count']}/{s['expected']}  {progress_bar(s['pct'], 15)}")
        lines.append(f"- **Current streak:** {streak} {'day' if habit.get('frequency') != 'weekly' else 'week'}{'s' if streak != 1 else ''}" + (" 🔥" if streak >= 3 else ""))
        lines.append(f"- **Frequency:** {habit.get('frequency', 'daily').capitalize()}")
        lines.append("")

    # Best/worst
    lines.append("## Highlights")
    lines.append("")
    best_s = stats[best["id"]]
    worst_s = stats[worst["id"]]
    lines.append(f"- 🥇 **Best habit:** {best.get('emoji','')} {best['name']} — {best_s['pct']:.0f}%")
    lines.append(f"- 📉 **Needs work:** {worst.get('emoji','')} {worst['name']} — {worst_s['pct']:.0f}%")

    top_streaks = sorted(active_habits, key=lambda h: streaks[h["id"]], reverse=True)
    if streaks[top_streaks[0]["id"]] > 0:
        h = top_streaks[0]
        unit = "week" if h.get("frequency") == "weekly" else "day"
        lines.append(f"- 🔥 **Longest active streak:** {h.get('emoji','')} {h['name']} — {streaks[h['id']]} {unit}s")

    lines.append("")

    # Motivation
    lines.append("## Summary")
    lines.append("")
    lines.append(motivation_line(overall_pct, best, worst))
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate weekly habit review.")
    parser.add_argument("--week", metavar="YYYY-MM-DD",
                        help="Week containing this date (default: current week)")
    parser.add_argument("--output", metavar="FILE", help="Write to file")
    parser.add_argument("--obsidian", action="store_true",
                        help="Save to Obsidian vault (habits/weekly-reviews/)")
    parser.add_argument("--data-dir", help="Override data directory")

    args = parser.parse_args()
    data_dir = get_data_dir(args.data_dir)
    today = date.today()

    if args.week:
        try:
            anchor = date.fromisoformat(args.week)
        except ValueError:
            print(f"Error: invalid date '{args.week}'", file=sys.stderr)
            sys.exit(1)
    else:
        anchor = today

    week_start, week_end = get_week_range(anchor)

    habits_file = data_dir / "habits.json"
    if not habits_file.exists():
        print("No habits configured. Run setup_habits.py --add to get started.")
        return

    habits_data = load_json(habits_file, {"habits": []})
    log_data = load_json(data_dir / "log.json", {})

    report = generate_report(habits_data, log_data, week_start, week_end, today)

    if args.obsidian:
        vault_dir = DEFAULT_VAULT_DIR / "habits" / "weekly-reviews"
        vault_dir.mkdir(parents=True, exist_ok=True)
        out_path = vault_dir / f"{week_start.isoformat()}.md"
        with open(out_path, "w") as f:
            f.write(report)
        print(f"✓ Saved to {out_path}")
    elif args.output:
        out_path = Path(args.output)
        with open(out_path, "w") as f:
            f.write(report)
        print(f"✓ Saved to {out_path}")
    else:
        print(report)


if __name__ == "__main__":
    main()
