#!/usr/bin/env python3
"""Show course progress overview — ASCII visualization."""

import argparse
import json
import os


def show_progress(course_dir: str):
    path = os.path.join(course_dir, "progress", "state.json")
    with open(path) as f:
        state = json.load(f)

    total = state["total_lessons"]
    completed = state["completed"]
    pct = round(completed / total * 100) if total > 0 else 0

    # Progress bar
    bar_width = 30
    filled = round(bar_width * completed / total) if total > 0 else 0
    bar = "=" * filled + "." * (bar_width - filled)
    print(f"\n  Course: {state['title']}")
    print(f"  Progress: [{bar}] {completed}/{total} ({pct}%)\n")

    # Lesson list
    for num in sorted(state["lessons"].keys(), key=int):
        l = state["lessons"][num]
        status = l["status"]
        if status == "completed":
            icon = "✅"
            suffix = f" — {l['score']}/3"
        elif status == "in-progress":
            icon = "🔵"
            steps = ", ".join(l.get("steps_completed", []))
            suffix = f" ← in progress ({steps})"
        else:
            icon = "⬜"
            suffix = ""

        # Mark current
        marker = ""
        if int(num) == state["current_lesson"] and status != "completed":
            marker = "  👈 you are here"

        print(f"  {icon} Lesson {num}: {l['title']}{suffix}{marker}")

    # Weak points summary
    all_weak = []
    for num in sorted(state["lessons"].keys(), key=int):
        l = state["lessons"][num]
        if l["weak_points"]:
            for w in l["weak_points"]:
                all_weak.append(f"L{num}: {w}")

    if all_weak:
        print(f"\n  ⚠️  Weak points to revisit:")
        for w in all_weak:
            print(f"     - {w}")

    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Show course progress")
    parser.add_argument("course_dir", help="Course directory path")
    args = parser.parse_args()
    show_progress(args.course_dir)
