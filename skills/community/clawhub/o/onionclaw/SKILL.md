---
name: onionclaw
description: >
  Search the Tor dark web, fetch .onion hidden-service pages, rotate Tor
  identities, and run structured multi-step OSINT investigations.
  Use when the user asks to search the dark web, investigate .onion sites,
  check whether data appeared on the dark web, fetch a .onion URL, look up
  leaked credentials, investigate ransomware groups, or conduct any Tor-based
  threat intelligence or OSINT task.
homepage: https://github.com/JacobJandon/OnionClaw
metadata:
  {
    "openclaw": {
      "emoji":   "🧅",
      "os":      ["darwin", "linux"],
      "requires": {
        "bins": ["python3", "pip3", "tor"],
        "pip":  ["requests[socks]", "beautifulsoup4", "python-dotenv", "stem"]
      },
      "version":  "2.1.13",
      "author":   "JacobJandon",
      "license":  "MIT-0",
      "repo":     "https://github.com/JacobJandon/OnionClaw",
      "tags":     ["tor", "dark-web", "osint", "onion", "threat-intel", "privacy"]
    }
  }
---

# OnionClaw — Tor / Dark Web OSINT

**v2.1.13 · by JacobJandon · MIT-0 License**
[github.com/JacobJandon/OnionClaw](https://github.com/JacobJandon/OnionClaw)

OnionClaw routes all requests through the Tor network. It queries 12 verified
dark web search engines simultaneously, fetches `.onion` hidden-service pages,
rotates Tor circuits, schedules recurring watch/alert jobs, and produces
structured OSINT reports (Markdown, JSON, STIX, MISP, CSV) using the Robin
investigation pipeline.

---

## Setup (run once after install)

```bash
# 1. Install Python dependencies
pip3 install requests[socks] beautifulsoup4 python-dotenv stem

# 2. Interactive first-run wizard (sets up .env, torrc, and Tor in one step)
python3 {baseDir}/setup.py

# — OR — manual setup:
cp {baseDir}/.env.example {baseDir}/.env
# Edit {baseDir}/.env — add your LLM key (search + fetch work without one)
```

**Start Tor** (required before any command):

```bash
# Linux:
sudo apt install tor && sudo systemctl start tor

# macOS:
brew install tor && brew services start tor

# Custom (no root needed — setup.py can do this automatically):
tor -f /tmp/sicry_tor.conf &
# torrc: SocksPort 9050 / ControlPort 9051 / CookieAuthentication 1 / DataDirectory /tmp/tor_data
```

Enable **circuit rotation** (required for `renew.py` and `--daemon-poll`):

```
Add to /etc/tor/torrc:
  ControlPort 9051
  CookieAuthentication 1
Then: systemctl restart tor
setup.py does this automatically.
```

---

## Commands

### Check Tor is running

**Always run this first** before any dark web operation.

```bash
python3 {baseDir}/check_tor.py
```

Returns your exit IP and `tor_active: true/false`. If `false`, tell the user to
start Tor before continuing.

---

### Rotate Tor identity

Get a fresh exit node and a new three-hop circuit. Use between sessions or
whenever a new IP is needed.

```bash
python3 {baseDir}/renew.py
```

Returns `success: true/false`. If `false`, ensure ControlPort 9051 is enabled
and `TOR_DATA_DIR` is set in `.env` (or use `setup.py`).

---

### Check which search engines are alive

Ping all 12 engines via Tor and return latency + up/down for each.

```bash
python3 {baseDir}/check_engines.py
```

Run before a large search session; pass the alive engine names to `--engines`
to skip dead ones and save time.

---

### Search the dark web

Query all 12 dark web engines simultaneously. Returns deduplicated
`{title, url, engine}` results.

```bash
# Basic:
python3 {baseDir}/search.py --query "SEARCH_TERM"

# Limit results:
python3 {baseDir}/search.py --query "SEARCH_TERM" --max 30

# Specific engines:
python3 {baseDir}/search.py --query "SEARCH_TERM" --engines Ahmia Tor66 Ahmia-clearnet
```

**Available engines:** Ahmia, OnionLand, Amnesia, Torland, Excavator, Onionway,
Tor66, OSS, Torgol, TheDeepSearches, DuckDuckGo-Tor, Ahmia-clearnet

> **Tip:** Use short keyword queries (≤5 words). Dark web indexes respond far
> better to focused keywords than natural-language questions.

---

### Fetch a .onion page

Read the full text of any `.onion` URL (or clearnet URL) through Tor.

```bash
python3 {baseDir}/fetch.py --url "http://SOME.onion/path"
```

Returns: `{title, text (first 3000 chars), links, status, error}`.
If `status: 0` or `error` is set, the hidden service is offline — they go
down frequently; try a different result from `search.py`.

---

### OSINT analysis

Analyse raw dark web text with an LLM and produce a structured sectioned report.

```bash
# From a string:
python3 {baseDir}/ask.py --query "QUERY" --mode MODE --content "RAW_TEXT"

# From a file:
python3 {baseDir}/ask.py --query "QUERY" --mode MODE --file /path/to/content.txt

# From stdin (pipe):
echo "CONTENT" | python3 {baseDir}/ask.py --query "QUERY" --mode MODE
```

**Analysis modes:**

| Mode | Use for |
|---|---|
| `threat_intel` | General OSINT (default) — artifacts, insights, next steps |
| `ransomware` | Malware / C2 / MITRE ATT&CK TTPs, victim orgs, indicators |
| `personal_identity` | PII / breach exposure, severity, protective actions |
| `corporate` | Leaked credentials / code / internal docs, IR steps |

```bash
# With custom focus appended to the prompt:
python3 {baseDir}/ask.py --query "QUERY" --mode threat_intel \
  --custom "Focus on cryptocurrency wallet addresses"
```

---

### Full OSINT pipeline (single command)

Runs the complete Robin pipeline:
**refine query → check live engines → search → filter best results →
batch scrape → OSINT analysis → save report**

```bash
python3 {baseDir}/pipeline.py --query "INVESTIGATION_QUERY" --mode MODE
```

**Essential flags:**

| Flag | Default | Description |
|---|---|---|
| `--query TEXT` | required | Investigation topic (natural language OK — refined automatically) |
| `--mode MODE` | `threat_intel` | `threat_intel` / `ransomware` / `personal_identity` / `corporate` |
| `--max N` | `30` | Max raw results from search |
| `--scrape N` | `8` | Pages to batch-fetch (use `0` to skip scraping and get results-only report) |
| `--custom TEXT` | | Extra LLM instructions appended to the mode prompt |
| `--out FILE` | | Save report to file (exits 1 on permission error) |
| `--format FMT` | `md` | Output format: `md` / `json` / `csv` / `stix` / `misp` |
| `--no-llm` | | Skip all LLM steps — dump raw results / entity extraction only |
| `--confidence` | | Show BM25 confidence score per result |
| `--engines NAME…` | | Restrict to specific engines (skip dead ones) |
| `--no-cache` | | Bypass query/page cache for this run |
| `--clear-cache` | | Flush the result cache, then run |
| `--resume JOB_ID` | | Resume a checkpointed pipeline run by job ID |
| `--interactive` | | After the report, open a follow-up REPL for drill-down |
| `--output-dir DIR` | | Write `<job_id>.<ext>` into DIR (batch pipeline friendly) |
| `--modes` | | List all modes and their engine routing, then exit |
| `--engine-stats` | | Print per-engine reliability / latency table, then exit |
| `--check-update` | | Check for a newer OnionClaw release and exit |
| `--version` | | Print version and exit |

**MISP-specific flags:**

| Flag | Default | Description |
|---|---|---|
| `--misp-threat-level N` | `2` | MISP threat level 1–4 (1=high, 4=undefined) |
| `--misp-distribution N` | `0` | MISP distribution (0=your org, 1=connected, 2=all, 3=inherited) |

**Watch / alert flags:**

| Flag | Description |
|---|---|
| `--watch` | Register this query as a recurring watch job and exit |
| `--interval HOURS` | Re-run interval in hours for `--watch` (default 6) |
| `--watch-check` | Run all due watch jobs now and print alerts |
| `--watch-check --output-dir DIR` | Same but write each job's JSON to DIR (exits 1 on write error) |
| `--watch-list` | List all active watch jobs |
| `--watch-disable JOB_ID` | Disable a watch job by ID |
| `--watch-clear-all` | Disable ALL active watch jobs at once |
| `--watch-daemon` | *(deprecated alias)* Run as a blocking daemon loop |
| `--daemon-poll SECONDS` | Run `--watch-check` every N seconds in a daemon loop |

---

### Daemon mode (continuous monitoring)

Keep OnionClaw running and poll watch jobs at a fixed interval:

```bash
python3 {baseDir}/pipeline.py --daemon-poll 3600   # check every hour
```

---

### Scheduling watch jobs

Register a query as a recurring alert:

```bash
# Register (runs every 6 hours by default):
python3 {baseDir}/pipeline.py --query "ransomware hospital 2026" --watch --interval 6

# List all active jobs:
python3 {baseDir}/pipeline.py --watch-list

# Check due jobs now and write JSON files for each:
python3 {baseDir}/pipeline.py --watch-check --output-dir /tmp/alerts/

# Disable one job:
python3 {baseDir}/pipeline.py --watch-disable <JOB_ID>

# Clear all:
python3 {baseDir}/pipeline.py --watch-clear-all
```

---

## Typical investigation flows

### "Search the dark web for X"

1. `python3 {baseDir}/check_tor.py` — verify connected
2. `python3 {baseDir}/search.py --query "X"` — search all 12 engines
3. `python3 {baseDir}/fetch.py --url "URL"` — read top 2–3 results
4. `python3 {baseDir}/ask.py --mode threat_intel --query "X" --content "..."` — generate report

### "Has company.com appeared in dark web leaks?"

1. `python3 {baseDir}/check_tor.py`
2. `python3 {baseDir}/pipeline.py --query "company.com credentials leak" --mode corporate`
3. Present the structured report

### "Investigate ransomware group X"

1. `python3 {baseDir}/check_tor.py`
2. `python3 {baseDir}/pipeline.py --query "GROUP_NAME ransomware" --mode ransomware`

### "Write a STIX bundle for this investigation"

```bash
python3 {baseDir}/pipeline.py \
  --query "QUERY" --mode threat_intel \
  --format stix --out bundle.json
```

### "Fetch this .onion URL"

1. `python3 {baseDir}/check_tor.py`
2. `python3 {baseDir}/fetch.py --url "URL"`
3. Show the user the title + text content

### "Monitor for new leaks mentioning acme.com, alert me daily"

```bash
python3 {baseDir}/pipeline.py \
  --query "acme.com leak credentials" --watch --interval 24
# Later, in a cron job or daemon:
python3 {baseDir}/pipeline.py --watch-check --output-dir /tmp/acme-alerts/
```

---

## Output formats

| Format | Flag | Use for |
|---|---|---|
| Markdown | `--format md` (default) | Human-readable reports, `--out report.md` |
| JSON | `--format json` | Structured machine-readable, automation |
| CSV | `--format csv` | Spreadsheet import, result lists |
| STIX 2.1 | `--format stix` | Threat-intel platforms (MISP, OpenCTI, Splunk ES) |
| MISP | `--format misp` | Direct MISP event import |

---

## Important notes

- All traffic routes through Tor — tell the user this when relevant.
- `.onion` hidden services go offline frequently. `status: 0` means the site
  is temporarily unreachable — try a different result from `search.py`.
- Dark web search indexes go down often — run `check_engines.py` first and
  pass only alive engine names with `--engines`.
- LLM tools (`ask.py`, pipeline steps 3/5/7) require an API key in
  `{baseDir}/.env`. Set `LLM_PROVIDER=ollama` for fully local inference with
  no key. `search.py`, `fetch.py`, `check_tor.py`, `renew.py`, and
  `check_engines.py` work with **no key at all**.
- `--scrape 0` skips page fetching. The pipeline still runs step 7 (LLM
  analysis on search-result metadata only) and writes `--out` / `--output-dir`
  normally. A `WARN: --scrape 0` notice is printed to stderr.
- Use responsibly and lawfully — OSINT, security research, and threat
  intelligence only.

---

## Maintenance

### Update the bundled sicry.py engine

OnionClaw bundles `sicry.py` from the upstream
[SICRY™ repo](https://github.com/JacobJandon/Sicry).
After a new SICRY™ release, sync the bundled copy:

```bash
# Pull latest:
python3 {baseDir}/sync_sicry.py

# Pull a specific release tag:
python3 {baseDir}/sync_sicry.py --tag v2.1.13

# Preview without writing:
python3 {baseDir}/sync_sicry.py --dry-run
```

### Checking for OnionClaw updates

OnionClaw checks the **GitHub Releases API** (published releases only — not
plain git tags) for newer versions. A one-line notice is printed automatically
at pipeline startup when an update is available.

```bash
# On-demand update check:
python3 {baseDir}/pipeline.py --check-update

# Programmatic:
import sicry
r = sicry.check_update()
if not r["up_to_date"]:
    print(f"Update: {r['current']} → {r['latest']}  {r['url']}")
```

```bash
# Upgrade:
git -C {baseDir} pull
python3 {baseDir}/sync_sicry.py
```
