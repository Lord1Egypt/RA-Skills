---
name: job-hunter
description: LinkedIn job search assistant that scrapes listings, filters by technologies and countries, and scores matches with AI. Use when the user wants to find jobs, search for job openings, look for work, job hunt, or find career opportunities. Triggers on phrases like "find jobs", "job search", "looking for work", "job openings", "search LinkedIn", "remote jobs", "buscar trabajo", "ofertas de trabajo", "ofertas de empleo", "empleo remoto", "vacantes", "buscar empleo", "trabajo remoto", "career opportunities", "hiring", "job listings".
metadata:
  { "openclaw": { "requires": { "bins": ["python3"], "packages": { "pip": ["httpx", "selectolax", "google-genai"] } }, "emoji": "🔍" } }
---

# Job Hunter

AI-powered LinkedIn job search assistant that scrapes real-time listings, filters by technology and location, and scores each match — delivered through chat.

## Setup

Before first use, the user needs a **Google Gemini API key** for AI scoring. Ask for it and save it:

```bash
python3 scripts/job_hunter.py setkey "USER_GEMINI_KEY_HERE"
```

If the user doesn't have one, searches still work but without AI scoring (all jobs get a neutral 0.5 score). Free keys available at https://aistudio.google.com/apikey

## Core Workflow

### 1. Conversational Search

When the user asks to search for jobs, gather these parameters conversationally:

- **keywords** (required): job title or search terms (e.g., "Python developer", "data engineer")
- **technologies** (optional): required tech stack (e.g., ["Python", "AWS", "Docker"])
- **countries** (optional): countries to search in (e.g., ["Spain", "Germany"])
- **remote** (optional): true/false for remote-only jobs
- **experience** (optional): "entry", "mid", "senior", "director", "executive"
- **exclude** (optional): terms to exclude (e.g., ["consultant", "staffing"])
- **company_size** (optional): LinkedIn size codes "1"-"8" (1=1-10, 4=201-500, 7=5001-10000)
- **salary_min** (optional): minimum salary in EUR
- **ai_prompt** (optional): extra criteria for AI scoring (e.g., "Must use microservices")
- **max_pages** (optional): pages to scrape per location (default 3, max 5)
- **min_score** (optional): minimum AI score to show (default 0.6)

Don't ask for ALL parameters — just ask the essentials (keywords, technologies, countries) and use sensible defaults for the rest. Let the user add filters if they want.

### 2. Run the Search

```bash
python3 scripts/job_hunter.py search '{
  "keywords": "Python developer",
  "technologies": ["Python", "FastAPI", "AWS"],
  "countries": ["Spain", "Germany"],
  "remote": true,
  "experience": "mid",
  "exclude": ["consultant"],
  "min_score": 0.6,
  "max_pages": 3
}'
```

The script returns JSON with scored jobs. Present the results in a clean format:

> **1. Senior Python Engineer** — TechCorp
> Madrid, Spain | Remote | €50k-60k
> Score: 0.92 — "Excelente match: remoto, Python/FastAPI"
> https://linkedin.com/jobs/view/12345

Show the top results (score >= min_score) sorted by score. If there are many results, show the top 10 and mention how many more are available.

**Important:** Searches take time (30-90 seconds) due to LinkedIn scraping. Tell the user to wait.

### 3. Save Interesting Jobs

Users can save jobs they like for later review:

```bash
# Save a job
python3 scripts/job_hunter.py save '{
  "title": "Senior Python Engineer",
  "company": "TechCorp",
  "location": "Madrid",
  "url": "https://linkedin.com/jobs/view/12345",
  "score": 0.92,
  "notes": "Great match, applied on 2026-03-19"
}'

# List saved jobs
python3 scripts/job_hunter.py saved

# Remove a saved job
python3 scripts/job_hunter.py unsave "https://linkedin.com/jobs/view/12345"
```

### 4. Search History

```bash
# Show recent searches
python3 scripts/job_hunter.py history

# Re-run a previous search
python3 scripts/job_hunter.py rerun 1
```

## Handling Different Languages

Detect the user's language and:
- Respond in their language
- AI summaries are always in the user's language (pass it in ai_prompt, e.g., "Respond in Spanish")
- Job data stays in the original LinkedIn language

## Tips

- **Per-country searches** give much better results than global "Remote" searches on LinkedIn
- If no results, suggest broadening: fewer technologies, more countries, lower experience level
- LinkedIn may rate-limit after many searches — suggest waiting 5-10 minutes if errors occur
- Encourage users to save interesting jobs before they disappear from LinkedIn

## Storage

All data stored as JSON in `~/.openclaw/job-hunter/`:
- `config.json` — Gemini API key and settings
- `history.json` — search history
- `saved.json` — saved jobs

See [references/search_format.md](references/search_format.md) for full schemas.
