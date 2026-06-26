---
name: moodle-student-sync
description: Sync and summarize student Moodle data including courses, upcoming deadlines, grades, files, and announcements. Use this skill whenever a user asks for Moodle course sync, assignment tracking, grade overviews, study planning, or daily academic digests, even if they do not explicitly say "Moodle API."
license: MIT
compatibility: Requires Python 3.10+, requests, and environment variables MOODLE_URL and MOODLE_TOKEN.
metadata: {"openclaw":{"requires":{"bins":["python3"],"env":["MOODLE_URL","MOODLE_TOKEN"]},"primaryEnv":"MOODLE_TOKEN"}}
---

# Moodle Student Sync

Use this skill to pull student-facing data from Moodle Web Services and turn it into useful outputs such as deadline lists, grade summaries, and study plans.

## Required environment

Set these values before running commands:

```bash
export MOODLE_URL="https://moodle.example.edu"
export MOODLE_TOKEN="your_mobile_web_service_token"
export MOODLE_USER_ID="14042"  # optional
```

## Workflow

1. Verify API connectivity with `core_webservice_get_site_info`.
2. Resolve user ID from `MOODLE_USER_ID` or site info response.
3. Pull enrolled courses via `core_enrol_get_users_courses`.
4. Pull high-value overview data:
   - `core_calendar_get_calendar_upcoming_view`
   - `gradereport_overview_get_course_grades`
   - `message_popup_get_popup_notifications`
5. Optionally fetch per-course content (`core_course_get_contents`) for active courses.
6. Format one of these outputs:
   - JSON sync snapshot
   - deadlines report
   - grades report
   - daily digest markdown
   - study plan markdown

## Commands

```bash
python scripts/moodle_sync.py sync --include-contents --max-courses 5
python scripts/moodle_sync.py deadlines --limit 20
python scripts/moodle_sync.py grades
python scripts/moodle_sync.py digest --limit 10
python scripts/moodle_sync.py plan --days 7 --grade-threshold 70
```

## Quality guardrails

- Always check Moodle responses for `exception` and fail with a clear error.
- Respect rate limiting between calls (default 15 seconds).
- Prefer `rawgrade` values for calculations; treat formatted grade strings as display-only.
- Handle nulls for `progress`, `rawgrade`, and missing dates.
- Filter to active/current courses when computing plans and deadline alerts.

## File map

- `scripts/moodle_client.py`: API client, auth, error handling, parameter flattening.
- `scripts/moodle_sync.py`: command entrypoint for sync/deadlines/grades/digest/plan.
- `scripts/digest.py`: markdown digest generation.
- `scripts/study_planner.py`: priority-based study plan generation.
- `templates/*.md`: reusable output templates.
- `tests/`: basic client tests and sample fixtures.
