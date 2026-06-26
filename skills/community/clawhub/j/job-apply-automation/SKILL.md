---
name: job-email-apply
description: "Automated job application assistant. Searches for jobs on LinkedIn, Indeed, Glassdoor, Wellfound, Agentur für Arbeit, and direct URLs, composes personalised application emails with CV attached, sends via Gmail SMTP, and maintains a JSON tracker. Use when: apply to jobs, find jobs, job search, check tracker, update application, send application email, or check inbox for job replies."
---

# job-email-apply

Automated job application workflow — search, draft, send, track.

## How It Works

1. **Search** — Scans job boards for matching roles
2. **Score** — Filters by relevance threshold (0.75)
3. **Draft** — Composes a tailored email using templates
4. **Send** — Delivers via Gmail SMTP with CV attached
5. **Track** — Logs every application in `Applications.json`

**Review Mode:** First 3 applications go to you for approval before sending.
**Auto Mode:** After that, emails send immediately.

---

## File Map

```
job-email-apply/
├── SKILL.md
├── README.md
├── Applications.json         ← tracker database (auto-created on first run)
└── references/
    ├── job-profile.md         ← YOUR profile & personal data (fill this in)
    ├── email-templates.md     ← email templates
    ├── tracker-commands.md    ← tracker schema & operations
    └── platform-notes.md      ← platform tips & target companies
```

---

## Setup (First Run)

1. Copy `references/config.md` → `references/CONFIG.md` and fill in your details
2. Drop your CV PDF into `references/` — update `config.md` with the filename
3. Review `references/platform-notes.md` and add your target companies
4. See `README.md` for full setup instructions

---

## Core Workflow

### Agent Instructions

When invoked, follow this sequence:

**STEP 1 — Load context**
Read these files before anything else:
- `references/email-templates.md`
- `references/tracker-commands.md`
- `references/platform-notes.md`
- `references/CONFIG.md`
- `Applications.json`

**STEP 2 — Search**
Check: LinkedIn, Indeed, Glassdoor, Wellfound, Agentur für Arbeit, direct URLs.
Score each listing. Discard below 0.75. Dedup against Applications.json.

**STEP 3 — Per listing**
1. Find application email
2. Extract key skills from JD
3. Select template (cold / startup / referral)
4. Compose tailored email (< 200 words)
5. Attach CV from `references/`
6. Send via Gmail SMTP → to application email, BCC personal email
7. Log to Applications.json with status APPLIED

**STEP 4 — Check inbox**
Process replies: interview requests, rejections, spam. Update statuses. Alert on anything needing attention.

**STEP 5 — Session summary**
Output summary. Log to Applications.json session_log.

---

## Scoring Criteria (0.0–1.0)

| Factor | Weight |
|---|---|
| Role title match | 0.25 |
| Stack overlap | 0.25 |
| Location match | 0.20 |
| Seniority fit | 0.15 |
| Salary in range | 0.10 |
| Company quality | 0.05 |

Hard disqualifiers: Junior/Graduate title, 10+ years required, on-site outside targets, company on exclude list.

---

## Constraints

- Max 15 applications per session
- No re-apply within 60 days (unless previous was REJECTED)
- CV must attach — abort and log EMAIL_SEND_FAILED if it fails
- Never fabricate experience or skills
- Review mode: first 3 require user approval before sending
