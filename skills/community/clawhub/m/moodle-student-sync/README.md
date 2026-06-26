# Moodle Student Sync

OpenClaw skill package for syncing Moodle data for students.

## What it does

- Syncs student Moodle data into a single snapshot.
- Lists upcoming deadlines.
- Shows grade overview.
- Generates a daily markdown digest.
- Builds a short-term study plan.

## Requirements

- Python 3.10+
- `requests`
- Moodle mobile web service token

Install dependency:

```bash
pip install requests
```

Environment variables:

```bash
export MOODLE_URL="https://moodle.example.edu"
export MOODLE_TOKEN="your_token"
export MOODLE_USER_ID="14042"  # optional
```

## Local usage

```bash
python scripts/moodle_sync.py sync --include-contents --max-courses 5
python scripts/moodle_sync.py deadlines --limit 20
python scripts/moodle_sync.py grades
python scripts/moodle_sync.py digest --limit 10
python scripts/moodle_sync.py plan --days 7 --grade-threshold 70
```

## Validate and package for ClawHub

From repository root:

```bash
python .agents/skills/skill-creator/scripts/quick_validate.py moodle-student-sync
python .agents/skills/skill-creator/scripts/package_skill.py moodle-student-sync dist
```

This produces:

- `dist/moodle-student-sync.skill`

Upload the generated `.skill` file to ClawHub.
