# Paradex Margin Model & Risk Scoring Reference

Detailed reference for the margin system, liquidation mechanics, stress testing methodology,
and risk score computation used by the Risk Guardian skill.

---

## 1. Cross-Margin Model

Paradex uses a **cross-margin** system. All open positions share the account's total equity
as collateral. This means:

- Profits from one position increase the available margin for all other positions.
- Losses from one position reduce the available margin for all other positions.
- A large loss on a single position can trigger liquidation of the entire account,
  not just that position.

**Key implication for risk assessment:** Positions are not isolated. A seemingly safe
portfolio can become dangerous if one position moves sharply against you, because it
erodes the margin buffer for every other position simultaneously.

---

## 2. Initial Margin

Initial margin is the minimum equity required to **open** a new position.

```
initial_margin = position_notional / initial_margin_leverage
```

Where:
- `position_notional = abs(position_size) × mark_price`
- `initial_margin_leverage` is a market-specific parameter (available from `paradex_markets`)

**Example:**
- Opening 0.5 BTC-USD-PERP at mark price $65,000
- Position notional = 0.5 × $65,000 = $32,500
- If initial margin leverage = 20x, then initial margin = $32,500 / 20 = $1,625

The account must have at least $1,625 in free margin to open this position. If the
account already holds other positions, the free margin is reduced by their existing
margin requirements.

---

## 3. Maintenance Margin

Maintenance margin is the minimum equity required to **keep** a position open.
It is always lower than initial margin.

```
maintenance_margin = position_notional / maintenance_margin_leverage
```

Where `maintenance_margin_leverage` is a market-specific parameter, always higher
than `initial_margin_leverage` (meaning less margin is needed to maintain than to open).

**Example:**
- Holding 0.5 BTC-USD-PERP at mark price $65,000
- Position notional = $32,500
- If maintenance margin leverage = 50x, then maintenance margin = $32,500 / 50 = $650

**Liquidation trigger:** When total account equity falls below the sum of maintenance
margins across all positions, the account enters liquidation.

```
liquidation_condition: total_equity < sum(maintenance_margin for each position)
```

---

## 4. Margin Utilization

Margin utilization measures how much of the account's equity is consumed by margin
requirements.

```
margin_utilization = (used_margin / total_equity) × 100%
```

Where:
- `used_margin` = sum of initial margin requirements across all positions
- `total_equity` = account balance + unrealized P&L

### Threshold Levels

| Utilization | Status | Color | Interpretation |
|---|---|---|---|
| < 50% | Healthy | Green | Comfortable buffer, room for new positions |
| 50% - 75% | Caution | Yellow | Getting crowded, monitor closely |
| 75% - 90% | Warning | Orange | Limited headroom, adverse moves could trigger liquidation |
| > 90% | Danger | Red | Very close to liquidation, consider reducing positions |

### Practical Notes

- At 50% utilization, you can roughly absorb a 50% loss on unrealized P&L before
  maintenance margin becomes a concern (depending on maintenance vs. initial margin gap).
- At 90% utilization, even a small adverse price move can push the account into
  liquidation territory.
- Margin utilization changes continuously as mark prices move.

---

## 5. Liquidation Price Estimation

Simplified formulas for estimating the price at which a single position would cause
the account to breach maintenance margin.

### For a Long Position

```
liq_price_long ≈ entry_price × (1 - (free_margin / position_notional))
```

**Intuition:** The position loses money as price drops. Free margin is the buffer
before liquidation. The larger the free margin relative to position size, the further
away liquidation is.

### For a Short Position

```
liq_price_short ≈ entry_price × (1 + (free_margin / position_notional))
```

**Intuition:** The position loses money as price rises. Free margin absorbs losses
until it's exhausted.

### Example (Long)

- Entry price: $65,000
- Position notional: $32,500 (0.5 BTC)
- Free margin: $8,000
- Liquidation price estimate: $65,000 × (1 - ($8,000 / $32,500))
- = $65,000 × (1 - 0.246)
- = $65,000 × 0.754
- **= ~$49,010**
- Distance to liquidation: ~24.6%

### Example (Short)

- Entry price: $3,500
- Position notional: $14,000 (4.0 ETH)
- Free margin: $8,000
- Liquidation price estimate: $3,500 × (1 + ($8,000 / $14,000))
- = $3,500 × (1 + 0.571)
- = $3,500 × 1.571
- **= ~$5,500**
- Distance to liquidation: ~57.1%

### Important Caveats

- These are **simplified estimates**. Actual liquidation depends on:
  - **Mark price** (not last traded price) — mark price is used for margin calculations
  - **Cross-margin interactions** — other positions' P&L changes simultaneously
  - **Maintenance margin** (not initial margin) — the actual trigger threshold
  - **Funding payments** — can erode equity over time
- In a cross-margin account with multiple positions, a correlated move can cause
  multiple positions to lose simultaneously, bringing liquidation much closer than
  the single-position estimate suggests.
- Always recommend the user verify liquidation prices on the Paradex UI.

---

## 6. Stress Test Methodology

The Risk Guardian runs scenario analysis to estimate portfolio impact under adverse
price moves.

### Price Shock Scenarios

| Scenario | BTC Move | ETH Move (1.2x beta) | Alt Move (1.5-2.0x beta) |
|---|---|---|---|
| Mild | -5% | -6% | -7.5% to -10% |
| Moderate | -10% | -12% | -15% to -20% |
| Severe | -20% | -24% | -30% to -40% |

### Per-Position Impact Calculation

```
position_impact = position_size × current_price × price_shock_pct × direction_multiplier
```

Where:
- `direction_multiplier` = -1 for longs (lose money when price drops), +1 for shorts
- For upward shocks, reverse: longs gain, shorts lose

### Crypto Beta Adjustments

Crypto assets are highly correlated, but alts tend to move with higher amplitude than BTC.

| Asset Class | Beta to BTC | Rationale |
|---|---|---|
| BTC | 1.0x | Reference asset |
| ETH | ~1.2x | Major alt, slightly more volatile |
| Large-cap alts (SOL, AVAX) | ~1.5x | Higher volatility, stronger reactions |
| Mid/small-cap alts (DOGE, ARB, etc.) | ~1.5-2.0x | Highest volatility, amplified moves |

**Note:** These betas are approximate historical averages. During extreme stress events
(exchange outages, depegs, regulatory news), correlations tend to spike to 1.0 while
beta amplification increases further.

### Portfolio-Level Stress Test

```
total_impact = sum(position_impact_i for each position i)
stressed_equity = current_equity + total_impact
margin_after_stress = stressed_equity - sum(maintenance_margin_i after repricing)
```

If `margin_after_stress < 0`, the account would be liquidated in that scenario.

### Example Stress Test

**Portfolio:** Long 0.25 BTC, Long 4.0 ETH, Short 80 SOL

| Position | Notional | -10% BTC Scenario | Impact |
|---|---|---|---|
| BTC-USD-PERP (Long) | $16,375 | BTC -10.0% | -$1,638 |
| ETH-USD-PERP (Long) | $14,000 | ETH -12.0% (1.2x beta) | -$1,680 |
| SOL-USD-PERP (Short) | $12,560 | SOL -15.0% (1.5x beta) | +$1,884 |
| **Total impact** | | | **-$1,434** |

- Current equity: $24,512
- Equity after stress: $24,512 - $1,434 = $23,078
- Maintenance margin (repriced): ~$860
- **Surplus: $22,218 — account survives this scenario comfortably**

---

## 7. Risk Score Weighting

The Risk Guardian computes an overall risk score from 1 (low risk) to 10 (high risk)
using five weighted factors.

### Factor Weights

| Factor | Weight | Description |
|---|---|---|
| Margin utilization | 30% | How much of equity is used as margin |
| Position concentration | 20% | How concentrated exposure is in few markets |
| Effective leverage | 20% | Total notional exposure relative to equity |
| Funding cost (daily) | 15% | Net funding payments as % of equity |
| Liquidity risk | 15% | Ability to exit positions without excessive slippage |

### Scoring Rubric Per Factor

#### Margin Utilization (Weight: 30%)

| Score | Utilization Range |
|---|---|
| 1 | < 20% |
| 2 | 20% - 30% |
| 3 | 30% - 40% |
| 4 | 40% - 50% |
| 5 | 50% - 60% |
| 6 | 60% - 70% |
| 7 | 70% - 75% |
| 8 | 75% - 85% |
| 9 | 85% - 90% |
| 10 | > 90% |

#### Position Concentration (Weight: 20%)

| Score | Criteria |
|---|---|
| 1-2 | No position > 25% of total exposure, 4+ markets |
| 3-4 | Largest position 25-35%, 3+ markets |
| 5-6 | Largest position 35-50%, 2-3 markets |
| 7-8 | Largest position 50-60%, 1-2 markets |
| 9-10 | Single position > 60% of exposure, or single market |

#### Effective Leverage (Weight: 20%)

| Score | Leverage |
|---|---|
| 1 | < 1x |
| 2 | 1x - 2x |
| 3 | 2x - 3x |
| 4 | 3x - 4x |
| 5 | 4x - 5x |
| 6 | 5x - 6x |
| 7 | 6x - 7x |
| 8 | 7x - 8x |
| 9 | 8x - 10x |
| 10 | > 10x |

#### Funding Cost (Weight: 15%)

| Score | Daily Funding Cost (% of equity) |
|---|---|
| 1 | Net positive (receiving funding) |
| 2-3 | 0% - 0.02% of equity |
| 4-5 | 0.02% - 0.05% of equity |
| 6-7 | 0.05% - 0.10% of equity |
| 8-9 | 0.10% - 0.20% of equity |
| 10 | > 0.20% of equity |

#### Liquidity Risk (Weight: 15%)

| Score | Criteria |
|---|---|
| 1-2 | All positions can be exited within 0.5% slippage |
| 3-4 | All positions within 1% slippage |
| 5-6 | Most positions within 1%, some need 2% |
| 7-8 | Some positions cannot exit within 2% slippage |
| 9-10 | Major positions are illiquid (orderbook depth < 50% of position within 2%) |

### Computing the Final Score

```
risk_score = round(
    margin_score × 0.30 +
    concentration_score × 0.20 +
    leverage_score × 0.20 +
    funding_score × 0.15 +
    liquidity_score × 0.15
)
```

### Example Calculation

| Factor | Raw Score | Weight | Weighted |
|---|---|---|---|
| Margin utilization (42%) | 4 | 0.30 | 1.20 |
| Concentration (largest 26%) | 3 | 0.20 | 0.60 |
| Effective leverage (2.5x) | 3 | 0.20 | 0.60 |
| Funding cost (0.016%/day) | 2 | 0.15 | 0.30 |
| Liquidity (all within 0.5%) | 1 | 0.15 | 0.15 |
| **Total** | | | **2.85 -> Risk Score: 3/10** |

### Risk Score Interpretation

| Score | Label | Action |
|---|---|---|
| 1-2 | Low Risk | No action needed |
| 3-4 | Moderate | Monitor, no immediate concern |
| 5-6 | Elevated | Review positions, consider reducing exposure |
| 7-8 | High | Actively reduce risk, close weakest positions |
| 9-10 | Critical | Immediate action required, liquidation risk is real |
