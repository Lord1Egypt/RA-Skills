# Lead Time & Safety Stock Reference

The reorder decision lives or dies on two numbers: how long replenishment really takes, and how much buffer absorbs the variance. Both are routinely underestimated.

## 1. Lead time decomposition

Always build door-to-door lead time from components. Ask the user for each; fill gaps with these defaults and flag them:

| Component | Typical range | Notes |
|---|---|---|
| Production / manufacturing | 15-45 days | Supplier quote; add 20% if the supplier has missed dates before |
| Pre-shipment QC / inspection | 2-5 days | Often forgotten; longer if third-party inspection is booked |
| Export handling + origin port | 2-4 days | Consolidation adds time for LCL shipments |
| Ocean freight (Asia → US West) | 14-20 days | East coast +10-14 days; port congestion can double this |
| Ocean freight (intra-SEA) | 3-8 days | |
| Air freight (door-to-door) | 5-12 days | Includes customs; 3-5x ocean cost |
| Customs clearance | 1-5 days | Holds/exams can add 1-3 weeks — this is the variance driver |
| Inbound receiving (3PL/FBA) | 2-14 days | FBA check-in during Q4 can hit 3+ weeks |

**Rule:** lead time for the reorder formula = sum of components at their *expected* values; lead time *variance* feeds safety stock. Track quoted vs. actual on every PO and recalibrate.

**Seasonal inflation:** add 15-30% to freight and receiving components for September-December POs (peak season congestion) and around Chinese New Year (factories close 2-4 weeks; queue effects last 6+ weeks).

## 2. Safety stock formulas

**Statistical (use for A-SKUs):**

Safety stock = z × σ_d × √L

- z = service-level factor: 1.28 (90%), 1.65 (95%), 2.05 (98%), 2.33 (99%)
- σ_d = standard deviation of daily demand (compute from the same cleaned data as velocity)
- L = lead time in days

**With lead-time variance (when supplier reliability is poor):**

Safety stock = z × √(L × σ_d² + d̄² × σ_L²)

where d̄ = mean daily demand and σ_L = std dev of lead time in days. Use this form whenever actual lead times have varied by more than ±1 week.

**Heuristic (acceptable for B/C-SKUs):** safety stock = 20-30% × (daily velocity × lead time). Simple, slightly generous at short lead times, slightly thin at long ones.

**Service level assignment:** A-SKUs (top 80% of revenue) → 95-98%. B-SKUs → 90-95%. C-SKUs → 85-90% or made-to-order. Pushing everything to 99% roughly doubles inventory cost versus 95% for a 4-point availability gain.

## 3. Reorder point and order quantity

**Reorder point (ROP):** ROP = (forecast daily demand × L) + safety stock. When on-hand + inbound ≤ ROP, order now.

**Order quantity (order-up-to method, default):**
Q = forecast demand over (L + R) − on-hand − inbound + safety stock
where R = review period (how often the user checks/places orders). Round up to MOQ and case pack; if rounding adds >30 days of extra cover, surface the carrying-cost tradeoff instead of silently ordering.

**Last safe order date:** projected stockout date − L. This single date per SKU is the most actionable output of the whole forecast. For promos: promo start date − L − buffer of 5-7 days.

**Days of cover:** (on-hand + inbound) ÷ forecast daily demand. Healthy bands: A-SKUs 30-75 days post-reorder for ≤30-day lead times; 60-120 days for 60-90-day lead times. >180 days = overstock flag (seasonal pre-builds excepted).

## 4. Cash and carrying-cost guardrails

- Carrying cost ≈ 20-30% of inventory value annually (capital, storage, insurance, shrinkage, obsolescence). Use 25% if unknown.
- Marketplace storage fees punish overstock directly (e.g., FBA long-term storage fees at 271+ days, monthly fees that triple in Q4). When the platform is known, factor its fee schedule into overstock recommendations.
- When the reorder plan's cash outlay exceeds what the user can fund, prioritize by contribution margin × velocity, not by stockout date alone — protect the SKUs that pay the bills.

## 5. Stockout cost framing

When a user hesitates on a reorder, quantify the downside: lost units = daily velocity × stockout days; lost revenue = lost units × price; plus rank decay — listings typically need 2-4 weeks of restored sales to recover search position after a multi-day stockout, so the true cost is commonly 2-3x the direct lost sales. Present both numbers.
