# Inventory Buffer Calculator — Reference Guide

## Why Buffers Matter

Inventory buffers are the units you hold back from available-to-sell counts to prevent overselling during sync delays. Without buffers, a 15-minute sync gap during a high-velocity period means two channels can sell the same unit. With over-aggressive buffers, you artificially restrict availability and lose sales. The goal is right-sized buffers that match each channel's risk profile.

## Buffer Calculation Formula

**Buffer = (Daily Velocity × Lead Time Days × Channel Risk Multiplier) + Safety Stock**

### Daily Velocity
Calculate using the trailing 30-day average, weighted toward recent performance:
- Standard SKU: simple 30-day average
- Seasonal SKU: use same period last year × year-over-year growth rate
- New SKU: use comparable product velocity × 1.2 (uncertainty multiplier)
- Promotion period: use projected promotion velocity, not historical average

### Lead Time
The time from "need more stock" to "stock available to sell":
- In-warehouse items: 0 days (already available)
- In-transit from supplier: actual transit time + receiving time
- Made-to-order: production time + transit + receiving
- FBA replenishment: shipping to Amazon + receiving time (typically 5-14 days)

### Channel Risk Multiplier
Weight buffers by the consequences of an oversell on each channel:

| Channel | Risk Multiplier | Rationale |
|---|---|---|
| Amazon (FBA) | 1.5x | Account health impact, potential suspension, difficult reinstatement |
| Amazon (FBM) | 1.4x | Same account health impact, plus you bear fulfillment failure |
| Walmart | 1.3x | Seller scorecard impact, listing suppression risk |
| eBay | 1.2x | Defect rate impact, below standard risk |
| TikTok Shop | 1.3x | Volatile demand spikes from viral content, platform still maturing |
| Shopify DTC | 1.0x | You control the experience, can offer backorders or waitlists |
| B2B / Wholesale | 0.8x | Typically pre-negotiated quantities, longer fulfillment windows |

### Safety Stock
Minimum units to hold regardless of velocity:
- Hero SKUs (top 20% by revenue): 10-20 units or 7 days of cover, whichever is higher
- Standard SKUs: 5-10 units or 5 days of cover
- Long-tail SKUs: 2-5 units or 3 days of cover
- Custom/made-to-order: 0 (buffer is built into lead time)

## Buffer Calculation Examples

### Example: High-Velocity Beauty SKU
- Daily velocity: 25 units/day
- Lead time: 3 days (in-warehouse, reorder from supplier takes 3 days)
- Amazon risk multiplier: 1.5x
- Safety stock: 15 units (hero SKU)

**Amazon buffer = (25 × 3 × 1.5) + 15 = 127.5 → 128 units**
**DTC buffer = (25 × 3 × 1.0) + 15 = 90 units**

### Example: Slow-Moving Home Goods SKU
- Daily velocity: 2 units/day
- Lead time: 7 days (supplier shipping)
- Amazon risk multiplier: 1.5x
- Safety stock: 5 units (standard SKU)

**Amazon buffer = (2 × 7 × 1.5) + 5 = 26 units**
**DTC buffer = (2 × 7 × 1.0) + 5 = 19 units**

## Low-Stock Throttling Rules

When total available inventory drops below certain thresholds, progressively restrict channels:

| Available Stock Level | Action |
|---|---|
| Below 50% of total buffer | Alert operations team, increase sync frequency to real-time on all channels |
| Below 30% of total buffer | Pause lowest-priority channel listings (typically newest or lowest-margin channel) |
| Below 15% of total buffer | Pause all channels except anchor channel |
| Below safety stock | Pause all channels, trigger emergency reorder |

### Channel Priority for Throttling
Rank channels by strategic importance to determine pause order:
1. Revenue contribution (higher = pause last)
2. Customer acquisition value (new customer channels may rank higher than revenue suggests)
3. Penalty severity (high-penalty channels should be paused early, not late)
4. Contractual obligations (wholesale commitments may override revenue ranking)

## Promotion Buffer Adjustments

Before any promotion, adjust buffers:

- **Estimate promotion demand:** historical promotion performance × expected traffic increase
- **Add promotion buffer:** projected promotion units × 1.3 (overperformance safety)
- **Reserve from non-promotion channels:** reduce available quantity on non-participating channels by the promotion reserve amount
- **Set auto-pause triggers:** if promotion channel inventory drops below 20% of reserve, pause non-participating channels entirely

## SKU Segmentation for Buffer Management

Not all SKUs deserve the same buffer attention:

| Segment | SKU Count (typical) | Buffer Strategy | Monitoring |
|---|---|---|---|
| Hero (top 20% revenue) | ~20% of catalog | SKU-level calculated buffers, real-time sync | Real-time alerts |
| Core (next 30%) | ~30% of catalog | Category-level buffers, near-time sync | Daily review |
| Long-tail (bottom 50%) | ~50% of catalog | Minimal buffers, batch sync | Weekly review |
| New launches (first 90 days) | Variable | 1.2x standard buffer (demand uncertainty), real-time sync | Daily review |

## Common Buffer Mistakes

1. **Flat percentage buffers:** Using 10% across all SKUs ignores velocity and risk differences. A 10% buffer on a 1,000-unit SKU is 100 units (probably too much); on a 5-unit SKU it's 0.5 units (not enough).

2. **Never updating buffers:** Velocity changes seasonally and with promotions. Recalculate buffers monthly at minimum, weekly for hero SKUs.

3. **Buffering against the wrong risk:** Holding large buffers on your DTC site (where you control the experience) while under-buffering Amazon (where oversells damage account health). Weight buffers by consequence.

4. **Ignoring sync frequency in buffer sizing:** If your sync runs every 15 minutes, you need enough buffer to cover the maximum number of units that could sell in 15 minutes across all channels. Faster sync = smaller required buffer.

5. **Not accounting for return-to-stock timing:** Returned units that aren't immediately available for sale create phantom inventory. Buffers should account for the inspection and restocking lag.
