# Forecast Quality Checklist

Run before delivering any inventory forecast. Every unchecked item is either fixed or disclosed in Assumptions.

## Data inputs
- [ ] Sales history covers ≥90 days (or short-history caveat applied)
- [ ] Stockout periods identified and demand-corrected, not counted as zero
- [ ] Past promo days excluded from baseline and modeled separately
- [ ] One-off outliers (bulk orders, viral spikes) verified or excluded
- [ ] Current on-hand AND inbound inventory both captured
- [ ] MOQ and case-pack constraints collected per SKU

## Velocity & demand
- [ ] Recent-weighted velocity used (not lifetime average)
- [ ] Trend factor applied and capped at ±30% absent a structural driver
- [ ] Seasonal index from own data where ≥12 months exist
- [ ] Benchmark curves flagged as benchmarks wherever used
- [ ] Multi-channel demand forecast per channel where lead-time-critical

## Lead time
- [ ] Lead time built door-to-door (production + QC + freight + customs + receiving)
- [ ] Lead-time variance considered (supplier reliability, customs risk)
- [ ] Peak-season / CNY inflation applied to affected POs
- [ ] Air-freight bridge option costed where timelines are tight

## Promotions
- [ ] Every confirmed promo in the window is modeled
- [ ] Lift multiplier from own history where available; source stated
- [ ] Halo days added and post-promo dip subtracted
- [ ] Promo stock plan checked against actual stock position

## Reorder math
- [ ] Reorder point = velocity × lead time + safety stock, per SKU
- [ ] Safety stock method matches SKU class (statistical for A-SKUs)
- [ ] Order quantities rounded to MOQ/case pack; excess-cover tradeoffs surfaced
- [ ] Last safe order date computed for every URGENT and Scheduled SKU
- [ ] Days of cover within healthy band post-reorder

## Output quality
- [ ] Executive summary ≤120 words with the single biggest risk named
- [ ] Tables sorted URGENT first, then days-of-cover ascending
- [ ] Cash outlay timeline shown, not just units
- [ ] Overstock SKUs get an action (markdown/bundle/pause), not just a flag
- [ ] All assumptions and data gaps numbered in their own section
- [ ] Review cadence and re-run triggers stated

## Sanity checks
- [ ] Total forecast reconciles with trailing revenue within ±20% (or explained)
- [ ] No forecast >3x best month without an explicit driver
- [ ] No SKU simultaneously URGENT and overstocked (data error check)
- [ ] Units, currency, and dates use the user's formats and SKU names
