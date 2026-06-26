---
name: inventory-forecast
description: Project inventory needs based on historical order velocity, seasonality, supplier lead times, and planned promotions so you reorder before stockouts hurt rankings. Use when calculating reorder points, planning promo stock, building reorder calendars, or comparing sell-through across SKUs.
---

# Inventory Forecast

Running out of stock is one of the most costly mistakes in ecommerce — it tanks your search rankings, hands sales to competitors, and can take weeks to recover from. This skill projects inventory needs by analyzing historical order velocity, seasonal demand patterns, supplier lead times, and upcoming promotional events so you can place reorders with confidence before stockouts damage your momentum.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Velocity baseline | Trailing 90-day daily average, weighted toward recent 30 days, excluding promo spikes | Trailing 30-day simple average | Lifetime average or single best month |
| Safety stock | Statistical: z-score × demand std dev × √lead time | Fixed 20-30% buffer on lead-time demand | None, or "whatever is left over" |
| Lead time input | Full door-to-door: production + QC + freight + customs + receiving, with variance | Supplier's quoted production time + standard transit | Supplier's quoted production time alone |
| Promo demand lift | Modeled from your own past promo lift for the same SKU/category | Category benchmark (e.g., 2-4x for flash sales) | Guessing or ignoring the promo |
| Seasonality | Month-over-month index built from 12+ months of own data | Platform/category seasonal curve (e.g., Q4 lift) | Assuming flat demand year-round |
| Reorder trigger | Reorder point = (daily velocity × lead time) + safety stock, reviewed weekly | Fixed calendar reorders (e.g., monthly) sized by forecast | Reordering when stock "looks low" |
| Overstock handling | Flag SKUs with >90 days of cover and propose markdown/bundle plan | Note slow movers in the report | Treat all SKUs the same |

## Solves

1. Stockouts on fast-moving SKUs that destroy search ranking and Buy Box position, discovered only after inventory hits zero.
2. Promotional events (flash sales, 9.9/11.11 campaigns, Prime Day) that sell through prepared stock in hours because the demand lift was never modeled.
3. Long supplier lead times (30-90 days) that make "order when low" impossible — the reorder decision has to happen weeks before the shelf looks empty.
4. Cash trapped in overstocked slow movers while bestsellers starve for reorder budget.
5. No visibility into which SKUs need urgent action — everything is tracked in a spreadsheet nobody updates.
6. New warehouse or FBA allocation decisions made by gut feel rather than regional demand data.
7. Seasonal demand swings (holiday, back-to-school, summer) that catch the catalog under- or over-stocked every single year.

## Workflow

### Step 1 — Gather inputs
Collect from the user: (a) sales history per SKU — ideally 12 months, minimum 90 days, daily or weekly granularity; (b) current on-hand and inbound inventory; (c) supplier lead times per SKU including production, freight mode, and customs; (d) upcoming promotions with dates and expected discount depth; (e) any MOQ (minimum order quantity) and case-pack constraints. If data is in a CSV or export, parse it. If anything critical is missing, state the assumption you are making rather than stalling.

### Step 2 — Compute baseline velocity
For each SKU, compute daily sales velocity over the trailing 90 days, weighting the most recent 30 days more heavily (e.g., 50/30/20 across the three months). Exclude or normalize days affected by past promotions and stockouts — a stockout day is not a zero-demand day; estimate lost demand from the run rate before the stockout.

### Step 3 — Apply seasonality and trend
Build a seasonal index from the user's own history if 12+ months exist (each month's sales ÷ average month). Otherwise apply a category curve and say so. Multiply baseline velocity by the index for the forecast window. Apply a trend factor if the SKU is clearly growing or declining (compare trailing 30-day vs. trailing 90-day velocity).

### Step 4 — Layer in promotional lift
For each planned promotion, estimate units: promo lift multiplier × baseline daily velocity × promo duration. Derive the multiplier from the user's past promos on the same SKU when available; otherwise use conservative category benchmarks (flash sale 2-4x, sitewide sale 1.5-2.5x, livestream feature 3-8x) and flag the uncertainty. Add post-promo pull-forward decay (typically 10-20% velocity dip for 1-2 weeks after).

### Step 5 — Calculate reorder points and quantities
For each SKU: reorder point = (forecast daily velocity × full lead time in days) + safety stock. Safety stock = z × σ_demand × √(lead time), using z = 1.65 for 95% service level on A-SKUs; a simpler 25% buffer is acceptable for C-SKUs. Order quantity = forecast demand over (lead time + review period) − on-hand − inbound + safety stock, rounded up to MOQ/case pack. Flag any SKU already past its reorder point as URGENT.

### Step 6 — Build the reorder calendar
Lay out a rolling 90-day calendar: for each SKU, the last safe order date (promo date or projected stockout date minus full lead time), quantity, and estimated PO cost. Sequence POs so cash outlay is visible week by week. Flag conflicts: orders that must be placed this week, and promos that cannot be fully stocked in time with options (air freight portion, cap promo units, split shipment).

### Step 7 — Verify and deliver
Sanity-check: does total forecast demand roughly reconcile with trailing revenue? Are days-of-cover post-reorder within 30-90 days for A-SKUs? Is any SKU both flagged urgent and overstocked (data error)? Deliver using the output template in `references/output-template.md`, run the checklist in `assets/forecast-quality-checklist.md`, and state every assumption made.

## Worked Example 1 — Flash sale prep with a 45-day lead time

**Input:** "I sell a collagen drink on TikTok Shop. Baseline is about 38 units/day over the last 90 days (last 30 days: 45/day). I'm confirmed for a Flash Sale on July 15, 25% off, 24 hours. Supplier lead time is 30 days production + 12 days sea freight + 3 days receiving. On hand: 1,850 units. Inbound: 1,000 arriving June 20. Last flash sale in March did 410 units in a day when baseline was 30/day. MOQ 500, case pack 50."

**Process:** Weighted velocity ≈ 42/day (recent 30 days weighted up). March promo lift = 410 ÷ 30 ≈ 13.7x — well above the 2-4x benchmark, so use own data: forecast promo day ≈ 13.7 × 42 ≈ 575 units, plus 15% halo on the surrounding 2 days ≈ 640 total event units. Post-promo dip: −15% for 10 days. Full lead time = 45 days. Demand June 1 → July 15 (44 days): ≈ 42/day × 44 ≈ 1,850 units + event 640 ≈ 2,490. Available = 1,850 + 1,000 = 2,850. Post-event position ≈ 360 units ≈ 9 days of cover — under safety stock (z=1.65, σ≈12, √45 ≈ 6.7 → ≈ 135 units, but 9 days cover with 45-day lead time means certain stockout before the next PO can land). Reorder qty for next 75 days: 42 × 75 × 1.05 seasonal ≈ 3,300 − 360 on-hand-after + 135 safety ≈ 3,100 → round to 3,100 → 3,100/50 = 62 case packs. Last safe order date: July 15 + 9 days cover − 45 days lead = **June 9 — order this week.**

**Output:** Urgent PO of 3,100 units by June 9; flash sale fully stockable; post-event coverage restored to 75 days. If the PO slips past June 14, recommend 600 units by air (12-day door-to-door) to bridge the gap.

## Worked Example 2 — Multi-SKU triage with overstock

**Input:** CSV export with 14 SKUs from a Shopee home-goods store, 12 months of history, current stock levels, all from one supplier with 60-day door-to-door lead time, reviewing orders monthly.

**Process:** Compute weighted velocity and seasonal index per SKU. Results cluster into three groups. (a) Three A-SKUs (storage boxes, drying racks) at 25-60 units/day with 20-35 days of cover — all past reorder point given 60-day lead time → URGENT, with lost-demand adjustment because the drying rack stocked out for 6 days in May (velocity corrected from 31 to 36/day). (b) Seven B-SKUs healthy at 70-100 days cover → schedule normal POs in the calendar across the next 6 weeks. (c) Four C-SKUs with 180-400 days of cover including a seasonal fan stand heading into low season → no reorder; propose 11.11 bundle with the storage boxes and a 20% markdown to free an estimated $4,200 in cash by year end.

**Output:** Reorder table with urgent/scheduled/skip flags, a 90-day PO calendar showing ~$18,400 in POs across 3 batches, lost-demand-corrected velocities, and an overstock action plan. Assumptions stated: no promotions planned (user confirmed), category seasonality applied to 2 SKUs with <12 months history.

## Common Mistakes

1. **Using lifetime average velocity.** A SKU growing 15% month over month will stock out long before a lifetime average predicts; always weight recent data.
2. **Treating stockout days as zero-demand days.** This bakes past failures into future forecasts and guarantees you under-order again. Estimate lost demand from the pre-stockout run rate.
3. **Using the supplier's quoted lead time.** "30 days" from the supplier means production only. Door-to-door including freight, customs, and receiving is the number that matters.
4. **Ignoring the post-promo dip.** A big promo pulls demand forward; ordering as if the promo-week velocity continues leads to overstock.
5. **Applying one safety-stock policy to all SKUs.** A-SKUs deserve statistical safety stock at high service levels; tying the same buffer to C-SKUs traps cash.
6. **Forgetting MOQ and case-pack rounding.** A mathematically perfect order quantity of 1,037 units is useless if MOQ is 2,000 — surface the conflict and model the carrying cost.
7. **Forecasting in units while the user budgets in cash.** Always show the PO cost timeline, not just unit counts — the binding constraint is often the bank account.
8. **Hiding assumptions.** When you substitute a category benchmark for missing data, say so explicitly; a forecast with hidden guesses is worse than no forecast.
9. **One-and-done forecasting.** A forecast is stale in two weeks. Always include the review cadence and the trigger conditions for re-running it.

## Resources

- `references/output-template.md` — structured output template for the forecast report
- `references/demand-forecasting-methods.md` — velocity weighting, seasonality indexing, promo lift modeling
- `references/lead-time-and-safety-stock.md` — lead time decomposition, safety stock formulas, service levels, reorder math
- `assets/forecast-quality-checklist.md` — pre-delivery quality checklist
