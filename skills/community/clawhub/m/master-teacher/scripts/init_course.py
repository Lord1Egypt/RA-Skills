#!/usr/bin/env python3
"""Initialize a course directory structure."""

import argparse
import os
import json
from datetime import datetime


def init_course(course_dir: str, title: str, lessons: list[dict]):
    """
    Create course directory with README, progress tracking, and prep folder.
    
    Args:
        course_dir: path to course root
        title: course title
        lessons: list of {"number": int, "title": str, "summary": str}
    """
    os.makedirs(os.path.join(course_dir, "lessons"), exist_ok=True)
    os.makedirs(os.path.join(course_dir, "progress"), exist_ok=True)
    os.makedirs(os.path.join(course_dir, "prep", "repos"), exist_ok=True)
    os.makedirs(os.path.join(course_dir, "prep", "articles"), exist_ok=True)

    # README.md
    lesson_table = "| # | Title | Summary |\n|---|-------|--------|\n"
    for l in lessons:
        lesson_table += f"| {l['number']} | {l['title']} | {l['summary']} |\n"

    readme = f"""# {title}

Created: {datetime.now().strftime('%Y-%m-%d')}

## Lessons

{lesson_table}
"""
    with open(os.path.join(course_dir, "README.md"), "w") as f:
        f.write(readme)

    # progress/tracking.md
    status_rows = ""
    for l in lessons:
        status_rows += f"| {l['number']} | {l['title']} | pending | - | - | - |\n"

    tracking = f"""# Progress: {title}

## Current State
- Completed: 0/{len(lessons)}
- Current lesson: 1
- Last session: not started
- Overall: 0%

## Lessons
| # | Title | Status | Date | Score | Weak points |
|---|-------|--------|------|-------|-------------|
{status_rows}
## Session Log
"""
    with open(os.path.join(course_dir, "progress", "tracking.md"), "w") as f:
        f.write(tracking)

    # progress/state.json (machine-readable state)
    state = {
        "title": title,
        "total_lessons": len(lessons),
        "completed": 0,
        "current_lesson": 1,
        "current_step": None,
        "lessons": {
            str(l["number"]): {
                "title": l["title"],
                "status": "pending",
                "score": None,
                "weak_points": [],
                "started_at": None,
                "completed_at": None,
                "steps_completed": [],
                "last_student_response": None,
                "key_points_covered": [],
                "key_points_remaining": []
            }
            for l in lessons
        }
    }
    with open(os.path.join(course_dir, "progress", "state.json"), "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    print(f"Course initialized: {course_dir}")
    print(f"  Lessons: {len(lessons)}")
    print(f"  Files: README.md, progress/tracking.md, progress/state.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize a course")
    parser.add_argument("course_dir", help="Course directory path")
    parser.add_argument("--title", required=True, help="Course title")
    parser.add_argument("--lessons", required=True, help='JSON array: [{"number":1,"title":"...","summary":"..."}]')
    args = parser.parse_args()

    lessons = json.loads(args.lessons)
    init_course(args.course_dir, args.title, lessons)
