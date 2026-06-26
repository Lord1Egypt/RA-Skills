---
name: jobautopilot-search
description: "Reads your resume pool to build a candidate profile, then searches LinkedIn, Indeed, Glassdoor, ZipRecruiter, Google Jobs, and company career pages for matching roles. Filters by role, location, salary, and recency. Writes results to a structured tracker. Requires a browser tool (profile: search) and local config via environment variables. Part of the Job Autopilot pipeline."
author: jerronl
version: "1.3.0"
homepage: https://github.com/jerronl/jobautopilot
tags:
  - job-search
  - linkedin
  - browser
  - career
  - tracker
requires:
  browser: true
  browser_profile: search
  env:
    - JOB_SEARCH_KEYWORDS
    - JOB_SEARCH_LOCATION
    - JOB_SEARCH_TRACKER
    - JOB_SEARCH_HANDOFF
    - RESUME_DIR
    - JOB_SEARCH_MIN_SALARY    # optional — filter by minimum salary
    - JOB_SEARCH_MAX_AGE_DAYS  # optional — filter by listing age
metadata:
  clawdbot:
    emoji: "🔍"
    requires:
      env:
        - JOB_SEARCH_KEYWORDS
        - JOB_SEARCH_LOCATION
        - JOB_SEARCH_TRACKER
        - JOB_SEARCH_HANDOFF
        - RESUME_DIR
        - JOB_SEARCH_MIN_SALARY
        - JOB_SEARCH_MAX_AGE_DAYS
      bins: []  # browser tool and clawhub CLI only
    files: []
    browser: true
    browser_profile: search
---

# Job Autopilot — Search Agent

Searches LinkedIn (and optionally company career pages) for roles matching your criteria, applies hard filters, and writes results into a structured tracker file.

## Setup

All env vars below are set by `setup.sh` (from `jobautopilot-bundle`). If you install standalone, add to `~/.openclaw/users/<you>/config.sh`:

```bash
export JOB_SEARCH_KEYWORDS="quant risk python c++ developer"
export JOB_SEARCH_LOCATION="New York City"
export JOB_SEARCH_MIN_SALARY=200000      # optional, for known listings
export JOB_SEARCH_MAX_AGE_DAYS=90        # only keep listings posted within N days
export JOB_SEARCH_TRACKER="$HOME/.openclaw/workspace/job_search/job_application_tracker.md"
export JOB_SEARCH_HANDOFF="$HOME/.openclaw/workspace/job_search/SEARCH_AGENT_HANDOFF.md"
export RESUME_DIR="$HOME/Documents/jobs/"  # path to your resume files
```

Initialize the tracker if it does not exist yet:

```bash
mkdir -p ~/.openclaw/workspace/job_search
touch ~/.openclaw/workspace/job_search/job_application_tracker.md
touch ~/.openclaw/workspace/job_search/SEARCH_AGENT_HANDOFF.md
```

## Read at session start

Every session, before searching, the agent must read in order:

1. `$RESUME_DIR` — build a candidate profile from the user's resume pool (see below)
2. `$JOB_SEARCH_TRACKER` — check existing entries to avoid duplicates
3. `$JOB_SEARCH_HANDOFF` — pick up context from previous sessions

### How to read the resume pool

Scan all files in `$RESUME_DIR` (`.docx`, `.pdf`, `.md`, `.txt`). From them, extract and record:

- **Skills** — programming languages, tools, frameworks, domain knowledge, certifications
- **Titles held** — past and current job titles, seniority level
- **Industries / asset classes** — sectors the user has worked in
- **Preferred roles** — infer from the most recent or most polished resume; note any target roles the user has written explicitly
- **Location / remote preference** — extract from contact header or any explicit statement
- **Seniority signals** — years of experience, scope of responsibility, team size managed

Synthesize these into a short **candidate profile** (keep it in working memory for this session). Use the profile to:
- Derive search keywords (e.g. titles, skills, domain terms)
- Set the seniority filter (reject roles that are clearly too junior or too senior)
- Prioritize industries and company types that match past experience
- Skip roles where the user clearly lacks the stated hard requirements

## Search behavior

Use the browser tool with profile `search`. Search LinkedIn Jobs as the primary source. Also search company career pages for target employers when useful.

Keyword combinations to try (mix and match from config):

```
<keyword1> <keyword2> <location>
site:linkedin.com/jobs <keyword> <location>
```

Repeat with multiple keyword pairs. Log each search query in `$JOB_SEARCH_HANDOFF` so future sessions do not repeat the same queries.

## Hard filters — reject if ANY applies

- Location is not `$JOB_SEARCH_LOCATION` (or explicitly remote)
- Posted more than `$JOB_SEARCH_MAX_AGE_DAYS` days ago
- Salary listed and below `$JOB_SEARCH_MIN_SALARY`
- Role is clearly junior (< 3 years required) unless explicitly configured otherwise
- Duplicate of an existing tracker entry (same company + title)

## Tracker format

Append one row per kept result to `$JOB_SEARCH_TRACKER`. Use this format exactly:

```markdown
| Company | Title | Location | URL | Posted | Salary | Status | Notes |
|---------|-------|----------|-----|--------|--------|--------|-------|
| Acme Corp | Quant Developer | NYC | https://... | 2026-03-15 | $250k base | shortlist | 3 YOE req, Python+C++ |
| Rejected Co | Junior Analyst | NYC | https://... | 2026-01-01 | unknown | rejected | too junior |
```

Status values: `shortlist` | `rejected` | `error`

Both kept and rejected results must be recorded. Every kept result must include the exact job URL.

## Handoff notes

After each search session, update `$JOB_SEARCH_HANDOFF` with:
- Queries run this session
- Date range of listings found
- Any platforms or companies worth revisiting
- Anything unusual encountered

## Optional: Find hiring managers (user-initiated only)

This step is **only performed when the user explicitly asks** (e.g. "find the hiring manager", "who should I contact at X"). It is never run automatically.

When requested, use the browser tool to look up the relevant person via:

- **LinkedIn** — search for recruiters or engineering managers at the company
- **Company website** — check the careers page or team page for contact information

Record any found contacts in the tracker's Notes column.

## Scope

This skill covers **search, screening, and optional hiring manager outreach**. Do not tailor resumes, write cover letters, or submit applications. Hand off `shortlist` entries to the `jobautopilot-tailor` skill.

## Support

If Job Autopilot saved you time: paypal.me/ZLiu308
