# EV-Maximizing Portfolio Review Framework

## Core Principle

**Holding a position each day = implicitly re-buying at today's price.**

Your entry price is a sunk cost. The only question that matters: "If I had cash instead of this position, would I buy it now at the current price?"

## Core Formula

```
daily_expected_return = (p_now - c_now) / (c_now × d_remaining)
```

Where:
- `p_now` = your updated probability estimate (after fresh research)
- `c_now` = current market price (cost to hold / re-buy)
- `d_remaining` = days until market resolution

This metric normalizes all positions to a common unit: **expected return per day per dollar at risk**.

## Decision Tree (6 Steps)

For each position, execute these steps in order:

### Step 1: Update Probability (p_now)

- Perform 2-3 web searches for the latest news on this event
- Start from your prior estimate, update with new evidence
- Document your reasoning (event-level thinking)
- Assign confidence: High / Medium / Low

### Step 2: Check Edge Direction

```
edge = p_now - c_now
```

- If edge > 0 → position has positive expected value, proceed to Step 3
- If edge ≤ 0 → **SELL** — edge has reversed, no reason to hold
- If edge is negative but small (0 to -3%) → consider friction cost before selling

### Step 3: Check Thesis Integrity

Ask yourself:
- Has the core thesis changed since entry?
- Are there new risks not priced in?
- Has the resolution criteria become ambiguous?

If thesis is broken → **SELL** regardless of edge

### Step 4: Compare Daily Expected Return

Rank all positions by `daily_expected_return`:

| Daily ER | Rating | Action |
|----------|--------|--------|
| > 0.50% | Excellent | Strong hold |
| 0.10% – 0.50% | Good | Hold |
| 0.02% – 0.10% | Marginal | Hold only if no better alternatives |
| < 0.02% | Capital-inefficient | Rotate to better opportunity |
| Negative | Losing edge | **SELL** |

### Step 5: Kelly & Concentration Check

For each position:
```
f* = (p_now - c_now) / (1 - c_now)
f_q = f* / 4  (quarter Kelly)
```

**Portfolio-level checks:**
- Total Kelly exposure ≤ 100% of bankroll
- Single theme ≤ 40% of bankroll (e.g., all Iran-related positions)
- Single market ≤ 25% of bankroll
- Expiry diversification: not all positions expiring in same week

If over-concentrated → trim largest position, even if edge is good

### Step 6: Final Verdict

Combine all signals into one of three actions:

| Verdict | Criteria |
|---------|----------|
| **HOLD** | Positive edge, thesis intact, Kelly within range, no better alternative |
| **SELL** | Negative edge, OR thesis broken, OR over-concentrated, OR capital-inefficient with better alternatives |
| **ROTATE** | Position is marginally positive but a specific better opportunity exists (name the replacement) |

## Sell Signal Checklist

- [ ] Edge has reversed (p_now < c_now for your side)
- [ ] Thesis has collapsed (new information invalidates original reasoning)
- [ ] Better opportunity exists (higher daily_er available)
- [ ] Over-concentrated (>25% of bankroll in one market, or >40% in one theme)
- [ ] Over Kelly (position size > f_q of current bankroll)
- [ ] Near-zero daily_er with long time to expiry (capital lock-up)

## Hold Signal Checklist

- [ ] Edge is positive (p_now > c_now for your side)
- [ ] Within quarter-Kelly range
- [ ] No better alternative available (daily_er comparison)
- [ ] Thesis remains intact
- [ ] Not over-concentrated

## Rotation Friction Cost

Every sell+buy cycle costs approximately **2-4% in spread/slippage**:
- Selling: lose ~1-2% to bid-ask spread
- Buying new: lose ~1-2% to bid-ask spread

**Rule of thumb:** Only rotate if the new position's daily_er exceeds the current position's daily_er by at least 0.05% per day (to cover friction).

## Daily Expected Return Interpretation

| Daily ER | Annualized (approx) | Interpretation |
|----------|---------------------|----------------|
| > 0.50% | > 500% | Exceptional — rare, usually short-dated |
| 0.20% – 0.50% | 100-500% | Excellent edge |
| 0.10% – 0.20% | 40-100% | Good, solid hold |
| 0.05% – 0.10% | 20-40% | Decent, beats most alternatives |
| 0.02% – 0.05% | 8-20% | Marginal — review regularly |
| < 0.02% | < 8% | Capital-inefficient — likely should rotate |

## Portfolio-Level Checks

After analyzing individual positions, verify at portfolio level:

1. **Total Kelly ≤ 100%** — Sum of all f_q values should not exceed 100%
2. **Theme concentration ≤ 40%** — Group positions by theme (Iran, crypto, politics, etc.)
3. **Expiry diversification** — Positions should have staggered end dates
4. **Cash reserve** — At least 20-30% available for new opportunities
5. **Correlation** — Avoid positions that all move in the same direction on the same news
