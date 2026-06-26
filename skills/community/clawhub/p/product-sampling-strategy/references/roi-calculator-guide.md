# Sampling Campaign ROI Calculator Guide

## Core ROI Formula

```
Campaign ROI (%) = ((Total Attributed Revenue - Total Campaign Cost) / Total Campaign Cost) × 100
```

## Cost Components

### 1. Direct Product Costs
| Item | Formula | Example |
|---|---|---|
| Sample COGS | Units × Cost per unit | 1,000 × $3.50 = $3,500 |
| Sample packaging | Units × Package cost | 1,000 × $1.25 = $1,250 |
| Insert cards/QR codes | Units × Print cost | 1,000 × $0.35 = $350 |
| **Subtotal** | | **$5,100** |

### 2. Distribution Costs
| Item | Formula | Example |
|---|---|---|
| Shipping (direct mail) | Units × Avg shipping | 500 × $3.50 = $1,750 |
| Order insert labor | Units × Handling cost | 500 × $0.50 = $250 |
| Event fees | Per-event cost × Events | $2,000 × 2 = $4,000 |
| Event staff | Hours × Rate × Events | 16 × $25 × 2 = $800 |
| Subscription box fees | Units × Partnership rate | 300 × $3.00 = $900 |
| **Subtotal** | | **$7,700** |

### 3. Technology & Tracking
| Item | Formula | Example |
|---|---|---|
| Survey platform | Monthly cost × Months | $99 × 3 = $297 |
| Landing page | One-time setup | $200 |
| Analytics/attribution | Monthly cost × Months | $50 × 3 = $150 |
| **Subtotal** | | **$647** |

### 4. Incentive Costs
| Item | Formula | Example |
|---|---|---|
| Discount redemptions | Converts × Avg discount | 200 × $6.75 = $1,350 |
| Survey incentives | Respondents × Incentive | 500 × $2.00 = $1,000 |
| **Subtotal** | | **$2,350** |

### 5. Labor & Overhead
| Item | Formula | Example |
|---|---|---|
| Campaign management | Hours × Rate | 40 × $50 = $2,000 |
| Creative/design | Hours × Rate | 15 × $75 = $1,125 |
| Analysis & reporting | Hours × Rate | 10 × $50 = $500 |
| **Subtotal** | | **$3,625** |

### Total Campaign Cost Example
**$5,100 + $7,700 + $647 + $2,350 + $3,625 = $19,422**

## Revenue Attribution

### Short-Term Revenue (0-90 days)
```
First-purchase revenue = Number of converts × Average order value
```
Example: 200 converts × $45 AOV = $9,000

### Medium-Term Revenue (91-365 days)
```
Repeat purchase revenue = Converts × Repeat rate × AOV × Avg purchases per year
```
Example: 200 × 0.35 × $45 × 2.5 = $7,875

### Long-Term Revenue (Lifetime Value)
```
LTV revenue = Converts × Customer LTV
```
Example: 200 × $320 = $64,000

## ROI Calculation by Time Horizon

| Time Horizon | Revenue | Cost | ROI |
|---|---|---|---|
| 90-day | $9,000 | $19,422 | -54% |
| 12-month | $16,875 | $19,422 | -13% |
| Lifetime (3yr) | $64,000 | $19,422 | **230%** |

## Interpreting Results

### ROI Benchmarks for Sampling Campaigns

| ROI Range | Assessment | Action |
|---|---|---|
| > 300% (LTV) | Excellent | Scale aggressively |
| 150-300% (LTV) | Good | Optimize and scale |
| 50-150% (LTV) | Acceptable | Optimize before scaling |
| 0-50% (LTV) | Marginal | Significant optimization needed |
| < 0% (LTV) | Poor | Reassess strategy fundamentally |

### Non-Revenue Value

Factor in qualitative benefits that don't appear in direct ROI:
- **Survey data value**: Market research equivalent cost ($5-50 per response)
- **UGC content**: Content creation equivalent cost ($50-500 per asset)
- **Brand awareness lift**: Estimated media value of impressions
- **Email list growth**: Value per new subscriber ($1-5)
- **Social followers gained**: Value per follower ($0.50-2.00)

### Adjusted ROI Formula (Including Non-Revenue Value)
```
Adjusted ROI = ((Revenue + Non-Revenue Value - Cost) / Cost) × 100
```

## Common ROI Pitfalls

1. **Counting organic sales as sampling conversions** — Always use a control group to isolate the sampling effect. True incremental revenue = sample group revenue - control group revenue (normalized).

2. **Ignoring cannibalization** — If sample recipients would have purchased anyway, the true ROI is lower. Adjust by subtracting the baseline purchase rate of your control group.

3. **Overlooking hidden costs** — Internal labor is the most commonly omitted cost. Track all hours spent on campaign management, creative, and analysis.

4. **Using retail price instead of net revenue** — Calculate ROI on net revenue (after returns, discounts, payment processing, and COGS), not gross sales.

5. **Projecting LTV without data** — Use actual customer cohort data to estimate LTV, not industry averages. If you don't have cohort data yet, use 90-day ROI as your primary metric.
