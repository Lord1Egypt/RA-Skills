# Reorder Recommendation Quality Checklist

Before delivering a reorder recommendation, verify each item:

---

## Demand estimation
- [ ] Demand average based on actual sales data (not guess)?
- [ ] Measurement window appropriate for velocity (30/60/90 days)?
- [ ] Demand variability (σ or CV) calculated or estimated?
- [ ] Stockout periods excluded or adjusted in historical data?
- [ ] Trend accounted for (growing/declining products)?
- [ ] Seasonality considered if relevant?
- [ ] Promotional spikes separated from organic demand?

## Lead time modeling
- [ ] Lead time sourced from historical POs (not just supplier quote)?
- [ ] Lead-time variability accounted for (σLT or range)?
- [ ] Buffer added if using supplier quote only (+20–30%)?
- [ ] Upcoming disruptions flagged (holidays, port congestion, etc.)?

## Safety stock
- [ ] Safety stock method stated (service-level vs days-of-cover)?
- [ ] Service level appropriate for product importance?
- [ ] Formula shown with intermediate steps?
- [ ] Both demand AND lead-time variability included?
- [ ] Result sanity-checked (not obviously too high or low)?
- [ ] Plain-English interpretation provided?

## Reorder point
- [ ] ROP = lead time demand + safety stock (formula shown)?
- [ ] In-transit inventory accounted for in position calculation?
- [ ] Current inventory position compared to ROP?
- [ ] Clear status: above ROP / below ROP / critical?
- [ ] Days to stockout estimated if below ROP?

## Reorder quantity
- [ ] Coverage period stated and justified?
- [ ] MOQ constraint respected?
- [ ] Carton / packaging multiples applied?
- [ ] Cash impact calculated (units × unit cost)?
- [ ] Storage capacity checked?
- [ ] EOQ considered if ordering/holding costs available?

## Risk and tradeoffs
- [ ] Conservative / recommended / aggressive scenarios shown?
- [ ] Stockout risk quantified or described for each?
- [ ] Cash tied up shown for each scenario?
- [ ] Stockout cost vs carrying cost framed?
- [ ] No false precision (ranges shown where appropriate)?

## Assumptions and transparency
- [ ] Every input value has a stated source?
- [ ] Confidence level flagged (high / medium / low)?
- [ ] Fragile assumptions called out explicitly?
- [ ] "If X changes, recalculate" triggers listed?

## Actionability
- [ ] Clear next step (order now / wait until DATE / review in X days)?
- [ ] Recommendation can be executed without further analysis?
- [ ] Operator can explain the logic to a buyer or founder?
- [ ] Review cadence recommended?

## Common error check
- [ ] Not using weekly σ in a daily formula (units match)?
- [ ] Not confusing on-hand with inventory position?
- [ ] Not recommending below MOQ?
- [ ] Not ignoring in-transit stock?
- [ ] Not extrapolating growth beyond 2–3 months?
- [ ] Numbers pass a gut check (not absurdly high or low)?
