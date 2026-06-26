---
name: inventory-reorder-calculator
description: Estimate ecommerce reorder timing and quantity using demand, lead time, and safety stock assumptions so teams can set reorder points and reduce stockout risk with less guesswork.
---

# Inventory Reorder Calculator

Estimate when to reorder and how much to buy before stock risk turns into lost revenue or excess inventory.

This skill goes beyond plugging numbers into a formula. It applies a structured inventory-planning workflow — demand analysis, lead-time modeling, safety stock calibration, and cash-vs-stockout tradeoff framing — to produce reorder recommendations operators can actually act on.

---

## Quick Reference

| Decision | Key Signal | Strong | Acceptable | Weak |
|---|---|---|---|---|
| Demand estimation | Historical vs assumed | Uses actual sales data + trend/seasonality | Reasonable assumption documented | Made-up round number |
| Safety stock | Risk calibration | Service-level-based (z-score × σ) | Days-of-cover heuristic | No safety stock or arbitrary buffer |
| Lead time | Supplier reliability | Avg + variability modeled | Single estimate documented | Ignored or assumed instant |
| Reorder point | Formula clarity | ROP = LT demand + safety stock, shown | Calculated but not explained | Just a number with no breakdown |
| Order quantity | Constraint-aware | Accounts for MOQ, carton multiples, cash | Basic EOQ or demand × days | Arbitrary round number |
| Risk framing | Actionable tradeoffs | Stockout cost vs carrying cost quantified | Risks named qualitatively | No risk discussion |

---

## Solves

Most ecommerce teams get reorder planning wrong not because they lack data, but because:

- **Gut-feel ordering** — buying "about the same as last time" without modeling demand changes
- **Ignoring lead-time variability** — treating supplier lead time as fixed when it fluctuates 20–50%
- **No safety stock logic** — either zero buffer (stockouts) or massive buffer (cash drag)
- **Formula without context** — calculating ROP without explaining what drives it or when it breaks
- **Missing constraints** — ignoring MOQs, carton multiples, storage limits, or cash flow
- **No risk framing** — presenting a single number without showing the stockout vs overstock tradeoff
- **Static calculations** — one-time number with no guidance on when to recalculate

Goal: **Produce a reorder recommendation that an ops lead, buyer, or founder can act on today — with the math shown, assumptions visible, and risks framed.**

---

## Use when

- You need a practical reorder point for a SKU or product group
- Demand is growing, volatile, or seasonal
- Lead time is long or unreliable
- You want to reduce stockouts without overbuying cash-intensive inventory
- A team needs to explain reorder logic to a buyer, founder, or ops lead
- You're setting up initial reorder rules for a new product or supplier
- Transitioning from gut-feel ordering to data-informed replenishment

## Do not use when

- You need a full supply-chain planning system or ERP implementation
- Historical demand is too weak to support even rough assumptions
- Supplier constraints are unknown and nobody can estimate them
- The task is warehouse slotting or operations design rather than reorder planning
- You need multi-echelon or multi-warehouse optimization

---

## Inputs

Gather these inputs — mark any gaps explicitly:

**Demand data:**
- Average daily or weekly unit sales (last 30/60/90 days)
- Demand trend direction (growing / stable / declining)
- Demand variability (standard deviation of daily sales, or coefficient of variation)
- Known seasonality, promotions, or launches upcoming
- Historical stockout periods (to adjust demand estimates)

**Supply data:**
- Supplier average lead time (order-to-receipt, in days)
- Lead-time variability (best case / worst case / std dev)
- Minimum order quantity (MOQ)
- Carton multiples or packaging constraints
- Supplier reliability notes (late shipment frequency, quality issues)

**Inventory data:**
- Current on-hand stock (units)
- Current in-transit stock (units, ETA)
- Storage capacity constraints
- Current inventory carrying cost (% of COGS per year, or $/unit/month)

**Business context:**
- Target service level (e.g., 95%, 98%, 99%)
- Stockout cost estimate (lost margin + customer impact)
- Cash flow constraints or budget limits
- Review cycle / reorder cadence (daily / weekly / monthly)
- Product lifecycle stage (launch / growth / mature / clearance)

See `references/safety-stock-guide.md` for service level and z-score tables.
See `references/demand-analysis-guide.md` for demand estimation methods.

---

## Workflow

### 1. Analyze demand pattern

Before calculating anything, understand the demand signal:

```
Average daily demand: [X] units/day
Demand std deviation: [σd] units/day
Trend: [growing / stable / declining at Y% per period]
Seasonality: [none / seasonal with peak in Z months]
Data quality: [strong (90+ days) / moderate (30–90 days) / weak (<30 days)]
```

If demand data is weak, flag this prominently — the entire calculation depends on this input.

See `references/demand-analysis-guide.md` for methods to handle trend, seasonality, and sparse data.

### 2. Model lead time

Supplier lead time is rarely constant. Model both average and variability:

```
Average lead time: [LT] days
Lead time std deviation: [σLT] days
Best case: [X] days
Worst case: [Y] days
Data source: [supplier quote / historical POs / assumption]
```

**Rule: If lead time is based on a supplier quote alone (not historical data), add 20–30% buffer. Suppliers are optimistic.**

### 3. Calculate safety stock

Safety stock bridges the gap between average expectations and real-world variability:

**Method 1: Service-level approach (preferred when data exists)**
```
SS = z × √(LT × σd² + d² × σLT²)

Where:
z = service level z-score (1.65 for 95%, 1.96 for 97.5%, 2.33 for 99%)
LT = average lead time in days
σd = standard deviation of daily demand
d = average daily demand
σLT = standard deviation of lead time in days
```

**Method 2: Days-of-cover heuristic (when data is limited)**
```
SS = average daily demand × safety days

Where safety days = typically 5–14 days depending on:
- Lead time length (longer LT → more safety days)
- Demand variability (higher variability → more safety days)
- Stockout cost (higher cost → more safety days)
```

See `references/safety-stock-guide.md` for z-score tables and method selection guidance.

### 4. Calculate reorder point

```
ROP = (average daily demand × average lead time) + safety stock
ROP = (d × LT) + SS
```

Interpret the result: "When on-hand inventory drops to [ROP] units, place a new order."

If in-transit stock exists, use **effective inventory position**:
```
Inventory position = on-hand + in-transit - backorders
Trigger reorder when: inventory position ≤ ROP
```

### 5. Determine reorder quantity

**Basic approach:**
```
Reorder quantity = average daily demand × days of coverage target
```

**Constraint-adjusted approach:**
```
Raw quantity = demand × coverage days
Adjusted for MOQ: max(raw quantity, MOQ)
Adjusted for carton multiple: round up to nearest carton multiple
Adjusted for cash: min(adjusted quantity, budget ÷ unit cost)
Adjusted for storage: min(adjusted quantity, available storage)
```

**EOQ approach (when holding and ordering costs are known):**
```
EOQ = √(2 × annual demand × order cost / holding cost per unit per year)
```

See `references/output-template.md` for the complete output format.

### 6. Frame the risk tradeoffs

Every reorder decision involves tradeoffs. Make them visible:

| Scenario | Stockout Risk | Cash Tied Up | Coverage |
|---|---|---|---|
| Conservative (ROP + 20%) | Very low | High | [X] days |
| Recommended (ROP) | Low | Moderate | [Y] days |
| Aggressive (ROP - 20%) | Moderate | Low | [Z] days |

Quantify when possible:
- "Stockout of [X] days costs ~$[Y] in lost margin"
- "Extra [X] units ties up $[Y] in cash for [Z] weeks"

### 7. Quality-check the recommendation

Before delivering, verify with `assets/reorder-checklist.md`:

- Is the demand estimate based on data (not just a guess)?
- Is lead-time variability accounted for?
- Is safety stock calibrated to a service level or risk tolerance?
- Does the reorder quantity respect MOQ and packaging constraints?
- Are cash flow implications visible?
- Are assumptions explicitly stated?
- Is there guidance on when to recalculate?

---

## Output

Return a structured package (see `references/output-template.md`):

1. **Assumptions table**
   - Every input value with source and confidence level

2. **Demand and lead-time model**
   - Demand stats, trend, variability
   - Lead time stats and variability

3. **Reorder point calculation**
   - Safety stock with method shown
   - ROP with formula and plain-English interpretation

4. **Reorder quantity recommendation**
   - Raw quantity and constraint-adjusted quantity
   - Cash impact estimate

5. **Risk scenario table**
   - Conservative / recommended / aggressive options
   - Stockout risk and cash tradeoff for each

6. **Action items and review triggers**
   - When to place the next order
   - When to recalculate (demand shift, supplier change, etc.)
   - Sensitivity warnings

---

## Quality bar

Strong output should:
- Show the math AND explain it in plain English
- Separate reorder point (when to order) from reorder quantity (how much)
- Account for demand variability, not just averages
- Account for lead-time variability, not just supplier quotes
- Respect real-world constraints (MOQ, cash, storage)
- Frame the stockout vs overstock tradeoff explicitly
- Flag fragile assumptions that could change the recommendation

## What "better" looks like

Better output helps the operator act with confidence:
- Knows when to reorder (and understands why that number, not another)
- Knows roughly how much to buy (and sees the tradeoff in buying more or less)
- Sees the cash vs stockout tradeoff in concrete terms
- Understands where lead-time risk changes the answer
- Can explain the decision to a buyer, founder, or ops lead
- Has clear triggers for when to recalculate

---

## Examples

### Example 1: Growing DTC skincare brand

**Inputs:**
- Product: Vitamin C Serum 30ml
- Average daily sales: 42 units/day (last 90 days, growing ~8%/month)
- Daily demand std dev: 12 units
- Unit cost: $8.50, selling price: $29.99
- Supplier lead time: 21 days avg (std dev: 4 days)
- MOQ: 500 units, carton multiple: 50
- Current stock: 890 units, none in transit
- Target service level: 95%
- Review cadence: weekly

**Output excerpt:**

```
DEMAND MODEL
Avg daily demand: 42 units → adjusted for growth: 46 units/day (8%/mo trend)
Demand σ: 12 units/day
Data quality: Strong (90 days, consistent)

SAFETY STOCK (Service-level method, z=1.65 for 95%)
SS = 1.65 × √(21 × 12² + 46² × 4²)
SS = 1.65 × √(3024 + 33856)
SS = 1.65 × 192
SS = 317 units → round to 320

REORDER POINT
ROP = (46 × 21) + 320 = 966 + 320 = 1,286 units

⚠️ Current stock (890) is BELOW reorder point. Order now.

REORDER QUANTITY
Target coverage: 30 days post-receipt
Raw qty: 46 × 30 = 1,380 units
Adjusted for MOQ: 1,380 (above 500 MOQ ✓)
Adjusted for carton: 1,400 (nearest 50 multiple)
Cash required: 1,400 × $8.50 = $11,900

RISK SCENARIOS
| Scenario | Order Qty | Stockout Risk | Cash | Coverage |
|---|---|---|---|---|
| Conservative | 1,700 | <2% | $14,450 | 37 days |
| Recommended | 1,400 | ~5% | $11,900 | 30 days |
| Aggressive | 1,100 | ~12% | $9,350 | 24 days |
```

### Example 2: Seasonal product with unreliable supplier

**Inputs:**
- Product: Insulated water bottle
- Average daily sales: 18 units/day (but seasonal: 30/day in summer, 8/day in winter)
- Current month: April (ramping up)
- Supplier lead time: 35 days avg, range: 28–50 days
- MOQ: 200, unit cost: $6.20
- Current stock: 520, 300 in transit (ETA 2 weeks)

**Output excerpt:**

```
DEMAND MODEL
Current avg: 18 units/day
Seasonal forecast (next 60 days): ramping to ~25 units/day
Using forward estimate: 25 units/day
Demand σ: 7 units/day (higher variability due to seasonal transition)

⚠️ LEAD TIME WARNING
Avg LT: 35 days, but range is 28–50 days (σLT ≈ 6 days)
This supplier has high variability — safety stock must account for this.

SAFETY STOCK (z=1.65 for 95%)
SS = 1.65 × √(35 × 49 + 625 × 36) = 1.65 × √(1715 + 22500) = 1.65 × 156 = 257 units

REORDER POINT
ROP = (25 × 35) + 257 = 875 + 257 = 1,132 units

INVENTORY POSITION
On-hand: 520 + in-transit: 300 = 820
820 < 1,132 → ⚠️ Below ROP. Order immediately.

Days until stockout (no reorder): 520 ÷ 25 = 20.8 days
In-transit arrives in ~14 days → post-arrival: (520 - 350) + 300 = 470 units
470 ÷ 25 = 18.8 more days → ~33 days total before stockout

ACTION: Order now. Lead time of 35 days means new stock arrives just as
current + in-transit runs out. Any delay = stockout during peak season.
```

---

## Common mistakes

1. **Using averages without variability** — "We sell 20/day" ignores that some days are 8 and others are 35
2. **Trusting supplier lead times** — Quoted lead times are best-case; actual delivery is often 20–50% longer
3. **Forgetting in-transit inventory** — Reordering when stock is low but 1,000 units are already shipping
4. **Ignoring MOQ and carton constraints** — Calculating a perfect 347-unit order when MOQ is 500
5. **No cash flow context** — Recommending a $50K order to a business with $30K available
6. **Static one-time calculation** — Giving a number without saying when it should be recalculated
7. **Safety stock = gut feel** — Using "2 weeks of safety stock" without connecting it to demand variability
8. **Not adjusting for trend** — Using historical averages for a product that's growing 15%/month

---

## Resources

- `references/output-template.md` — Complete structured output template
- `references/safety-stock-guide.md` — Service levels, z-scores, and safety stock methods
- `references/demand-analysis-guide.md` — Demand estimation, trend adjustment, and seasonality handling
- `assets/reorder-checklist.md` — Pre-delivery quality checklist
