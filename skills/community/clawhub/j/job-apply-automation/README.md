# job-email-apply

Automated job application assistant for OpenClaw. Searches for roles, drafts personalised emails, sends via Gmail, and tracks everything.

---

## Features

- **Multi-source search** — LinkedIn, Indeed, Glassdoor, Wellfound, Agentur für Arbeit, direct URLs
- **Smart scoring** — Filters jobs by relevance before applying
- **Email templates** — Cold, startup, referral — all tailored to each role
- **Gmail integration** — Sends from your dedicated job-hunting inbox
- **JSON tracker** — Every application logged with full history
- **Approval gate** — Every email requires your explicit confirmation before sending (no auto-send)
- **Optional digests** — Redacted WhatsApp summary of applications (only if you explicitly enable this feature)

---

## Privacy & Data Handling

**⚠️ Important: This skill processes sensitive personal data. Please review before installing.**

### Data Collected & Stored Locally
- Your CV, contact information, phone number, LinkedIn profile
- Job preferences (roles, locations, salary expectations)
- Application history (companies, roles, dates, status, recruiter emails)
- Interview details (dates, times, links)

### Data Sent to Third Parties
- **Job boards** (LinkedIn, Indeed, Glassdoor, Wellfound): Browsing job listings
- **Gmail SMTP**: Application emails with your CV attached
- **Recruiter inboxes**: Application emails containing your contact details
- **WhatsApp** (optional): Redacted job-application summary digests (only if explicitly enabled)

### Data Retention
- `Applications.json` retains active applications for 180 days
- Old entries are archived to `applications_archive.json`
- No automatic deletion — you control your data

### Your Control
- Every email requires explicit approval before sending
- You can disable WhatsApp notifications at any time
- You can delete all data by removing the skill directory and `Applications.json`
- No data is sent to the skill developer or any external analytics service

---

## Prerequisites

- OpenClaw running (WhatsApp connection optional — only needed for digests)
- A **dedicated Gmail account** for job applications
- Gmail **App Password** (not your main password)

---

## Setup

### 1. Create job-profile.md

Copy `references/job-profile.md` to `references/JOB-PROFILE.md` and fill in your real details:

```bash
cp references/job-profile.md references/JOB-PROFILE.md
nano references/JOB-PROFILE.md
```

Required fields:
- Name, emails, phone, LinkedIn, location
- `Resume file` — name of your CV file in `references/`
- Your skills, background, and projects
- Target roles, locations, and job type

### 2. Add your CV

Drop your CV PDF into `references/`. Match the filename to `Resume file` in JOB-PROFILE.md.

### 3. Review platform notes

Edit `references/platform-notes.md`:
- Add your target companies to `TARGET COMPANIES`
- Add companies to skip to `EXCLUDE LIST`

---

## Usage

Message your assistant with explicit job-email-apply commands:

```
job-email-apply: search for full-stack jobs in Berlin
job-email-apply: draft application for [paste job URL]
job-email-apply: show tracker
job-email-apply: update Stripe to interviewed
job-email-apply: check inbox for replies
```

**Note:** This skill only activates with explicit `job-email-apply` prefix or `use job-email-apply to` phrasing. Generic requests like "find jobs" or "show tracker" will not activate this skill unless explicitly prefixed.

### Application flow

1. Agent finds a match → drafts email (no sending yet)
2. You review and approve the draft
3. Agent sends only after your explicit "send" command
4. Updates tracker with status
5. If the user has explicitly enabled notifications, sends a redacted summary digest.

---

## Tracker

`Applications.json` is your source of truth. The agent updates it after every session.

### Status values

| Status | Meaning |
|---|---|
| `APPLIED` | Email sent, awaiting response |
| `RESPONDED` | Recruiter replied with interest |
| `INTERVIEW_SCHEDULED` | Interview date confirmed |
| `INTERVIEW_DONE` | Interview completed |
| `OFFER` | Offer received |
| `REJECTED` | Application declined |
| `WITHDRAWN` | You withdrew |
| `EMAIL_NOT_FOUND` | Couldn't find application email |
| `NEEDS_REVIEW` | Reply needs your attention |

### Dedup rule

No re-applying to the same company within 60 days unless your last application was REJECTED.

---

## Customising Templates

Edit `references/email-templates.md` to change how your emails look.

Each template uses `[BRACKETED]` placeholders — the agent fills these in per-application. Do not remove the brackets.

---

## Troubleshooting

**"App Password not working"**
→ Make sure 2-Step Verification is ON in your Google Account, then generate a fresh App Password.

**"Email won't send"**
→ Check that `smtp.gmail.com:587` is not blocked on your network.

**"CV not attaching"**
→ Verify the filename in JOB-PROFILE.md matches the actual file in `references/` exactly.

**"Applying to the wrong jobs"**
→ Adjust your `target_roles` and `target_locations` in JOB-PROFILE.md, or raise/lower the scoring threshold in SKILL.md.

---

## Uninstall

To remove this skill, delete the following files and directory manually:

1. The skill directory itself
2. `references/CONFIG.md` (contains your credentials — delete securely)
3. `Applications.json` (your job-application history)
4. Any other files you created in `references/`

Ensure no personal data or credentials remain after removal.
