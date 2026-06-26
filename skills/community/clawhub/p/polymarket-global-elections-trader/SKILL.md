---
name: polymarket-global-elections-trader
description: Trades Polymarket prediction markets on elections, referendums, and democratic events worldwide. Exploits two structural edges — electoral system type predictability (FPTP amplification vs PR majority impossibility) and regional information lag (non-English polling aggregators update daily; Polymarket prices don't).
metadata:
  author: snetripp
  version: "1.0"
  displayName: Global Elections & Democracy Trader
  difficulty: advanced
---

# Global Elections & Democracy Trader

> **This is a template.**
> The default signal is keyword-based market discovery combined with conviction-based sizing and `election_bias()` — remix it with the data sources listed below.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Global election markets on Polymarket have two layered structural edges that compound cleanly without any external API:

1. **Electoral system type** — Polymarket retail trades all elections as if they were US presidential races. They aren't. FPTP systems amplify poll leads into landslides; proportional representation systems make outright majorities near-impossible. Retail systematically misprices both.

2. **Regional information lag** — Polymarket is US-English-speaking. Wahlrecht.de updates German polling daily. DataFolha updates Brazilian tracking daily. Neither is read by the average Polymarket trader. The lag between a 3-point swing in a non-English aggregator and Polymarket repricing is 12–48 hours.

## Signal Logic

### Default Signal: Conviction-Based Sizing with Election Bias

1. Discover active election and referendum markets on Polymarket
2. Compute base conviction from distance to threshold (0% at boundary → 100% at p=0/p=1)
3. Apply `election_bias()` — combines electoral system type with regional information lag
4. Size = `max(MIN_TRADE, conviction × bias × MAX_POSITION)` — capped at MAX_POSITION
5. Skip markets with spread > MAX_SPREAD or fewer than MIN_DAYS to resolution

### Election Bias (built-in, no API required)

**Factor 1 — Electoral System Type**

| System / question type | Multiplier | The structural reality |
|---|---|---|
| FPTP "will X win" (UK, Australia, Canada) | **1.20x** | A 5% poll lead → ~80-85% win probability; retail anchors to raw margin, not seat translation |
| Runoff / second round | **1.15x** | Post-round-1 head-to-head polling has <3% average error; retail treats it like first round |
| Referendum (binary yes/no) | **1.10x** | Clean resolution criteria, well-polled in democracies |
| Snap election / early dissolution | **0.85x** | No steady polling baseline — volatility dominates |
| Coalition formation / who governs | **0.80x** | Multi-party negotiation dynamics genuinely unpredictable from polls alone |
| No-confidence / leadership challenge | **0.80x** | Parliamentary arithmetic + defection timing — hard to model |
| PR system "will X win outright majority" | **0.70x** | Near-impossible in Germany, Sweden, Netherlands, Spain, Israel — retail massively overprices |

**The PR Majority Rule** — In proportional representation systems, a single party winning an outright majority is a statistical anomaly, not a plausible baseline. Germany's Bundestag, Sweden's Riksdag, Israel's Knesset, the Netherlands' Tweede Kamer — single-party majorities happen perhaps once per generation. Yet retail prices these markets at 15–30% because they project the US two-party binary onto a multi-party system. Every such market is a structural NO unless one party is polling above 45%, which essentially never happens in mature PR democracies.

**Factor 2 — Regional Information Lag**

| Region | Multiplier | Key data sources retail doesn't read |
|---|---|---|
| Germany / France / Benelux / Scandinavia | **1.20x** | Wahlrecht.de (daily), Politico Europe, Votecompass — 12-36h lag vs Polymarket |
| Brazil / Latin America | **1.15x** | DataFolha, Quaest (daily tracking in Portuguese); CIEP, CNC for other countries |
| South / Southeast Asia | **1.15x** | India: CSDS, ABP-CVoter; Indonesia: LSI/Indikator; Philippines: Pulse Asia — local exit polls hours ahead of English |
| UK / Australia / Canada | **1.05x** | English but underweighted vs US — Electoral Calculus MRP models give structural edge |
| Sub-Saharan Africa / fragile democracies | **0.75x** | Low polling quality, coup risk, result disputes — resolution risk is material |

### Combined Examples

| Market | System mult | Region mult | Final bias |
|---|---|---|---|
| "Will SPD win majority in Bundestag?" | 0.70x (PR majority) | 1.20x (Germany lag) | **0.84x** — skeptical |
| "Will CDU win German general election?" | 1.20x (FPTP-style win) | 1.20x (Germany lag) | **1.35x cap** |
| "Who wins Brazil runoff?" | 1.15x (runoff) | 1.15x (Latin America) | **1.32x** |
| "Will UK Labour win majority?" | 1.20x (FPTP) | 1.05x (English) | **1.26x** |
| "Will snap election be called?" | 0.85x (snap) | 1.0x | **0.85x** |
| "Will Nigerian election resolve cleanly?" | 1.0x | 0.75x (Africa) | **0.75x** |

### Keywords Monitored

```
election, referendum, vote, prime minister, chancellor, president,
Germany election, France election, Brazil election, India election,
UK election, Japan election, South Korea, Taiwan election, snap election,
coalition, majority, parliament, polling, exit poll, incumbent, runoff,
second round, Bundestag, Riksdag, Assemblée, Duma, Diet, Congress,
Lok Sabha, confidence vote, no confidence, hung parliament,
minority government, proportional representation, first past the post
```

### Remix Signal Ideas

- **Wahlrecht.de**: German polling aggregator updated daily — compare to Polymarket for German election markets; the lag is often >24h and actionable
- **Politico Europe Poll of Polls**: Aggregated EU-wide polling — covers France, Germany, Italy, Spain, Poland simultaneously
- **DataFolha / Quaest**: Brazilian tracking polls in Portuguese — daily updates on presidential and state races
- **Electoral Calculus MRP (UK)**: Constituency-level seat projections — translates raw polling to seat counts, far more predictive than national vote share alone


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
| `SIMMER_MIN_VOLUME` | `10000` | Min market volume filter (USD) — elections need liquidity |
| `SIMMER_MAX_SPREAD` | `0.08` | Max bid-ask spread (8%) |
| `SIMMER_MIN_DAYS` | `5` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
