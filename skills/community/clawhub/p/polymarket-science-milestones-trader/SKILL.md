---
name: polymarket-science-milestones-trader
description: Trades Polymarket prediction markets on scientific breakthroughs, Nobel Prizes, physics discoveries, and research milestones. Corrects for systematic retail overpricing of hype-driven claims (fusion, RT superconductors, cancer cure) and exploits Nobel calendar timing via Clarivate Citation Laureates data.
metadata:
  author: snetripp
  version: "1.0"
  displayName: Science Milestones & Research Trader
  difficulty: advanced
---

# Science Milestones & Research Trader

> **This is a template.**
> The default signal is keyword-based market discovery combined with conviction-based sizing and `science_bias()` — remix it with the data sources listed below.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Science markets are priced by non-experts following journalist headlines. Journalists systematically amplify the most optimistic interpretation of scientific results. The research community knows the replication rates, timeline track records, and definitional ambiguities behind each claim type. Retail doesn't. This creates large, consistent mispricings — and two of the most exploitable edges anywhere on Polymarket: **hype-claim dampening** and **Nobel calendar timing**.

## Signal Logic

### Default Signal: Conviction-Based Sizing with Science Hype Correction

1. Discover active science and research markets on Polymarket
2. Compute base conviction from distance to threshold (0% at boundary → 100% at p=0/p=1)
3. Apply `science_bias()` — combines science claim type with Nobel calendar timing
4. Size = `max(MIN_TRADE, conviction × bias × MAX_POSITION)` — capped at MAX_POSITION
5. Skip markets with spread > MAX_SPREAD or fewer than MIN_DAYS to resolution

### Science Bias (built-in, no API required)

**Factor 1 — Science Claim Type: Hype Cycle vs Replication Reality**

| Claim type | Multiplier | The real signal |
|---|---|---|
| CRISPR / gene therapy clinical | **1.15x** | clinicaltrials.gov tracks endpoints; regulatory path is public — retail treats as sci-fi |
| Alzheimer / neurodegeneration drug | **1.10x** | Post-Lecanemab/Donanemab, Phase 3 approval path established; calendar trackable |
| Nobel Prize (any field) | **1.15x** (+ timing) | Clarivate Citation Laureates ~40% hit rate; committee rewards 10–30yr replicated work |
| Dark matter / particle physics | **0.85x** | Binary rare events; sensitivity curves published but genuine detections are rare |
| Quantum computing milestone | **0.85x** | Roadmaps exist but corporate "supremacy" claims are marketing-contaminated |
| AGI / AI consciousness by date | **0.70x** | No agreed definition; every AGI timeline since 1956 has been wrong |
| Longevity / aging reversal | **0.70x** | Mouse→human gap is 10–15 years minimum; conference culture creates retail overcrowding |
| Cancer "cure" / universal treatment | **0.65x** | Fundamental category error — cancer is 200+ distinct diseases; premise is incoherent |
| Commercial / grid-connected fusion | **0.65x** | ITER delayed 2016→2020→2025→2035; every commercial fusion timeline has slipped >50% |
| Room temperature superconductor | **0.55x** | Near-100% replication failure rate; LK-99 (2023) is the definitive template |

**The RT Superconductor Rule** — 0.55x is the lowest multiplier in the entire project across all traders. The reason is historical: every significant "room temperature superconductor" claim since 1987 has either failed replication or been retracted. The 2023 LK-99 episode — global excitement, total replication failure within two weeks — is not an outlier. It is the pattern. When a RT superconductor market appears on Polymarket, the YES side is being priced by media excitement, not physics consensus. The NO edge is structural.

**The Fusion Rule** — "Fusion is always 5 years away" is not a joke; it's a documented pricing pattern. NIF's December 2022 ignition (Q>1) was genuinely historic. But *commercial* fusion — grid-connected, cost-competitive electricity — requires solving plasma engineering, materials science, and economic problems that are decades away. Every market asking "will fusion power X by Y" where Y is within 10 years is systematically overpriced.

**Factor 2 — Nobel Calendar Timing**

The Nobel Prize follows a known annual schedule. Two data sources are public every year:

| Condition | Multiplier | Why |
|---|---|---|
| Nobel market + October (announcement week) | **1.25x** | Physics Mon, Chemistry Tue, Medicine Mon, Peace Fri — Polymarket takes 15–30 min to reprice each announcement |
| Nobel market + September (Clarivate month) | **1.15x** | Clarivate Citation Laureates shortlist published — citation data retail doesn't read |
| Nobel market + all other months | **1.00x** | Clarivate predictions still useful but no immediate timing catalyst |

The skill prints `nobel=ANNOUNCEMENT / CLARIVATE / off-season` on startup.

**Clarivate Citation Laureates** — Clarivate analyzes citation impact across all scientific literature and publishes annual shortlists of researchers predicted to win Nobel Prizes. Their hit rate is ~40% correct in advance — far above the base rate. The key insight: Nobel committees reward *longevity of impact*, not recency. The Clarivate list reflects citation networks built over decades; retail chases last year's hottest paper. These systematically diverge.

### Keywords Monitored

```
Nobel Prize, Nobel, physics, fusion energy, ITER, nuclear fusion, dark matter,
quantum computer, quantum computing, breakthrough, nature paper, CERN,
James Webb, room temperature superconductor, AGI, consciousness, cancer cure,
Alzheimer treatment, longevity, aging reversal, CRISPR, gene therapy,
clinical trial, phase 3, replication, preprint, arXiv, peer review,
superconductor, LK-99, qubit, quantum supremacy, drug approval
```

### Remix Signal Ideas

- **Clarivate Citation Laureates**: September shortlist — use to adjust YES_THRESHOLD per Nobel candidate market; candidates on the shortlist deserve lower YES_THRESHOLD than those off it
- **arXiv API**: Monitor preprint velocity per keyword topic — spikes 3–7 days before mainstream coverage, before markets reprice
- **ClinicalTrials.gov**: Gene therapy and Alzheimer drug trial completion dates — feed expected date into days-to-resolution analysis
- **Semantic Scholar API**: Real-time citation graph — detect breakout papers early before journal publication drives Polymarket question creation


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
| `SIMMER_MAX_POSITION` | `25` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_VOLUME` | `5000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.12` | Max bid-ask spread (12%) — wider for low-volume science markets |
| `SIMMER_MIN_DAYS` | `14` | Min days until resolution — science markets need longer runway |
| `SIMMER_MAX_POSITIONS` | `6` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
