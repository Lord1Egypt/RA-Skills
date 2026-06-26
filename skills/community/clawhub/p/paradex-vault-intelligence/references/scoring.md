# Vault Scoring & Ranking Methodology

Detailed reference for risk scoring, performance ranking, recommendation engine logic,
and JMESPath query patterns used by the Vault Intelligence skill.

---

## 1. Risk Score (1-5)

Each vault receives a risk score from 1 (low risk) to 5 (high risk) based on four
dimensions: drawdown history, diversification, leverage, and TVL trend.

### Score 1 — Low Risk

| Dimension | Criteria |
|---|---|
| Max drawdown | < 5% (all-time) |
| Diversification | 3+ markets in current positions |
| Leverage | < 3x effective leverage |
| TVL trend | Stable or growing over 30 days |
| Additional | Positive ROI across all timeframes (7d, 30d, total) |

**Profile:** Conservative vault with a diversified, low-leverage strategy. Suitable
for risk-averse depositors seeking steady, modest returns.

### Score 2 — Low-Moderate Risk

| Dimension | Criteria |
|---|---|
| Max drawdown | < 10% (all-time) |
| Diversification | 2-3 markets in current positions |
| Leverage | < 5x effective leverage |
| TVL trend | Stable (not declining >10% in 30 days) |
| Additional | Positive total ROI, minor recent dips acceptable |

**Profile:** Relatively safe vault with moderate diversification. Occasional small
drawdowns but generally controlled risk.

### Score 3 — Medium Risk

| Dimension | Criteria |
|---|---|
| Max drawdown | < 20% (all-time) |
| Diversification | 2-3 markets, some concentration (largest position 40-60%) |
| Leverage | 3x-7x effective leverage |
| TVL trend | Neutral (may fluctuate +-15% over 30 days) |
| Additional | Mixed performance across timeframes |

**Profile:** Active vault with meaningful risk exposure. Higher return potential comes
with notable drawdown history. Suitable for moderate risk tolerance.

### Score 4 — Elevated Risk

| Dimension | Criteria |
|---|---|
| Max drawdown | < 30% (all-time) |
| Diversification | Single-market focus or heavily concentrated |
| Leverage | 5x-10x effective leverage |
| TVL trend | May be declining (depositor outflows) |
| Additional | High variance in returns across timeframes |

**Profile:** Aggressive vault with concentrated, high-leverage positions. Significant
drawdown history. Only suitable for depositors comfortable with substantial losses.

### Score 5 — High Risk

| Dimension | Criteria |
|---|---|
| Max drawdown | > 30% (all-time) |
| Diversification | Single market, single direction |
| Leverage | > 10x effective leverage |
| TVL trend | Declining TVL, depositor exodus |
| Additional | Large unrealized losses, negative recent ROI |

**Profile:** High-risk vault with a history of severe drawdowns. May be a new vault
with an untested operator or an aggressive strategy that has experienced significant
losses. Exercise extreme caution.

### Scoring Decision Tree

```
START
  |
  ├─ max_drawdown > 30%? ──────────────────────> Score 5
  |
  ├─ max_drawdown > 20%? ──┐
  |                         ├─ leverage > 5x OR single market? ──> Score 4
  |                         └─ else ──────────────────────────────> Score 3
  |
  ├─ max_drawdown > 10%? ──┐
  |                         ├─ leverage > 7x OR declining TVL? ──> Score 4
  |                         ├─ concentrated (< 2 markets)? ──────> Score 3
  |                         └─ else ──────────────────────────────> Score 3
  |
  ├─ max_drawdown > 5%? ───┐
  |                         ├─ leverage > 5x? ──────────────────> Score 3
  |                         ├─ stable TVL + 2-3 markets? ───────> Score 2
  |                         └─ else ────────────────────────────> Score 2
  |
  └─ max_drawdown <= 5%? ──┐
                            ├─ 3+ markets + leverage < 3x? ────> Score 1
                            ├─ growing TVL? ────────────────────> Score 1
                            └─ else ────────────────────────────> Score 2
```

---

## 2. Sharpe-like Ratio

A simplified risk-adjusted return metric for comparing vaults.

### Formula

```
sharpe_like_ratio = total_roi / max_drawdown
```

Where:
- `total_roi` is the vault's all-time return (as a decimal, e.g., 0.15 for 15%)
- `max_drawdown` is the vault's worst peak-to-trough decline (as a positive decimal, e.g., 0.08 for 8%)

### Interpretation

| Ratio | Quality |
|---|---|
| < 0 | Negative returns — avoid |
| 0 - 1.0 | Poor risk-adjusted returns (drawdown exceeds or matches returns) |
| 1.0 - 2.0 | Acceptable (returns outpace drawdown) |
| 2.0 - 5.0 | Good risk-adjusted returns |
| > 5.0 | Excellent — but verify with longer track record |

### Examples

| Vault | Total ROI | Max Drawdown | Ratio | Assessment |
|---|---|---|---|---|
| Vault A | 25% | 8% | 3.13 | Good — strong returns relative to risk |
| Vault B | 40% | 35% | 1.14 | Acceptable but volatile — high returns come with high pain |
| Vault C | 5% | 2% | 2.50 | Good — modest but very controlled |
| Vault D | 60% | 5% | 12.0 | Exceptional — verify: may be a new vault with limited history |

### Caveats for Zero-Drawdown Vaults

When `max_drawdown = 0` (or very close to zero):
- The ratio is mathematically undefined (division by zero)
- Use `total_roi` alone as the ranking metric
- Flag the vault as "insufficient drawdown history" — zero drawdown often means:
  - The vault is very new (hasn't experienced adverse conditions)
  - The vault has been inactive or has negligible positions
  - The strategy hasn't been tested through volatility
- Do NOT rank a zero-drawdown vault above a vault with a proven track record and
  non-zero drawdown simply because the ratio is higher

### Timeframe Variants

The ratio can be computed for different timeframes to assess recent vs. historical quality:

```
sharpe_30d = roi_30d / max_drawdown_30d
sharpe_total = total_roi / max_drawdown
```

Compare the two: if `sharpe_30d` is much lower than `sharpe_total`, the vault's
recent performance is deteriorating relative to its history.

---

## 3. Recommendation Engine Scoring

When a user asks "which vault should I deposit in?", the engine scores vaults based
on the user's risk tolerance and time horizon.

### Risk Tolerance Profiles

| Profile | Prioritizes | Accepts |
|---|---|---|
| Conservative | Low drawdown, stable TVL, many depositors | Lower returns |
| Moderate | Balance of ROI and drawdown | Some volatility |
| Aggressive | Highest absolute ROI | High drawdowns, concentration |

### Time Horizon Profiles

| Horizon | Key Metrics | Weight Focus |
|---|---|---|
| Short-term (< 1 week) | roi_24h, roi_7d | Recent momentum |
| Medium-term (1-4 weeks) | roi_30d, max_drawdown_30d | Recent track record |
| Long-term (> 1 month) | total_roi, max_drawdown, sharpe_like | Full history |

### Scoring Matrix — Metric Weights by Profile

| Metric | Conservative + Short | Conservative + Long | Moderate + Short | Moderate + Long | Aggressive + Short | Aggressive + Long |
|---|---|---|---|---|---|---|
| ROI (timeframe-appropriate) | 15% | 20% | 25% | 30% | 40% | 40% |
| Max drawdown | 30% | 30% | 20% | 20% | 10% | 10% |
| Sharpe-like ratio | 15% | 20% | 15% | 20% | 10% | 15% |
| TVL (size/stability) | 20% | 15% | 15% | 10% | 10% | 10% |
| Depositor count | 15% | 10% | 10% | 10% | 10% | 5% |
| Recent momentum (7d ROI) | 5% | 5% | 15% | 10% | 20% | 20% |

### Scoring Procedure

1. **Screen:** Filter out inactive vaults, vaults with < $1,000 TVL, and vaults
   with negative total ROI (unless aggressive profile)

2. **Normalize:** For each metric, normalize to 0-100 scale across the filtered set:
   ```
   normalized_score = (value - min_value) / (max_value - min_value) × 100
   ```
   For drawdown, invert (lower is better):
   ```
   normalized_drawdown = (1 - (value - min_value) / (max_value - min_value)) × 100
   ```

3. **Weight:** Apply weights from the scoring matrix based on user's profile

4. **Rank:** Sort by weighted total score, present top 3-5

### Example Scoring (Moderate + Long-term)

**Weights:** ROI 30%, Drawdown 20%, Sharpe 20%, TVL 10%, Depositors 10%, Momentum 10%

| Vault | ROI (30%) | DD (20%) | Sharpe (20%) | TVL (10%) | Deps (10%) | Mom (10%) | Total |
|---|---|---|---|---|---|---|---|
| Vault A | 72 | 85 | 78 | 60 | 70 | 55 | 73.1 |
| Vault B | 90 | 40 | 55 | 80 | 85 | 80 | 70.5 |
| Vault C | 45 | 95 | 90 | 50 | 40 | 30 | 62.5 |

Recommendation order: Vault A > Vault B > Vault C

---

## 4. JMESPath Query Cookbook

Common screening queries for use with `paradex_vault_summary` and `paradex_vaults`.

### Top N by ROI

```jmespath
# Top 5 by total ROI
sort_by([*], &to_number(total_roi))[-5:]

# Top 10 by 30-day ROI
sort_by([*], &to_number(roi_30d))[-10:]

# Top 5 by 7-day ROI
sort_by([*], &to_number(roi_7d))[-5:]

# Top 3 by 24-hour ROI
sort_by([*], &to_number(roi_24h))[-3:]
```

### Filter by Max Drawdown Threshold

```jmespath
# Vaults with max drawdown under 5%
[?to_number(max_drawdown) < `0.05`]

# Vaults with max drawdown under 10% AND positive total ROI
[?to_number(max_drawdown) < `0.1` && to_number(total_roi) > `0`]

# Vaults with low recent drawdown (30d < 3%)
[?to_number(max_drawdown_30d) < `0.03`]
```

### Active Vaults with Minimum TVL

```jmespath
# Vaults with TVL > $10,000
[?to_number(tvl) > `10000`]

# Vaults with TVL > $50,000 (established vaults)
[?to_number(tvl) > `50000`]

# Vaults with TVL > $100,000 sorted by ROI
sort_by([?to_number(tvl) > `100000`], &to_number(total_roi))
```

### Sort by Depositor Count

```jmespath
# All vaults sorted by depositor count (descending)
reverse(sort_by([*], &num_depositors))

# Top 10 most popular vaults
reverse(sort_by([*], &num_depositors))[:10]

# Vaults with 5+ depositors (social proof)
[?num_depositors >= `5`]
```

### Combined Filters

```jmespath
# Profitable + low drawdown + high TVL (the "safe picks" screen)
[?to_number(total_roi) > `0` && to_number(max_drawdown) < `0.1` && to_number(tvl) > `10000`]

# Strong recent performance + manageable drawdown
[?to_number(roi_30d) > `0.05` && to_number(max_drawdown_30d) < `0.1`]

# High ROI with good risk-adjusted returns (approximated)
[?to_number(total_roi) > `0.2` && to_number(max_drawdown) < `0.15`]

# Popular vaults with positive returns (wisdom of the crowd)
[?num_depositors >= `3` && to_number(total_roi) > `0`]

# Large vaults sorted by 30-day ROI (institutional-grade screen)
sort_by([?to_number(tvl) > `50000`], &to_number(roi_30d))

# Conservative screen: low drawdown + stable + decent returns
[?to_number(max_drawdown) < `0.05` && to_number(tvl) > `5000` && to_number(total_roi) > `0.05`]
```

### Sorting Combined Filter Results

```jmespath
# Safe picks, sorted by total ROI (best first)
reverse(sort_by([?to_number(total_roi) > `0` && to_number(max_drawdown) < `0.1` && to_number(tvl) > `10000`], &to_number(total_roi)))

# Moderate risk, sorted by Sharpe-like proxy (ROI relative to drawdown)
# Note: JMESPath can't compute ratios directly, so sort by ROI after filtering for low DD
reverse(sort_by([?to_number(max_drawdown) < `0.15` && to_number(max_drawdown) > `0`], &to_number(total_roi)))

# Recent momentum leaders with minimum safety
reverse(sort_by([?to_number(roi_7d) > `0` && to_number(max_drawdown) < `0.2`], &to_number(roi_7d)))
```

### Useful Field Reference

| Field | Type | Description |
|---|---|---|
| `total_roi` | string (numeric) | All-time return as decimal (e.g., "0.15" = 15%) |
| `roi_24h` | string (numeric) | 24-hour return |
| `roi_7d` | string (numeric) | 7-day return |
| `roi_30d` | string (numeric) | 30-day return |
| `max_drawdown` | string (numeric) | All-time max peak-to-trough decline |
| `max_drawdown_30d` | string (numeric) | 30-day max drawdown |
| `tvl` | string (numeric) | Total value locked (USD) |
| `volume_24h` | string (numeric) | 24-hour trading volume |
| `num_depositors` | integer | Number of current depositors |
| `last_month_return` | string (numeric) | Last calendar month return |

**Note:** Most numeric fields in the vault summary API are returned as strings.
Use `to_number()` in JMESPath to enable numeric comparisons and sorting.
