# Sensitivity Analysis Guide

How to model the impact of price changes, cost fluctuations, and operational improvements on per-unit profit margins.

---

## Why Sensitivity Analysis Matters

A single profit waterfall shows current state. Sensitivity analysis answers "what if" questions that drive real decisions:
- "If I raise the price by $3, do I lose enough volume to offset the margin gain?"
- "If my supplier raises COGS by 10%, which SKUs go negative?"
- "If I can reduce my return rate by 5 points, how much margin do I recover?"

Without these models, pricing and cost decisions are gut calls.

---

## Method 1 — Single Variable Sensitivity

Change one input at a time while holding everything else constant. This isolates the impact of each variable.

### Price Sensitivity Table

For each SKU on each channel, model margin at multiple price points:

| Price Point | Revenue | Platform Fees | COGS | Shipping | Ad Cost | Returns | Overhead | **Net Margin** | **Change** |
|------------|---------|--------------|------|----------|---------|---------|----------|---------------|-----------|
| Current −$5 | $ | $ | $ | $ | $ | $ | $ | % | −___ pts |
| Current −$2 | $ | $ | $ | $ | $ | $ | $ | % | −___ pts |
| **Current** | **$** | **$** | **$** | **$** | **$** | **$** | **$** | **%** | **baseline** |
| Current +$2 | $ | $ | $ | $ | $ | $ | $ | % | +___ pts |
| Current +$5 | $ | $ | $ | $ | $ | $ | $ | % | +___ pts |
| Current +$10 | $ | $ | $ | $ | $ | $ | $ | % | +___ pts |

**Important nuances when modeling price changes:**
- Platform fees that are percentage-based (referral fees, payment processing) change in dollar terms when price changes
- Ad cost as a percentage of revenue stays the same, but ad cost per unit changes if you assume constant ROAS
- Volume may decrease at higher prices — model with and without volume impact
- Competitor pricing constrains how much you can raise on marketplaces

### COGS Sensitivity Table

| COGS Scenario | Landed Cost | Gross Margin | Net Margin | **Margin Change** |
|--------------|------------|-------------|-----------|-------------------|
| −15% (renegotiated) | $ | % | % | +___ pts |
| −10% | $ | % | % | +___ pts |
| **Current** | **$** | **%** | **%** | **baseline** |
| +10% (supplier increase) | $ | % | % | −___ pts |
| +20% (tariff impact) | $ | % | % | −___ pts |
| +30% (supply disruption) | $ | % | % | −___ pts |

### Return Rate Sensitivity

| Return Rate | Cost/Unit Sold | Net Margin | **Margin Change** |
|------------|---------------|-----------|-------------------|
| Current −10 pts | $ | % | +___ pts |
| Current −5 pts | $ | % | +___ pts |
| **Current** | **$** | **%** | **baseline** |
| Current +5 pts | $ | % | −___ pts |
| Current +10 pts | $ | % | −___ pts |

### Ad Spend Sensitivity

| ROAS Scenario | Ad Cost/Unit | Net Margin | **Margin Change** |
|--------------|-------------|-----------|-------------------|
| ROAS improves 50% | $ | % | +___ pts |
| ROAS improves 25% | $ | % | +___ pts |
| **Current ROAS** | **$** | **%** | **baseline** |
| ROAS declines 25% | $ | % | −___ pts |
| ROAS declines 50% | $ | % | −___ pts |
| No ad spend | $ | % | +___ pts |

---

## Method 2 — Multi-Variable Scenario Modeling

Combine multiple changes into realistic scenarios.

### Scenario Template

| Scenario Name | Price Change | COGS Change | Return Rate Change | Ad Spend Change | Net Margin | vs. Current |
|--------------|-------------|-------------|-------------------|----------------|-----------|-------------|
| **Optimistic** | +$3 | −5% | −3 pts | ROAS +20% | % | +___ pts |
| **Base case** | $0 | $0 | 0 pts | 0% | % | baseline |
| **Pessimistic** | −$2 | +10% | +2 pts | ROAS −15% | % | −___ pts |
| **Tariff impact** | $0 | +25% | 0 pts | 0% | % | −___ pts |
| **Growth push** | −$3 | $0 | +2 pts | Spend +50% | % | −___ pts |

### Common Realistic Scenarios to Model

**1. Supplier price increase**
Suppliers typically raise prices 5–15% annually. Model what happens if COGS increases and you cannot raise retail price (competitive pressure on marketplaces).

**2. Peak season (Q4)**
Amazon storage fees triple in Q4. Ad CPMs increase 30–80% across Meta and Google. Return rates spike in January. Model the Q4 margin separately from the annual average.

**3. New channel launch**
When launching on a new channel, initial ROAS is typically 30–50% worse than established channels. Model the expected margin during the ramp period (usually 3–6 months).

**4. Free shipping threshold change**
If you lower or remove the free shipping threshold, average shipping cost per order changes. Model the impact on per-unit margins and the expected lift in conversion rate.

**5. 3PL rate renegotiation**
3PL contracts are typically renegotiated annually or at volume thresholds. Model the margin impact of a 10–20% reduction in fulfillment costs.

---

## Method 3 — Break-Even Analysis

Determine the minimum volume, price, or ROAS needed to maintain profitability.

### Break-Even Volume

At current margins, how many units must you sell to cover all fixed costs?

**Formula:**
Break-even units = Total monthly fixed costs ÷ Contribution margin per unit (before overhead)

**Example:**
- Monthly overhead: $25,000
- Contribution margin per unit (before overhead): $8.50
- Break-even: 25,000 ÷ 8.50 = 2,941 units/month

### Break-Even Price

Given current cost structure, what is the minimum price to achieve target margin?

**Formula:**
Minimum price = (COGS + shipping + return cost/unit + overhead/unit + target profit/unit) ÷ (1 − platform fee % − ad cost %)

**Example:**
- Total costs: $7.40 + $9.15 + $1.52 + $3.67 + $1.50 target = $23.24
- Fee drain: 3.9% platform + 23.8% ad = 27.7%
- Minimum price: $23.24 ÷ (1 − 0.277) = $32.14

### Break-Even ROAS

What ROAS do you need to maintain positive margin?

**Formula:**
Break-even ROAS = Revenue ÷ Maximum affordable ad spend
Maximum affordable ad spend = Revenue − COGS − fees − shipping − returns − overhead − minimum acceptable profit

---

## Method 4 — Margin Tornado Chart

Rank variables by their impact on margin to prioritize optimization efforts.

### How to Build

1. For each variable, calculate margin at ±10% of current value
2. Record the margin swing (high minus low)
3. Rank variables by swing size
4. Present as a tornado chart (horizontal bar chart, widest at top)

### Typical Variable Ranking (ecommerce)

Variables usually ranked by margin impact, highest to lowest:

1. **Retail price** — highest leverage, small changes have outsized impact
2. **Return rate** — especially in apparel, can swing margin 5–10 points
3. **Ad spend / ROAS** — second-highest discretionary cost after COGS
4. **COGS / landed cost** — large absolute number but harder to change quickly
5. **Shipping cost** — significant for DTC, less for FBA
6. **Platform fees** — mostly fixed by platform, limited optimization
7. **Overhead allocation** — important at scale but low per-unit sensitivity

---

## Presenting Sensitivity Results

### Do
- Show the current baseline prominently so stakeholders have an anchor
- Highlight the 2–3 variables with the largest margin impact
- Include realistic scenario ranges, not just theoretical extremes
- Tie each scenario to a decision ("if we raise price $3, margin goes from 5% to 12%")
- Show break-even points for critical variables

### Don't
- Model more than 5–6 variables — it becomes noise
- Use unrealistic ranges (e.g., "what if COGS drops 50%")
- Present without action items — every scenario should map to a decision
- Forget to note assumptions (volume held constant, fees unchanged, etc.)
- Mix up margin percentage points and margin percentage change (a move from 10% to 15% is +5 points, not +50%)
