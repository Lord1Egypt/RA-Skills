import json
import os
import time
import urllib.parse

from hoseo_utils import (
    BASE_URL,
    LMS_PATHS,
    load_credentials,
    set_secure_permissions,
    install_cookie_opener,
    http_get,
    http_post,
    TokenParser,
    CourseListParser,
    ActivityParser,
    FirstTableParser,
)

ATTENDANCE_FULL_ROW_LENGTH = 7
ATTENDANCE_SHORT_ROW_LENGTH = 5
ASSIGNMENT_MIN_COLUMNS = 4
QUIZ_MIN_COLUMNS = 3


def _build_url(path_key: str, course_id: str = "") -> str:
    path = LMS_PATHS[path_key]
    if course_id:
        return f"{BASE_URL}{path}?id={course_id}"
    return f"{BASE_URL}{path}"


def parse_attendance(course_id: str) -> list:
    html = http_get(_build_url("attendance", course_id))
    parser = FirstTableParser()
    parser.feed(html)

    attendance = []
    current_week = ""

    for row in parser.rows[1:]:
        if len(row) == ATTENDANCE_FULL_ROW_LENGTH:
            week = row[0].strip()
            title = row[1].strip()
            required_time = row[2].strip()
            status = row[5].strip()
            if week:
                current_week = week
        elif len(row) >= ATTENDANCE_SHORT_ROW_LENGTH:
            week = current_week
            title = row[0].strip()
            required_time = row[1].strip()
            status = row[4].strip()
        else:
            continue

        if not title or ":" not in required_time:
            continue

        attendance.append({
            "week": week,
            "title": title,
            "required_time": required_time,
            "status": status,
        })

    return attendance


def parse_assignments(course_id: str) -> list:
    html = http_get(_build_url("assignments", course_id))
    parser = FirstTableParser()
    parser.feed(html)

    assignments = []
    for row in parser.rows[1:]:
        if len(row) < ASSIGNMENT_MIN_COLUMNS:
            continue
        assignments.append({
            "week": row[0].strip(),
            "title": row[1].strip(),
            "deadline": row[2].strip(),
            "submitted": row[3].strip(),
        })

    return assignments


def parse_quizzes(course_id: str) -> list:
    html = http_get(_build_url("quizzes", course_id))
    parser = FirstTableParser()
    parser.feed(html)

    quizzes = []
    for row in parser.rows[1:]:
        if len(row) < QUIZ_MIN_COLUMNS:
            continue
        quizzes.append({
            "week": row[0].strip(),
            "title": row[1].strip(),
            "deadline": row[2].strip(),
        })

    return quizzes


def _crawl_course(course: dict) -> dict:
    course_url = course["url"]
    course_id = urllib.parse.parse_qs(
        urllib.parse.urlparse(course_url).query
    ).get("id", [""])[0]

    print(f"  - {course['title']} ({course_id}) / {course['professor']}")

    course_data = {
        "title": course["title"],
        "professor": course["professor"],
        "url": course_url,
        "id": course_id,
        "activities": [],
        "attendance": [],
        "assignments": [],
        "quizzes": [],
    }

    collectors = {
        "activities": lambda: _parse_activities(course_url),
        "attendance": lambda: parse_attendance(course_id),
        "assignments": lambda: parse_assignments(course_id),
        "quizzes": lambda: parse_quizzes(course_id),
    }

    for key, collect in collectors.items():
        try:
            course_data[key] = collect()
        except Exception as ex:
            print(f"    Warning: failed to parse {key} ({ex})")

    return course_data


def _parse_activities(course_url: str) -> list:
    html = http_get(course_url)
    parser = ActivityParser()
    parser.feed(html)
    return parser.activities


def main():
    creds = load_credentials()
    install_cookie_opener()

    print("Step 1/3: Logging in...")
    login_url = _build_url("login")
    login_html = http_get(login_url)
    token_parser = TokenParser()
    token_parser.feed(login_html)

    http_post(login_url, {
        "username": creds["id"],
        "password": creds["pw"],
        "anchor": "",
        "logintoken": token_parser.logintoken,
    })

    print("Step 2/3: Fetching course list...")
    dashboard_html = http_get(_build_url("course_list"))
    course_parser = CourseListParser()
    course_parser.feed(dashboard_html)

    result = {
        "metadata": {
            "last_updated": int(time.time()),
            "last_updated_str": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "source": BASE_URL,
            "course_count": len(course_parser.courses),
        },
        "courses": [],
    }

    print("Step 3/3: Crawling course details...")
    for course in course_parser.courses:
        result["courses"].append(_crawl_course(course))
        time.sleep(0.3)

    output_path = os.path.expanduser("~/.config/hoseo_lms/data.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    set_secure_permissions(output_path)
    print(f"Done. Data written to: {output_path}")


if __name__ == "__main__":
    main()

