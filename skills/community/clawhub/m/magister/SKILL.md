---
name: magister
description: Fetch schedule, grades, and infractions from https://magister.net 🇳🇱 portal
metadata: {"clawdbot":{"emoji":"🇲","requires":{"bins":["node"],"env":["MAGISTER_HOST","MAGISTER_USER","MAGISTER_PASSWORD"]}}}
---
# Commands

```bash
node magister.mjs students                       # list students (works for parent and child credentials)
node magister.mjs schedule <id> <from> <to>      # schedule, YYYY-MM-DD dates
node magister.mjs grades <aanmelding_id> [top]   # grades (default top=50)
node magister.mjs infractions <id> <from> <to>   # absences
```

# Flow

Run `students` first to get each student's `id` and `aanmelding_id`. Use `id` for schedule and infractions, `aanmelding_id` for grades.

