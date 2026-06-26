---
name: portfolio-review-polymarket
version: 1.0.2
description: Review Polymarket portfolio using EV-maximizing framework. Fetches current positions, updates probabilities via web research, applies hold/sell/rotate logic. Use when user asks to review portfolio, evaluate positions, or optimize holdings.
metadata: {"openclaw": {"emoji": "🔍", "requires": {"bins": ["python3"]}}}
---

# Polymarket Portfolio Review

Review your Polymarket portfolio using an EV-maximizing framework. For each position, update probabilities with fresh web research, compute daily expected returns, rank positions, and produce hold/sell/rotate decisions.

**Core Principle:** Holding a position each day = implicitly re-buying at today's price. Entry price is a sunk cost. The only thing that matters is current edge.

## Workflow

Execute the following 6 steps in order. Do not skip steps.

### Step 1: Read Portfolio Configuration

Read the portfolio configuration file to determine the user's wallet mode:

```
~/polymarket-reports/portfolio-address.md
```

This file contains:
- `username` — display name for reports
- `wallet_address` — Polymarket wallet address (0x...)

**If the file does not exist:**
1. Ask the user: "Do you have a Polymarket wallet address, or should I use paper portfolio mode (based on recommendation history)?"
2. If wallet address provided → proceed with wallet mode
3. If paper mode → use `--from-history` with recommendation-history.md

### Step 2: Fetch Current Positions

Run the portfolio fetcher script:

**Wallet mode:**
```bash
python3 scripts/fetch_portfolio.py --address 0xYourWalletAddress --output /tmp/portfolio-positions.json
```

**Paper mode (default — based on latest 9 recommendations):**
```bash
python3 scripts/fetch_portfolio.py --from-history ~/polymarket-reports/recommendation-history.md --latest 9 --output /tmp/portfolio-positions.json
```

The script:
1. Parses recommendation history or fetches wallet positions
2. Deduplicates same-market recommendations (aggregates position size, weighted average entry price)
3. Matches each position to an event slug via fuzzy text matching
4. Fetches current prices from Polymarket CLOB Midpoint API
5. Computes P&L, days remaining, and position details
6. Outputs structured JSON

**Default paths:** `--reports-dir ~/polymarket-reports/`

If the script fails, check:
- Network connectivity to `gamma-api.polymarket.com` and `clob.polymarket.com`
- That `recommendation-history.md` exists and has the expected table format
- That at least some `market-pulse-*.md` reports exist with `polymarket.com/event/` URLs

### Step 3: Save Holdings Snapshot

Read the JSON output from Step 2. Format the holdings data and save as a snapshot file:

**File path:** `~/polymarket-reports/portfolio-holding-{YYYY-MM-DD}-{HHMMSS}.md`

The snapshot should include:
- Timestamp and portfolio mode
- Summary table (total invested, current value, P&L)
- Position table with all fields from the JSON

This snapshot serves as a historical record of portfolio state at review time.

### Step 4: Research & Update Probabilities

**This is the most critical step.** For each position, perform fresh web research and form an updated probability estimate.

For each position:

1. **Web Search (2-3 queries):**
   - Search for the latest news related to this event
   - Search for any upcoming catalysts or deadlines
   - Prioritize: official data > authoritative media > expert analysis

2. **Update Probability (p_now):**
   - Start from the current market price as prior
   - Update with each piece of evidence (strong shift: 10-20%, moderate: 5-10%, weak: 1-5%)
   - Assign confidence level: High / Medium / Low

3. **Event-Level Thinking (mandatory):**
   - What has changed since the position was opened?
   - Is the original thesis still intact?
   - What upcoming catalysts could move this market?
   - Are there new risks not reflected in the price?

Record all sources with URLs and retrieval timestamps.

For the full EV-maximizing framework, see [references/review-framework.md](references/review-framework.md).

### Step 5: Apply Review Framework & Generate Report

For each position, compute:

```
edge = p_now - c_now
daily_expected_return = (p_now - c_now) / (c_now × d_remaining)
f* = (p_now - c_now) / (1 - c_now)
f_q = f* / 4
```

Where:
- `p_now` = updated probability estimate (from Step 4)
- `c_now` = current market price (your side's price)
- `d_remaining` = days until market resolution

**Apply the decision tree:**

1. If edge ≤ 0 → **SELL** (edge reversed)
2. If thesis broken → **SELL** (regardless of edge)
3. If daily_er < 0.02% AND better opportunity exists → **ROTATE**
4. If position > 25% of bankroll → trim (over-concentrated)
5. If total theme > 40% of bankroll → trim theme exposure
6. Otherwise → **HOLD**

**Rank all positions** by daily expected return (highest first).

**Daily ER interpretation:**
| Daily ER | Rating |
|----------|--------|
| > 0.50% | Excellent |
| 0.10% – 0.50% | Good |
| 0.02% – 0.10% | Marginal |
| < 0.02% | Capital-inefficient |
| Negative | Sell |

**Rotation friction:** Only recommend rotation if the new position's daily_er exceeds the current by at least 0.05%/day (to cover ~2-4% spread/slippage).

**Portfolio-level checks:**
- Total quarter-Kelly (f_q) sum ≤ 100%
- Single theme ≤ 40% of bankroll
- Expiry date diversification
- Action summary with priority ordering

Format the report using the template in [references/output-template.md](references/output-template.md).

### Step 6: Save Report

Save the complete review report as Markdown:

```bash
mkdir -p ~/polymarket-reports
```

**File path:** `~/polymarket-reports/portfolio-review-report-{YYYY-MM-DD}-{HHMMSS}.md`

Use the Write tool to save the report. Confirm the file path to the user after saving.

**Example filename:** `portfolio-review-report-2026-02-27-030000.md`

## Troubleshooting

- **Script returns empty positions**: Check that recommendation-history.md has Open positions. If using `--latest 9`, try without the flag to include all open positions.
- **Many unmatched positions**: The slug matching depends on pulse report files. If reports were deleted, the script cannot extract slugs. Manually search Polymarket for the market name.
- **Midpoint returns None**: Market may be very illiquid or CLOB API may be down. The script falls back to Gamma API `outcomePrices`.
- **Aggregation seems wrong**: The script groups by normalized market name + direction. Check that similar market names are correctly grouped.
- **No portfolio-address.md**: This is normal for first-time users. Default to paper mode using recommendation history.

## Reference Files

- [references/review-framework.md](references/review-framework.md) — EV-maximizing decision framework
- [references/output-template.md](references/output-template.md) — Report formatting template
- [references/polymarket-api.md](references/polymarket-api.md) — Full API endpoint documentation
