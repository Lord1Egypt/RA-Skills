# Rally Research and Scoring

Read this file before `rally.universe.refresh`, `rally.research.signals`, or `rally.candidates.rank`.

---

## Universe Filtering

**Default universe:** US-listed equities meeting all of the following:
- Market cap >= `config.universe.min_market_cap_bn` billion (default: $2B)
- 30-day average daily volume >= `config.universe.min_adv_mn` million (default: $5M)
- Primary listing on NYSE, NASDAQ, or NYSE American

**Excluded by default:**
- SPACs (Special Purpose Acquisition Companies)
- BDCs (Business Development Companies)
- Closed-end funds and interval funds
- Foreign private issuers and ADRs (unless `config.universe.include_foreign: true`)
- Securities under active delisting review or trading halt

**Sector diversification:** No single GICS sector may exceed `config.constraints.max_sector_pct` (default: 30%) of the portfolio by target weight. During candidate selection, if adding the next-ranked candidate would breach the sector cap, skip it and take the next eligible candidate. Log skipped candidates with reason `"sector_cap_breach"` in `decisions.jsonl`.

**Market cap floor adjustment:** Market cap floor can be reduced to $1.0B if `config.position_sizing` is `"score_vol_weighted"` — the inverse-volatility weighting controls risk contribution from higher-vol small-caps. If `position_sizing` is `"score_weighted"` or `"equal_weight"`, the floor must remain >= $2.0B. Validate this constraint during `rally.init` and `rally.validate`.

**Data source:** Use whatever price and fundamental data source is available and configured. Acceptable defaults: Yahoo Finance, Polygon.io, Alpha Vantage. Document the source in `evidence_refs` for every candidate.

---

## Factor Model

Rally uses a Quality-Momentum strategy with a Fundamental Safety gate, a short-term Reversion signal, and an optional Congressional Flow signal. Five signal categories with explicit default weights:

| Category | Default Weight | Purpose |
|---|---|---|
| Quality | 40% (`config.scoring.quality_weight`) | Identify financially durable businesses |
| Momentum | 20% (`config.scoring.momentum_weight`) | Favor stocks being rewarded by the market |
| Fundamental Safety | 25% (`config.scoring.safety_weight`) | Screen out value traps and deteriorating businesses |
| Reversion | 10% (`config.scoring.reversion_weight`) | Reward short-term pullbacks in otherwise strong names |
| Congressional Flow | 5% (`config.scoring.congressional_flow_weight`) | Detect unusual clustering of congressional trading as a catalyst signal |

Weights are configurable. They must sum to 1.0. If `congressional_flow.enabled` is false, redistribute its 5% to Momentum (making Momentum 25%).

---

### Quality Signals (40%)

Computed from trailing 12-month financial data:

| Signal | Description | Direction |
|---|---|---|
| ROE | Return on equity (net income / avg shareholders equity) | Higher is better |
| Operating margin | Operating income / revenue | Higher is better |
| Debt/equity ratio | Total debt / shareholders equity | Lower is better |
| FCF margin | Free cash flow / revenue | Higher is better |

Score each signal independently as a z-score within the current universe, then average the four z-scores to produce the category score.

---

### Momentum Signals (20%)

Computed from price history:

| Signal | Description | Direction |
|---|---|---|
| 6-month return | Price return over months T-7 to T-1 (exclude most recent month) | Higher is better |
| 12-month return | Price return over months T-13 to T-1 (exclude most recent month) | Higher is better |
| Relative strength vs. SPY | 6-month return minus SPY 6-month return over same period | Higher is better |
| Path quality | Smoothness of the 6-month price path (R-squared of linear regression on daily closes over months T-7 to T-1) | Higher is better |

Exclude the most recent calendar month from all momentum windows. This avoids short-term reversal effects where recent strong performers temporarily mean-revert.

Path quality measures how linear the price trend is. Compute an ordinary least squares regression of daily closing prices over the 6-month momentum window. The R-squared value (0 to 1) becomes the path quality signal.

Interpretation: R-squared near 1.0 = steady grind higher (institutional accumulation). R-squared near 0 = choppy, news-driven, or pump-and-dump price action.

Score each signal independently as a z-score (including path quality), then average all four z-scores to produce the category score.

---

### Fundamental Safety Signals (25%)

Used as a gate to penalize or exclude structurally broken businesses:

| Signal | Description | Scoring |
|---|---|---|
| P/E vs. sector median | Forward P/E divided by sector median forward P/E | Penalty if ratio >1.5x; full exclusion if ratio >3.0x or P/E is negative |
| Revenue growth trend | 3-year compound annual revenue growth rate | Higher is better; negative CAGR applies a penalty |
| Earnings consistency | Number of EPS misses in last 4 reported quarters | 0 misses = full score; 1 miss = moderate penalty; 2+ misses = disqualify |

The fundamental safety score is computed as a weighted average of the three component scores. A candidate that fails the P/E exclusion threshold or the earnings consistency disqualifier is removed from the AllocationPlan but may remain in ResearchCandidate records for reference.

---

### Reversion Signal (10%)

Captures short-term mean reversion to improve entry timing on momentum candidates.

| Signal | Description | Direction |
|---|---|---|
| 5-day RSI z-score (inverted) | RSI(5) computed for each candidate, z-scored across universe, then multiplied by -1 | Lower RSI = higher reversion score |

Procedure:
1. Compute 5-day RSI for each candidate (`config.scoring.reversion_lookback_days`, default: 5)
2. Z-score the RSI values across all candidates in the current universe
3. Invert: `reversion_z = -1 * rsi_z` (so oversold candidates score highest)
4. The category score is the single inverted z-score (no averaging needed, single signal)

Interpretation: A stock with strong Quality + Momentum scores AND a low recent RSI is a high-conviction entry — the market is temporarily pulling back on a structurally sound name.

---

### Congressional Flow Signal (5%)

Detects unusual clustering of stock trades disclosed by members of Congress under the STOCK Act. Used as a supplementary conviction signal, not a trade-copying mechanism.

Data source: Configured via `config.congressional_flow.api_source`. Default: QuiverQuant API (requires `QUIVERQUANT_API_KEY`). Alternatives: Finnhub (premium), Senate/House Stock Watcher (free, less reliable).

| Signal | Description | Direction |
|---|---|---|
| Net congressional flow (30-day) | Distinct buyers minus sellers over lookback window, with optional committee relevance weighting and cluster bonus | Higher net buy flow = higher score |

Procedure:
1. For each candidate, query the configured API for congressional trades in the trailing `config.congressional_flow.flow_lookback_days` (default: 30).
2. Count distinct members who bought vs. sold.
3. If committee membership data is available, apply `committee_relevance_multiplier` (default: 1.5x) to trades where the member's committee has jurisdiction over the stock's GICS sector.
4. Compute `net_flow = weighted_buyers - weighted_sellers`.
5. If 3+ distinct members traded the same direction (`cluster_threshold`), multiply net_flow by `cluster_bonus_multiplier` (default: 1.5x).
6. Z-score net_flow across the universe.
7. The z-score is the category score (single signal, no averaging needed).

Data freshness requirement: If the most recent data from the configured source is older than `config.congressional_flow.max_data_age_days` (default: 3), skip the signal entirely for this run. Set congressional_flow_score to null for all candidates. Log `"congressional_flow_stale"` in `decisions.jsonl`. Redistribute the 5% weight to Momentum for that run only.

Filing lag note: STOCK Act filings arrive 2-45 days after the actual trade. This signal captures legislative conviction and potential awareness of upcoming catalysts, not real-time flow. Treat it as a medium-term directional indicator, not a timing tool.

---

## Normalization

### Step 1: Sector-relative z-scores
For each signal, compute z-scores within each GICS sector:
  `z_sector = (x - sector_mean) / sector_stdev`
Winsorize at ±2.5 standard deviations.

Minimum sector size for intra-sector z-scoring: `config.scoring.min_sector_size` (default: 5) candidates. If a sector has fewer than 5 candidates, use universe-wide z-scores for that sector's members.

### Step 2: Universe-wide z-scores
Also compute z-scores across the full universe as before:
  `z_universe = (x - universe_mean) / universe_stdev`
Winsorize at ±2.5.

### Step 3: Blended z-scores
  `z_blended = sector_blend_weight * z_sector + (1 - sector_blend_weight) * z_universe`

Default `config.scoring.sector_blend_weight`: 0.50. This ensures top-of-sector names in out-of-favor sectors still surface, while preventing hot-sector names from dominating purely on sector tailwinds.

### Step 4: Category and composite scores
Compute category scores as average of blended z-scores within each category.

```
composite = (quality_weight * quality_score) + (momentum_weight * momentum_score) +
            (safety_weight * safety_score) + (reversion_weight * reversion_score) +
            (congressional_flow_weight * congressional_flow_score)
```

If `congressional_flow_score` is null (data unavailable or stale), omit the term and redistribute its weight to `momentum_weight` for that scoring run.

### Step 5: Percentile ranks
Convert composite scores to percentile ranks within the universe (0.0 = lowest, 1.0 = highest). Store both the raw composite z-score and the final percentile rank in `signals.jsonl`.

---

## Realized Volatility

For each candidate passing universe filters, compute:

```
daily_log_return_t = ln(close_t / close_{t-1})
realized_vol = stdev(daily_log_returns over lookback window) * sqrt(252)
```

Lookback window: `config.position_sizing_options.vol_lookback_days` (default: 60).
Minimum data requirement: `config.position_sizing_options.vol_min_days` (default: 20).

Store `realized_vol` in `signals.jsonl` alongside other signal data. If fewer than `vol_min_days` of returns are available, set `realized_vol` to null and flag the candidate as ineligible for allocation (confidence effectively 0 for sizing purposes).

---

## Confidence Scoring

Assign a confidence value to each candidate based on data completeness:

| Condition | Confidence |
|---|---|
| All signals present across all five categories | 1.0 |
| Missing Reversion alone OR Congressional Flow alone | 1.0 (supplementary signals) |
| Missing 1-2 non-critical signals in primary categories (minor data gaps) | 0.75 |
| Missing Reversion + another primary category signal | 0.75 |
| Missing all signals in Quality OR Momentum category | 0.5 |
| Missing all signals in both Quality and Momentum | Exclude |

Congressional Flow missing never reduces confidence (it is a supplementary signal with intermittent availability). Reversion missing alone also does not reduce confidence; however, missing Reversion combined with other missing signals follows the standard degradation.

**Confidence floor:** Candidates with confidence below `config.scoring.confidence_floor` (default: 0.40) are excluded from AllocationPlan generation. They may still appear as ResearchCandidate records with a note indicating exclusion reason.

---

## Missing Data Policy

- Never impute or assume missing values
- If a signal is unavailable, omit it from that candidate's category score computation; note the missing signal in `evidence_refs`
- If a full category is unavailable, record the category score as null and apply the confidence downgrade above
- Document data source and retrieval timestamp in `evidence_refs` for every signal that is successfully obtained

---

## Sentiment (Optional Enrichment)

Sentiment signals (analyst consensus, news tone, earnings revision direction) are not part of the default scoring model. They require real-time data sources that may not always be available.

If `config.scoring.sentiment_weight` is set and sentiment data is available via Sift enrichment, sentiment may be incorporated as an additional category. When enabled, redistribute weights proportionally so all categories continue to sum to 1.0. Never include sentiment if data freshness is >72 hours.

---

## Factor Decay Monitor

When `config.factor_monitor.enabled` is true, after each `rally.research.signals` run:

1. Compute the Information Coefficient (IC) for each scoring category:
   IC = rank correlation (Spearman) between the category's signal scores at time T and the subsequent forward returns over the next rebalance period.

2. Maintain a rolling window of IC values over the last `ic_lookback_runs` (default: 30 runs).

3. If any factor's rolling average IC drops below `alert_threshold_ic` (default: 0.0) for more than `alert_consecutive_days` (default: 60 calendar days), emit a warning in the daily report:

   `"FACTOR DECAY ALERT: [Category] IC has been at or below [threshold] for [N] days. Consider reducing this factor's weight or investigating regime-specific factor rotation."`

4. Log factor IC values in `signals.jsonl` alongside the scoring data for auditability.

This is advisory only — it does not automatically adjust weights. Weight changes require explicit user action.
