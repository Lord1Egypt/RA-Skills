---
name: polymarket-ai-tech-trader
description: Trades Polymarket prediction markets on AI model releases, tech IPOs, product launches, GPU infrastructure milestones, and AI regulation events. Use when you want to capture alpha on the dominant market theme of 2026 — AI and technology — using model benchmark feeds and tech press signals.
metadata:
  author: Diagnostikon
  version: '1.0'
  displayName: AI & Tech Launch Trader
  difficulty: advanced
---

# AI & Tech Launch Trader

> **This is a template.**
> The default signal is keyword discovery + LMSYS Chatbot Arena leaderboard monitoring — remix it with AI benchmark APIs (MMLU, HumanEval), tech news RSS feeds, SEC EDGAR filings for IPO signals, or GitHub commit activity as model release early warning.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

AI markets are the fastest-growing category on Polymarket in 2026. AI investment drove >90% of US GDP gains in H1 2025. This skill trades:

- **AI model benchmarks** — Which company leads LMSYS rankings at a given date
- **Model releases** — GPT-5, Claude 4, Gemini Ultra release/performance questions
- **Tech IPOs** — OpenAI, Databricks, Stripe IPO announcement markets
- **Product launches** — Apple Vision Pro 2, Tesla FSD milestones, Tesla Optimus
- **AI regulation** — EU AI Act enforcement, US federal AI legislation
- **Infrastructure** — NVIDIA datacenter revenue, H100 deployment counts

Key insight: AI news cycles are fast and retail trades on headlines. Informed traders with benchmark data have significant edge.

## Signal Logic

### Default Signal: Benchmark Divergence + News Catalyst

1. Discover active AI/tech markets on Polymarket
2. Monitor LMSYS Chatbot Arena for ranking shifts
3. Monitor Hugging Face Open LLM Leaderboard for benchmark updates
4. Compare quantitative model performance data vs market implied probability
5. When a model clearly leads benchmarks but market hasn't repriced, enter
6. For IPO markets: monitor SEC Form S-1 EDGAR filings as leading indicator

### Remix Ideas

- **GitHub API**: Watch for sudden commit activity/new repo creation on known model orgs
- **Perplexity/Google Trends**: Rising AI search terms as momentum signal
- **HuggingFace API**: Model download counts as proxy for adoption
- **SEC EDGAR**: Automated S-1 filing alerts for IPO markets
- **NVIDIA earnings call transcripts**: Forward guidance vs market pricing on infrastructure markets

## Market Categories Tracked

```python
AI_TECH_KEYWORDS = [
    "AI", "GPT", "Claude", "Gemini", "OpenAI", "Anthropic", "Google",
    "model", "benchmark", "AGI", "ChatGPT", "LLM",
    "IPO", "valuation", "Stripe", "Databricks", "SpaceX IPO",
    "Apple", "Vision Pro", "Tesla FSD", "Optimus", "robot",
    "NVIDIA", "GPU", "H100", "datacenter", "quantum",
    "EU AI Act", "regulation", "congress"
]
```

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Max position size | $40 USDC | High-liquidity markets allow larger size |
| Min market volume | $10,000 | AI markets are deeply liquid |
| Max bid-ask spread | 6% | Tight spreads expected in popular markets |
| Min days to resolution | 5 | News cycles move fast |
| Max open positions | 10 | AI/tech is broad category |

## Edge Opportunities

### Retail Recency Bias
After a major AI announcement (e.g., GPT-5 release), retail traders overweight recency and push other company markets down more than warranted. Fade the overreaction on competing platforms.

### Benchmark Lag
Markets often price on last-known model rankings. When a new benchmark publishes at ~midnight UTC, markets take 1–4 hours to fully reprice. Tight monitoring loop captures this window.

## Installation & Setup

```bash
clawhub install polymarket-ai-tech-trader
```

Requires: `SIMMER_API_KEY` environment variable.

## Cron Schedule

Runs every 5 minutes (`*/5 * * * *`). AI news breaks around the clock; tightest loop of all category skills.

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
| `SIMMER_MAX_POSITION` | `40` | Max USDC per trade (full conviction) |
| `SIMMER_MIN_TRADE` | `5` | Min USDC per trade (weak conviction floor) |
| `SIMMER_MIN_VOLUME` | `10000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.06` | Max bid-ask spread (0.10 = 10%) |
| `SIMMER_MIN_DAYS` | `5` | Min days until market resolves |
| `SIMMER_MAX_POSITIONS` | `10` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market probability ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market probability ≥ this value |

### Conviction-based position sizing

Position size scales automatically with signal strength — no flat bets.

- At the threshold boundary (e.g. p=38% for YES): minimum trade (`SIMMER_MIN_TRADE`, default $5)
- At maximum conviction (p=0% for YES, p=100% for NO): full position (`SIMMER_MAX_POSITION`, default $40)
- Everything in between scales linearly

**Example YES trades:**

| Market probability | Conviction | Size |
|--------------------|------------|------|
| 38% (at threshold) | 0% | $5 (floor) |
| 30% | 21% | $8 |
| 20% | 47% | $19 |
| 5% | 87% | $35 |
| 0% | 100% | $40 |

This means the skill automatically bets more when the edge is larger, and less when the signal is marginal.

