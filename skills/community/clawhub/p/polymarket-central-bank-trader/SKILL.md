---
name: polymarket-central-bank-trader
description: Trades Polymarket prediction markets on central bank decisions, interest rates, inflation prints, and Fed/ECB/Riksbank policy moves. Exploits three compounding structural edges — question tractability (near-term rate decisions are near-certain from CME FedWatch; emergency cuts are once-per-decade events retail perpetually overprices), FOMC communication cycle (maximum conviction post-meeting/dot-plot; minimum during blackout), and data calendar timing (CPI/PCE/NFP release weeks boost signal quality for inflation and rate markets).
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: Central Bank & Monetary Policy Trader
  difficulty: advanced
---

# Central Bank & Monetary Policy Trader

> **This is a template.**
> The default signal is keyword-based market discovery combined with conviction-based sizing and `central_bank_bias()` — three compounding structural edges, no external API required.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Central bank prediction markets are the most data-rich category on Polymarket — and among the worst-priced relative to the available data. The Fed publishes its own rate projections (dot plot), futures markets price every remaining meeting of the year, and inflation data is measured to two decimal places by multiple independent agencies. Three structural edges compound:

1. **Question tractability** — The Fed's "no surprise" doctrine means near-term rate decisions are, by design, nearly pre-determined from public data weeks before the meeting. CME FedWatch futures have ~95% accuracy when pricing ≥85% probability for a near-term decision. Polymarket retail prices the same meeting at 70–80%. Emergency cuts happened three times in 25 years. Retail prices them at 15–30% in every crisis.

2. **FOMC communication cycle** — The Fed operates on a strict 6-week cycle with a documented blackout period (~10 days before each meeting) when no official can speak publicly. Signal quality is highest in the 5 days post-meeting (fresh guidance, quarterly dot plot) and in the Fedspeak window (11–20 days before meeting). During blackout, no new guidance can arrive — markets are at maximum staleness. This cycle is computable from the published FOMC calendar.

3. **Data calendar timing** — BLS CPI (10th–17th of each month), BEA PCE (25th+), and BLS NFP (1st–7th) all have fixed release schedules. The window immediately around each release is when inflation and rate-path markets are most actionable: the Cleveland Fed CPI Nowcast is within 0.1pp of the final print, but retail anchors to the prior month's number and never checks the nowcast.

## Signal Logic

### Default Signal: Conviction-Based Sizing with Central Bank Bias

1. Discover active monetary policy markets on Polymarket
2. Compute base conviction from distance to threshold (0% at boundary → 100% at p=0/p=1)
3. Apply `central_bank_bias()` — question tractability × FOMC cycle position × data calendar
4. Size = `max(MIN_TRADE, conviction × bias × MAX_POSITION)` — capped at MAX_POSITION
5. Skip markets with spread > MAX_SPREAD or fewer than MIN_DAYS to resolution

### Central Bank Bias (built-in, no API required)

**Factor 1 — Question Type Tractability**

| Question type | Multiplier | The structural reality |
|---|---|---|
| Next-meeting rate decision (1–2 meetings out) | **1.25x** | "No surprise" doctrine; CME FedWatch ~95% accurate when ≥85% priced; retail still prices Polymarket as uncertain — 17-point structural gap |
| CPI / PCE inflation print at specific level | **1.20x** | Measured to two decimal places; Cleveland Fed CPI Nowcast within 0.1pp of final print updated daily; retail anchors to prior month's number |
| Year-end rate target / annual cut count | **1.15x** | Dot plot gives Fed's own median projection; CME futures curve gives market-implied path through every remaining meeting; both public, rarely read |
| Yield curve inversion / un-inversion | **1.10x** | FRED publishes 10Y-2Y and 10Y-3M daily; direction predictable from Fed rate path; retail treats yield curve as abstract not trackable |
| Recession declaration / GDP contraction | **0.80x** | NBER is backward-looking (6–18 month lag); Sahm Rule (real-time, near-perfect) unknown to retail; resolution criteria and signal are measuring different things |
| Chair fired / resigned / succession | **0.75x** | Fed independence norm strong (one removal-equivalent in modern history) but political risk real; resolution timing entirely in executive hands |
| Emergency / inter-meeting rate action | **0.70x** | Three times in 25 years (9/11, 2008, COVID); retail prices at 15–30% in every VIX spike; lowest-edge category in monetary policy |

**The "No Surprise" Doctrine** — The Fed designs its communication precisely to eliminate decision uncertainty before the meeting. When FedWatch prices a hold at 92%, that is not the market's opinion — it is the Fed's advance communication, expressed in futures. Polymarket retail prices 75% for the same event. The 17-point gap is not an opportunity; it is a structural feature of how the Fed operates, which replenishes every meeting cycle.

**The Emergency Cut Trap** — Three inter-meeting rate actions in 25 years (2001, 2008, 2020). Each was precipitated by a specific systemic shock (9/11, Lehman, COVID lockdown). Retail anchors to all three during every market stress episode and prices "will there be an emergency cut?" at 15–30% when the base rate in any given quarter is near zero. Dampen to 0.70x — the Stuxnet Rule of monetary policy.

**The NBER Lag Problem** — "Will there be a recession by Q3 2026?" resolves based on NBER's official declaration, which typically comes 6–18 months *after* the actual peak. The Sahm Rule (triggers when 3-month average unemployment rises 0.5pp above prior 12-month low) is a near-real-time recession indicator with a near-perfect historical track record — but NBER's formal definition lags it by over a year. This mismatch between the predictive signal and the resolution criteria makes recession timing markets structurally noisier than they appear. Trade at 0.80x.

**Factor 2 — FOMC Communication Cycle**

The FOMC calendar is published by the Federal Reserve Board at least one year in advance. The bias function reads it exactly — every run computes the current position in the cycle:

| Phase | Days relative to decision date | Multiplier | Why |
|---|---|---|---|
| Post-meeting | 0–5 days after | **1.20x (+0.05 in SEP months)** | Statement public, press conference indexed, dot plot fresh (Mar/Jun/Sep/Dec) |
| Fedspeak window | 11–20 days before | **1.15x** | Officials actively telegraph upcoming decision; forward guidance sharpest |
| Mid-cycle | All other periods | **1.00x** | Normal inter-meeting baseline |
| Blackout | 1–10 days before | **0.85x** | No Fed communication permitted; last guidance already priced; no new signal can arrive |

The **SEP boost** (+0.05x) applies in March, June, September, and December — the four meetings where the Fed publishes a fresh Summary of Economic Projections including the dot plot. The median dot is the Fed's own official rate forecast for the next 3 years. In these months, post-meeting clarity is at its maximum.

**Factor 3 — Data Calendar Overlay**

| Condition | Overlay mult | Release schedule |
|---|---|---|
| Inflation question + CPI release week (10th–17th) | **1.20x** | BLS CPI at 8:30 AM ET; Cleveland Fed nowcast closes in |
| Inflation question + PCE release week (25th+) | **1.15x** | BEA PCE at 8:30 AM ET; Fed's preferred measure |
| Labor market question + NFP week (1st–7th) | **1.15x** | BLS NFP first Friday; labor market shapes rate path |
| Rate decision question + any data release week | **1.10x** | Fresh macro data recalibrates rate path conviction |

### Combined Examples

| Market | Type | Cycle | Data | Final bias |
|---|---|---|---|---|
| "Will Fed cut 25bp at next meeting?" — post-SEP-FOMC + CPI week | 1.25x | 1.25x (post-SEP) | 1.20x | **1.40x cap** |
| "Will CPI fall below 3% this month?" — CPI week | 1.20x | 1.00x (mid-cycle) | 1.20x | **1.40x cap** |
| "Will Fed cut 3 times in 2026?" — mid-cycle | 1.15x | 1.00x | 1.00x | **1.15x** |
| "Will there be an emergency rate cut?" — any blackout | 0.70x | 0.85x | 1.00x | **0.60x → MIN_TRADE** |
| "Will Powell be fired?" — any | 0.75x | 1.00x | 1.00x | **0.75x** |
| "Will there be a recession by Q3 2026?" | 0.80x | 1.00x | 1.00x | **0.80x** |
| "Will Fed cut at next meeting?" — during blackout | 1.25x | 0.85x | 1.00x | **1.06x** — staleness penalty applies |

### Keywords Monitored

```
Federal Reserve, Fed rate, FOMC, interest rate, rate cut, rate hike,
basis points, Fed funds rate, ECB, Bank of England, Riksbank, BOJ,
Bank of Japan, RBA, Norges Bank, inflation, CPI, PCE, core CPI,
Jerome Powell, Christine Lagarde, dot plot, forward guidance,
quantitative easing, QE, quantitative tightening, QT, yield curve,
inverted yield curve, recession, soft landing, stagflation,
non-farm payroll, NFP, unemployment rate, Sahm Rule, pivot,
emergency rate cut, inter-meeting, Jackson Hole
```

### Remix Signal Ideas

- **CME FedWatch**: When FedWatch prices ≥85% for a near-term decision and Polymarket prices <70%, the divergence is structural — wire FedWatch probability directly into `p` and the conviction formula becomes the arbitrage signal; the gap reliably closes within 15–45 minutes of Fed communication
- **Cleveland Fed CPI Nowcast**: Updated daily using TIPS breakevens and commodity prices; consistently within 0.1pp of final CPI print — compare to Polymarket "will CPI be above/below X?" markets in the 72 hours before the BLS release
- **FRED API**: 10Y-2Y yield spread, SOFR term structure, Sahm Rule indicator — all free, updated daily; yield curve and recession markets on Polymarket are almost never priced against the actual FRED data
- **BLS / BEA Release Calendar**: CPI release schedule (bls.gov), PCE release schedule (bea.gov), NFP dates — the 30-minute window before each release is when rate-path markets are most mispriced relative to the incoming data


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
| `SIMMER_MAX_POSITION` | `35` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_VOLUME` | `15000` | Min market volume filter (USD) — monetary policy markets are liquid |
| `SIMMER_MAX_SPREAD` | `0.07` | Max bid-ask spread (7%) |
| `SIMMER_MIN_DAYS` | `5` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `6` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
