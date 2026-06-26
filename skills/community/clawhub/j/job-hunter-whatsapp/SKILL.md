---
name: job-hunter
description: "Automated job search, JD parsing, resume customization, and application tracking pipeline. Use when: user wants to find jobs, set up automated job searches, parse job descriptions, customize/tailor resumes for specific roles, track job applications, or get job hunt updates via WhatsApp/messaging. Supports free job APIs (LinkedIn guest, Jobicy, RemoteOK, Remotive, Adzuna, JSearch/RapidAPI). Triggers on: find jobs, job search, customize resume, tailor resume for [company], track applications, job hunt, apply to [company], show jobs, job status, set up job alerts."
---

# Job Hunter

Automated job search pipeline with JD parsing, resume tailoring, and application tracking.

## Setup

### 1. Initialize Project

Create the project structure in the workspace:

```
job-hunter/
├── config.json          # User profile, target roles, API config
├── api_keys.json        # API credentials (gitignored)
├── resumes/
│   ├── base_resume.md   # User's master resume (text)
│   └── [company]_[role].md  # Customized per job
├── jobs/
│   └── tracked_jobs.json    # All discovered jobs + status
```

### 2. Gather User Profile

Ask the user for (store in `config.json`):
- Current role, company, years of experience
- Core skills and technologies
- Target roles (e.g., "Senior iOS Engineer", "Staff Engineer")
- Location priority tiers (e.g., Remote then City A then City B then Other)
- Salary preference: disclose or private
- Resume file (extract text from PDF if needed, save as `resumes/base_resume.md`)

### 3. Configure APIs

See [references/apis.md](references/apis.md) for full API documentation.

**Free, no auth required:**
- LinkedIn guest API (best for local/country-specific jobs)
- Jobicy (remote jobs)
- RemoteOK (remote tech jobs)
- Remotive (remote dev jobs)

**Free, API key required (ask user to register):**
- Adzuna (country-specific, https://developer.adzuna.com)
- JSearch/RapidAPI (aggregates Indeed/Glassdoor, https://rapidapi.com — search "JSearch")

Store keys in `api_keys.json` with rate limits:
```json
{
  "adzuna": { "app_id": "...", "app_key": "...", "daily_budget": 4 },
  "rapidapi": { "key": "...", "daily_budget": 2 }
}
```

## Core Workflows

### Job Finding

1. Query all configured APIs (see [references/apis.md](references/apis.md))
2. For each result, check against `tracked_jobs.json` — skip duplicates (match by URL or title+company)
3. **Read the actual JD** for each new job — extract real data only:
   - Required skills/technologies (from JD text, not assumed)
   - Years of experience required (from JD text)
   - Salary (only if posted in listing)
   - Location and remote policy
4. Calculate match score (0-100) by comparing user's actual skills against JD requirements
5. Assign location tier based on user's priority config
6. Add to `tracked_jobs.json`

**Critical rule: Never hallucinate or assume JD data. If the JD can't be fetched, mark fields as "not fetched" and note it.**

Salary estimates: Only use JSearch estimated-salary API endpoint. Label clearly as "market estimate" vs "posted salary".

### JD Parsing

Extract from actual job posting text:
```
- title, company, location
- required_skills[] (from JD)
- experience_years (from JD)  
- salary (only if stated)
- tech_stack[] (from JD)
- nice_to_have[] (from JD)
- apply_url
```

### Resume Customization

When user says "customize resume for [company]":
1. Read the base resume from `resumes/base_resume.md`
2. Read the parsed JD for that job from `tracked_jobs.json`
3. Reorder and reframe existing experience to match JD requirements
4. Emphasize matching skills, use language from the JD
5. **Never add skills, experience, or achievements the user doesn't have**
6. **Never inflate numbers or add hallucinated data**
7. Save to `resumes/[company]_[role].md`

### Application Tracking

Track status in `tracked_jobs.json`:
```
new → parsed → customized → applied → screening → interviewing → offer/rejected
```

Each entry:
```json
{
  "id": "unique",
  "source": "linkedin|jobicy|remoteok|adzuna|jsearch",
  "title": "from API",
  "company": "from API",
  "location": "from API",
  "location_tier": 1,
  "match_score": 85,
  "salary": "only if posted",
  "tech_stack": ["from actual JD"],
  "experience_required": "from actual JD",
  "apply_url": "url",
  "status": "new",
  "found_date": "YYYY-MM-DD",
  "notes": ""
}
```

## Automation

### Cron Jobs

Set up two cron jobs:

1. **Job Finder** — Daily at user's preferred time (default 9 AM local):
   - Query all APIs, parse new JDs, update tracker
   - `sessionTarget: "isolated"`, `delivery: "announce"`

2. **Status Update** — Daily at user's preferred time (default 11 AM local):
   - Read tracker, compile summary, send to user's messaging channel
   - `sessionTarget: "isolated"`, `delivery: "announce"`

### WhatsApp/Messaging Format

Format updates for mobile readability (40-50 chars per line). Group jobs by:
1. 🌐 Remote (user's country) 
2. 🌍 Remote (international)
3. 🏠 Office (by city, user's priority order)

Per job card:
```
━━━━━━━━━━━━━━━━━━
🏢 *Company Name*
📋 Role Title
📅 X+ yrs (from JD)
💰 Salary (if posted)
🛠 Tech: from actual JD
📍 Location
🎯 Match: X% — reason
```

**Only show data from actual JD. Mark unfetched JDs with ⚠️.**

## Interactive Commands

Users can ask anytime:
- "show jobs" / "what's available" → list tracked jobs
- "show hyderabad jobs" → filter by location
- "customize resume for [company]" → trigger customizer
- "apply to [company]" → update status, note action needed
- "status" → summary of all applications
- "mark [company] as [status]" → update tracker
