# job-email-apply

Automated job application assistant for OpenClaw. Searches for roles, drafts personalised emails, sends via Gmail, and tracks everything.

---

## Features

- **Multi-source search** — LinkedIn, Indeed, Glassdoor, Wellfound, Agentur für Arbeit, direct URLs
- **Smart scoring** — Filters jobs by relevance before applying
- **Email templates** — Cold, startup, referral — all tailored to each role
- **Gmail integration** — Sends from your dedicated job-hunting inbox
- **JSON tracker** — Every application logged with full history
- **Review mode** — First 3 applications go to you for approval
- **Auto mode** — After approval, emails send immediately
- **Daily digests** — WhatsApp summary of all sent applications

---

## Prerequisites

- OpenClaw running with WhatsApp connected
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

Message your assistant:

```
find me full-stack jobs in Berlin
apply to this: [paste job URL]
show tracker
update Stripe to interviewed
weekly report
```

### Application flow

**Review mode (first 3):**
1. Agent finds a match → drafts email → sends preview to WhatsApp
2. You edit or approve
3. Agent sends → updates tracker

**Auto mode (after 3):**
1. Agent finds match → drafts → sends immediately
2. Updates tracker
3. Sends you a daily digest

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

Remove the skill directory:
```bash
rm -rf ~/.openclaw/workspace/skills/job-email-apply
```
