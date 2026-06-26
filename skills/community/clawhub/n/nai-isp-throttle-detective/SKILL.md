---
name: isp-throttle-detective
description: Run speed tests to multiple endpoints, log results, and detect ISP throttling patterns. Use when the user mentions speed test, internet slow, ISP throttling, bandwidth test, is my ISP throttling, speed history, internet speed, slow at night, or peak-hour slowdowns. Measures download speed from Cloudflare, Google, and CDN endpoints plus upload, logs with timestamps and time-of-day context, and generates evidence reports (peak vs off-peak tables, CDN discrimination analysis, trend charts) suitable for ISP complaints or plan upgrade decisions.
---

# ISP Throttle Detective

Scripts live in `scripts/`. Log and config default to `~/.isp-throttle-detective/`. See `references/setup-guide.md` for full setup, scheduling, and interpretation guidance.

## Workflow

### Run a single test and log it
```bash
python3 scripts/speedtest.py | python3 scripts/log_result.py
```

### Analyze patterns (needs ≥5 tests across multiple hours/days)
```bash
python3 scripts/analyze.py
python3 scripts/analyze.py --days 30 --json   # machine-readable
```

### Generate evidence report
```bash
python3 scripts/report.py --days 30 --out ~/report.md
```

## Scripts

| Script | Purpose |
|--------|---------|
| `speedtest.py` | Download from 3 endpoints + upload to Cloudflare. Outputs JSON to stdout. |
| `log_result.py` | Append speedtest JSON to JSONL log with hour, day_of_week enrichment. |
| `analyze.py` | Detect peak vs off-peak, CDN discrimination, trend, anomalies. |
| `report.py` | Generate markdown evidence report with tables and plain-English conclusion. |

## Configuration

Copy `assets/config.example.json` to `~/.isp-throttle-detective/config.json`. All scripts auto-detect it. Key fields:
- `log_file` — where the JSONL log lives
- `endpoints` — add/remove test targets; set `category: "cdn"` vs `"general"` to enable CDN discrimination detection
- `peak_hours` — list of hours (0–23) considered peak

Pass `--config /path/to/config.json` to any script to override.

## Scheduling

See `references/setup-guide.md` for launchd (macOS) and cron (Linux) snippets. Recommended: every 30 minutes for meaningful data within a day or two.

## Throttling Signals

- Peak-hour drop **>20%** vs off-peak → time-based throttling
- CDN speed **<75%** of general internet → destination-based throttling
- Declining trend slope → infrastructure degradation
- Multiple low-speed anomalies at the same hour → systematic, not random

## Using the Evidence Report

`report.py` produces a markdown file with a peak/off-peak comparison table, per-endpoint breakdown, hourly chart, trend analysis, and a plain-English conclusion. Share it directly with ISP support or use it to evaluate whether upgrading your plan would actually help (if CDN throttling is confirmed, a faster plan won't fix it).
