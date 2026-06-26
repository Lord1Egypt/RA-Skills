#!/usr/bin/env python3
"""Generate lesson report after completion."""

import argparse
import json
import os
from datetime import datetime


def lesson_report(course_dir: str, lesson_num: int, strengths: str, weak_points: str, takeaway: str):
    path = os.path.join(course_dir, "progress", "state.json")
    with open(path) as f:
        state = json.load(f)

    key = str(lesson_num)
    l = state["lessons"][key]
    total = state["total_lessons"]
    completed = state["completed"]
    pct = round(completed / total * 100) if total > 0 else 0

    started = l.get("started_at", "?")
    ended = l.get("completed_at", datetime.now().strftime("%Y-%m-%d %H:%M"))
    score = l.get("score", "?")

    report = f"""
╔══════════════════════════════════════════╗
║          📋 Lesson Report                ║
╠══════════════════════════════════════════╣
║  Lesson:    {lesson_num} — {l['title']:<28}║
║  Score:     {score}/3                            ║
║  Started:   {started:<28}║
║  Completed: {ended:<28}║
╠══════════════════════════════════════════╣
║  ✅ Strengths:                           ║
║     {strengths:<36}║
║  ⚠️  Weak points:                        ║
║     {weak_points:<36}║
║  💡 Key takeaway:                        ║
║     {takeaway:<36}║
╠══════════════════════════════════════════╣
║  Overall: {completed}/{total} lessons ({pct}%)               ║
╚══════════════════════════════════════════╝
"""
    print(report)

    # Also save to file
    report_path = os.path.join(course_dir, "progress", f"report-lesson-{lesson_num:02d}.md")
    with open(report_path, "w") as f:
        f.write(f"# Lesson {lesson_num} Report: {l['title']}\n\n")
        f.write(f"- Date: {ended}\n")
        f.write(f"- Score: {score}/3\n")
        f.write(f"- Strengths: {strengths}\n")
        f.write(f"- Weak points: {weak_points}\n")
        f.write(f"- Key takeaway: {takeaway}\n")
        f.write(f"- Overall progress: {completed}/{total} ({pct}%)\n")

    print(f"Report saved: {report_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate lesson report")
    parser.add_argument("course_dir", help="Course directory path")
    parser.add_argument("lesson", type=int, help="Lesson number")
    parser.add_argument("--strengths", required=True, help="What student understood well")
    parser.add_argument("--weak", default="none", help="What needs revisiting")
    parser.add_argument("--takeaway", required=True, help="One sentence key takeaway")
    args = parser.parse_args()
    lesson_report(args.course_dir, args.lesson, args.strengths, args.weak, args.takeaway)
