# Stage Classification Framework

## Overview

The lifecycle stage classification converts raw sales trajectory data into one of four stages: Introduction, Growth, Maturity, or Decline. Each assignment includes a confidence level and supporting data points. This guide details the classification rules, thresholds, and edge cases.

## Stage Definitions and Thresholds

### Introduction Stage

**Primary indicators**:
- Product launched within the last 6 months (if launch date available)
- Revenue below 10% of category average
- Positive but modest month-over-month growth
- Limited sales history (fewer than 6 data points)

**Secondary indicators**:
- High customer acquisition cost relative to revenue
- Low or negative profit contribution
- Small review/rating count (for marketplace products)
- Frequent listing or pricing adjustments

**Confidence scoring**:
- High: Launch date confirmed, <3 months old, clear upward trajectory
- Medium: No launch date but revenue pattern consistent with new product
- Low: Ambiguous — could be Introduction or underperforming Maturity product

### Growth Stage

**Primary indicators**:
- Positive revenue acceleration (growth rate itself is increasing)
- Revenue between 10-80% of eventual peak (estimated from trajectory)
- Month-over-month unit growth above 10% sustained for 3+ months
- Expanding customer base (repeat rate increasing OR new customer acquisition rising)

**Secondary indicators**:
- Improving margins from scale efficiencies
- Increasing organic search visibility or Best Seller Rank improvement
- Positive review velocity (reviews accumulating faster than average)
- Competitor response (new entrants appearing in the subcategory)

**Confidence scoring**:
- High: 6+ months of data showing clear accelerating pattern
- Medium: 3-5 months of positive trend
- Low: Short data window or growth driven by a single promotional event

### Maturity Stage

**Primary indicators**:
- Revenue within 20% of all-time peak
- Month-over-month growth rate between -5% and +5% for 3+ months
- Stable or slowly declining unit velocity
- Peak absolute profit contribution

**Secondary indicators**:
- Market saturation signals (flattening new customer acquisition)
- Price competition increasing
- Advertising cost per acquisition rising
- Category growth slowing

**Confidence scoring**:
- High: 12+ months of data, clear plateau pattern
- Medium: 6-11 months, appears stable but limited history
- Low: Could be temporary plateau in Growth or early Decline

### Decline Stage

**Primary indicators**:
- Revenue more than 20% below all-time peak
- Negative month-over-month trend sustained for 3+ consecutive months
- Decelerating sales velocity
- Shrinking contribution to total catalog revenue

**Secondary indicators**:
- Margin compression from increased discounting
- Rising inventory days of supply
- Declining search visibility or Best Seller Rank
- Customer reviews mentioning "outdated" or mentioning competitor alternatives

**Confidence scoring**:
- High: Clear sustained downtrend with no external explanation (not seasonal, not stockout)
- Medium: Downtrend present but could be influenced by external factors
- Low: Recent decline that may be temporary or seasonal

## Edge Cases and Overrides

### Seasonal Products
Do NOT classify seasonal products using out-of-season data. Options:
1. Use year-over-year comparisons for the same season
2. Exclude off-season months from trajectory analysis
3. Flag as "Seasonal — classify during peak window"

### Stockout-Affected Products
A stockout creates an artificial decline in sales data. If inventory was at zero for any period:
1. Exclude zero-inventory periods from trajectory analysis
2. Use pre-stockout and post-restock data to assess true demand
3. Flag the stockout in the confidence notes

### Promotional Spikes
A one-time promotional spike doesn't indicate Growth. Rules:
1. If more than 50% of a product's best month came from a single promotion, discount that month
2. Use the underlying trend excluding promotional periods
3. A product that only sells well during promotions is likely Maturity or Decline, not Growth

### Platform Migration
Products moved to a new platform will show Introduction patterns despite being mature:
1. If historical data from the previous platform is available, use combined trajectory
2. If not, flag as "Platform Migration — true stage uncertain"

### Relaunched Products
Products that were discontinued and relaunched should be treated as new introductions for classification purposes, but with the caveat that historical performance provides a demand ceiling estimate.

## Composite Classification Logic

When primary indicators conflict, use this priority order:
1. Revenue trajectory direction (most weight)
2. Growth rate acceleration/deceleration
3. Distance from peak revenue
4. Time since launch (least weight, as this is unreliable without confirmed dates)

If two stages score equally, default to the more conservative (later-stage) classification to avoid over-investing in a product that may already be peaking.
