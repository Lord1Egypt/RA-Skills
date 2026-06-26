---
name: job-tracker
description: Track job applications, contacts, deadlines, and follow-up reminders in a local SQLite database.
version: 0.1.0
metadata:
  openclaw:
    homepage: https://github.com/Mehulupase01/openclaw-skill-suite/tree/main/skills/job-tracker
    requires:
      bins:
        - python
---

# Job Tracker

Use this skill when the user wants to capture job applications, update status,
list upcoming follow-ups, or summarize the health of their application pipeline.

## When to Use

- Logging a new application from a chat message.
- Updating status after an interview or recruiter reply.
- Finding deadlines or follow-ups due soon.
- Summarizing the current application pipeline.

## Commands

The helper script stores state in `{baseDir}/.runtime/job-tracker.db`.

### Add an application

```bash
python {baseDir}/scripts/job_tracker.py add --company "Example Corp" --role "AI Engineer" --status applied --applied-on 2026-03-20 --next-follow-up 2026-03-27 --contact-name "Priya" --contact-email "priya@example.com"
```

### Update an application

```bash
python {baseDir}/scripts/job_tracker.py update --id 1 --status interview --note "Recruiter scheduled first-round screen" --next-follow-up 2026-03-30
```

### List applications

```bash
python {baseDir}/scripts/job_tracker.py list --status interview
```

### Show follow-ups due soon

```bash
python {baseDir}/scripts/job_tracker.py due --window 7
```

### Show a summary

```bash
python {baseDir}/scripts/job_tracker.py summary
```

## Safety Boundaries

- Never invent application updates that the user did not supply.
- Treat inferred dates as tentative unless explicitly confirmed.
- Keep recruiter notes factual and avoid speculative judgments.
- If a required field is missing, say so clearly instead of writing partial garbage into the database.
