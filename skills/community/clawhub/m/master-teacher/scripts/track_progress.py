#!/usr/bin/env python3
"""Update course progress — lesson completion, intra-lesson state, scores."""

import argparse
import json
import os
from datetime import datetime


def load_state(course_dir: str) -> dict:
    path = os.path.join(course_dir, "progress", "state.json")
    with open(path) as f:
        return json.load(f)


def save_state(course_dir: str, state: dict):
    path = os.path.join(course_dir, "progress", "state.json")
    with open(path, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    rebuild_tracking_md(course_dir, state)


def rebuild_tracking_md(course_dir: str, state: dict):
    """Rebuild tracking.md from state.json (single source of truth)."""
    completed = state["completed"]
    total = state["total_lessons"]
    pct = round(completed / total * 100) if total > 0 else 0

    lines = [
        f"# Progress: {state['title']}\n",
        f"## Current State",
        f"- Completed: {completed}/{total}",
        f"- Current lesson: {state['current_lesson']}",
        f"- Overall: {pct}%\n",
        f"## Lessons",
        "| # | Title | Status | Date | Score | Weak points |",
        "|---|-------|--------|------|-------|-------------|",
    ]

    for num in sorted(state["lessons"].keys(), key=int):
        l = state["lessons"][num]
        date = l.get("completed_at") or l.get("started_at") or "-"
        score = f"{l['score']}/3" if l["score"] is not None else "-"
        weak = ", ".join(l["weak_points"]) if l["weak_points"] else "-"
        lines.append(f"| {num} | {l['title']} | {l['status']} | {date} | {score} | {weak} |")

    lines.append("\n## Session Log")

    # Append in-progress details if any
    cur = str(state["current_lesson"])
    if state["lessons"].get(cur, {}).get("status") == "in-progress":
        l = state["lessons"][cur]
        lines.append(f"\n### Lesson {cur} — in progress")
        lines.append(f"- Started: {l.get('started_at', '-')}")
        lines.append(f"- Steps completed: {', '.join(l.get('steps_completed', []))}")
        if l.get("key_points_covered"):
            lines.append(f"- Covered: {', '.join(l['key_points_covered'])}")
        if l.get("key_points_remaining"):
            lines.append(f"- Remaining: {', '.join(l['key_points_remaining'])}")

    path = os.path.join(course_dir, "progress", "tracking.md")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


def start_lesson(course_dir: str, lesson_num: int):
    state = load_state(course_dir)
    key = str(lesson_num)
    state["lessons"][key]["status"] = "in-progress"
    state["lessons"][key]["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    state["current_lesson"] = lesson_num
    state["current_step"] = "position"
    save_state(course_dir, state)
    print(f"Lesson {lesson_num} started")


def update_step(course_dir: str, lesson_num: int, step: str, points_covered: list = None, points_remaining: list = None, last_response: str = None):
    state = load_state(course_dir)
    key = str(lesson_num)
    l = state["lessons"][key]
    if step not in l["steps_completed"]:
        l["steps_completed"].append(step)
    if points_covered:
        l["key_points_covered"] = points_covered
    if points_remaining:
        l["key_points_remaining"] = points_remaining
    if last_response:
        l["last_student_response"] = last_response
    state["current_step"] = step
    save_state(course_dir, state)
    print(f"Lesson {lesson_num}: step '{step}' recorded")


def complete_lesson(course_dir: str, lesson_num: int, score: int, weak_points: list = None):
    state = load_state(course_dir)
    key = str(lesson_num)
    state["lessons"][key]["status"] = "completed"
    state["lessons"][key]["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    state["lessons"][key]["score"] = score
    state["lessons"][key]["weak_points"] = weak_points or []
    state["lessons"][key]["steps_completed"] = ["position", "concepts", "code", "practice", "verify"]
    state["completed"] += 1
    state["current_lesson"] = lesson_num + 1
    state["current_step"] = None
    save_state(course_dir, state)
    print(f"Lesson {lesson_num} completed. Score: {score}/3. Progress: {state['completed']}/{state['total_lessons']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update course progress")
    sub = parser.add_subparsers(dest="command")

    p_start = sub.add_parser("start", help="Start a lesson")
    p_start.add_argument("course_dir")
    p_start.add_argument("lesson", type=int)

    p_step = sub.add_parser("step", help="Record a completed step within a lesson")
    p_step.add_argument("course_dir")
    p_step.add_argument("lesson", type=int)
    p_step.add_argument("step_name", help="position|concepts|code|practice|multimedia|verify")
    p_step.add_argument("--covered", nargs="*", help="Key points covered so far")
    p_step.add_argument("--remaining", nargs="*", help="Key points remaining")
    p_step.add_argument("--response", help="Student's last response snippet")

    p_complete = sub.add_parser("complete", help="Complete a lesson")
    p_complete.add_argument("course_dir")
    p_complete.add_argument("lesson", type=int)
    p_complete.add_argument("--score", type=int, required=True, help="Score out of 3")
    p_complete.add_argument("--weak", nargs="*", help="Weak points")

    args = parser.parse_args()

    if args.command == "start":
        start_lesson(args.course_dir, args.lesson)
    elif args.command == "step":
        update_step(args.course_dir, args.lesson, args.step_name,
                    points_covered=args.covered, points_remaining=args.remaining,
                    last_response=args.response)
    elif args.command == "complete":
        complete_lesson(args.course_dir, args.lesson, args.score, weak_points=args.weak)
