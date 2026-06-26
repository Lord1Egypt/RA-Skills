---
name: ofek-galim
description: Check, monitor, and summarize student homework/tasks from Webtop (SmartSchool), Galim Pro, and Ofek. Use when the user asks to inspect homework, pending tasks, submission status, due items, or daily school updates for children across Webtop / Galim / Ofek, or when building/maintaining automation that sends alerts about new tasks.
---

# Webtop / Galim / Ofek

Use this skill to work with Webtop / SmartSchool, Galim Pro, and Ofek student task portals.

## Status

Both portals are working ✅

- **Ofek** (`students.myofek.cet.ac.il`) — working via Ministry of Education SSO
- **Galim Pro** (`lms.galim.org.il`) — working via Ministry of Education SSO

## Quick start

```bash
# Webtop only
python3 /root/.openclaw/workspace/skills/webtop-galim/scripts/webtop_fetch_summary.py

# Galim only
python3 /root/.openclaw/workspace/skills/webtop-galim/scripts/galim_fetch_tasks.py

# Ofek only
python3 /root/.openclaw/workspace/skills/webtop-galim/scripts/fetch_tasks.py

# Unified report (Webtop + Galim + Ofek)
python3 /root/.openclaw/workspace/skills/webtop-galim/scripts/unified_report.py

# Expanded report for WhatsApp / review
python3 /root/.openclaw/workspace/skills/webtop-galim/scripts/expanded_report.py --days 30 --limit 5

# Sync Galim due dates to calendar
python3 /root/.openclaw/workspace/skills/webtop-galim/scripts/sync_galim_calendar.py --days 30

# JSON output
python3 /root/.openclaw/workspace/skills/webtop-galim/scripts/fetch_tasks.py --json
python3 /root/.openclaw/workspace/skills/webtop-galim/scripts/galim_fetch_tasks.py --json
```

## Credentials

Stored in `/root/.openclaw/workspace/.env/galim.env`:

```
GALIM_USERNAME_CHILD1=...   GALIM_PASSWORD_CHILD1=...
GALIM_USERNAME_CHILD2=...   GALIM_PASSWORD_CHILD2=...
OFEK_USERNAME_CHILD1=...    OFEK_PASSWORD_CHILD1=...
OFEK_USERNAME_CHILD2=...    OFEK_PASSWORD_CHILD2=...
```

Credentials are Ministry of Education student IDs and passwords.
Same credentials work for both portals.

## Important: Ofek URL

The correct URL for Ofek is **`students.myofek.cet.ac.il`** (not `myofek.cet.ac.il`).
`myofek.cet.ac.il` blocks datacenter IPs (503). `students.myofek.cet.ac.il` does not.

## Login flow

**Ofek:**
1. `https://students.myofek.cet.ac.il/he`
2. Click "התחברות משרד החינוך"
3. Redirects to `lgn.edu.gov.il` SSO (EduCombinedAuthUidPwd)
4. Fill `#userName` + `#password`, click "כניסה"
5. Redirects back to `students.myofek.cet.ac.il/he` with full session

**Galim Pro:**
1. `https://userdata.galim.org.il/login_idm?request_uri=https%3A%2F%2Fpro.galim.org.il%2F%3Flang%3Dhe`
2. Fill `#userName` + `#password`, click "כניסה"
3. Navigate to `https://lms.galim.org.il/personal?lang=he`

## Task counters extracted

**Ofek** (from page body text):
- `לביצוע (N)` → open_count
- `הוחזר לתיקון (N)` → fix_count
- `מחכה לבדיקת מורה (N)` → waiting_count
- `בוצע ונבדק (N)` → checked_count
- Visible activity extraction when present:
  - title
  - subject
  - teacher
  - due date
  - sections such as urgent / overdue activities

**Galim** (parsed from table text):
- Per task: assigned_at, title, task_type, subject, due_at, overdue

## Suggested output format

```
📚 משימות תלמידים

👤 Child 1
גלים: 13 משימות | אופק: לביצוע 9, לתיקון 1

👤 Child 2
גלים: 1 משימה ⚠️ | אופק: לביצוע 27
```

## Automation

Configured daily flow:

- `06:15` — `scripts/sync_galim_calendar.py --days 30`
  - creates family-calendar events for Galim tasks with clear due dates
  - reminders: 1 day before + 3 hours before
- `06:20` — `scripts/expanded_report.py --days 30 --limit 5`
  - sends a WhatsApp update to the family updates group
  - covers Ofek + Galim + Webtop

Notes:
- Calendar target is configurable via `OFEK_GALIM_CALENDAR_ID`
- WhatsApp target group is configurable via `OFEK_GALIM_WHATSAPP_GROUP`
- Child credentials should be provided via env vars / `OFEK_KIDS_JSON`, not stored in the skill
- Ofek currently provides counters plus visible activity details parsed from page text (for example overdue / urgent visible items); Galim still provides the richer structured task list with due dates.

## Files

- `scripts/webtop_fetch_summary.py` — Webtop / SmartSchool fetcher
- `scripts/galim_fetch_tasks.py` — Galim Pro fetcher (Playwright, LMS)
- `scripts/fetch_tasks.py` — Ofek fetcher (Playwright, students portal)
- `scripts/unified_report.py` — runs Webtop + Galim + Ofek and prints a combined Hebrew report
- `scripts/expanded_report.py` — richer report with task titles and due dates
- `scripts/sync_galim_calendar.py` — syncs Galim tasks with due dates into the family Google Calendar
- `scripts/auto_update_flow.py` — helper for stateful daily automation flow
- `scripts/install.sh` — creates a local env template and prints setup/test steps
- `scripts/galim_probe.py` — legacy Selenium probe (kept for reference)
- `scripts/webtop_fetch_summary.py` — Webtop/SmartSchool fetcher
- `references/ofek-bot-notes.md` — notes from reference repo and migration history
- `references/ofek-investigation-summary.md` — detailed Ofek debugging notes and findings
- `references/env-example.md` — credentials file format
