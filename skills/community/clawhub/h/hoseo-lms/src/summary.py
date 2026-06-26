import json
import os

from hoseo_utils import DATA_PATH, SUBMISSION_KEYWORDS

SEPARATOR = "=" * 72


def classify_submission(value: str) -> str:
    lowered = (value or "").lower()
    for keyword in SUBMISSION_KEYWORDS:
        if keyword in lowered:
            return "submitted"
    if not value.strip():
        return "unknown"
    return "not_submitted"


def print_summary():
    data_path = os.path.expanduser(DATA_PATH)
    if not os.path.exists(data_path):
        print("Data file not found. Run scraper.py first.")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated_at = data.get("metadata", {}).get("last_updated_str", "unknown")
    print(f"Hoseo LMS summary (last updated: {updated_at})")
    print(SEPARATOR)

    for course in data.get("courses", []):
        title = course.get("title", "Unknown course")
        professor = course.get("professor", "Unknown professor")
        print(f"\nCourse: {title}")
        print(f"Professor: {professor}")

        unwatched = [a for a in course.get("attendance", []) if a.get("status") != "O"]
        if unwatched:
            print("  Unwatched online lectures:")
            for item in unwatched:
                print(
                    f"    - Week {item.get('week', '?')}: {item.get('title', '')} "
                    f"(required: {item.get('required_time', '-')}, status: {item.get('status', '-')})"
                )
        else:
            print("  Unwatched online lectures: none")

        assignments = course.get("assignments", [])
        if assignments:
            print("  Assignments:")
            for item in assignments:
                state = classify_submission(item.get("submitted", ""))
                print(
                    f"    - {item.get('week', '-')} | {item.get('title', '-')} | "
                    f"deadline: {item.get('deadline', '-')} | submission: {state}"
                )
        else:
            print("  Assignments: none")

        quizzes = course.get("quizzes", [])
        if quizzes:
            print("  Quizzes:")
            for item in quizzes:
                print(
                    f"    - {item.get('week', '-')} | {item.get('title', '-')} | "
                    f"deadline: {item.get('deadline', '-')}"
                )
        else:
            print("  Quizzes: none")


if __name__ == "__main__":
    print_summary()

