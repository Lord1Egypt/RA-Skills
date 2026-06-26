---
name: job-hunter
description: "Build and deploy an automated job hunting system with Telegram bot. Scrapes LinkedIn jobs, scores them by match percentage, sends notifications with apply buttons, and generates tailored CVs. Use when: setting up job search automation, building a job-matching bot, creating a Telegram-based job alert system, helping someone find a job automatically. Triggers: 'job search bot', 'automated job hunting', 'find jobs for', 'job alert system', 'build job bot'."
---

# Job Hunter - Automated Job Search System

Build a complete job hunting system: LinkedIn scraper, match scorer, and Telegram bot with inline buttons.

## What This System Does

1. Scrapes real jobs from LinkedIn (public guest API, no login needed)
2. Scores each job 0-100% based on candidate profile (title, skills, experience, location)
3. Sends matching jobs to Telegram with action buttons (details, apply, remove)
4. Provides a clean foundation you can extend with CV generation later if needed

## Setup Flow

### 1. Gather Candidate Profile

Ask the user for:
- **Target roles** (e.g. data analyst, BI developer, frontend developer)
- **Core skills** (e.g. SQL, Python, React, Power BI)
- **Bonus skills** (nice-to-have)
- **Max years of experience** they qualify for
- **Preferred location** and metro area cities
- **Contact info** (name, email, phone, LinkedIn URL)
- **Work experience** (companies, roles, dates, bullet points)
- **Education** (degree, institution, year)

### 2. Create Telegram Bot

Guide the user:
1. Open Telegram, search for @BotFather
2. Send `/newbot`, choose a name and username
3. Copy the bot token
4. Get their Telegram user ID (send a message to @userinfobot)
5. Optionally add more authorized users (e.g. the job seeker)

### 3. Deploy the System

Create a project directory and deploy these scripts (from `scripts/`):

```
job-hunter/
├── config.json          # Bot token, user IDs, candidate profile
├── jobs.db              # SQLite database (auto-created)
├── scorer.py            # Match scoring engine
├── linkedin_scraper.py  # LinkedIn job scraper
├── bot.py               # Telegram bot with inline buttons
└── notify_new_jobs.py   # Send new matches to Telegram
```

#### config.json Structure

```json
{
  "telegram_bot_token": "TOKEN_FROM_BOTFATHER",
  "telegram_user_id": 123456789,
  "authorized_users": [123456789],
  "notify_users": [123456789],
  "candidate": {
    "name": "Full Name",
    "email": "email@example.com",
    "phone": "054-1234567",
    "linkedin": "linkedin.com/in/username",
    "location": "Tel Aviv, Israel",
    "target_titles": ["data analyst", "bi developer"],
    "good_titles": ["business analyst"],
    "core_skills": ["sql", "python", "power bi"],
    "bonus_skills": ["etl", "dax", "pandas"],
    "max_years": 2,
    "preferred_locations": ["tel aviv", "herzliya", "ramat gan"],
    "metro_locations": ["petah tikva", "rishon lezion"]
  }
}
```

### 4. Customize Scripts

After copying scripts from `scripts/`, customize:
- `scorer.py` - Update PROFILE dict with candidate's profile from config.json
- `linkedin_scraper.py` - Update DEFAULT_QUERIES with relevant search terms
- `bot.py` - Should work with just config.json changes
- `notify_new_jobs.py` - Verify notification flow and recipients

### 5. Install Dependencies

Install Python dependencies required by the included scripts. At minimum, verify the libraries imported by the scraper and bot are available in your environment.

### 6. Initialize Database

The database auto-creates on first run. Schema:

```sql
CREATE TABLE jobs (
    job_id TEXT PRIMARY KEY,
    title TEXT, company TEXT, location TEXT,
    url TEXT, career_url TEXT,
    description TEXT, requirements TEXT,
    required_years INTEGER,
    published_date TEXT, found_date TEXT,
    status TEXT DEFAULT 'new'
);
```

### 7. Start the Bot

```bash
nohup python3 -u bot.py > bot.log 2>&1 &
```

### 8. Set Up Daily Search (Cron)

```bash
# Run daily job search + notify at 9 AM
0 9 * * * cd /path/to/job-hunter && python3 linkedin_scraper.py && python3 notify_new_jobs.py
```

Or use OpenClaw cron:
```
openclaw cron add --name daily-job-search --schedule "0 9 * * *" --prompt "Run job search and notify"
```

## Bot Commands

| Command | What it does |
|---------|-------------|
| `/top` | Show top jobs (score >= 60%) |
| `/jobs` | List all jobs with scores |
| `/search` | Trigger new LinkedIn search |
| `/stats` | Show statistics |
| `/applied` | Show applied jobs |
| `/help` | Show commands |

## Scoring Weights

| Factor | Points | Logic |
|--------|--------|-------|
| Title match | 0-30 | Perfect match = 30, partial = 15 |
| Skills match | 0-30 | Core skills = 5 each (max 20), bonus = 2 each (max 10) |
| Experience | 0-40 | 0yr = 40, 1yr = 30, 2yr = 10, 3+ = -20 |
| Location | 0-25 | Preferred = 25, metro = 15, country = 5 |
| Junior keywords | 0-10 | Entry-level indicators |

Thresholds: 🟢 >= 70% apply | 🟡 >= 50% review | 🔴 < 50% skip

## Troubleshooting

- **Bot not responding**: Check only ONE instance is running (`ps aux | grep bot.py`)
- **409 Conflict**: Multiple bot instances. Kill all, restart one.
- **No jobs found**: Check search queries match real LinkedIn job titles
- **Scoring too high/low**: Adjust weights in scorer.py
