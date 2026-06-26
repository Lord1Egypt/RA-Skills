# Inventory Forecast — Output Template

Use this structure for every forecast deliverable. Omit sections that do not apply, but never omit Assumptions or Urgent Actions.

---

## 1. Executive Summary

- **Forecast window:** [start date] → [end date]
- **SKUs analyzed:** [n]
- **Urgent reorders (order this week):** [n SKUs, total estimated PO cost]
- **Scheduled reorders (next 90 days):** [n SKUs, total estimated PO cost]
- **Overstock flags:** [n SKUs, estimated cash tied up]
- **Biggest risk:** [one sentence — e.g., "SKU-A stocks out July 2, 13 days before the flash sale, unless PO is placed by June 9."]

## 2. Velocity & Demand Table

| SKU | Daily velocity (weighted) | Trend | Seasonal index (window) | Promo lift applied | Forecast daily demand |
|---|---|---|---|---|---|
| | | ↑/→/↓ | | | |

Notes: state the weighting scheme used, any stockout corrections (SKU, dates, corrected velocity), and any promo-spike exclusions.

## 3. Reorder Table

| SKU | On hand | Inbound | Days of cover | Reorder point | Status | Order qty (after MOQ/case rounding) | Last safe order date | Est. PO cost |
|---|---|---|---|---|---|---|---|---|
| | | | | | URGENT / Scheduled / Skip | | | |

Status rules: URGENT = already at/past reorder point. Scheduled = will cross reorder point within the forecast window. Skip = adequate cover or overstocked.

## 4. Reorder Calendar (rolling 90 days)

| Week of | POs to place | Units | Est. cash outlay | Notes |
|---|---|---|---|---|
| | | | | |

Include promo dates and inbound arrival dates as calendar rows so collisions are visible.

## 5. Promotion Stock Plan (if promotions planned)

For each event: event name/date, forecast event units (with multiplier source — own history vs. benchmark), stock position going in, shortfall/surplus, and the contingency option (air freight bridge, unit cap, split shipment) with cost.

## 6. Overstock & Slow-Mover Actions

| SKU | Days of cover | Cash tied up | Recommended action | Expected cash freed |
|---|---|---|---|---|
| | | | markdown / bundle / pause reorder / liquidate | |

## 7. Assumptions & Data Gaps

Numbered list. Every substituted benchmark, every estimate, every missing input. Example: "3. No promo history for SKU-C; applied 2.5x category flash-sale benchmark instead of own-data lift."

## 8. Review Cadence & Triggers

- Re-run forecast: [weekly / biweekly]
- Immediate re-run triggers: velocity shift >25% week-over-week, supplier lead time change, new promo confirmed, stockout event, large inbound delay.

---

### Formatting rules

- Round units to whole numbers; round currency to the user's currency, no decimals above 100.
- Sort all tables with URGENT items first, then by days of cover ascending.
- Use the user's SKU names/codes exactly as given.
- Keep the executive summary under 120 words; put detail in the tables.
- If delivering as a spreadsheet, one tab per section 2-6, summary as the first tab.
