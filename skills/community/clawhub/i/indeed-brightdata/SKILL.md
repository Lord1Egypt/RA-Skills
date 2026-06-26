---
name: indeed-brightdata
description: >
  Search and scrape Indeed job listings and company information using Bright Data's
  Web Scraper API. Use when the user asks to find jobs on Indeed, search for job
  postings by keyword or location, look up company information from Indeed, collect
  job listing details from Indeed URLs, discover companies by industry, or perform
  any Indeed-related recruiting research. Requires BRIGHTDATA_API_KEY env var.
  Supports: job search by keyword/location/URL, company lookup by URL/keyword/industry,
  batch collection with polling, and structured JSON output.
version: 2.0.0
license: MIT
allowed-tools: Bash
metadata: {"openclaw":{"requires":{"env":["BRIGHTDATA_API_KEY"],"bins":["curl","jq"]},"primaryEnv":"BRIGHTDATA_API_KEY","configPaths":["~/.config/indeed-brightdata/"]}}
---

# Indeed Bright Data Skill

Search Indeed for job listings and company info via Bright Data's Web Scraper API. Designed for recruiting workflows on messaging platforms (Telegram, Signal) with smart defaults.

## Prerequisites

- `BRIGHTDATA_API_KEY` environment variable must be set
- `curl` and `jq` must be available

## Workflow Decision Tree

```text
User wants job info?
├── Has a specific Indeed URL?
│   ├── Job URL (/viewjob?) → indeed_jobs_by_url.sh [SYNC — seconds]
│   ├── Company jobs URL (/cmp/*/jobs) → indeed_jobs_by_company.sh [ASYNC — minutes]
│   └── Company page URL (/cmp/*) → indeed_company_by_url.sh [SYNC — seconds]
├── Wants to search by keyword/location?
│   └── indeed_smart_search.sh [ASYNC — 3-8 min]
│       Agent says: "Searching now, this takes a few minutes."
│       If results < 5: auto-expands date range, do NOT ask user
│       Always pipe output through: indeed_format_results.sh --top 5
├── Wants company info?
│   ├── Has Indeed company URL → indeed_company_by_url.sh [SYNC — seconds]
│   ├── Has keyword → indeed_company_by_keyword.sh [ASYNC — minutes]
│   └── Has industry + state → indeed_company_by_industry.sh [ASYNC — minutes]
└── Check pending results? → indeed_check_pending.sh (run on heartbeat)
```

**Always prefer sync (URL-based) scripts when the user provides a URL — they return in seconds.**

## Scripts Reference

| Script | Purpose | Mode |
|--------|---------|------|
| `indeed_smart_search.sh` | **Primary job search** — keyword expansion, parallel queries, dedup, caching | ASYNC |
| `indeed_jobs_by_url.sh` | Collect job details by URL(s) | SYNC |
| `indeed_jobs_by_keyword.sh` | Low-level single-keyword job search (used by smart search internally) | ASYNC |
| `indeed_jobs_by_company.sh` | Discover jobs from company page | ASYNC |
| `indeed_company_by_url.sh` | Collect company info by URL | SYNC |
| `indeed_company_by_keyword.sh` | Discover companies by keyword | ASYNC |
| `indeed_company_by_industry.sh` | Discover companies by industry/state | ASYNC |
| `indeed_format_results.sh` | Format JSON results into summary, full, or CSV | Local |
| `indeed_check_pending.sh` | Check/fetch completed pending searches + auto-cleanup | Local/API |
| `indeed_poll_and_fetch.sh` | Poll async job and fetch results (internal) | API |
| `indeed_list_datasets.sh` | List available Indeed dataset IDs | API |

## Quick Start

User says: "Find me cybersecurity jobs in New York"
```bash
scripts/indeed_smart_search.sh "cybersecurity" US "New York, NY" \
  | scripts/indeed_format_results.sh --type jobs --top 5
```

User says: "Get details on this job: https://www.indeed.com/viewjob?jk=abc123"
```bash
scripts/indeed_jobs_by_url.sh "https://www.indeed.com/viewjob?jk=abc123"
```

## Behavior Rules (MANDATORY)

1. **NEVER return raw JSON to the user.** Always pipe results through `indeed_format_results.sh`.
2. **NEVER ask "want me to try broader keywords?"** if results < 5. The smart search auto-expands automatically. Just tell the user: "Found only N results with recent postings, expanding search..."
3. **NEVER present results older than 30 days** without noting they may be stale.
4. **When a discovery search is running**, immediately acknowledge: "Searching Indeed now — this usually takes 3-5 minutes. I'll come back with results."
5. **If the user asks a follow-up while a search is pending**, run `indeed_check_pending.sh` first before starting a new search.
6. **For Telegram**: keep each message under 3500 characters. Use the `---SPLIT---` markers from `indeed_format_results.sh` to break across messages.
7. **Always show total result count** and offer to show more: "Showing top 5 of 23 results. Want to see more, or filter by salary/location?"
8. **Default to "Last 7 days"** for date filtering. If the user says "find me jobs" without a time preference, the default is already set.

## Smart Search (Primary Entry Point)

```bash
# Basic search (expands keywords, deduplicates, defaults to last 7 days)
scripts/indeed_smart_search.sh "cybersecurity" US "Remote"

# All-time search
scripts/indeed_smart_search.sh "nursing" US "Texas" --all-time

# Skip keyword expansion
scripts/indeed_smart_search.sh "registered nurse" US "Ohio" --no-expand

# Bypass 6-hour cache
scripts/indeed_smart_search.sh "data science" US "New York" --force
```

Output is `{"meta": {...}, "results": [...]}` with metadata including query params, keywords used, and result counts.

## Result Formatting

```bash
# Telegram-friendly summary (default)
scripts/indeed_format_results.sh --type jobs --top 5 results.json

# CSV export
scripts/indeed_format_results.sh --type jobs --format csv results.json

# Companies
scripts/indeed_format_results.sh --type companies --top 5 companies.json

# Pipe from smart search
scripts/indeed_smart_search.sh "nurse" US "Ohio" | scripts/indeed_format_results.sh --top 5
```

## Heartbeat: Checking Pending Results

```bash
scripts/indeed_check_pending.sh
# Output: {"completed":[...],"still_pending":[...],"failed":[...]}
```

Run this periodically. If `~/.config/indeed-brightdata/pending.json` exists and is non-empty, check for completed results. Format completed results with `indeed_format_results.sh` and send to the user.

## Exit Codes

| Code | Meaning | Agent should... |
|------|---------|-----------------|
| 0 | Success — results on stdout | Format and present results |
| 1 | Error — something failed | Report the error |
| 2 | Deferred — still processing, saved to pending | Tell user "results are still processing, I'll follow up" |

## Caching

Smart search caches results for 6 hours. Identical searches (same keyword + location + country) return cached results without API calls. Use `--force` to bypass. Old results (>7 days) are auto-cleaned by `indeed_check_pending.sh`.

## Data Storage

All persistent data is stored under `~/.config/indeed-brightdata/`:

| File | Purpose | Lifecycle |
|------|---------|-----------|
| `datasets.json` | Bright Data dataset IDs | Created on first `indeed_list_datasets.sh --save`, rarely changes |
| `pending.json` | In-flight async snapshots | Entries added on poll timeout (exit 2) or fire-and-forget (`--no-wait`), removed when fetched or after 24h |
| `history.json` | Search cache index | Entries added per search, auto-cleaned after 7 days |
| `results/*.json` | Fetched result data | Written when snapshots complete, auto-cleaned after 7 days |

Auto-cleanup runs at the start of `indeed_check_pending.sh`. No data is sent anywhere other than the Bright Data API.

## Security

All scripts source `scripts/_lib.sh` for shared HTTP and persistence functions. The library:

- Makes requests to a **single endpoint**: `https://api.brightdata.com/datasets/v3`
- Uses **one credential**: `BRIGHTDATA_API_KEY` (sent via `Authorization: Bearer` header)
- Writes **only** to `~/.config/indeed-brightdata/` (see Data Storage above)
- Does not read other environment variables, contact other hosts, or modify files outside its config directory

## For full API parameter details

See `references/api-reference.md` for complete endpoint documentation, response schemas, and country/domain mappings.

## For keyword expansions

See `references/keyword-expansions.json` for the lookup table of keyword-to-job-title mappings.
