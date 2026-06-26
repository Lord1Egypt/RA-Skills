# Profit Margin Analysis — Quality Checklist

Use this checklist before delivering a margin analysis report. Every item should be confirmed or explicitly noted as not applicable.

## Data Completeness

- [ ] Selling prices captured for all SKUs on all active channels (net of coupons/promotions)
- [ ] COGS/landed cost documented per SKU with source (supplier invoice, ERP, manual entry)
- [ ] Landed cost includes manufacturing, tariffs/duties, and inbound freight — not just purchase price
- [ ] Platform fee schedules identified for each channel (Amazon referral %, FBA tier, Shopify plan)
- [ ] Payment processing rates confirmed for DTC channels (Stripe/PayPal rate + fixed fee)
- [ ] Shipping costs captured per product or per order with method and zone data
- [ ] Return rates available at the SKU or category level with return reason breakdown
- [ ] Advertising spend available at SKU or campaign level for the analysis period
- [ ] Storage/warehousing costs documented (FBA storage rates, 3PL rates, or own warehouse allocation)
- [ ] Data period is clearly stated and consistent across all sources (same date range)
- [ ] Any estimated or proxy data is flagged with estimation method documented

## Cost Accuracy

- [ ] Amazon referral fees applied at the correct category-specific rate (not a blended average)
- [ ] FBA fulfillment fees matched to each product's actual size tier and weight tier
- [ ] Products near FBA tier boundaries verified with correct dimensional measurements
- [ ] Storage fees calculated using the correct monthly rate (standard vs. Q4 rate)
- [ ] Long-term storage surcharges included for slow-moving inventory (271+ days)
- [ ] Payment processing calculated with both percentage and fixed fee components
- [ ] Shipping costs reflect actual carrier rates (negotiated/commercial, not retail)
- [ ] Return costs include all components: return shipping, restocking, lost referral fee, disposal
- [ ] Ad spend attribution method documented (direct ASIN, campaign-level, blended)
- [ ] Multi-channel products carry channel-specific cost stacks (not blended across channels)
- [ ] Currency conversions applied correctly if sourcing or selling internationally
- [ ] Fee schedule versions/dates confirmed as current

## Margin Calculations

- [ ] Net contribution margin calculated for every SKU (not just gross margin)
- [ ] Full cost waterfall presented: price → COGS → gross margin → fees → fulfillment → shipping → storage → returns → advertising → net contribution
- [ ] No cost layers omitted or double-counted in the waterfall
- [ ] Margin percentages calculated on net selling price (after coupons), not listed price
- [ ] Portfolio-level margins are revenue-weighted (not simple averages across SKUs)
- [ ] Margins calculated per channel for multi-channel products
- [ ] Contribution dollars calculated (not just percentages) — dollar amounts drive decisions
- [ ] Margin calculations independently verified on at least 3 representative SKUs (spot check)

## Product Classification

- [ ] Every SKU assigned to a margin tier (Strong >25% / Healthy 15-25% / Thin 5-15% / Breakeven 0-5% / Negative <0%)
- [ ] Tier thresholds appropriate for the business (adjusted if industry norms differ)
- [ ] Pareto analysis completed: top 20% of SKUs by contribution identified
- [ ] Margin-negative SKUs individually listed with specific cost drivers identified
- [ ] Category-level and channel-level margin summaries calculated
- [ ] Revenue share and contribution share calculated per tier (not just SKU counts)

## Margin Leak Analysis

- [ ] Systematic review completed across all cost layers (not just the obvious ones)
- [ ] FBA tier boundary opportunities identified (products within 0.5" or 2 oz of a threshold)
- [ ] High-return-rate products identified with return costs quantified per unit
- [ ] High-ACoS products identified with breakeven ACoS calculated per product
- [ ] Slow-moving inventory flagged with annualized storage cost per unit calculated
- [ ] Category misclassification opportunities identified (lower-fee category eligibility)
- [ ] Free shipping margin impact quantified (orders where shipping cost exceeds margin benefit)
- [ ] Each margin leak ranked by annual dollar impact (not just per-unit impact)
- [ ] Root cause documented for each leak (not just the symptom)
- [ ] At least 3 margin leaks identified and quantified (if fewer, document why)

## Improvement Scenarios

- [ ] At least 3 improvement scenarios modeled with specific financial projections
- [ ] Each scenario includes: lever, current state, target state, per-unit impact, annual impact
- [ ] Assumptions stated explicitly for each scenario (not embedded in calculations)
- [ ] Implementation cost and timeline estimated for each scenario
- [ ] Risk or tradeoff documented for each scenario (what could go wrong)
- [ ] Combined scenario summary shows total portfolio impact (margin % and contribution $)
- [ ] Scenarios prioritized by ROI or impact-to-effort ratio
- [ ] No scenario assumes unrealistic improvements (e.g., 50% COGS reduction without evidence)
- [ ] Constraint validation completed: are the assumptions behind each scenario achievable?

## Report Quality

- [ ] Executive summary present with portfolio-level margin metrics and key findings
- [ ] Cost structure breakdown shows where each revenue dollar goes (waterfall table)
- [ ] Product-level margin table includes all SKUs (or top/bottom N with full table in appendix)
- [ ] Margin distribution chart or table shows tier breakdown by SKU count, revenue, and contribution
- [ ] Margin leaks ranked and quantified with annual dollar impact
- [ ] Improvement scenarios are specific and actionable (not generic advice)
- [ ] Risk register included with likelihood, impact, and mitigation for key risks
- [ ] Methodology notes document fee schedules used, allocation methods, and data limitations
- [ ] Next steps include specific actions with dates and owners
- [ ] Report follows the output template structure
- [ ] No math errors in summary tables (totals add up, percentages sum correctly)
- [ ] All dollar figures consistent between summary and detail sections
