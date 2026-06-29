# job-search-belgrade — OpenClaw Skill

Searches LinkedIn, Poslovi Infostud, and HelloWorld.rs for jobs matching
your target roles. Your OpenClaw agent scores each listing against your
resume PDF using its own reasoning — no extra API keys needed.

Optional: daily cron scheduling and HTML email digest.
Cover letters on demand. Never auto-applies.

---

## Quick Setup

### 1. Install
```bash
mkdir -p ~/.openclaw/skills
cp -r job-search-belgrade ~/.openclaw/skills/
```

### 2. Add your resume PDF
```
~/.openclaw/skills/job-search-belgrade/workspace/resume.pdf
```
Replace this file whenever your CV changes.

### 3. Install the PDF library
```bash
pip install pypdf
```

### 4. Edit your target roles
```
~/.openclaw/skills/job-search-belgrade/workspace/roles.txt
```
One job title per line.

---

## Usage

**Run a search:**
> "Run the job search"

**Schedule daily:**
> "Set up daily job search at 9am"

**Enable email digest:**
> "Enable email for job results"
Then follow the agent's prompts for your Gmail App Password.

**Get a cover letter:**
> "Write me a cover letter for Senior .NET Developer at Luxoft"

---

## Optional: Email Setup

Edit `workspace/config.json`:
```json
"email": {
  "enabled": true,
  "smtp_user": "you@gmail.com",
  "smtp_pass": "xxxx xxxx xxxx xxxx",
  "recipient": "you@gmail.com"
}
```

Gmail App Password: myaccount.google.com/apppasswords

---

## Settings

| Setting | File | Key |
|---------|------|-----|
| Target roles | `workspace/roles.txt` | — |
| Locations | `workspace/config.json` | `search.locations` |
| Min score to show | `workspace/config.json` | `search.min_score_to_include` |
| Email on/off | `workspace/config.json` | `email.enabled` |
| Cron time | `workspace/config.json` | `cron.time` |

---

## File Structure

```
job-search-belgrade/
├── SKILL.md
├── README.md
├── workspace/
│   ├── resume.pdf          ← DROP YOUR CV HERE
│   ├── roles.txt           ← target job titles
│   └── config.json         ← search + email + cron settings
├── scripts/
│   ├── scrape.py           ← LinkedIn + Infostud + HelloWorld.rs
│   ├── extract_resume.py   ← PDF text extraction
│   ├── mark_seen.py        ← deduplication
│   └── send_email.py       ← optional HTML email digest
└── data/                   ← auto-created at runtime
    ├── raw_jobs.json
    ├── scored_jobs.json
    └── seen_jobs.db
```
