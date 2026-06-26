# Runway Calculation & Survival Math

How to calculate runway, interpret burn rate, and know when to act.

---

## Core Formulas

### Monthly Burn Rate

```
monthly_burn = Σ(critical recurring) + Σ(important recurring) + avg(variable costs, 3 months)
```

Include only `upcoming` or `paid` status outflows. Exclude `cancelled` and `deferred`.

Optional items are excluded from burn rate — they're the first to cut.

### Weighted Monthly Income

```
weighted_monthly_income = Σ(high_confidence_inflows × 0.95) + Σ(medium × 0.60) + Σ(low × 0.20)
```

Use only inflows with `status = expected` or `status = partial` (for remaining amount).

### Net Monthly Burn

```
net_monthly_burn = monthly_burn - weighted_monthly_income
```

- Positive = spending more than earning (burning cash)
- Zero = breaking even
- Negative = earning more than spending (building cash)

### Runway

```
If net_monthly_burn > 0:
  runway_months = opening_cash / net_monthly_burn

If net_monthly_burn <= 0:
  runway = unlimited (cash-flow positive)
  reserve_months = opening_cash / monthly_burn  (if all income stops)
```

---

## Survival Thresholds

| Runway | Status | Action Required |
|--------|--------|----------------|
| **6+ months** | Healthy | Focus on growth. Build cash reserve. Invest in marketing. |
| **3–6 months** | Warning | Start cost optimization. Accelerate collections. Review pricing. |
| **1–3 months** | Critical | Activate survival mode. Cut all optional expenses. Chase all AR. |
| **< 1 month** | Emergency | Immediate action. Consider bridge financing. Defer all non-critical payments. |

### Conservative vs Base Runway

Always calculate runway under both base and conservative scenarios:

```
runway_base = opening_cash / net_burn_base
runway_conservative = opening_cash / net_burn_conservative
```

**Use conservative runway for all threshold decisions.** If conservative runway is < 3 months, it's critical — even if base runway shows 5 months.

---

## Alert Triggers

| Alert Type | Condition | Severity |
|------------|-----------|----------|
| `runway_warning` | Conservative runway < 3 months | critical |
| `runway_warning` | Conservative runway < 6 months | warning |
| `negative_cash` | Any scenario shows negative cash in forecast period | critical |
| `collection_urgent` | High-confidence inflow overdue > 7 days | warning |
| `collection_urgent` | Any inflow overdue > 30 days | critical |
| `large_outflow` | Single outflow > 30% of opening cash | warning |
| `concentration_risk` | Single client > 50% of expected inflows (weighted) | warning |

### Alert Priority

When multiple alerts fire, sort by:
1. Severity: critical → warning → info
2. Type priority: negative_cash → runway_warning → collection_urgent → large_outflow → concentration_risk
3. Amount impacted (descending)

---

## Cash Reserve Recommendations

| Business Stage | Recommended Reserve |
|----------------|-------------------|
| Pre-revenue / early stage | 6+ months of critical expenses |
| Revenue but < break-even | 4–6 months of total burn |
| Break-even | 3–4 months of total burn |
| Profitable | 3 months of critical expenses |

Reserve = cash you refuse to spend on operations. It's your personal runway floor.

---

## Burn Rate Breakdown Display

Show burn rate broken down by essentiality:

```
Monthly Burn Rate: $8,500
  Critical:  $4,200 (49%) — rent, insurance, hosting, taxes
  Important: $3,100 (36%) — contractors, key software, utilities
  Optional:  $1,200 (14%) — subscriptions, marketing, coworking

If you cut all optional:  $7,300/mo → extends runway by X months
If you also defer important: $4,200/mo → extends runway by Y months
```

This shows the founder exactly how much runway each tier of cuts buys.

---

## Seasonal Adjustment

If the business has seasonal revenue patterns:

1. Tag inflows with historical monthly revenue percentages
2. Apply seasonal factor to medium/low confidence inflows
3. Don't apply to high-confidence (they have specific invoices/contracts)

Example: If Q1 is typically 60% of Q3 revenue, adjust medium-confidence Q1 inflows by 0.6.

---

## When to Panic vs When to Optimize

### Don't Panic If:

- Base runway > 6 months and conservative > 3 months
- You have confirmed high-confidence inflows covering next month's burn
- Burn rate is stable or decreasing month-over-month
- You have a clear path to collecting outstanding AR

### Take Action If:

- Conservative runway < 6 months
- Any forecast scenario shows negative cash within 60 days
- Largest client represents > 50% of income (concentration risk)
- AR aging is getting worse (average days to pay increasing)
- Burn rate is increasing without corresponding revenue growth

### Emergency If:

- Conservative runway < 2 months
- Cannot cover next month's critical expenses
- Major client has stopped responding / is in dispute
- Multiple high-confidence inflows have been delayed

---

## Runway Display Format

```
=== RUNWAY ANALYSIS ===

Cash on hand:        $25,000
Monthly burn rate:   $8,500
Weighted income:     $6,200
Net monthly burn:    $2,300

Runway (base):         10.9 months
Runway (conservative):  6.2 months  ← USE THIS FOR DECISIONS
Runway (aggressive):   18.4 months

Status: ⚠️ WARNING — Conservative runway < 6 months

If all income stops:    2.9 months (critical expenses only)
```
