# ontario-immigration-expert

A generic Ontario immigration policy assistant (OINP Ontario Workforce Priority / RCIP/FCIP).

Built on real-time official OINP/ontario.ca policy, supports:
- **OINP Ontario Workforce Priority** stream EOI scoring — all 11 factors (employment/labour-market + human capital + regionalization)
- Eligibility gating (requires a job offer + employer approval on the Employer Portal → register EOI within 30 days of the Job Offer ID)
- **Sudbury RCIP/FCIP** community pilot (designated employers / priority occupations / community recommendation)
- Policy update monitoring (daily cron patrol of official sources, only pushes on changes)

## Features
- Works for **any candidate**: no bound personal profile — pass background via stdin JSON
- Fully local, offline scoring — no network / no API key required
- Auto-derives NOC TEER and major occupational category from the 5-digit NOC code
- Official bilingual rule (both official languages CLB 6+ = 10 points, one language = 5)
- All policy judgements follow real-time official sources (as of 2026-06-25 OINP Phase 1 restructure, legacy stream names are obsolete)

## Install

**Option 1 — via ClawHub CLI (recommended):**
```bash
clawhub install ontario-immigration-expert --workdir ~/.openclaw/workspace
```
This downloads the skill into `~/.openclaw/workspace/skills/ontario-immigration-expert/`.

**Option 2 — manual:** clone/copy this repo into the workspace skills directory so OpenClaw auto-discovers it:
```bash
git clone https://github.com/Forrest-tech/ontario-immigration-expert.git \
  ~/.openclaw/workspace/skills/ontario-immigration-expert
```

After installing, open a **new** OpenClaw session for the skill to be loaded.

Expected structure:
```text
ontario-immigration-expert/
├── SKILL.md
├── README.md
├── LICENSE
├── scripts/       evaluator.py, policy_monitor.py, auto_discover.py
└── data/          sources.json + official OINP snapshot
```

## Usage
```bash
echo '{"age":30,"noc":"21232","hourlyWage":41,"currentJobMonths":14,"ontarioTotalMonths":14,"latestNOAEarnings":72000,"permitType":"PGWP","highestEducation":"Master","canadianCredentialsCount":1,"lowestCLB":9,"isBilingual":false,"workRegion":"Northern Ontario","hasJobOffer":true}' | python3 scripts/evaluator.py
```
With no input it prints a demo candidate.

## Data sources (official)
- Ontario Workforce Priority Stream: ontario.ca/page/ontario-workforce-priority-stream
- OINP 2026 updates: ontario.ca/page/2026-ontario-immigrant-nominee-program-updates
- O. Reg. 422/17: ontario.ca/laws/regulation/170422
- Sudbury RCIP/FCIP: investsudbury.ca/.../rcipfcip/
- Official snapshot: data/snapshots/oinp-workforce-priority-OFFICIAL.txt (fetched 2026-08-21)

## Scripts
- `evaluator.py`: OINP EOI scoring engine (eligibility gate + NOC auto-derivation)
- `policy_monitor.py`: policy diff monitor (sanitized sha256 comparison)
- `auto_discover.py`: official source auto-discovery

## Disclaimer
Policy information is for reference only and **does not constitute immigration legal advice**. Always defer to the official provincial (OINP) decision. Policy changes over time — rely on the live official sources as the primary reference.

## License
MIT
