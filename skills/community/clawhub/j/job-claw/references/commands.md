# JobClaw Commands Reference

Quick reference for all agent commands and workflow patterns.

## Setup & First Run

```bash
# Interactive setup wizard (recommended)
python3 scripts/setup.py

# Non-interactive (uses defaults, for automation)
python3 scripts/setup.py --non-interactive

# Verify config
cat ~/Documents/JobClaw/config.json
```

## Daily Search

```bash
# Full search (coding + non-coding)
python3 scripts/search.py --mode all

# Coding roles only (ML engineer, data scientist, etc.)
python3 scripts/search.py --mode coding

# Non-coding roles only (research, healthcare, consulting)
python3 scripts/search.py --mode noncoding

# Preview without writing (dry run)
python3 scripts/search.py --mode all --dry-run

# Custom keyword + location
python3 scripts/search.py --mode coding --keyword "LLM engineer" --location "Berlin, DE"

# Run the full daily script (search + notify)
./scripts/run_daily.sh
./scripts/run_daily.sh --mode coding
./scripts/run_daily.sh --dry-run
```

## Tracker Management

```bash
# Summary statistics
python3 scripts/tracker.py stats

# Top 10 jobs by score
python3 scripts/tracker.py top

# View the CSV directly
cat ~/Documents/JobClaw/data/jobs.csv

# Open in spreadsheet app (macOS)
open ~/Documents/JobClaw/data/jobs.csv

# Open in spreadsheet app (Linux)
libreoffice ~/Documents/JobClaw/data/jobs.csv
```

## Archive Management

```bash
# Preview what would be archived (no changes)
python3 scripts/archiver.py

# Apply — moves expired jobs to jobs_archive.csv
python3 scripts/archiver.py --commit

# Stats
python3 scripts/archiver.py --stats

# Restore a job by company/role/URL fragment
python3 scripts/archiver.py --restore "Google"
python3 scripts/archiver.py --restore "Research Scientist"
```

Archive rules:
| Rule | Trigger | Reason tag |
|------|---------|------------|
| 30-day inactivity | status=New/Interested, date_found 30+ days ago | `expired_30d` |
| Auto-rejected | status=Rejected/Passed, 60+ days ago | `auto_rejected` |
| Dead URL | non-LinkedIn URL returns 404/dead phrase | `url_dead` |

LinkedIn URLs are **skipped** for URL checking (always returns inconclusive).

## Notifications

```bash
# Test notification (sends a sample message)
python3 scripts/notify.py --test
```

## OpenClaw Integration (Chat Commands)

When using JobClaw as an OpenClaw skill, these natural language commands work:

| Command | Action |
|---------|--------|
| `run job search` | Runs search for all modes |
| `run coding job search` | Coding roles only |
| `run noncoding job search` | Non-coding roles only |
| `/newjob <url>` | Analyse and add a specific job URL |
| `show job stats` | Print tracker summary |
| `top jobs` | List top 10 by match score |
| `set up daily search` | Configure OpenClaw cron for 7:30 AM |
| `search for "LLM engineer" in Berlin` | Custom keyword/location search |

## Config.json Structure

```json
{
  "user": {
    "name": "Your Name",
    "background": "Brief description for scoring context",
    "target_roles": ["ML Engineer", "Research Scientist"],
    "skill_keywords": ["pytorch", "transformers", "rlhf"],
    "cv_path": "/path/to/cv.pdf"
  },
  "search": {
    "coding_keywords": [...],
    "noncoding_keywords": [...],
    "locations": ["London, UK", "Cambridge, UK"],
    "min_score": 70,
    "hours_old": 48,
    "results_per_search": 10,
    "platforms": ["linkedin", "indeed"]
  },
  "notifications": {
    "enabled": true,
    "telegram_bot_token": "...",
    "telegram_chat_id": "...",
    "openclaw_channel": "telegram",
    "openclaw_account": "your_account_id"
  },
  "schedule": {
    "daily_time": "07:30",
    "weekdays_only": true,
    "timezone": "Europe/London"
  },
  "csv_filename": "jobs.csv",
  "version": "1.0"
}
```

## CSV Columns

| Column | Description |
|--------|-------------|
| `company` | Company name |
| `role` | Job title |
| `location` | City, country |
| `work_mode` | Remote / Hybrid / On-site / Unknown |
| `salary` | Salary if listed |
| `job_url` | Direct link to job posting |
| `date_posted` | When the job was posted (YYYY-MM-DD) |
| `date_found` | When JobClaw found it (YYYY-MM-DD) |
| `source` | `Daily Search` / `Manual` / `Agency` |
| `match_score` | 0-100 relevance score |
| `ml_direction` | e.g. NLP/LLM, Healthcare AI |
| `seniority` | Junior / Mid / Senior / Lead |
| `interview_type` | e.g. Research Talk, No Leetcode |
| `status` | New / Applied / Interview / Offer / Rejected |
| `date_applied` | YYYY-MM-DD (fill manually) |
| `referral` | Name of referral contact |
| `recruiter_contact` | Recruiter name/email |
| `followup_date` | When to follow up (YYYY-MM-DD) |
| `priority` | High / Medium / Low |
| `notes` | Free text, source platform, description excerpt |
| `job_category` | `coding` / `noncoding` / `unknown` |

## Troubleshooting

**No results found:**
- Lower `min_score` in config (try 60)
- Increase `hours_old` (try 72)
- Check `platforms` list in config

**python-jobspy import error:**
```bash
pip install python-jobspy --break-system-packages
# or in a venv:
python3 -m venv .venv && source .venv/bin/activate && pip install python-jobspy
```


**Notifications not working:**
- Check `notifications.enabled: true` in config
- For Telegram Bot: verify `telegram_bot_token` and `telegram_chat_id`
- Test: `python3 scripts/notify.py --test`
