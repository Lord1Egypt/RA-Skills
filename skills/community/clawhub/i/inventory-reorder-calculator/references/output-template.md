# Inventory Reorder Calculator Output Template

Structure every reorder recommendation with this format:

---

## Assumptions

| Variable | Value | Source | Confidence |
|---|---|---|---|
| Average daily demand | [X] units/day | [Sales data, last N days] | [High / Medium / Low] |
| Demand std deviation | [σd] units/day | [Calculated from data / estimated] | [High / Medium / Low] |
| Demand trend | [Growing / Stable / Declining at Y%] | [Data trend / assumption] | [High / Medium / Low] |
| Supplier lead time | [LT] days | [Historical POs / supplier quote] | [High / Medium / Low] |
| Lead time std deviation | [σLT] days | [Historical / estimated] | [High / Medium / Low] |
| Unit cost (landed) | $[X] | [Invoice / quote] | [High / Medium / Low] |
| Target service level | [X]% | [Business decision] | — |
| MOQ | [X] units | [Supplier terms] | [High / Medium / Low] |
| Carton multiple | [X] units | [Supplier / 3PL spec] | [High / Medium / Low] |
| Review cadence | [Daily / Weekly / Monthly] | [Current process] | — |

---

## Demand Model

```
Average daily demand: [X] units/day
Adjusted for trend: [Y] units/day (if applicable)
Demand σ: [σd] units/day
Coefficient of variation: [CV = σd/d] → [low (<0.5) / moderate (0.5–1.0) / high (>1.0)]
Data quality: [Strong / Moderate / Weak] — based on [X] days of history
Seasonality: [None / Peak in X months / Currently in peak]
```

⚠️ [Flag any demand-data concerns here]

---

## Lead Time Model

```
Average lead time: [LT] days
Lead time σ: [σLT] days
Best case: [X] days
Worst case: [Y] days
Source: [Historical POs (N orders) / Supplier quote / Assumption]
```

⚠️ [Flag any lead-time concerns here — e.g., supplier based in region with holiday shutdowns, port congestion, etc.]

---

## Safety Stock Calculation

**Method used:** [Service-level / Days-of-cover heuristic]

```
[Show formula and calculation step by step]

Service level: [X]% → z-score: [Z]
SS = z × √(LT × σd² + d² × σLT²)
SS = [Z] × √([LT] × [σd]² + [d]² × [σLT]²)
SS = [Z] × √([A] + [B])
SS = [Z] × [C]
SS = [result] units → rounded to [final] units
```

Plain English: "Keep [X] units as a buffer to maintain [Y]% chance of not stocking out during a replenishment cycle."

---

## Reorder Point

```
ROP = Lead Time Demand + Safety Stock
ROP = (d × LT) + SS
ROP = ([d] × [LT]) + [SS]
ROP = [LTD] + [SS]
ROP = [result] units
```

**Interpretation:** "When your inventory position (on-hand + in-transit − backorders) drops to **[ROP] units**, place a new purchase order."

### Current Status
```
On-hand: [X] units
In-transit: [Y] units (ETA: [date])
Inventory position: [X + Y] units
ROP: [Z] units
Status: [✅ Above ROP — no action needed / ⚠️ Below ROP — order now / 🚨 Critical — days to stockout: N]
```

---

## Reorder Quantity

```
Target coverage: [X] days post-receipt
Raw quantity: [d] × [coverage days] = [Q] units
```

**Constraint adjustments:**
| Constraint | Adjustment | Result |
|---|---|---|
| MOQ ([X] units) | [Above / rounded up] | [Q'] units |
| Carton multiple ([X] units) | [Rounded up to nearest] | [Q''] units |
| Cash available ($[X]) | [Within / exceeds budget] | [Q'''] units |
| Storage capacity | [Within / exceeds limit] | [Final Q] units |

**Final recommended order: [Final Q] units**
**Estimated cost: $[Final Q × unit cost]**

---

## Risk Scenario Table

| Scenario | Order Qty | Safety Stock | Stockout Risk | Cash Tied Up | Coverage Post-Receipt |
|---|---|---|---|---|---|
| Conservative (+20% SS) | [Q] | [SS×1.2] | [X]% | $[Y] | [Z] days |
| **Recommended** | **[Q]** | **[SS]** | **[X]%** | **$[Y]** | **[Z] days** |
| Aggressive (−20% SS) | [Q] | [SS×0.8] | [X]% | $[Y] | [Z] days |

**Stockout cost context:** [X] days of stockout ≈ $[Y] in lost gross margin + [qualitative impact: review damage, ad waste, etc.]
**Carrying cost context:** [X] extra units ≈ $[Y]/month in holding cost

---

## Action Items

**Immediate:**
- [ ] [Place PO for X units / No action needed — next review on DATE]
- [ ] [Confirm lead time with supplier before ordering]
- [ ] [Review in-transit shipment status]

**Recalculate when:**
- Demand shifts >15% from current average
- Supplier lead time changes significantly
- Upcoming promotion or seasonal shift (recalculate 1 lead time in advance)
- After a stockout event (review safety stock adequacy)
- [Specific trigger for this product]

**Sensitivity warnings:**
- [Which assumptions, if wrong, change the recommendation most?]
- [What's the breakeven point where conservative vs aggressive flips?]
- [Any upcoming events that could disrupt this calculation?]
