---
name: kalshi-fed-speech-signal-trader
description: Trades Fed rate markets on Kalshi based on hawkish/dovish sentiment signals from market question text. Scores net sentiment from keyword dictionaries and adjusts rate cut probabilities. Requires SIMMER_API_KEY and simmer-sdk.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Kalshi Fed Speech Signal Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Kalshi Fed Speech Signal Trader

> **This is a template.**
> The default signal uses static keyword dictionaries -- remix it with NLP sentiment models, live Fed speech transcripts via FRED API, or real-time news feeds.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Fed speeches contain hawkish and dovish signals that predict rate decisions. This skill scores net sentiment from keyword matching on market question text, then adjusts the fair probability of a rate cut. When the adjustment creates a gap vs. rate cut market prices, it trades.

Key advantages:
- **No external data needed** -- extracts signal from market question text itself
- **Extensible** -- add new keywords, adjust weights, or plug in NLP models
- **Cross-signal aggregation** -- pools sentiment across all Fed-related markets

## Signal Logic

### Sentiment Scoring

1. Scan all Fed rate market questions for hawkish/dovish keywords
2. Weight matches (some keywords stronger signals than others)
3. Compute net sentiment: dovish_total - hawkish_total
4. Adjust baseline cut probability by 5% per net unit
5. Trade rate cut markets when `|fair - market| >= entry_edge`

### Keyword Dictionaries

**Hawkish** (reduce cut probability): "inflation persistent", "tightening", "restrictive", "price stability", "higher for longer", etc.

**Dovish** (increase cut probability): "data dependent", "labor softening", "gradual", "balanced", "appropriate to reduce", etc.

### Conviction-Based Sizing

- `conviction = min(|edge| / entry_edge, 2.0) / 2.0`
- `size = max($1.00, conviction * MAX_POSITION_USD)`
- Larger edge = larger position, capped at MAX_POSITION_USD

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Entry edge | 10% | Min fair-vs-market divergence to trade |
| Exit threshold | 45% | Sell when position price reaches this |
| Max position size | $5.00 USDC | Per market |
| Max trades per run | 3 | Rate limiting |
| Max slippage | 15% | Skip if slippage exceeds |
| Min liquidity | $0 | Disabled by default |

## Installation & Setup

```bash
clawhub install kalshi-fed-speech-signal-trader
```

Requires: `SIMMER_API_KEY` and `SOLANA_PRIVATE_KEY` environment variables.

## Cron Schedule

Cron is set to `null` -- the skill does not run on a schedule until you configure it in the Simmer UI.

## Safety & Execution Mode

**The skill defaults to dry-run mode. Real trades only execute when `--live` is passed explicitly.**

| Scenario | Mode | Financial risk |
|----------|------|----------------|
| `python trader.py` | Dry run | None |
| Cron / automaton | Dry run | None |
| `python trader.py --live` | Live (Kalshi via DFlow) | Real USDC |

## Required Credentials

| Variable | Required | Notes |
|----------|----------|-------|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as a high-value credential. |
| `SOLANA_PRIVATE_KEY` | Yes | Base58-encoded Solana private key for live trading. |

## Tunables (Risk Parameters)

| Variable | Default | Purpose |
|----------|---------|---------|
| `SIMMER_FED_SPEECH_ENTRY_EDGE` | `0.10` | Min divergence to trigger trade |
| `SIMMER_FED_SPEECH_EXIT_THRESHOLD` | `0.45` | Sell position when price reaches this level |
| `SIMMER_FED_SPEECH_MAX_POSITION_USD` | `5.00` | Max USDC per trade |
| `SIMMER_FED_SPEECH_MAX_TRADES_PER_RUN` | `3` | Max trades per execution cycle |
| `SIMMER_FED_SPEECH_SLIPPAGE_MAX` | `0.15` | Max slippage before skipping trade |
| `SIMMER_FED_SPEECH_MIN_LIQUIDITY` | `0` | Min market liquidity USD (0 = disabled) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
