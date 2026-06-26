# Demand Analysis Guide for Reorder Planning

Methods for estimating demand when data quality varies — from strong historical data to sparse or noisy signals.

---

## Demand Estimation Methods

### Method 1: Simple moving average (SMA)

**Use when:** Demand is stable with no clear trend or seasonality.

```
Avg daily demand = sum of daily sales (last N days) ÷ N

Recommended windows:
- Fast-moving items (10+ units/day): 30 days
- Moderate movers (2–10/day): 60 days
- Slow movers (<2/day): 90 days
```

**Calculate variability:**
```
σd = √(Σ(daily sales − average)² ÷ (N − 1))
CV (coefficient of variation) = σd ÷ average

CV < 0.5: Low variability — averages are reliable
CV 0.5–1.0: Moderate — safety stock matters
CV > 1.0: High — lumpy demand, consider different approach
```

### Method 2: Trend-adjusted demand

**Use when:** Product is clearly growing or declining.

```
Step 1: Calculate trailing average (last 30 days vs prior 30 days)
Step 2: Growth rate = (recent avg − prior avg) ÷ prior avg
Step 3: Forward estimate = recent avg × (1 + monthly growth rate)^(months ahead)
```

**Example:**
```
Last 30 days avg: 42 units/day
Prior 30 days avg: 38 units/day
Growth rate: (42 − 38) ÷ 38 = 10.5% per month
Forward estimate (1 month): 42 × 1.105 = 46.4 units/day
Forward estimate (2 months): 42 × 1.105² = 51.3 units/day
```

**Warning:** Don't extrapolate growth beyond 2–3 months without additional validation. Growth rarely stays linear.

### Method 3: Seasonal adjustment

**Use when:** Demand has clear seasonal patterns (holiday, summer, back-to-school, etc.)

```
Step 1: Get same-period-last-year sales (SPLY)
Step 2: Calculate year-over-year growth factor
Step 3: Forward estimate = SPLY × YoY growth factor

Example:
Last June sales: 800 units
This vs last year overall growth: +25%
June forecast: 800 × 1.25 = 1,000 units → 33 units/day
```

**If no prior-year data:** Use industry seasonal indices or estimate peak-to-trough ratio from whatever data exists.

### Method 4: Sparse / new product estimation

**Use when:** <30 days of sales data, new product launch, or highly intermittent demand.

Options:
1. **Analog method:** Use sales data from a similar product as proxy
2. **Marketing-adjusted:** Pre-launch forecast × actual-vs-forecast ratio from previous launches
3. **Conservative start:** Use the lower bound of any estimate, set a short review cycle (weekly), and adjust rapidly
4. **Order-based:** If early orders are lumpy (wholesale/B2B), separate wholesale from DTC demand

**Rule: With weak data, shorten the review cycle. Don't compensate by adding massive safety stock — you'll tie up cash on an unproven product.**

---

## Adjusting for Data Quality Issues

### Stockout periods in historical data

If the product was out of stock during your measurement window, raw sales underestimate true demand.

```
Adjustment:
1. Identify stockout days (zero sales + zero inventory)
2. Remove stockout days from the average calculation
3. Or: estimate lost sales = avg daily demand × stockout days
```

**Example:**
```
90-day window, 12 days out of stock
Recorded sales: 2,340 units
Naive average: 2,340 ÷ 90 = 26/day
Adjusted average: 2,340 ÷ 78 = 30/day ← use this
```

### Promotional spikes

If the measurement window includes a major promotion, separate organic from promoted demand:

```
1. Identify promotion days
2. Calculate avg during promo and avg outside promo
3. Use non-promo average for baseline demand
4. Add promo impact separately if another promotion is planned
```

### Return rate adjustment

For products with significant return rates:

```
Net demand = gross sales × (1 − return rate)
Use net demand for reorder planning
```

---

## Demand Classification

Classify products to select the right method:

| Pattern | Characteristics | Best Method | Safety Stock Approach |
|---|---|---|---|
| **Smooth** | CV < 0.5, consistent daily sales | SMA or trend-adjusted | Standard formula (Method 1) |
| **Erratic** | CV 0.5–1.0, variable but regular | SMA with longer window | Higher service level or days-of-cover |
| **Lumpy** | CV > 1.0, intermittent large orders | Separate B2B from DTC | Days-of-cover + manual review |
| **Seasonal** | Clear peaks and troughs | Seasonal adjustment | Adjust by season, peak needs more |
| **New/Launch** | <30 days data | Analog or conservative | Minimal stock + weekly review |

---

## When to Recalculate Demand Estimates

| Trigger | Action |
|---|---|
| Monthly (routine) | Refresh SMA with latest 30/60/90 days |
| Demand shifts >15% | Investigate cause, update forward estimate |
| New promotion planned | Build separate promo demand estimate |
| Seasonal transition | Switch to seasonal method, update SPLY |
| Stockout occurred | Adjust historical data, review safety stock |
| New sales channel added | Separate channel demand, recalculate total |
| Product entering decline | Shorten measurement window, reduce forward estimate |
