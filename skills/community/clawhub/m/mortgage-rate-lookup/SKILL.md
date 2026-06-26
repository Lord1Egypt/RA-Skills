---
name: mortgage-rate-lookup
description: Multi-lender mortgage rate comparison — scrapes 13 lenders + Freddie Mac + Mortgage News Daily benchmarks, ranks lowest to highest, tracks day-over-day changes.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "\U0001F3E0"
    homepage: https://github.com/seang1121/Multi-Lender-Mortgage-Rate-Lookup
    os:
      - macos
      - linux
    install:
      - kind: node
        package: patchright
        bins: []
---

# Mortgage Rate Lookup

Multi-lender mortgage rate comparison tool. Scrapes real rates from 13 lenders + 2 national benchmarks (Freddie Mac PMMS, Mortgage News Daily), ranks them lowest to highest, and tracks day-over-day changes.

## What It Does

- Scrapes **13 lenders** via patchright stealth browser (headless Chromium)
- Pulls **Freddie Mac PMMS** via direct CSV API (no browser)
- Pulls **Mortgage News Daily** via urllib (no browser)
- Compares 30yr fixed, 15yr fixed, ARM, FHA, VA products
- Ranks by lowest rate with APR
- Tracks 90-day rolling history for day-over-day change detection
- Outputs clean text report to stdout (pipe to Discord/Slack/email)

## Setup

```bash
pip install patchright
python3 -m patchright install chromium
```

Create `config.json` in the skill directory:
```json
{
  "zip_code": "YOUR_ZIP"
}
```

## Usage

```bash
# Headless, automated lenders only
python3 mortgage_rate_report.py

# Override ZIP code
python3 mortgage_rate_report.py --zip 90210

# Visible browser for debugging
python3 mortgage_rate_report.py --headed
```

## Architecture

### Two-tier fetching
1. **Tier 1 — Direct APIs (no browser):** Freddie Mac CSV + MND HTML via urllib. Fastest.
2. **Tier 2 — Stealth browser:** 13 lenders via patchright. Parallel batches of 4, sequential retry on failure.

### Retry logic
- Batches of 4 lenders in parallel
- Failed lenders retry sequentially (up to 3 attempts)
- Wait schedule: 8s → 12s → 15s

### Rate extraction
Regex patterns find rate/APR pairs for each product type. Rates validated between 3.0% and 12.0%.

## Output Example

```
=== Mortgage Rate Report (2026-04-06) ===
ZIP: 12540

30-Year Fixed (lowest → highest):
  Freddie Mac PMMS:  6.65%
  Rocket Mortgage:   6.75% (APR 6.82%)  ▼ -0.125
  Wells Fargo:       6.875% (APR 6.94%)
  Chase:             6.99% (APR 7.05%)  ▲ +0.125
  ...

15-Year Fixed (lowest → highest):
  ...
```

## Cron Integration

Works as an OpenClaw cron job — outputs to stdout, OpenClaw delivers to Discord/Telegram.

## Dependencies

- `patchright` (stealth Chromium automation)
- Python 3.10+ stdlib only beyond that

## Lenders Covered

Automated (headless): Rocket, Wells Fargo, Chase, Bank of America, US Bank, Citizens, PNC, Navy Federal, USAA, TD Bank, Guaranteed Rate, New American Funding, loanDepot

Benchmarks: Freddie Mac PMMS, Mortgage News Daily
