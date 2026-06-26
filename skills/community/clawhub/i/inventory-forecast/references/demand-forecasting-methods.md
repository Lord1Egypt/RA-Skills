# Demand Forecasting Methods

How to turn raw sales history into a usable forward demand number. Use the simplest method the data supports — more sophistication than the data quality warrants is false precision.

## 1. Velocity baselines

**Weighted trailing average (default).** Daily velocity = 0.5 × (last 30 days avg) + 0.3 × (days 31-60 avg) + 0.2 × (days 61-90 avg). Responds to growth/decline without overreacting to a single good week.

**Simple trailing 30-day.** Acceptable when the SKU is stable and mature. Dangerous for anything growing, declining, or seasonal.

**When history is short (<90 days):** use what exists, widen safety stock (z = 2.0+), and label the forecast low-confidence. For brand-new SKUs, anchor to the closest analog SKU's launch curve and say so.

## 2. Data cleaning before averaging

- **Stockout correction:** a day at zero inventory is missing data, not zero demand. Replace stockout-day demand with the average of the 14 days before the stockout. If a stockout lasted >25% of your lookback window, shorten the window to clean days only.
- **Promo-spike exclusion:** exclude promo days (and 2 halo days each side) from the baseline; model promos separately (section 4). Otherwise a single flash sale inflates the baseline for 90 days.
- **Outlier days:** a single day >4x median daily sales with no known cause — verify (viral video? bulk B2B order?) before including. One-off bulk orders should be excluded from velocity.
- **Channel mixing:** if the user sells on multiple platforms, forecast per channel when lead-time-critical, because platform algorithms make demand non-transferable.

## 3. Seasonality

**Own-data index (12+ months of history):** index_month = (that month's sales) ÷ (average monthly sales). Apply the index of the months the forecast window covers. Smooth with adjacent months if any single month was distorted by a stockout or promo.

**Category curves (fallback):** typical patterns when own data is insufficient — state clearly the curve is a benchmark:
- Q4 gifting categories (toys, beauty sets, electronics accessories): Oct 1.1x, Nov 1.6x, Dec 1.8x, Jan 0.6x
- SEA marketplace double-days (9.9, 10.10, 11.11, 12.12): each event month +20-40% on top of baseline month
- Summer seasonal (fans, coolers, outdoor): ramp from 1.2x to 1.8x across the 3 peak months, 0.4-0.6x off-season
- Back-to-school (stationery, bags, dorm goods): 1.5-2x in the 6 weeks before term start

**Trend adjustment:** trend factor = (trailing 30-day velocity) ÷ (trailing 90-day velocity). Cap applied trend at ±30% per forecast cycle unless there is a structural reason (new ad campaign, listing rank jump) — extrapolating a hot streak is how overstock happens.

## 4. Promotional lift modeling

**Own-history multiplier (preferred).** lift = (units sold during past promo) ÷ (baseline daily velocity at that time × promo days). Use the same SKU; same-category promo is second best. Adjust for discount depth: lift scales roughly linearly with discount between 10-40% off for most categories.

**Benchmark multipliers (fallback, flag as estimates):**

| Event type | Typical lift | Range |
|---|---|---|
| Platform flash sale (24h, featured slot) | 3x | 2-13x — own data essential, variance is huge |
| Sitewide discount 20-30% | 2x | 1.5-2.5x |
| Livestream feature (mid-tier host) | 4x | 3-8x for event duration |
| Double-day campaign (11.11 etc.) | 3x | 2-5x on event day, +30% event week |
| Email/SMS promo to own list | 1.5x | 1.2-2x for 48h |

**Halo and dip:** add 10-20% extra demand in the 1-2 days around the event (traffic spillover); subtract 10-20% from baseline for 7-14 days after (pull-forward). Net event demand = event units + halo − dip recovery.

## 5. Forecast horizon and granularity

- Forecast horizon must cover at least: full lead time + review period + one promo cycle. With 60-day lead times, a 30-day forecast is useless.
- Weekly granularity for the reorder calendar; daily only matters inside promo weeks.
- Confidence degrades fast: beyond 90 days, present ranges (±25%) rather than point estimates.

## 6. Reconciliation sanity checks

Before delivering, verify:
1. Sum of (forecast daily demand × 30) across SKUs ≈ trailing 30-day total units within ±20%, unless promos/seasonality explain the gap.
2. No SKU forecast exceeds its category's plausible ceiling (e.g., forecast > 3x best month ever needs an explicit driver).
3. Seasonal indexes average to ~1.0 across 12 months.
4. Promo forecasts cross-checked against available stock — a forecast you cannot stock is a planning problem to surface, not a number to print.
