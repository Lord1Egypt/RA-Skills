#!/usr/bin/env python3
"""
phy-content-calendar — Auto Content Calendar Generator

Generates a 2-week content calendar based on:
- Your content atom library (what you already have to say)
- Platform best practices (optimal days, format, frequency)
- Content mix strategy (30% insight, 20% story, 20% data, 15% contrarian, 15% question)

Input: topic pillars + platform + (optional) content library path
Output: Markdown calendar with draft outlines per day

Zero external dependencies — pure Python 3.7+ stdlib.
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import sys
import textwrap
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


# ─── Content mix strategy ─────────────────────────────────────────────

CONTENT_MIX: list[dict[str, str]] = [
    {"style": "insight", "desc": "Share a non-obvious lesson or pattern you've noticed", "emoji": "💡"},
    {"style": "story", "desc": "Tell a personal experience with specific details", "emoji": "📖"},
    {"style": "data", "desc": "Lead with a specific number, stat, or benchmark", "emoji": "📊"},
    {"style": "contrarian", "desc": "Challenge a common belief in your space", "emoji": "🔥"},
    {"style": "question", "desc": "Ask a genuine question to start a discussion", "emoji": "❓"},
    {"style": "how-to", "desc": "Share a step-by-step process or framework", "emoji": "🔧"},
    {"style": "build-update", "desc": "Share progress on what you're building", "emoji": "🚀"},
]

# Platform-specific optimal days and frequency
PLATFORM_SCHEDULE: dict[str, dict] = {
    "linkedin": {
        "best_days": ["Tuesday", "Wednesday", "Thursday"],
        "ok_days": ["Monday", "Friday"],
        "avoid_days": ["Saturday", "Sunday"],
        "frequency": "3-4 posts/week",
        "best_time": "8-10 AM local",
        "format_tip": "Text posts with line breaks. No external links in body. 3-5 hashtags.",
    },
    "reddit": {
        "best_days": ["Monday", "Tuesday", "Wednesday", "Thursday"],
        "ok_days": ["Friday"],
        "avoid_days": ["Saturday", "Sunday"],
        "frequency": "2-3 posts/week + daily comments",
        "best_time": "9 AM - 12 PM Eastern",
        "format_tip": "Text posts. No self-promo in first paragraph. End with a question.",
    },
    "twitter": {
        "best_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "ok_days": ["Saturday", "Sunday"],
        "avoid_days": [],
        "frequency": "1-2 posts/day",
        "best_time": "9 AM - 12 PM, 5-7 PM",
        "format_tip": "Strong hook. No links in tweet (put in reply). Threads on Wed/Thu.",
    },
    "hackernews": {
        "best_days": ["Monday", "Tuesday", "Wednesday"],
        "ok_days": ["Thursday", "Friday"],
        "avoid_days": ["Saturday", "Sunday"],
        "frequency": "1-2 posts/week max",
        "best_time": "9 AM - 12 PM Pacific",
        "format_tip": "Show HN for projects. Factual titles. Technical depth.",
    },
}


@dataclass
class CalendarEntry:
    date: str           # YYYY-MM-DD
    weekday: str
    platform: str
    style: str
    emoji: str
    topic_pillar: str
    outline: str
    atoms_hint: str = ""  # relevant atoms from library
    is_best_day: bool = False


def _next_weekday(start: datetime, target_days: list[str], skip_days: int = 0) -> datetime:
    """Find the next occurrence of a target weekday."""
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    current = start + timedelta(days=skip_days)
    for _ in range(14):
        if weekdays[current.weekday()] in target_days:
            return current
        current += timedelta(days=1)
    return current


def generate_calendar(
    pillars: list[str],
    platform: str,
    weeks: int = 2,
    start_date: Optional[str] = None,
    library_path: Optional[str] = None,
) -> list[CalendarEntry]:
    """Generate a content calendar."""
    platform = platform.lower()
    schedule = PLATFORM_SCHEDULE.get(platform, PLATFORM_SCHEDULE["linkedin"])

    # Start date
    if start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
    else:
        start = datetime.now()
        # Start from next Monday
        while start.weekday() != 0:
            start += timedelta(days=1)

    weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    posting_days = schedule["best_days"] + schedule["ok_days"]

    # Load content library if available
    atoms_by_topic: dict[str, list[str]] = {}
    if library_path:
        compound_path = None
        for candidate in [
            Path.home() / ".claude" / "skills" / "phy-content-compound" / "scripts" / "content_compound.py",
            Path.home() / "Desktop" / "openclaw-skills-publish" / "phy-content-compound" / "scripts" / "content_compound.py",
        ]:
            if candidate.exists():
                compound_path = str(candidate)
                break

        if compound_path:
            try:
                spec = importlib.util.spec_from_file_location("content_compound", compound_path)
                if spec and spec.loader:
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    library = mod.scan_directory(library_path)
                    for pillar in pillars:
                        results = mod.retrieve_atoms(library, pillar, top_n=3)
                        if results:
                            atoms_by_topic[pillar] = [
                                f"[{a.atom_type}] {a.text[:80]}... ({a.source_file})"
                                for a, _ in results
                            ]
            except Exception:
                pass

    # Generate entries
    entries: list[CalendarEntry] = []
    style_idx = 0
    pillar_idx = 0
    current_date = start

    for week in range(weeks):
        week_posts = 0
        for day_offset in range(7):
            d = current_date + timedelta(days=week * 7 + day_offset)
            day_name = weekday_names[d.weekday()]

            if day_name not in posting_days:
                continue

            # Pick style and pillar
            style_info = CONTENT_MIX[style_idx % len(CONTENT_MIX)]
            pillar = pillars[pillar_idx % len(pillars)]

            # Build outline
            outline = f"{style_info['desc']} about \"{pillar}\""

            # Add atoms hint
            atoms_hint = ""
            if pillar in atoms_by_topic:
                atoms_hint = " | ".join(atoms_by_topic[pillar][:2])

            entries.append(CalendarEntry(
                date=d.strftime("%Y-%m-%d"),
                weekday=day_name,
                platform=platform,
                style=style_info["style"],
                emoji=style_info["emoji"],
                topic_pillar=pillar,
                outline=outline,
                atoms_hint=atoms_hint,
                is_best_day=day_name in schedule["best_days"],
            ))

            style_idx += 1
            pillar_idx += 1
            week_posts += 1

    return entries


def format_calendar(entries: list[CalendarEntry], platform: str) -> str:
    lines: list[str] = []
    w = lines.append

    schedule = PLATFORM_SCHEDULE.get(platform.lower(), PLATFORM_SCHEDULE["linkedin"])

    w("=" * 66)
    w("  phy-content-calendar — Content Calendar")
    w("=" * 66)
    w(f"  Platform  : {platform.title()}")
    w(f"  Frequency : {schedule['frequency']}")
    w(f"  Best time : {schedule['best_time']}")
    w(f"  Format tip: {schedule['format_tip']}")
    w(f"  Posts     : {len(entries)}")
    w("=" * 66)

    current_week = ""
    for entry in entries:
        # Week header
        week_start = datetime.strptime(entry.date, "%Y-%m-%d")
        week_label = f"Week of {week_start.strftime('%b %d')}"
        if week_label != current_week:
            current_week = week_label
            w(f"\n{'─' * 66}")
            w(f"  📅  {week_label}")
            w(f"{'─' * 66}")

        star = "⭐" if entry.is_best_day else "  "
        w(f"\n  {star} {entry.weekday:<10} {entry.date}")
        w(f"     {entry.emoji} Style: {entry.style}")
        w(f"     📌 Topic: {entry.topic_pillar}")
        w(f"     📝 {entry.outline}")
        if entry.atoms_hint:
            w(f"     🔗 Atoms: {entry.atoms_hint[:100]}")

    # Weekly checklist
    w(f"\n{'=' * 66}")
    w("  📋  Weekly Checklist")
    w("=" * 66)
    w("  □ Write drafts for the week (use content-compound for atoms)")
    w("  □ Run humanizer-audit on each draft")
    w("  □ Run platform-rules-engine pre-flight")
    w("  □ Schedule/publish")
    w("  □ End of week: run post-forensics on this week's posts")
    w("")

    return "\n".join(lines)


def format_markdown(entries: list[CalendarEntry], platform: str) -> str:
    """Output as markdown table for easy copy-paste."""
    lines = [
        f"# Content Calendar — {platform.title()}",
        "",
        "| Date | Day | Style | Topic | Outline |",
        "|------|-----|-------|-------|---------|",
    ]
    for e in entries:
        star = " ⭐" if e.is_best_day else ""
        lines.append(f"| {e.date} | {e.weekday}{star} | {e.emoji} {e.style} | {e.topic_pillar} | {e.outline} |")
    return "\n".join(lines)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="phy-content-calendar: Auto Content Calendar Generator",
        epilog=textwrap.dedent("""\
            Examples:
              python3 content_calendar.py --pillars "dev tools" "AI" "startup" --platform linkedin
              python3 content_calendar.py --pillars "security" "OpenClaw" --platform reddit --weeks 4
              python3 content_calendar.py --pillars "AI" "growth" --platform twitter --library ~/content/
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--pillars", nargs="+", required=True, help="3-5 topic pillars")
    parser.add_argument("--platform", "-p", required=True,
                        choices=["linkedin", "reddit", "twitter", "hackernews"])
    parser.add_argument("--weeks", "-w", type=int, default=2, help="Number of weeks (default: 2)")
    parser.add_argument("--start", help="Start date YYYY-MM-DD (default: next Monday)")
    parser.add_argument("--library", "-l", help="Content library path for atom hints")
    parser.add_argument("--format", default="text", choices=["text", "markdown", "json"])

    args = parser.parse_args()

    entries = generate_calendar(
        pillars=args.pillars,
        platform=args.platform,
        weeks=args.weeks,
        start_date=args.start,
        library_path=args.library,
    )

    if args.format == "json":
        print(json.dumps([{
            "date": e.date, "weekday": e.weekday, "style": e.style,
            "topic": e.topic_pillar, "outline": e.outline,
        } for e in entries], indent=2))
    elif args.format == "markdown":
        print(format_markdown(entries, args.platform))
    else:
        print(format_calendar(entries, args.platform))


if __name__ == "__main__":
    main()
