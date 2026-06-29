---
name: job-search-belgrade
description: >
  Searches LinkedIn, Poslovi Infostud, and HelloWorld.rs for jobs matching
  your target roles. Scores each listing against your resume PDF (1-10 with
  justification) using your configured LLM. Results in chat, optional email
  digest, optional daily cron. No auto-applying. Cover letters on demand.

  Use when the user says:
  - "Run the job search"
  - "Find jobs for me" / "Search for jobs"
  - "Set up daily job search" / "Schedule the job search"
  - "Enable email for job results"
  - "Write a cover letter for [job title / company]"
  - "Generate a cover letter for [pasted job description]"
---

# Job Search — Serbia & Remote

## Overview

Three modes:

1. **Job Digest** — Scrape → extract resume → YOU score and output in chat
2. **Email** — Optional. After chat output, send HTML digest via SMTP
3. **Cover Letter** — On demand, YOU write it following strict human-voice rules

---

## File Locations

| File | Purpose |
|------|---------|
| `workspace/resume.pdf` | Resume PDF. User replaces to update CV. |
| `workspace/roles.txt` | Target job titles, one per line. |
| `workspace/config.json` | Search, email, and cron settings. |
| `data/seen_jobs.db` | SQLite — deduplication across runs. Auto-created. |
| `scripts/scrape.py` | Fetches jobs from LinkedIn, Infostud, HelloWorld.rs. |
| `scripts/extract_resume.py` | Extracts text from resume.pdf. Prints to stdout. |
| `scripts/mark_seen.py` | Marks shown jobs as seen. Run after output. |
| `scripts/send_email.py` | Sends HTML email digest. Only if email.enabled=true. |

---

## Running the Job Digest

### Step 1 — Scrape

```bash
python scripts/scrape.py
```

Writes new unseen jobs to `data/raw_jobs.json`.

### Step 2 — Extract resume

```bash
python scripts/extract_resume.py
```

Read the printed resume text carefully — you need it for scoring.

### Step 3 — YOU score each job

Read `data/raw_jobs.json`. For each job score the fit against the resume 1–10.

Scoring guide:
- 9–10: Exceptional. Meets nearly all requirements, strong stack + seniority match.
- 7–8:  Strong. Meets most requirements, minor gaps won't block candidacy.
- 5–6:  Moderate. Core match but notable gaps or a stretch.
- 3–4:  Weak. Some overlap but significant mismatches.
- 1–2:  Poor. Little alignment.

Be specific. Reference actual skills/experience from the resume against actual
requirements in the job. Use the tags field where descriptions are absent.
Only include jobs at or above `config.json → search.min_score_to_include`.

### Step 4 — Output in chat

Sort by score descending, grouped by source. Format each job as:

```
🟢 [9/10] Strong fit
   Senior .NET Developer
   Luxoft Serbia · Belgrade
   Tags: .NET, Azure, SQL
   🔗 https://...
   ↳ [your 2-3 sentence justification]
```

🟢 = score 8–10 · 🟡 = 6–7 · 🔴 = below 6

Top summary line: "Found X jobs — Y 🟢 strong · Z 🟡 good · W 🔴 moderate"

### Step 5 — Mark seen + optional email

Always run after outputting results:
```bash
python scripts/mark_seen.py
```

Then check config for email:
```bash
python scripts/send_email.py
```

If `email.enabled` is false in config.json, the email script prints "Email disabled"
and exits cleanly — no error, nothing to do.

If email is enabled, it sends the HTML digest automatically.

---

## Setting Up Daily Cron (Automation)

When the user says "set up daily job search" or "schedule this" or "run it every day at [time]":

1. Read `workspace/config.json` to get the preferred time and timezone.
   Default is 09:00 Europe/Belgrade unless the user specifies otherwise.

2. Update config.json to set `cron.enabled = true` and the user's preferred time.

3. Register the cron job with OpenClaw:

```bash
openclaw cron add \
  --name "Daily Job Search" \
  --cron "0 9 * * *" \
  --tz "Europe/Belgrade" \
  --session isolated \
  --message "Run the job search"
```

Adjust the hour (0 9 = 9am) to match the user's chosen time.

4. Confirm to the user: "Daily job search scheduled for 9:00 AM Belgrade time.
   Your OpenClaw gateway must be running for the schedule to fire."

To cancel: `openclaw cron list` to find the job ID, then `openclaw cron delete <id>`

---

## Enabling Email

When the user says "enable email" or "also send results by email":

1. Ask for: Gmail address, Gmail App Password (16-char, from myaccount.google.com/apppasswords),
   and recipient email (can be the same address).

2. Update `workspace/config.json`:
   - Set `email.enabled` to `true`
   - Fill in `smtp_user`, `smtp_pass`, `recipient`

3. Confirm: "Email enabled. Results will be sent to [address] after each job search."

Note: Gmail requires an App Password (not the regular login password).
Generate one at: myaccount.google.com/apppasswords

---

## Cover Letter (On Demand)

When the user asks for a cover letter for a specific job:

1. Run `python scripts/extract_resume.py` and read the output.
2. Use the job title, company, and any description the user provided.
3. Write the letter yourself following these rules exactly:

**Rules — non-negotiable:**
- Do NOT open with "I am writing to apply for..." or any variation
- No AI buzzwords: cut "leverage", "passionate", "dynamic", "synergy",
  "results-driven", "excited to", "I believe I would be a great fit"
- Reference SPECIFIC things from the resume against SPECIFIC requirements in the job
- Vary sentence rhythm — mix short sentences with longer ones, not uniform blocks
- 3–4 paragraphs, under 350 words total
- End with a direct, confident close — not "I look forward to hearing from you"
- Sign off as the user's name (check resume for name)
- Must sound like a thoughtful person wrote it after reading the JD carefully

Output the letter in chat. The user copies and edits it themselves.

---

## Important Rules

- Never auto-apply to any job under any circumstances.
- Never make external LLM API calls FROM SCRIPTS — scoring and cover letters are handled by YOU directly within this conversation session.
- If `workspace/resume.pdf` is missing: stop and tell the user.
- If `workspace/roles.txt` is empty: stop and tell the user.
- Email is always optional — skill works fully without it.
