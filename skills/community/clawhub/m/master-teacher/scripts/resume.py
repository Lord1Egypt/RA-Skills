#!/usr/bin/env python3
"""Load resume state — determine where student left off and what to review."""

import argparse
import json
import os


def resume(course_dir: str):
    path = os.path.join(course_dir, "progress", "state.json")
    with open(path) as f:
        state = json.load(f)

    completed = state["completed"]
    total = state["total_lessons"]
    current = state["current_lesson"]
    current_key = str(current)

    print(f"Course: {state['title']}")
    print(f"Progress: {completed}/{total} completed")
    print()

    if current_key not in state["lessons"]:
        print(f"STATUS: course_complete")
        print(f"All {total} lessons completed.")
        return

    l = state["lessons"][current_key]

    if l["status"] == "in-progress":
        # Mid-lesson resume
        print(f"STATUS: mid_lesson")
        print(f"LESSON: {current} — {l['title']}")
        print(f"STARTED: {l.get('started_at', '?')}")
        print(f"STEPS_DONE: {', '.join(l.get('steps_completed', []))}")
        print(f"NEXT_STEP: {_next_step(l.get('steps_completed', []))}")
        if l.get("key_points_covered"):
            print(f"COVERED: {', '.join(l['key_points_covered'])}")
        if l.get("key_points_remaining"):
            print(f"REMAINING: {', '.join(l['key_points_remaining'])}")
        if l.get("last_student_response"):
            print(f"LAST_RESPONSE: {l['last_student_response']}")

        # Suggest review of what was covered
        if l.get("key_points_covered"):
            print(f"\nREVIEW_SUGGESTION: Ask student to recall: {l['key_points_covered'][0]}")

    elif l["status"] == "pending":
        # Between lessons
        print(f"STATUS: between_lessons")
        print(f"NEXT_LESSON: {current} — {l['title']}")

        # Find last completed lesson for review
        prev_key = str(current - 1)
        if prev_key in state["lessons"] and state["lessons"][prev_key]["status"] == "completed":
            prev = state["lessons"][prev_key]
            print(f"LAST_COMPLETED: {current - 1} — {prev['title']} (score: {prev['score']}/3)")
            if prev.get("weak_points"):
                print(f"WEAK_POINTS: {', '.join(prev['weak_points'])}")
                print(f"REVIEW_SUGGESTION: Review weak points from lesson {current - 1} before starting")
            else:
                print(f"REVIEW_SUGGESTION: Quick recall question on lesson {current - 1}")
    else:
        print(f"STATUS: unknown ({l['status']})")

    # Check if spaced review is due
    spaced_review = _check_spaced_review(state)
    if spaced_review:
        print(f"\nSPACED_REVIEW_DUE: Revisit lessons {', '.join(map(str, spaced_review))}")


def _next_step(completed_steps: list) -> str:
    all_steps = ["position", "concepts", "code", "practice", "multimedia", "verify"]
    for s in all_steps:
        if s not in completed_steps:
            return s
    return "all_done"


def _check_spaced_review(state: dict) -> list:
    """Check if spaced review is due based on current progress."""
    completed = state["completed"]
    review_lessons = []

    # At lesson 3, review lesson 1
    if completed == 2:
        review_lessons.append(1)
    # At lesson 6, review lessons 1-3
    elif completed == 5:
        review_lessons.extend([1, 2, 3])
    # At midpoint, review all weak points
    elif completed == state["total_lessons"] // 2:
        for num, l in state["lessons"].items():
            if l.get("weak_points"):
                review_lessons.append(int(num))

    return review_lessons


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load resume state")
    parser.add_argument("course_dir", help="Course directory path")
    args = parser.parse_args()
    resume(args.course_dir)
