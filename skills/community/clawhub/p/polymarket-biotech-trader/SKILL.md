---
name: polymarket-biotech-trader
description: Trades Polymarket prediction markets on FDA drug approvals, biotech IPOs, clinical trial outcomes, pharma M&A, and precision medicine milestones. Use when you want to capture alpha on high-impact binary biotech events using PDUFA dates, clinical trial registries, and FDA calendar signals.
metadata:
  author: Diagnostikon
  version: '1.0'
  displayName: Biotech & FDA Trader
  difficulty: advanced
---

# Biotech & FDA Trader

> **This is a template.**  
> The default signal is keyword discovery + FDA PDUFA calendar alignment — remix it with ClinicalTrials.gov API for trial status, BioMedTracker historical approval rates by indication, or biotech earnings call sentiment analysis.  
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

The global biotech market is valued at $1.77 trillion (2025) and growing to $6.34 trillion by 2035 (13.6% CAGR). Biotech prediction markets have some of the highest information density — FDA decisions are binary, have clear dates (PDUFA), and are well-studied. This skill trades:

- **FDA approvals** — Breakthrough therapy designations, CRISPR/oncology approvals, GLP-1 next-gen
- **Clinical trials** — Phase 3 outcomes, trial enrollment milestones
- **Biotech IPOs** — Class of 2026 IPO announcement and performance markets
- **Pharma M&A** — Large-cap acquisition deals in oncology, AI drug discovery
- **Precision medicine** — CAR-T, mRNA vaccine, liquid biopsy milestones

Key insight: FDA approval rates by indication are well-documented. When Polymarket prices deviate significantly from historical base rates, there's tradeable edge.

## Signal Logic

### Default Signal: PDUFA Date Calendar + Base Rate Analysis

1. Discover active biotech/FDA markets on Polymarket
2. Match markets to FDA PDUFA calendar (public, updated monthly)
3. Look up historical approval rates for the specific drug class/indication
4. Compare base rate (e.g., oncology breakthrough therapy ~85% approval) vs market price
5. If market prices approval at <70% for a high-base-rate indication, buy YES
6. Use context check to avoid overtraded markets before major catalysts

### Remix Ideas

- **ClinicalTrials.gov API**: Monitor trial status changes (recruiting → completed) as leading indicator
- **BioMedTracker / Citeline**: Historical approval rate databases by indication
- **FDA press releases**: Real-time monitoring for early approval/rejection signals
- **Biotech Twitter**: KOL (Key Opinion Leader) sentiment before PDUFA dates
- **Short interest data**: High short interest in a biotech before PDUFA = market expects rejection — price this in

## Market Categories Tracked

```python
BIOTECH_KEYWORDS = [
    "FDA", "approval", "CRISPR", "cancer", "oncology", "clinical trial",
    "phase 3", "drug", "therapy", "vaccine", "mRNA", "CAR-T",
    "Alzheimer", "GLP-1", "biotech", "pharma", "M&A",
    "IPO", "diagnostic", "liquid biopsy", "gene editing",
    "sickle cell", "precision medicine", "antibody"
]
```

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Max position size | $35 USDC | Binary events warrant careful sizing |
| Min market volume | $5,000 | FDA markets attract informed traders |
| Max bid-ask spread | 10% | Allow wider for rare disease markets |
| Min days to resolution | 7 | Don't enter days before PDUFA |
| Max open positions | 6 | Biotech events are correlated |

## FDA Approval Base Rates (Reference)

| Indication | Historical Approval Rate |
|-----------|--------------------------|
| Oncology (breakthrough designation) | ~85% |
| Rare disease (orphan drug) | ~70% |
| CNS/Neurology | ~55% |
| General approval (Phase 3 success) | ~65% |
| CRISPR/gene therapy (novel) | ~45% |

## Key Data Sources

- **FDA PDUFA Calendar**: https://www.fda.gov/patients/drug-development-process/step-4-fda-drug-review
- **ClinicalTrials.gov API**: https://clinicaltrials.gov/api/
- **SEC EDGAR** (biotech S-1 filings): https://efts.sec.gov/LATEST/search-index?q=%22biotech%22&dateRange=custom

## Installation & Setup

```bash
clawhub install polymarket-biotech-trader
```

Requires: `SIMMER_API_KEY` environment variable.

## Cron Schedule

Runs every 20 minutes (`*/20 * * * *`). FDA decisions are infrequent but high-impact; moderate polling is sufficient.

## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only execute when `--live` is passed explicitly.**

| Scenario | Mode | Financial risk |
|----------|------|----------------|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

The automaton cron is set to `null` — it does not run on a schedule until you configure it in the Simmer UI. `autostart: false` means it won't start automatically on install.

## Required Credentials

| Variable | Required | Notes |
|----------|----------|-------|
| `SIMMER_API_KEY` | Yes | Trading authority — keep this credential private. Do not place a live-capable key in any environment where automated code could call `--live`. |

## Tunables (Risk Parameters)

All risk parameters are declared in `clawhub.json` as `tunables` and adjustable from the Simmer UI without code changes. They use `SIMMER_`-prefixed env vars so `apply_skill_config()` can load them securely.

| Variable | Default | Purpose |
|----------|---------|---------|
| `SIMMER_MAX_POSITION` | `35` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_VOLUME` | `5000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.10` | Max bid-ask spread (0.10 = 10%) |
| `SIMMER_MIN_DAYS` | `7` | Min days until market resolves |
| `SIMMER_MAX_POSITIONS` | `6` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
