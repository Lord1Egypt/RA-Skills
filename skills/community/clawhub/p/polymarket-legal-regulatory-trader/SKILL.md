---
name: polymarket-legal-regulatory-trader
description: Trades Polymarket prediction markets on landmark court cases, antitrust rulings, SEC enforcement actions, EU regulatory decisions, and DOJ investigations. Use when you want to capture alpha on legal markets using court filing data, PACER records, and regulatory docket signals.
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: Legal & Regulatory Trader
  difficulty: advanced
---

# Legal & Regulatory Trader

> **This is a template.**
> The default signal is keyword-based market discovery combined with probability-extreme detection — remix it with the data sources listed in the Edge Thesis below.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Legal prediction markets have enormous information asymmetry — most Polymarket retail participants don't read court filings or understand regulatory procedure. They price criminal convictions as coin flips when the actual DOJ conviction rate is ~97%. This skill encodes documented institutional base rates directly into conviction sizing.

## Signal Logic

### Default Signal: Conviction-Based Sizing with Precedent Bias

1. Discover active legal and regulatory markets on Polymarket
2. Compute base conviction from distance to threshold (0% at boundary → 100% at p=0/p=1)
3. Apply `precedent_bias()` — multiplier based on documented legal/regulatory outcome statistics
4. Size = `max(MIN_TRADE, conviction × bias × MAX_POSITION)` — capped at MAX_POSITION
5. Skip markets with spread > MAX_SPREAD or fewer than MIN_DAYS to resolution

### Precedent Bias (built-in, no API required)

Retail prices legal outcomes as coin flips. `precedent_bias()` corrects this using documented historical statistics:

| Action type | Historical rate | Multiplier |
|---|---|---|
| DOJ criminal conviction (post-indictment) | ~97% plea/conviction | **1.35x** |
| Class action settlement | ~90%+ settle before trial | **1.25x** |
| SEC enforcement (post-Wells Notice) | ~85% result in formal action | **1.20x** |
| EU Phase 2 antitrust outcome | ~80%+ conditions or fine | **1.20x** |
| SCOTUS reversal (cert granted) | ~70% reverse lower court | **1.15x** |
| Crypto enforcement (post-charges) | High after formal charges | **1.15x** |
| Big tech merger blocked (FTC/DOJ) | ~40–60%, rising trend | **1.10x** |
| Regulatory approval / clearance | Harder to time | **0.80x** |

Example: "Will X be convicted?" market at 25% after indictment → conviction 34% × 1.35x = 46% → $14. Retail prices this at 25%; base rate says 97%. That's the edge.

### Why These Base Rates Hold

- **DOJ plea rate**: Federal prosecutors only indict when they have ~overwhelming evidence — they win 97%+ of cases taken to trial or plea
- **EU Phase 2**: The EC procedural calendar is legally defined — opening Phase 2 is a strong signal of serious concerns
- **SCOTUS cert**: The Court takes cases primarily to correct errors — ~70% reversal is a documented statistical pattern
- **Class action**: Discovery costs and litigation risk make settlement the rational outcome in ~90%+ of cases

### Remix Signal Ideas

- **CourtListener API**: Free PACER docket API — monitor filing velocity as leading indicator before markets react
- **SEC EDGAR enforcement**: Track Wells Notice dates to anticipate formal action timing (avg 4–6 months)
- **EU Competition docket**: Phase 2 opening date + 13 months = almost exact closing date
- **Courtroom View Network**: Live trial feeds for real-time signal on verdict direction


## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only with `--live` flag.**

| Scenario | Mode | Financial risk |
|---|---|---|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

`autostart: false` and `cron: null` — nothing runs automatically until you configure it in Simmer UI.

## Required Credentials

| Variable | Required | Notes |
|---|---|---|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as high-value credential. |

## Tunables (Risk Parameters)

All declared as `tunables` in `clawhub.json` and adjustable from the Simmer UI.

| Variable | Default | Purpose |
|---|---|---|
| `SIMMER_MAX_POSITION` | `30` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_VOLUME` | `8000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.10` | Max bid-ask spread (10%) |
| `SIMMER_MIN_DAYS` | `7` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `5` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
