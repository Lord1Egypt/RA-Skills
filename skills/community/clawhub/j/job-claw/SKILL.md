---
name: jobclaw
description: |
  AI-powered automated job search skill. Searches LinkedIn and Indeed daily,
  scores jobs against the user's profile, and saves results to a local CSV.
  
  Use when:
  - User says "run job search", "find jobs", "search for jobs", "start daily job search"
  - User types "/newjob URL" to analyse a specific job posting
  - User asks to set up automated daily job searching
  - User asks to show job stats, top matches, or update a job status
  - User asks to configure or set up job search preferences
  - User asks for "job tracker", "JobClaw", or "job search automation"
  
  First-time setup: guide the user through conversational onboarding (see Conversational Setup below).
  After setup: search.py handles all searching; run_daily.sh for the full automated pipeline.
  Install via ClawHub: clawhub install job-claw
---

# JobClaw

AI-powered job search automation. Searches multiple platforms, scores results against the user's profile, and maintains a local CSV tracker. No backend server or web dashboard required.

## Quick Reference

See `references/commands.md` for all CLI commands and chat commands.
See `references/screening_guide.md` for scoring logic and interview type classification.
See `references/keywords.md` for keyword lists and search strategy.

---

## Conversational Setup (First Run)

When a user first activates JobClaw, **do not run setup.py directly**. Instead, guide them through a natural conversation to collect all config values, then write `config.json` yourself at the end.

Check first:
```bash
test -f ~/Documents/JobClaw/config.json && echo "exists" || echo "not found"
```

If config doesn't exist, start the conversational flow below. Ask **one topic at a time** — never dump all questions at once.

### Conversation Flow

**Step 1 — Greeting**
```
Hey! Let's get JobClaw set up. I'll ask you a few quick questions and have you searching for jobs in minutes.

First — what's your name?
```

**Step 2 — Background** (after they give name)
```
Nice to meet you, [name]! 

Tell me a bit about your background — what kind of work do you do or want to do? 
(e.g. "software engineer with Python/ML experience", "data scientist at a fintech", "researcher in NLP")

This helps me score jobs that actually fit you.
```

**Step 3 — Skills** (after background)
```
Got it. What are your key technical skills or tools? List whatever feels most relevant — I'll use these to boost scoring for matching jobs.

(e.g. pytorch, python, sql, docker, react, java — whatever fits you)
```

**Step 4 — Target roles** (after skills)
```
What kinds of roles are you looking for? You can be specific or broad.

(e.g. "ML engineer or data scientist", "backend engineer", "product manager", "research scientist")
```

**Step 5 — Locations** (after roles)
```
Where are you looking? List cities or regions — I'll search each one separately.

(e.g. "London, UK", "Remote", "Berlin, DE and Amsterdam, NL", "New York, NY")
```

**Step 6 — Search preferences** (after locations)
```
A couple of quick settings:

- How recently posted should jobs be? (default: 48 hours)
- Minimum match score to save a job? (default: 70 out of 100 — higher = fewer but better results)

Hit enter to keep defaults, or tell me what you'd prefer.
```

**Step 7 — Daily schedule** (after preferences)
```
Do you want a daily automated search? I can run it every weekday morning and notify you of new matches.

If yes — what time? (e.g. "7:30am", default is 07:30)
And your timezone? (e.g. Europe/London, America/New_York)
```

**Step 8 — Notifications** (after schedule)
```
Last one — how do you want to be notified when new jobs are found?

1. Telegram Bot (you'll need a bot token from @BotFather)
2. Through OpenClaw (if you're using another channel like Signal or WhatsApp)
3. No notifications — I'll just save to CSV

Which works for you?
```

For option 1, ask for: bot token + chat ID (tell them to message @userinfobot to get their chat ID).
For option 2, ask for: channel name (e.g. telegram) and their chat/user ID.
For option 3, set `notifications.enabled: false`.

**Step 9 — Write config and confirm**

Once all answers collected, write `~/Documents/JobClaw/config.json` using the template from `assets/config.example.json`, populated with the user's answers. Then confirm:

```
All set! Here's your config summary:

👤 Name: [name]
🔍 Skills: [skills]
📍 Locations: [locations]
⏰ Daily search: [time], [timezone]
🔔 Notifications: [method]

Want me to run your first search now? (takes ~1-2 minutes)
```

If they say yes, run: `python3 <skill_dir>/scripts/search.py --mode all`

---

## Daily Automated Search Workflow

Triggered by cron or the user saying "run job search":

```bash
# Reads: ~/Documents/JobClaw/config.json
# Writes: ~/Documents/JobClaw/data/jobs.csv
# Logs:   ~/Documents/JobClaw/logs/daily.log

./run_daily.sh              # both coding + noncoding
./run_daily.sh --mode coding
./run_daily.sh --mode noncoding
```

Or directly:
```bash
python3 scripts/search.py --mode all
python3 scripts/search.py --mode coding --dry-run
```

The search pipeline:
1. Reads `config.json` for keywords, locations, min_score, platforms
2. Searches LinkedIn + Indeed via python-jobspy
3. Scores each job (keyword-based, 0-100) using `user.skill_keywords` as boosters
4. Filters by `min_score` (default 70), deduplicates by company+role and URL
5. Appends qualified jobs to `data/jobs.csv`
6. Sends notification via OpenClaw/Telegram (if configured)

---

## /newjob Command

When user says `/newjob <url>`:

1. **Fetch** the JD: `browser(action="navigate", url=<url>)` then `browser(action="snapshot")`
2. **Analyse** against `references/screening_guide.md`:
   - Company, Role, Location, Work Mode, Salary
   - Match Score 0-100 with reasoning
   - Interview Type estimate
   - ML Direction, Seniority
3. **Add to CSV**:
   ```python
   import sys; sys.path.insert(0, "<skill_dir>/scripts")
   from tracker import JobTracker
   t = JobTracker()
   t.add_jobs([{...job dict...}])
   ```
4. **Reply** with score, match reasons, interview type, apply angle

---

## Archive Management

When user says "archive expired jobs", "clean up old jobs", "auto-archive":

```bash
# Dry-run (see what would be archived, no changes)
python3 scripts/archiver.py

# Apply archiving
python3 scripts/archiver.py --commit

# View archive stats
python3 scripts/archiver.py --stats

# Restore a job (by company name, role, or URL fragment)
python3 scripts/archiver.py --restore "DeepMind"
```

Archive rules (same as the web dashboard):
- `expired_30d` — status New/Interested with no update for 30+ days
- `auto_rejected` — status Rejected/Passed for 60+ days
- `url_dead` — non-LinkedIn URL returns 404/410 or contains "job has expired" etc.

Archived jobs move from `data/jobs.csv` → `data/jobs_archive.csv`.
Auto-archive runs automatically at the end of every daily search (`run_daily.sh`).

## Showing Stats

When user asks "show job stats", "how many jobs", "top jobs":

```python
import sys; sys.path.insert(0, "<skill_dir>/scripts")
from tracker import JobTracker
t = JobTracker()
t.print_summary()
top = t.top_jobs(10)
```

---

## Setting Up Daily Automation (OpenClaw Cron)

1. Confirm daily time and timezone from `config.json`
2. Register an OpenClaw cron job:
   ```
   Schedule: daily at <config.schedule.daily_time>, weekdays only
   Command: JOBCLAW_DIR=~/Documents/JobClaw <skill_dir>/scripts/run_daily.sh
   ```

---

## Updating Config Mid-Conversation

When user says things like "also search in Berlin", "add React to my skills", "change time to 8am":

1. Load `~/Documents/JobClaw/config.json`
2. Edit the relevant field
3. Save back
4. Confirm the change: "Done — I've added Berlin, DE to your search locations."

---

## Environment

- **Config**: `~/Documents/JobClaw/config.json` (override with `JOBCLAW_DIR` env var)
- **CSV data**: `~/Documents/JobClaw/data/jobs.csv`
- **Logs**: `~/Documents/JobClaw/logs/daily.log`
- **Dependency**: `python-jobspy` — install with `pip install python-jobspy`
