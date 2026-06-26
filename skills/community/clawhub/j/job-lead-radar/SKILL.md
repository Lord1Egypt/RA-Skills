---
name: job-lead-radar
description: Scrape and collect job leads from major job boards on a schedule. Covers Indeed, ZipRecruiter, ProductionHUB, LinkedIn, and Peerspace. Note: Indeed, ZipRecruiter, and LinkedIn employ anti-bot protections that may reduce results; ProductionHUB and Peerspace scrape reliably. Use when asked to collect job leads, find production/creative work, monitor job postings, or run a job lead audit. Trigger phrases: "scrape jobs", "find job leads", "job openings", "production work", "freelance gigs", "career page", "job monitoring", "hiring now".
---

# Job Lead Radar

Automated job lead scraping across multiple sources. Runs on a schedule or on-demand.

**Note on job boards:** Indeed, ZipRecruiter, and LinkedIn employ anti-bot protections. Results may be reduced or zero on these sources. ProductionHUB and Peerspace scrape reliably. This is a known limitation of web scraping — not a defect in the skill.

## Quick Start

```bash
cd ~/.openclaw/skills/job-lead-radar
python scripts/scrape.py [source] [query]
```

**Sources:** `all` (default), `indeed`, `ziprecruiter`, `productionhub`, `peerspace`, `linkedin`
**Query:** Any job search term (default: "film producer")

## Output

Results saved to `job_leads.json` in the script directory. Each entry includes:
- `source` — job board name
- `timestamp` — ISO timestamp
- `jobs[]` — array of `{title, company, link}`

## Cron Setup

Add to OpenClaw cron for weekly job monitoring:

```
0 10 * * 1 cd ~/.openclaw/skills/job-lead-radar && python scripts/scrape.py all "film producer" >> logs/weekly.log 2>&1
```

## Custom Queries

Edit `references/queries.md` for industry-specific search terms. Common queries:

| Industry | Query |
|----------|-------|
| Film/TV Production | `film producer`, `video editor`, `production assistant` |
| Sports Production | `sports producer`, `broadcast`, `remote producer` |
| Creative | `content creator`, `social media`, `digital media` |
| Web3/Crypto | `blockchain`, `crypto`, `web3 developer` |
| Streaming | `streaming`, `ott`, `video platform` |

## Dependencies

- Python 3.7+
- `scrapling` (`pip install scrapling`)

## File Structure

```
job-lead-radar/
├── SKILL.md           ← you are here
├── scripts/
│   └── scrape.py      ← main scraper
└── references/
    └── queries.md     ← query templates
```
