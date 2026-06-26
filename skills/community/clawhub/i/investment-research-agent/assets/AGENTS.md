# AGENTS.md — Investment Research Agent Workspace

This is the agent's working root directory.

## Startup Sequence (every session)

1. Read `SOUL.md` — who I am
2. Read `USER.md` — who I work for
3. Read `SKILLS.md` — **work rules and hard constraints (mandatory, includes report format requirements)**
4. Read `memory/YYYY-MM-DD.md` (today + yesterday) — recent context
5. Check `RESEARCH/` directory — existing research output

## Directory Structure

- `RESEARCH/` — industry & stock research reports (organized as `sector/company-name.md`)
- `DATA/` — raw structured data with provenance (organized by date: `YYYY-MM-DD/`)
- `memory/` — daily work logs (format: `YYYY-MM-DD.md`)

## Data Archiving Rules

- `DATA/YYYY-MM-DD/` stores only **structured data with reuse value**: financial statements, quantitative market data, scraped tabular datasets
- Routine web_search / web_fetch research **does not require archiving** — source links in reports are sufficient
- Files in DATA/ must include: source URL, retrieval timestamp, data description

## Research Report Rules

- Reports go in `RESEARCH/`, organized as `sector-name/company-name.md` (all English)
- Must include: data sources, analysis date, key conclusions, risk disclosures
- Notify the user when complete
- **Audience is professional investors**: no basics, no explainers — go straight to data
- **Data density priority**: every conclusion needs a number; source link immediately follows

## Memory / Log Rules

**When to write:**
- After completing each task, immediately update the day's log
- Confirm log is written before ending a session

**What to write:**
- Date & one-line task summary
- Key steps taken
- Output file paths
- Key data findings (for fast context recovery next session)
- Pending items / follow-ups (if any)

**Log format:**
```
## YYYY-MM-DD

### Task: [brief description]
- Steps: ...
- Output: RESEARCH/sector/company.md
- Key findings: [data point with source]
- Pending: ...
```

## Security

- Do not scrape login-gated data (no credentials)
- Respect robots.txt
- Do not store personally sensitive information
