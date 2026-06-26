# Loyalty Program Economics Guide

Financial modeling for points, tiers, and referral programs. Use these formulas before finalizing any program structure.

---

## Core Economic Principle

A loyalty program is only worth running if the incremental revenue it generates (from increased purchase frequency, AOV, and referrals) exceeds its cost (reward redemptions, tier perks, referral incentives, and administration).

Programs that treat loyalty as a marketing cost without measuring incremental revenue tend to run for years without evidence of positive ROI.

---

## Points Program Economics

### Earn Rate Cost
```
Points cost per order = (Points earned per $1) / (Points per $1 of reward) × (1 − Breakage Rate)

Example:
- Customer earns 5 points per $1
- 500 points = $5 reward
- Therefore: $1 of spend earns 5/500 × $5 = $0.05 of potential reward value
- After 30% breakage: $0.05 × 0.70 = $0.035 actual cost to merchant
- Effective program cost: 3.5% of revenue
```

### Breakage Rate
Breakage = points earned but never redeemed. Industry benchmarks:

| Program Type | Expected Breakage Range |
|---|---|
| General retail points | 20-35% |
| Airline/hotel miles | 15-25% |
| Credit card rewards | 5-15% (redeemed more actively) |
| Small brand loyalty | 35-50% (less top-of-mind) |

**Note:** Higher breakage means lower real cost to merchant, but also lower perceived value to customers. If breakage exceeds 50%, customers don't believe the program is worth engaging with.

### Point Liability
```
Liability = Total points outstanding × (Points value per unit) × (1 − Projected breakage)

Example:
- 500,000 points outstanding
- 100 points = $1 value
- 30% projected breakage
- Liability = 500,000/100 × $1 × 0.70 = $3,500
```

Review point liability quarterly. As programs scale, unredeemed point liability appears as a balance sheet item.

### Break-Even Calculation for Points Program
```
Program break-even = Incremental revenue needed to cover program costs

If program costs 3.5% of revenue, and gross margin is 45%:
Net margin contribution from program spend = 45% − 3.5% = 41.5%

Program is ROI-positive if it generates incremental repeat orders beyond baseline.
Threshold: (Program cost $) / (Gross margin per incremental order $) = Incremental orders needed
```

---

## Tier Program Economics

### Tier Upgrade Rate Modeling
```
Tier cost as % of revenue =
  (% of customers reaching Silver × Average Silver perk cost per customer)
  + (% of customers reaching Gold × Average Gold perk cost per customer)
  ÷ Total revenue
```

### Perk Cost Estimation

| Perk Type | Cost Basis | Estimation Method |
|---|---|---|
| Free shipping | Actual carrier cost per order | Average shipping cost × orders per tier member |
| % discount | Margin reduction on eligible orders | Discount % × AOV × orders per tier member |
| Free product | COGS of gifted item | COGS × expected redemption rate |
| Early access | No direct cost | Lost revenue if early access customers would have bought at full price anyway is zero |
| Dedicated support | Staff time | Hours per tier member × hourly support cost |

### Aspirational Gap Rule
Tier thresholds must create genuine aspiration without being unreachable:

- If more than 50% of customers automatically qualify for Tier 2, the tier is too easy
- If fewer than 5% of customers ever reach Tier 3, it's aspirational but not motivating
- Ideal: 20-35% of customers in Tier 2, 5-15% in Tier 3

---

## Referral Program Economics

### Referral Value Analysis
```
Referral program is worth running if:
Referral cost (referrer reward + referee discount) < Current blended CAC

And:
Gross margin on referred first order > Total referral incentive cost
```

### Referral Conversion Rate Benchmarks
- Ecommerce referral link click-to-purchase: 1-5%
- Referred customer vs. non-referred retention: Referred customers typically retain 25-35% better
- Average referrals per active enrolled member: 0.5-2.0 per year

### Referral ROI Calculation
```
Referral ROI = (LTV of referred customer − CAC via referral) / CAC via referral

Example:
- Referred customer 12-month LTV: $180
- Referral cost (incentives): $25
- Referral ROI = ($180 − $25) / $25 = 620%

Compare to paid acquisition:
- Paid CAC: $45, 12-month LTV: $120
- Paid acquisition ROI = ($120 − $45) / $45 = 167%

Conclusion: Referral channel is 3.7× more efficient than paid acquisition in this example.
```

---

## Combined Program Modeling

For hybrid programs (points + tiers + referral), model each component separately then sum:

```
Total loyalty program cost % of revenue =
  Points redemption cost %
  + Tier perk cost %
  + Referral incentive cost %
  + Admin / tech cost %

Constraint: Total must be ≤ (Gross Margin % − Target Contribution Margin %)
```

### Sensitivity Ranges by Gross Margin

| Gross Margin | Comfortable Program Budget | Maximum Program Budget |
|---|---|---|
| 30-40% | 2-3% of revenue | 4-5% |
| 40-50% | 3-5% of revenue | 6-7% |
| 50-60% | 4-6% of revenue | 8-10% |
| 60%+ | 5-8% of revenue | 10-12% |

High-margin categories (beauty, digital, specialty food) can afford more generous programs. Low-margin categories (electronics accessories, commodity goods) need lean program structures.
