# Rally Operating Model

Read this file before running the full ingest-to-report loop or before `rally.plan.allocation`, `rally.plan.trade`, or `rally.execute.trades`.

---

## Loop

1. Ingest portfolio state (`rally.ingest.portfolio`)
2. Refresh investable universe (`rally.universe.refresh`)
3. Compute signals and rankings (`rally.research.signals`)
4. Check rebalance triggers -- if none fire, proceed to step 7
5. Generate constrained allocation plan (`rally.plan.allocation`)
6. Derive trade plan from deltas (`rally.plan.trade`)
7. Optionally execute (if enabled) (`rally.execute.trades`)
8. Produce reports (`rally.report.daily` / `rally.report.monthly`)

---

## Execution Gate

Execution requires all three conditions to be true:
1. `config.execution.enabled: true`
2. `config.execution.broker_integration` is set to a valid broker identifier
3. Explicit user approval for the specific trade plan (never automatic)

Default state: disabled. Rally is fully useful as a research and planning tool without execution.

---

## Benchmark

Default benchmark: `config.benchmark` (default: `"SPY"`).

The benchmark is used for:
- **Relative strength signal:** momentum category includes return vs. SPY over the same 6-month window
- **Decision accuracy OKR:** "outperforming benchmark" means the position's return exceeds SPY's return over the same holding period
- **Sharpe ratio OKR:** risk-adjusted return computed relative to benchmark return as the risk-free proxy
- **Monthly attribution:** report shows portfolio return vs. benchmark return with factor contribution breakdown

Change the benchmark in `config.json` if a different index better represents the investment mandate (e.g., `"QQQ"` for tech-tilted portfolios, `"IWM"` for small-cap mandates).

---

## Market Regime Filter

Before generating any AllocationPlan, compute a composite regime score from four signals.

### Regime signals

Each signal is scored 0.0 to 1.0:

| Signal | Data source | 1.0 (Bullish) | 0.5 (Neutral) | 0.0 (Bearish) |
|---|---|---|---|---|
| Trend | Benchmark close vs SMA-200 | Above and SMA rising (20d slope > 0) | Above but SMA flat or falling | Below SMA-200 |
| Credit | ICE BofA HY OAS (or `config.regime.credit.source`) | Spread < `bullish_ceiling_bp` (350) | Between bullish_ceiling and bearish_floor | Spread > `bearish_floor_bp` (500) |
| Volatility | VIX front-month vs second-month futures | Contango > `contango_threshold_pct` (5%) | Flat (within +/- threshold) | Backwardation (front > second) |
| Breadth | % of index constituents above their 50-day MA | > `bullish_floor_pct` (65%) | Between bearish_ceiling and bullish_floor | < `bearish_ceiling_pct` (40%) |

### Composite and regime mapping

```
composite_regime = sum(signal_i * weight_i) for i in configured signals
```

| Composite | Regime | Cash target |
|---|---|---|
| >= `normal_floor` (0.65) | Normal | `config.cash.normal_pct` (5%) |
| >= `cautious_floor` (0.40) and < `normal_floor` | Cautious | `config.cash.cautious_pct` (15%) |
| < `cautious_floor` (0.40) | Defensive | `config.cash.defensive_pct` (30%) |

### Confidence floor adjustment

When regime is Cautious or Defensive, override the scoring confidence floor to `config.regime.elevated_confidence_floor` (default: 0.55). This concentrates capital in highest-conviction names during stress.

### Regime transitions

When moving from Defensive or Cautious back to Normal, deploy no more than `config.regime.reentry_deploy_max_pct` (default: 50%) of excess cash per rebalance cycle. This prevents buying a dead-cat bounce.

### Data availability fallback

If any signal's data source is unavailable:
- Use the most recent cached value if < 3 trading days old
- If stale > 3 days, drop the signal and re-weight remaining signals to sum to 1.0
- If only 1 signal is available, default to Cautious regime as a safety measure
- Log missing signals in `decisions.jsonl` with reason `"regime_signal_unavailable"`

---

## Earnings Event Overlay

When `config.earnings_overlay.enabled` is true, check for upcoming earnings before finalizing any AllocationPlan:

1. For each current holding and each candidate in the proposed allocation, check if confirmed earnings are within `config.earnings_overlay.lookahead_trading_days` (default: 5 trading days).

2. For flagged holdings:
   a. If the holding's composite percentile rank is >= `hold_through_percentile` (default: 0.80, i.e. top 20th percentile of the current portfolio), hold through earnings at full weight. Log `decision_type: "earnings_hold_through"` with rationale.
   b. If below that threshold, reduce the holding's target weight by `reduce_pct` (default: 50%). Redistribute freed weight to the next-best candidate NOT facing imminent earnings. Log `decision_type: "earnings_reduction"`.

3. For new candidates being added: if earnings are within the lookahead window and the candidate is below `hold_through_percentile`, defer entry to the next rebalance cycle. Log `decision_type: "earnings_entry_deferred"`.

Data source for earnings dates: Use whatever calendar source is available (e.g., Yahoo Finance earnings calendar, Polygon.io). Document the source in `evidence_refs`. If no earnings calendar is available, skip the overlay and log `"earnings_overlay_skipped"` in `decisions.jsonl`.

---

## Cash Allocation

Cash is a deliberate position, not a residual.

- **Normal regime:** Hold `config.cash.normal_pct` (default: 5%) as a rebalance buffer
- **Cautious regime:** Hold `config.cash.cautious_pct` (default: 15%)
- **Defensive regime:** Hold `config.cash.defensive_pct` (default: 30%)

Cash targets are enforced during position sizing. After all position weights are computed and clipped, verify total non-cash allocation equals `1.0 - cash_target`. If it doesn't, scale all positions proportionally to hit the target.

Cash balance is reported in every daily report alongside holdings.

---

## Position Sizing

Default method: `config.position_sizing` (default: `"score_vol_weighted"`).

### score_vol_weighted (default)

Allocate proportionally to score divided by realized volatility:

```
raw_weight_i = percentile_rank_i * (1 / realized_vol_i)
weight_i = raw_weight_i / sum(raw_weight_j for j in selected)
```

`realized_vol` = annualized standard deviation of daily log returns over `config.position_sizing_options.vol_lookback_days` (default: 60 trading days). Annualize by multiplying by sqrt(252).

If a candidate has fewer than `vol_min_days` (default: 20) of price history, exclude it from allocation (it may remain as a ResearchCandidate).

After computing raw weights, apply the same floor/cap/sector-cap procedure as score_weighted:
1. Clip any weight > `cap_pct` (default: 15%) to cap; redistribute surplus pro-rata
2. Clip any weight < `floor_pct` (default: 2%) up to floor; reduce largest positions to compensate
3. Enforce sector cap
4. Scale to `(1.0 - cash_target_pct)`

### score_weighted (alternate)
Allocate proportionally to each candidate's percentile rank score, subject to hard caps:
- Minimum position: 2% (suppress noise-level allocations)
- Maximum position: `config.constraints.max_position_pct` (default: 15%)
- Target number of positions: `config.universe.target_positions` (default: 15)

Procedure:
1. Take top-N candidates by percentile rank where N = `target_positions`
2. Assign raw weights proportional to percentile rank
3. Normalize raw weights to sum to 1.0 across non-cash allocation
4. Clip any weight exceeding max_position_pct down to the cap; redistribute surplus equally to remaining positions
5. Clip any weight below 2% up to 2%; reduce from the largest remaining positions to compensate

### equal_weight (alternate)
Allocate 1/N to each of the top-N candidates by percentile rank. Apply the same min/max caps as above. Use when simplicity and turnover reduction are preferred over signal-proportional sizing.

### Correlation filtering

After scoring and candidate selection, before final weight assignment:

1. Compute 60-day rolling pairwise Pearson correlation of daily returns for all candidates in the selected set (using `config.constraints.corr_lookback_days`).
2. For each pair where correlation > `config.constraints.max_pairwise_corr` (default: 0.85):
   a. Keep the candidate with the higher composite percentile rank.
   b. Multiply the lower-ranked candidate's raw weight by `(1 - corr_penalty_factor)` (default: reduce by 50%).
   c. If the penalized weight falls below `floor_pct`, drop the candidate entirely and replace with the next-highest-ranked candidate not already selected and not correlated > threshold with any existing selection.
3. Re-normalize weights after all penalties are applied.
4. Log correlation penalties in `decisions.jsonl` with `decision_type: "corr_penalty"`, including the pair, correlation value, and action taken.

Apply correlation filtering BEFORE sector cap enforcement so that sector caps operate on the post-correlation portfolio.

### Sector cap enforcement during sizing
After computing target weights, verify no GICS sector exceeds `config.constraints.max_sector_pct` (default: 30%). If breached, reduce the smallest position(s) in the over-concentrated sector until the cap is met. Redistribute freed weight to the highest-ranked candidates in under-represented sectors.

---

## Turnover Management

Each rebalance event is subject to a turnover budget: `config.rebalance.max_turnover_pct` (default: 30%).

**Turnover calculation:** Sum the absolute value of all weight changes divided by 2. If a rebalance would replace 12 of 15 positions, that's near-100% turnover -- well over budget.

**When turnover exceeds budget:**
1. Prioritize sells of holdings that fail the safety gate or fall below the displacement threshold
2. Prioritize buys of new candidates that rank highest by percentile
3. Defer remaining changes (mid-ranked swaps) to the next rebalance cycle
4. Log deferred changes in `decisions.jsonl` with reason `"turnover_cap_deferred"`

**Tax efficiency consideration:** When choosing which positions to sell within the turnover budget, prefer selling long-term holdings over short-term holdings (lower tax impact), unless the short-term holding has a loss (TLH opportunity).

### Cost-aware turnover (default when `config.rebalance.cost_aware_turnover` is true)

Instead of treating all weight changes equally, weight each change by its estimated transaction cost:

```
cost_adjusted_turnover = sum(|delta_weight_i| * cost_multiplier_i) / 2
```

Where `cost_multiplier_i` is derived from the stock's average daily volume:

| 30-day ADV | cost_multiplier |
|---|---|
| > $100M | 1.0 (baseline) |
| $50M - $100M | 1.5 |
| $20M - $50M | 2.5 |
| $5M - $20M | 4.0 |

The turnover budget (`max_turnover_pct`) applies to `cost_adjusted_turnover`. This means the system can make more swaps among liquid names within the same budget, while illiquid swaps consume more of the budget.

When prioritizing which changes to defer (see existing rules), prefer deferring swaps with higher `cost_multiplier` first — the most expensive trades get deferred.

---

## Rebalance Trigger Logic

At every `rally:daily` cron run, check whether rebalancing should occur before generating a trade plan.

**Triggers** -- any single condition is sufficient to initiate rebalancing:

1. **Drift trigger:** Any current holding deviates from its target allocation by more than `config.rebalance.drift_threshold` (default: 5%). Compute drift as `|actual_pct - target_pct|`.

2. **Signal displacement trigger:** A candidate not in the current portfolio ranks in the top-N by percentile rank, AND the weakest current holding scores below `config.rebalance.displacement_threshold` (default: 0.35 percentile). This replaces deteriorating positions with stronger candidates without requiring full drift.

3. **Manual override:** User explicitly invokes `rally.plan.allocation` or `rally.plan.trade` directly.

4. **Emergency sell trigger (dual stop):** A current holding triggers an emergency sell if EITHER condition is met:

   a. **ATR trailing stop:** The holding's current price falls below its trailing high minus (`atr_stop_multiplier` * 14-day ATR). The trailing high is the highest closing price since `acquisition_date` (or since the last rebalance that confirmed the position, whichever is later). ATR = average true range over `config.rebalance.atr_lookback_days` (default: 14). Multiplier default: 3.0.

      `stop_price = trailing_high - (atr_stop_multiplier * ATR_14)`

   b. **Hard floor:** The holding's current price is more than `config.rebalance.emergency_drop_pct` (default: 15%) below `cost_basis`.

      `floor_price = cost_basis * (1 - emergency_drop_pct)`

   Whichever triggers first initiates an emergency sell for that position. Emergency triggers bypass the minimum interval guard and the turnover budget. Log as `decision_type: "emergency_sell"` with the specific trigger (`atr_stop` | `hard_floor`), the stop price, and the current price.

   When `stop_type` is `"dual"` (default), both checks run. If `stop_type` is `"hard_floor_only"`, only the hard floor check runs (backward-compat with v2 behavior at the new 15% threshold).

   A holding also triggers an emergency sell if it fails the Fundamental Safety gate on fresh data (P/E exclusion or earnings consistency disqualification).

**Minimum interval guard:** Never rebalance if the most recent rebalance occurred fewer than `config.rebalance.min_interval_days` days ago (default: 14). This guard applies to drift and displacement triggers -- it does not block manual overrides or emergency sell triggers.

**If no trigger fires:** Run universe.refresh → research.signals → report.daily only. Do not generate a new AllocationPlan or TradePlan. Log the trigger check result in `decisions.jsonl`.

---

## Risk Controls

Every AllocationPlan is validated before any trade plan is derived:

- Max position size: no single target exceeds `config.constraints.max_position_pct`
- Max drawdown: if current portfolio drawdown from peak exceeds `config.constraints.max_drawdown` (default: 10%), halt and surface alert -- do not generate new allocations
- Concentration limit: top 3 positions must not exceed 35% of portfolio combined (derived from 3 × 15% max position with a buffer)
- Correlation limit: no pair of holdings may have 60-day correlation > `config.constraints.max_pairwise_corr` without penalty applied
- Prohibited instruments: reject any candidate appearing in a user-maintained exclusion list

Breach of any control halts the plan and writes a DecisionRecord with `decision_type: "risk_halt"`. Never proceed past a failed risk check.

### Drawdown-based exposure reduction

When `config.drawdown_risk_budget.enabled` is true, check the trailing portfolio return each day during the cron run:

```
trailing_return = (current_portfolio_value / peak_value_over_trailing_days) - 1
```

If `trailing_return` < `reduction_threshold_pct` (default: -8%):
1. Reduce all position target weights by `reduction_factor` (default: 25%). Move the freed capital to cash.
2. Log `decision_type: "drawdown_reduction"` with the trailing return and new cash target.
3. Do NOT generate new buys until recovery conditions are met.

Recovery conditions (all must be true to re-deploy):
- Trailing 20-day return is back above 0% (drawdown recovered)
- If `recovery_requires_regime_normal` is true, the regime model composite must also be in Normal territory (>= `normal_floor`)

When recovering, deploy using the same `reentry_deploy_max_pct` (default: 50%) rule from the regime transition logic — no more than 50% of excess cash per rebalance cycle.

This is INDEPENDENT of the `max_drawdown` halt (which is a hard stop at 10%). The drawdown risk budget triggers earlier (at -8%) and is a graduated response, not a full halt.

---

## Cost Basis Usage

`cost_basis` in PortfolioState is used for:

1. **Unrealized P&L calculation:** `unrealized_pnl = (current_price - cost_basis) * shares` -- reported in daily and monthly reports per holding and in aggregate

2. **Tax-loss harvesting (TLH) identification:** Flag any holding where `unrealized_pnl / (cost_basis * shares) < -0.08` (loss exceeds 8%) as a TLH candidate in the daily report. TLH candidates are surfaced for user review, never acted on automatically.

3. **Wash sale prevention:** Maintain a wash sale exclusion list at `~/openclaw/data/ocas-rally/wash_sale_exclusions.jsonl`. When any security is sold at a loss (including TLH), add it to the exclusion list with a `reentry_eligible_date` set to sale date + 31 calendar days. During candidate selection and allocation planning, treat any security on the exclusion list as ineligible until its `reentry_eligible_date` has passed. This prevents IRS wash sale disallowance. Log exclusion events with `decision_type: "wash_sale_exclusion"`.

Additionally, when a security is sold at a loss, add substantially identical securities to the exclusion list:
- Other share classes of the same company (e.g., GOOG/GOOGL)
- Sector-specific ETFs that hold the sold security as a top-10 holding (e.g., selling AAPL should also exclude XLK, VGT, QQQ if they hold AAPL in their top 10)

Substantially identical matching is best-effort based on available data. Log the rationale for each substantially identical exclusion in the WashSaleExclusion record.

4. **Holding period classification:** Track `acquisition_date` (stored in PortfolioState when a position is entered) to classify positions as short-term (<365 days) or long-term (>=365 days). Report this classification in monthly attribution to support tax planning.

---

## Reporting

**Daily** (`rally.report.daily`): current holdings with prices and unrealized P&L, drift from targets, risk check pass/fail status, TLH candidates, signal rankings for top-10 candidates, rebalance trigger check results.

**Monthly** (`rally.report.monthly`): portfolio return vs. benchmark, performance attribution by factor category (quality, momentum, safety, reversion, congressional flow contributions), holding period summary, rebalance activity log, OKR evaluation against 30-run window.

---

## Cron Behavior

The `rally:daily` cron runs the following sequence:

```
1. rally.universe.refresh
2. Update trailing_high and current_atr_14 for all holdings
3. Check dual stop-loss triggers (emergency sells bypass everything)
4. Fetch congressional flow data if enabled (cache in congressional_flow_cache.jsonl)
5. rally.research.signals (includes sector-relative scoring, reversion signal,
   path quality, realized vol, congressional flow)
6. Compute regime composite score
7. Check drawdown risk budget
8. Run factor decay monitor, log IC values
9. Check rebalance triggers (drift, displacement)
10. If rebalance triggered:
    a. Apply earnings overlay
    b. Apply correlation penalty
    c. Compute score_vol_weighted allocation with sector caps
    d. Enforce cost-aware turnover budget
    e. rally.plan.allocation -> rally.plan.trade
11. rally.report.daily
12. rally.journal
```

The daily cron must update `trailing_high` and `current_atr_14` for all holdings before checking rebalance triggers.

During `rally.research.signals`, if `congressional_flow` is enabled, fetch congressional trade data for all universe candidates before computing scores. Rate-limit API calls to avoid exceeding provider limits (QuiverQuant: respect their rate limits; Finnhub: max 60/min on free tier). Cache results in `congressional_flow_cache.jsonl` to avoid redundant calls within the same day.

`rally.plan.allocation` and `rally.plan.trade` execute within the cron only when a rebalance trigger fires. This prevents daily trade plan generation and the excessive turnover that would result.
