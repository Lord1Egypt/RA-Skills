# indeed-brightdata

Search and scrape Indeed job listings and company information using Bright Data's Web Scraper API. Works with Claude Code, Claude Desktop, Cursor, Codex, OpenClaw, and any agent supporting the [Agent Skills](https://agentskills.io) standard.

## Compatibility

| Platform | Install Method | Auto-Update |
|----------|---------------|-------------|
| Claude Code | Symlink or Plugin Marketplace | Yes (git pull) |
| Claude Desktop | ZIP upload | No (re-package) |
| Cursor | Symlink | Yes (git pull) |
| Codex | Symlink | Yes (git pull) |
| OpenClaw | Symlink | Yes (git pull) |

## Quick Start

```bash
git clone https://github.com/foreztgump/indeed-brightdata.git
cd indeed-brightdata
./install.sh --platform claude-code
```

## Prerequisites

- `curl` and `jq` installed
- Bash 4.0+
- A [Bright Data](https://brightdata.com) account with Indeed scraper access
- `BRIGHTDATA_API_KEY` environment variable set

## Installation

### Claude Code (Recommended)

**Option A --- Install script:**

```bash
git clone https://github.com/foreztgump/indeed-brightdata.git
cd indeed-brightdata
./install.sh --platform claude-code
```

**Option B --- Plugin marketplace:**

```bash
/plugin marketplace add foreztgump/indeed-brightdata
```

### Claude Desktop

```bash
git clone https://github.com/foreztgump/indeed-brightdata.git
cd indeed-brightdata
make package
```

Then upload `indeed-brightdata.zip` via **Settings > Features > Skills > Upload skill** in Claude Desktop.

### Cursor

```bash
git clone https://github.com/foreztgump/indeed-brightdata.git
cd indeed-brightdata
./install.sh --platform cursor
```

### Codex

```bash
git clone https://github.com/foreztgump/indeed-brightdata.git
cd indeed-brightdata
./install.sh --platform codex
```

### OpenClaw

```bash
git clone https://github.com/foreztgump/indeed-brightdata.git
cd indeed-brightdata
./install.sh --platform openclaw
```

This creates a symlink at `~/.openclaw/skills/indeed-brightdata`.

### All Platforms at Once

```bash
./install.sh --all
```

### Universal CLI (Community)

If you use the [add-skill](https://add-skill.org) CLI:

```bash
npx add-skill foreztgump/indeed-brightdata
```

## Usage

### Smart Job Search (Recommended)

```bash
# Expands keywords, runs parallel searches, deduplicates, caches results
scripts/indeed_smart_search.sh "cybersecurity" US "Remote"

# Format results for display
scripts/indeed_smart_search.sh "nursing" US "Texas" | scripts/indeed_format_results.sh --top 5

# Search all dates (default is last 7 days)
scripts/indeed_smart_search.sh "data science" US "New York, NY" --all-time

# Skip keyword expansion
scripts/indeed_smart_search.sh "registered nurse" US "Ohio" --no-expand

# Export to CSV
scripts/indeed_format_results.sh --type jobs --format csv results.json
```

### Single Keyword Search

```bash
scripts/indeed_jobs_by_keyword.sh "software engineer" US "Austin, TX"
scripts/indeed_jobs_by_keyword.sh "nurse" US "Ohio" --date-posted "Last 24 hours" --limit 20

# Fire-and-forget (returns immediately, check later):
scripts/indeed_jobs_by_keyword.sh "nurse" US "Ohio" --no-wait
scripts/indeed_check_pending.sh
```

### Job Details by URL

```bash
scripts/indeed_jobs_by_url.sh "https://www.indeed.com/viewjob?jk=abc123"
```

### Company Lookup

```bash
scripts/indeed_company_by_url.sh "https://www.indeed.com/cmp/Google"
scripts/indeed_company_by_keyword.sh "Tesla"
scripts/indeed_company_by_industry.sh "Technology" "Texas"
```

### Jobs from Company Page

```bash
scripts/indeed_jobs_by_company.sh "https://www.indeed.com/cmp/Google/jobs"
```

## Scripts

| Script | Purpose |
|--------|---------|
| `indeed_smart_search.sh` | **Smart job search** with keyword expansion, dedup, caching |
| `indeed_format_results.sh` | Format results for display (summary, CSV) |
| `indeed_jobs_by_url.sh` | Collect job details from Indeed URLs |
| `indeed_jobs_by_keyword.sh` | Single-keyword job search (used by smart search) |
| `indeed_jobs_by_company.sh` | Discover jobs from a company page |
| `indeed_company_by_url.sh` | Collect company info from URLs |
| `indeed_company_by_keyword.sh` | Search companies by keyword |
| `indeed_company_by_industry.sh` | Discover companies by industry/state |
| `indeed_poll_and_fetch.sh` | Poll async results and fetch data |
| `indeed_check_pending.sh` | Check/fetch completed pending searches |
| `indeed_list_datasets.sh` | List/save available dataset IDs |

All scripts support `--help` for detailed usage.

## Data Storage

The skill stores persistent data under `~/.config/indeed-brightdata/`:

- `datasets.json` — Bright Data dataset IDs (created once via `indeed_list_datasets.sh --save`)
- `pending.json` — In-flight async snapshot tracking (auto-cleaned after 24h)
- `history.json` — Search cache index for dedup (auto-cleaned after 7 days)
- `results/*.json` — Fetched search results (auto-cleaned after 7 days)

No data is sent anywhere other than the Bright Data API. Cleanup runs automatically via `indeed_check_pending.sh`.

## Development

```bash
make test      # Run all tests
make package   # Build ZIP for Claude Desktop
make help      # Show all targets
```

## License

MIT
