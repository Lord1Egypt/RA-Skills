---
name: polymarket-social-trends-trader
description: "Trades Polymarket prediction markets on social trend indicators: loneliness indices, mental health policy, drug legalization, and cultural inflection points. Exploits ideologically motivated retail overcrowding and US legislative calendar base rates."
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: Social Trends & Wellbeing Trader
  difficulty: advanced
---

# Social Trends & Wellbeing Trader

> **This is a template.**
> The default signal is keyword-based market discovery combined with conviction-based sizing and `policy_bias()` — remix it with the data sources listed below.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Social policy markets are dominated by ideologically motivated traders who bet on what they **want** to happen, not what evidence suggests will happen. This is the most consistent and exploitable mispricing pattern on Polymarket. The skill corrects for it with two hard-coded structural edges: issue-type ideological distortion and the US legislative calendar.

## Signal Logic

### Default Signal: Conviction-Based Sizing with Policy Bias

1. Discover active social policy and wellbeing markets on Polymarket
2. Compute base conviction from distance to threshold (0% at boundary → 100% at p=0/p=1)
3. Apply `policy_bias()` — combines ideological motivation correction with legislative calendar
4. Size = `max(MIN_TRADE, conviction × bias × MAX_POSITION)` — capped at MAX_POSITION
5. Skip markets with spread > MAX_SPREAD or fewer than MIN_DAYS to resolution

### Policy Bias (built-in, no API required)

**Factor 1 — Ideological Motivation Correction**

The dominant pricing force in social policy markets is not information — it is **tribal loyalty**. Each policy domain attracts a different ideological crowd, each systematically overpricing the outcome they *want*:

| Issue type | Multiplier | The bias to correct |
|---|---|---|
| FDA drug approval (post Phase 3 / NDA) | **1.20x** | Retail applies moral judgment to a regulatory process (~85-90% NDA approval rate) |
| Social media ban / teen smartphone restriction | **1.15x** | Bipartisan consensus exists — retail underprices because gridlock fatigue |
| Mental health funding / parity mandate | **1.05x** | Broadly popular across party lines — retail conflates sensitive topic with opposition |
| Homelessness / poverty statistics (data release) | **1.00x** | Objective HUD/Census data — no ideological signal |
| Gun control / background checks / red flag laws | **0.90x** | Bidirectional overcrowding — both crowds partially cancel, more efficient |
| UBI / guaranteed income / welfare expansion | **0.75x** | Progressive overcrowding — retail prices political wish, not legislative reality |
| Psychedelics outside FDA approval context | **0.72x** | Clinical enthusiasm → retail overprices state/federal legalization by years |
| Cannabis / marijuana federal legalization | **0.70x** | Most consistently overpriced category — advocates have dominated YES since 1970 |

**The Cannabis Rule** deserves emphasis: federal cannabis legalization markets have resolved NO every single time since 1970. Retail prices them at 15–40% based on polling support, confusing public opinion with legislative probability. The federal base rate is near zero. Every federal cannabis legalization market is a structural NO.

**Factor 2 — US Legislative Calendar**

GovTrack documents that all US bills pass at ~3–5%. But this already-low rate varies sharply by calendar:

| Condition | Multiplier | Why |
|---|---|---|
| Odd year (non-election, Jan–Dec) | **1.00x** | Normal legislative session |
| Even year (election year, Jan–Jul) | **0.95x** | Campaigns ramping, normal-ish |
| Even year (election year, Aug–Dec) | **0.80x** | Pre-election gridlock — passage rates drop ~40–50% vs odd years |

This calendar multiplier only applies to legislative markets ("will Congress pass X", "will Senate vote on Y"). FDA approvals, HUD data releases, and similar non-legislative markets are unaffected.

The skill prints `election_gridlock=True/False` on startup so you always know which regime you're in. (2026 is a US midterm year — gridlock mode activates August 2026.)

### Combined Examples

| Market | Issue mult | Calendar mult | Final bias |
|---|---|---|---|
| "Will FDA approve MDMA therapy?" | 1.20x | 1.00x (not legislative) | **1.20x** |
| "Will Congress pass social media age bill?" (Sep 2026) | 1.15x | 0.80x (election gridlock) | **0.92x** |
| "Will federal cannabis be legalized?" (odd year) | 0.70x | 1.00x | **0.70x** |
| "Will federal cannabis be legalized?" (Sep 2026) | 0.70x | 0.80x | **0.56x** → floor |

### Keywords Monitored

```
mental health, suicide rate, drug legalization, cannabis, psychedelics,
loneliness, social media ban, teen smartphone, TikTok ban, gun control,
marijuana, psilocybin, FDA mental health, universal basic income, UBI,
poverty rate, homelessness, opioid, fentanyl, drug decriminalization,
safe injection, gun violence, background check, red flag law,
assault weapon, SNAP, welfare, Medicaid expansion, healthcare access
```

### Remix Signal Ideas

- **GovTrack.us API**: Bill stage progression (introduced → committee → floor) — committee advancement is the single strongest predictor of passage; feed bill stage into `p` to trade divergence from naive retail pricing
- **SAMHSA drug survey data**: Annual survey release dates for drug use and policy markets — data-release markets have known calendars retail ignores
- **Gallup social trends polling**: Long-run public opinion series for legalization and mental health — useful for calibrating YES_THRESHOLD per issue


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
| `SIMMER_MAX_SPREAD` | `0.12` | Max bid-ask spread (12%) — wider for niche policy markets |
| `SIMMER_MIN_DAYS` | `7` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `7` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
