---
name: polymarket-market-pulse
version: 1.0.2
description: Discover profitable prediction markets on Polymarket by comparing AI-estimated probabilities against market-implied odds. Identifies the top 3 markets with the highest edge, analyzes information flow, resolution clarity, liquidity, and volatility, and provides position sizing recommendations. Use when the user asks about Polymarket opportunities, prediction market bets, daily market pulse, market recommendations, or finding mispriced markets.
metadata: {"openclaw": {"emoji": "📊", "requires": {"bins": ["python3"]}}}
---

# Polymarket Market Pulse

Scan Polymarket for mispriced prediction markets. Estimate true probabilities using web research, compare against market odds, and recommend the top 3 most profitable opportunities with position sizing.

## Workflow

Execute the following 7 steps in order. Do not skip steps.

### Step 1: Fetch Market Data

Run the market fetcher script to pull active markets from the Polymarket Gamma API:

```bash
python scripts/fetch_markets.py --pages 5 --min-liquidity 5000
```

The script uses the `/events` endpoint (each event contains nested markets), paginating 5 pages per sort dimension (volume, liquidity, recency, competitive) at 50 events per page — scanning up to ~1,000 events. Results are automatically merged, deduplicated, and expanded into individual markets.

For a deep scan (e.g., comprehensive weekly review), use `--pages 20` to cover up to 4,000 events across all dimensions.

If the script fails (network error, API change), fall back to manual API calls. See [references/polymarket-api.md](references/polymarket-api.md) for endpoint details.

### Step 2: Screen Candidates

From the fetched markets, apply these filters to narrow down to 10-15 candidates.

Note: The script already auto-filters the following junk markets — no manual handling needed:
- Crypto up/down gambling markets (titles containing "Up or Down" or time-range formats)
- Markets expiring within 24 hours
- Coin flip markets (all outcome prices in the 0.48-0.52 range)

**Exclude:**
- Markets with max outcome price > 0.95 or min < 0.05 (too settled, no edge room)
- Markets with liquidity < $5,000 (too thin to trade)
- Markets where the question is ambiguous or unresearchable via web search

**Prioritize:**
- New markets (created within last 7 days) — less efficiently priced
- Markets with high 24h volume — signals active interest and information flow
- Markets on topics where web search can yield strong evidence

**Longshot Bias Scan (Important):**
Each analysis must specifically select 3-5 markets with Yes price < 20% and liquidity > $50k as "No scan" candidates.
The Yes side in these markets is likely overpriced — the No side is the most common source of systematic edge.

**Multi-Outcome Markets (Top-N Mispricing Scan):**
Some markets have more than 2 outcomes (e.g., elections, tournament winners). **Do not skip these markets.** Multi-outcome markets often have the deepest liquidity and most participants, but because the number of outcomes is high, individual outcomes tend to be less efficiently priced.

How to handle:
1. For each multi-outcome market, sum the implied probabilities of all outcomes (should be close to 100%). If the sum is significantly > 100%, there is systematic overpricing (vig) and the No side has an advantage.
2. Extract the 2-3 outcomes with the largest pricing deviation as candidates; skip the rest. Deviation is determined by comparing against a rough baseline probability from a quick web search — the outcomes with the largest deviation are the candidates.
3. Treat each selected outcome as an independent binary market — buy that outcome's Yes or No.
4. Use the corresponding outcome token's order book (from `clob_token_ids`) for liquidity analysis.
5. Note in report metadata: scanned N multi-outcome markets, extracted M outcome candidates.

### Step 3: Research & Estimate Probabilities

For each of the ~10 candidates, perform web research and form an independent probability estimate. This is the most critical step.

**Resolution Rules Retrieval (must be done before probability estimation):**

For each candidate that passed screening (~10 markets), you must retrieve the full resolution rules:

1. Use WebFetch to access `https://polymarket.com/event/{event_slug}`
2. Extract the complete Resolution Rules:
   - Basic resolution conditions (usually already in the API description)
   - **Additional context** (critical! These are rule clarifications added after market creation — the API may not return them)
   - Specific quantitative thresholds (e.g., "80% decrease", "3 consecutive days", etc.)
   - Official data sources (e.g., IMF PortWatch, Binance, CME, etc.)
   - Edge case handling
3. Store the extracted full rules and reference them directly during subsequent probability estimation
4. If WebFetch fails, fall back to the API description field, but flag in the report with "⚠️ Unable to retrieve full resolution rules"

**Why this step is mandatory:** The "Additional context" on market pages frequently contains quantitative thresholds and data source definitions added after market creation. These directly determine resolution outcomes. Relying solely on the API description (truncated to ~500 characters) leads to serious misestimation.

**Information sourcing (A1):**
- Run 2-3 targeted web searches per market
- Record every source URL and key finding
- Prioritize: official data > authoritative media > expert analysis > social sentiment

**Reasoning (A2):**
- Start with a base rate (historical frequency or market price as prior)
- Update with each piece of evidence (strong: 10-20% shift, moderate: 5-10%, weak: 1-5%)
- Assign confidence: High / Medium / Low
- **Longshot calibration**: For events with market price < 20%, default to assuming the market overestimates the Yes probability.
  Start from historical base rates, not from market price. Ask yourself: "How often do similar events
  actually occur within the given time window?" Usually far less often than the market implies.

For the full methodology, see [references/analysis-framework.md](references/analysis-framework.md).

### Step 4: Calculate Edge

For each candidate, compute:

```
Edge = AI_estimated_probability - market_implied_probability
```

Where `market_implied_probability` is the `outcome_prices` value from Step 1 (e.g., 0.35 = 35%).

**Selection criteria:**
- Edge > 20%: Strong signal — high-priority recommendation
- Edge 10-20%: Moderate — standard recommendation
- Edge 5-10%: Weak — mention only if other dimensions are strong
- Edge < 5%: Skip

**Composite score ranking (replaces pure edge sorting):**

```
Composite Score = |Edge| × log10(Liquidity + 1)
```

Example: Edge 20% + $10k liquidity = 0.20 × 4.0 = 0.80; Edge 10% + $500k liquidity = 0.10 × 5.7 = 0.57. Edge still dominates but extremely illiquid markets are penalized.

The market data includes a pre-computed `liquidity_score` field (= log10(liquidity + 1)) — use it directly.

**Hard floor:** Markets with liquidity < $5,000 must not enter the Top 3 recommendations.

Select the top 3 markets by composite score (minimum 10% edge).

**Monthly Return Estimation:**

For each candidate passing the edge threshold, compute:
1. Holding period `d`: from `end_date` if present; else 90 days (mark "assumed"). Floor at 7 days.
2. `expected_return = (p - c) / c`
3. `monthly_return = (1 + expected_return) ^ (30 / d) - 1`

Display in per-market analysis. Flag: d<7 → "illustrative only"; d>365 → "long lock-up"; no end_date → "(assumed 90d)".

**Longshot Bias Reminder:**
Statistical evidence shows that prediction markets with Yes < 20% systematically exhibit No-side edge.
The final Top 3 recommendations should include at least 1 "buy No" recommendation (if No-side edge genuinely exists).
Do not ignore these opportunities just because "buying No seems like small profit" — high win rate × appropriate sizing = steady returns.

### Step 4.5: Comments Validation

For the top 3 markets that passed Edge screening, perform comments validation. This is the final verification step for probability estimates, independent of the web research in Step 3.

**Retrieve Comments:**

For each Top 3 market, run the comments fetcher script to pull the 20 most recent holder comments from the Gamma API:

```bash
python3 scripts/fetch_comments.py --event-id <event_numeric_id> --limit 20
```

Where `event_numeric_id` is the event's numeric ID (from the `id` field returned by the `/events` endpoint, not the slug). You can also query by slug:

```bash
python3 scripts/fetch_comments.py --slug <event_slug> --limit 20
```

The script outputs JSON containing each comment's `author` (username), `body` (comment text), `created_at` (timestamp), `is_reply` (whether it's a reply), and `reaction_count` (likes).

If 0 comments are returned (some events genuinely have no comments), note "No user comments available for this market" in the report and skip comments validation for that market.

**Analysis Dimensions:**

Review each comment looking for these signals:

1. **News source citations:** Do comments cite news sources not covered in Step 3? If so, follow the link and verify.
2. **Quantitative analysis:** Do commenters provide specific data, statistics, or models? Is the logic sound?
3. **Insider information signals:** Do commenters hint at non-public information? (evaluate credibility carefully)
4. **Opposing viewpoints:** For comments opposing the current AI assessment — is their reasoning sound? Do they cite overlooked evidence?
5. **Resolution rule discussions:** Are commenters debating ambiguities in resolution criteria? Do these discussions reveal potential risks?

**Probability Adjustment:**

- If comments reveal substantive new information not covered in Step 3 → re-evaluate probability
- If comments show widespread dispute over resolution criteria → lower confidence level
- If multiple holders' reasoning consistently supports a direction with sound logic → use as corroboration (not decisive)
- If no substantive new information found → maintain original assessment

**Output Requirements:**

Add a "Comments Validation" section in the report for each recommended market, documenting the validation results.
If validation leads to a probability adjustment, annotate the revised probability with "(adjusted after comments validation: was XX% → now YY%)".

### Step 5: Analyze Liquidity & Size Position

For each of the top 3 markets, fetch the order book:

```bash
python scripts/fetch_orderbook.py <token_id> --slippage 0.02
```

Pass the `clob_token_ids` from the market data. For a Yes bet, use the first token ID; for No, use the second.

The script outputs:
- Bid/ask spread and midpoint
- Maximum executable order size within 2% slippage
- Liquidity tier and suggested position range

**Quarter-Kelly Position Sizing:**

For each top 3 market:
1. `f* = (p - c) / (1 - c)` — p = AI win prob for chosen side, c = entry price for chosen side
2. `f_q = f* / 4`
3. `kelly_amount = f_q × bankroll` (default bankroll $10,000; use user-specified if provided)
4. `liquidity_cap = 0.10 × buy_capacity.max_cost_usd`
5. `position = min(kelly_amount, liquidity_cap)`

6. `position_pct = position / bankroll` (the percentage of bankroll to allocate)

Display: Full Kelly %, Quarter Kelly %, Kelly Amount (% → $), Liquidity Cap (% → $), **Recommended Size as % of bankroll** (with $ equivalent).

Safety: if p ≤ c → Kelly ≤ 0, do not recommend. Cap f* display at 100%.

### Step 6: Generate Report

Format the final output using the template in [references/output-template.md](references/output-template.md).

Each of the 3 recommended markets must include:
1. Market link (`https://polymarket.com/event/{event_slug}`, using the event-level slug, not the market slug)
2. Current implied probability and spread
3. AI estimated probability, confidence level, and edge
4. Four-dimensional analysis (information flow, resolution clarity, liquidity, volatility) — each scored 1-5 with a brief explanation
5. Position recommendation (direction, size range, limit price, order strategy)
6. Complete list of information sources with URLs and key takeaways

**Timestamp Requirements (Important):**
- Report header: Record report generation time and market data fetch time
- Each market: Record market data time and AI assessment time
- Each source: Record information retrieval time
- All timestamps in UTC timezone, format: `YYYY-MM-DD HH:MM:SS`

### Step 7: Save Report File

Save the complete report as a Markdown file:

```bash
mkdir -p ~/polymarket-reports
```

**File path:** `~/polymarket-reports/market-pulse-{YYYY-MM-DD}-{HHMMSS}.md`

Use the Write tool to save the report to the above path. Confirm the file path to the user after saving.

**Example filename:** `market-pulse-2026-02-23-134500.md`

**Append to Recommendation History:**

After saving the report, append to `~/polymarket-reports/recommendation-history.md`:

1. If file doesn't exist, create with header:

| Date | Market | Link | Direction | Entry Price | AI Prob | Edge | Full Kelly | 1/4 Kelly | Position | Mo. Return | End Date | Status |
|------|--------|------|-----------|-------------|---------|------|-----------|-----------|----------|------------|----------|--------|

2. Append 1 row per recommended market (3 rows per run). Market question truncated to 50 chars. Link column contains the Polymarket event URL (e.g., `https://polymarket.com/event/{slug}`).
3. Never overwrite — always append.
4. Read file first to verify header exists, then append rows.

**Terminal Summary Output (Important):**

After saving the report, output a concise summary to the terminal (not to the file) for the user. **Must include clickable links.**

Format for each of the Top 3 recommended markets:
```
### {rank}. {market_question} — {direction} @ {entry_price}
- **Link:** https://polymarket.com/event/{event_slug}
- **Edge:** {edge} | AI {ai_prob}% vs Market {market_prob}% | Confidence: {confidence}
- **Recommended Size:** {position} ({position_pct}% of bankroll)
- **EMR:** {monthly_return}% ({d}d)
```

Then output a **Candidate Pool Overview** table with Top 3 + next 5 (8 total), sorted by composite score:

```
| # | Market | Dir | Mkt | AI | Edge | EMR | Link |
|---|--------|-----|-----|-----|------|-----|------|
| 1 | {question, truncated 50 chars} | {Buy Yes/No} | {market}% | {ai}% | {+X%} | {X%} | [link](https://polymarket.com/event/{slug}) |
| ... | ... | ... | ... | ... | ... | ... | ... |
| 8 | ... | ... | ... | ... | ... | ... | ... |
```

Note: EMR = Estimated Monthly Return. Markets #4-8 have not undergone deep liquidity analysis or comments validation — for reference only.

## Troubleshooting

- **Script returns empty results**: Lower `--min-liquidity` threshold or increase `--pages` (e.g., `--pages 20`) to scan more markets
- **Fetching is slow**: `--pages 20` makes 80 API calls (20 pages × 4 dimensions), taking ~30-40 seconds. Use `--pages 5` to speed up
- **Order book fetch fails**: The token ID may be invalid; verify via Gamma API that `enableOrderBook` is true
- **Few markets pass screening**: Relax the edge threshold to 5% or include markets with moderate edge but strong liquidity
- **`--limit` flag**: Deprecated but still accepted — automatically mapped to `--pages`

## Reference Files

- [references/polymarket-api.md](references/polymarket-api.md) — Full API endpoint documentation
- [references/analysis-framework.md](references/analysis-framework.md) — Detailed A1/A2/B1/B2 methodology
- [references/output-template.md](references/output-template.md) — Report formatting template
