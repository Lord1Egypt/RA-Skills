# Safety Stock Guide

Framework for calculating safety stock based on service level targets, demand variability, and lead time uncertainty.

---

## Service Level and Z-Score Table

The service level represents the probability of NOT stocking out during a replenishment cycle.

| Service Level | Z-Score | When to Use |
|---|---|---|
| 85% | 1.04 | Low-value items, easy to substitute, minimal stockout cost |
| 90% | 1.28 | Standard items, moderate substitution risk |
| 95% | 1.65 | Important SKUs, meaningful revenue impact from stockout |
| 97.5% | 1.96 | High-value items, significant customer impact |
| 98% | 2.05 | Key products, brand-critical items |
| 99% | 2.33 | Mission-critical, no acceptable substitute, hero SKUs |
| 99.5% | 2.58 | Life-safety or contractual obligation items |
| 99.9% | 3.09 | Extreme — rarely justified in ecommerce |

### How to choose a service level

Ask these questions:

1. **What happens if this product stocks out?**
   - Customer buys from competitor → higher service level (97%+)
   - Customer waits or substitutes → moderate (90–95%)
   - No significant impact → lower (85–90%)

2. **What's the margin on this product?**
   - High margin → can afford more safety stock
   - Low margin → excess inventory cost matters more

3. **How long is the lead time?**
   - Long lead time → higher service level to compensate
   - Short lead time (< 7 days) → lower service level acceptable

4. **Is demand predictable?**
   - Stable, predictable → lower service level works
   - Volatile or seasonal → need higher service level

---

## Safety Stock Formulas

### Method 1: Combined demand and lead-time variability (preferred)

Use when you have data on both demand variability AND lead-time variability:

```
SS = z × √(LT × σd² + d² × σLT²)

Where:
z = z-score from service level table
LT = average lead time (days)
σd = standard deviation of daily demand
d = average daily demand
σLT = standard deviation of lead time (days)
```

**Example:**
```
z = 1.65 (95% service level)
LT = 14 days
σd = 5 units/day
d = 30 units/day
σLT = 3 days

SS = 1.65 × √(14 × 25 + 900 × 9)
SS = 1.65 × √(350 + 8100)
SS = 1.65 × √8450
SS = 1.65 × 91.9
SS = 152 units
```

### Method 2: Demand variability only

Use when lead time is reliable (σLT ≈ 0):

```
SS = z × σd × √LT
```

**Example:**
```
z = 1.65, σd = 5, LT = 14
SS = 1.65 × 5 × √14 = 1.65 × 5 × 3.74 = 31 units
```

Note: This gives MUCH less safety stock than Method 1. Only use if supplier lead time is truly consistent.

### Method 3: Days-of-cover heuristic

Use when you don't have good variability data:

```
SS = average daily demand × safety days
```

| Situation | Safety Days | Rationale |
|---|---|---|
| Short, reliable lead time (<7d) | 3–5 days | Low risk, quick recovery |
| Moderate lead time (7–21d) | 7–10 days | Standard buffer |
| Long lead time (21–45d) | 10–14 days | Significant exposure |
| Long + unreliable lead time | 14–21 days | High risk, slow recovery |
| Seasonal peak approaching | Add 5–7 days | Demand uncertainty increasing |

**Limitation:** This method doesn't account for actual variability. It's a starting point, not a precision tool.

### Method 4: Max–average method

Use as a quick sanity check:

```
SS = (max daily demand × max lead time) − (avg daily demand × avg lead time)
```

This represents the worst-case gap. It's usually too conservative but useful as an upper bound.

---

## Common Safety Stock Mistakes

1. **Using σ of weekly data for a daily formula** — Make sure demand σ matches the time unit. If using weekly​σ, divide by √7 for daily.

2. **Ignoring lead-time variability** — If you only model demand variability, you'll underestimate safety stock by 30–60% for suppliers with inconsistent delivery.

3. **Setting safety stock once and forgetting** — Demand and lead times change. Recalculate quarterly at minimum.

4. **Same service level for all SKUs** — Hero products deserve 98%+. Slow movers might need only 85%.

5. **Confusing service level types** — Cycle service level (% of cycles without stockout) .≠ fill rate (% of units shipped on time). This guide uses cycle service level.

6. **Not accounting for demand during review period** — If you review inventory weekly, add the review period to lead time in the formula: use (LT + review period) instead of just LT.

---

## Carrying Cost Reference

Safety stock ties up cash. Here's a rough guide to annual carrying cost:

| Cost Component | Typical Range | Notes |
|---|---|---|
| Cost of capital | 8–15% | Opportunity cost of cash tied in inventory |
| Storage / warehousing | 2–5% | 3PL fees, rent allocation |
| Insurance | 0.5–1% | Inventory insurance premiums |
| Shrinkage / obsolescence | 2–5% | Damage, expiry, write-offs |
| **Total carrying cost** | **12–25%** | **Of COGS per year** |

**Quick calculation:**
```
Monthly carrying cost per unit = unit cost × annual carrying rate ÷ 12
Example: $8.50 × 20% ÷ 12 = $0.14/unit/month
Safety stock of 300 units = $42/month in carrying cost
```

Compare this to stockout cost to validate your service level choice.
