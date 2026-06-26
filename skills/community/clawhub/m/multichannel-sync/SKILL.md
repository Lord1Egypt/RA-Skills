---
name: Multichannel Sync
description: Plan inventory, pricing, and listing synchronization across multiple sales channels to prevent overselling, maintain consistent branding, and optimize channel-specific pricing — whether selling on two platforms or ten.
---

# Multichannel Sync

Selling on Shopify plus Amazon plus TikTok Shop plus one or two regional marketplaces sounds great until two customers buy the last unit at the same time, or Amazon suppresses your Buy Box because a 10% TikTok flash sale violated their fair pricing policy. This skill produces a concrete multichannel synchronization plan covering inventory buffers, pricing rules, listing content alignment, and exception handling — so every channel stays in stock, in policy, and on brand without manual firefighting.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Inventory model | Shared pool with channel-specific buffers, safety stock rules, and low-stock throttling per channel | Single shared pool with basic buffer | Separate inventory per channel with no sync |
| Pricing architecture | Anchor price with documented per-channel differentials, MAP/parity compliance matrix | Uniform pricing across channels | Ad-hoc pricing with no cross-channel awareness |
| Listing sync | Field-level mapping per channel showing identical vs. adapted vs. unique fields | General content duplication guidance | Copy-paste listings with no channel adaptation |
| Promotion cascade | Pre-launch checklist covering inventory reserves, pricing parity review, and channel notification sequence | Informal heads-up before promotions | Promotions launched without cross-channel impact review |
| Buffer calculation | SKU-level buffers based on velocity, lead time, and channel penalty severity | Category-level flat buffers | No buffers or arbitrary round numbers |
| Reconciliation cadence | Scheduled sync intervals with drift detection and automated alerts | Daily manual checks | Reconciliation only when problems surface |
| Exception handling | Documented playbooks for oversells, price violations, and listing suspensions with escalation paths | General troubleshooting notes | No exception procedures |
| Tool evaluation | Scored requirements matrix comparing sync tools against actual channel mix and volume | Feature comparison table | Tool chosen on recommendation alone |

## Solves

1. **Overselling during promotions** — running a flash sale on TikTok Shop while Amazon inventory doesn't update fast enough, resulting in orders you can't fulfill, negative seller metrics, and potential account suspension.
2. **Pricing parity violations** — Amazon suppressing your Buy Box or Walmart flagging your listing because a channel-specific discount on your DTC site triggered their price-matching algorithms.
3. **Listing inconsistency across channels** — product titles optimized for Amazon SEO that sound robotic on Shopify, or missing bullet points on Walmart because the listing was copy-pasted from another platform without adaptation.
4. **Inventory fragmentation** — reserving 50 units per channel "just in case" when you only have 200 total, leaving 100 units unsellable while some channels stock out and others sit idle.
5. **Manual sync bottlenecks** — one person manually updating inventory counts across five platforms every morning, creating a single point of failure and a 4-hour window where counts are stale.
6. **Promotion coordination chaos** — launching a BOGO on your DTC site without adjusting Amazon pricing or Walmart inventory buffers, triggering parity warnings and oversells simultaneously.
7. **New channel onboarding paralysis** — wanting to add TikTok Shop or a regional marketplace but unsure how to integrate it into existing inventory and pricing architecture without breaking what works.

## Workflow

### Step 1 — Audit Current Channel Architecture

Map every sales channel and its current integration status:

- List all active channels: DTC storefront (Shopify, WooCommerce, BigCommerce), marketplaces (Amazon, Walmart, eBay, Etsy, TikTok Shop), B2B portals, wholesale, retail partners
- For each channel, document: monthly order volume, average order value, return rate, current inventory source, sync method (manual, API, middleware), sync frequency
- Identify the anchor channel — the one with highest volume, strictest policies, or most complex requirements (usually Amazon or your DTC site)
- Document current pain points: oversell frequency, pricing complaints, listing takedowns, manual time spent on sync
- Map the current tech stack: OMS, ERP, listing tools, inventory management software, any existing middleware (ChannelAdvisor, Sellbrite, Linnworks, Zentail, etc.)

Deliverable: Channel architecture map with volume data, integration status, and pain point inventory.

### Step 2 — Design Inventory Synchronization Model

Build the inventory sharing and buffer system:

**Inventory pool strategy:**
- Single pool (recommended for most sellers): all channels draw from one inventory count, adjusted by channel-specific buffers
- Split pool: dedicated inventory per channel, used when fulfillment paths are physically separate (e.g., FBA vs. self-fulfilled)
- Hybrid: single pool for self-fulfilled channels plus separate FBA allocation

**Buffer calculation framework:**
- Base buffer = (daily velocity × lead time in days) + safety stock
- Channel risk multiplier: Amazon (1.5x — highest penalty for oversells), DTC (1.0x — you control the experience), TikTok Shop (1.3x — volatile demand spikes)
- Promotion buffer: reserve additional units before any channel-specific promotion launches
- Low-stock throttling: define thresholds where secondary channels are paused before primary channels (e.g., when total stock < 20 units, suppress TikTok Shop listing first)

**Sync frequency tiers:**
- Real-time (< 5 min): critical for high-velocity SKUs and during promotions
- Near-time (15-30 min): standard for most SKUs
- Batch (hourly+): acceptable for slow-moving or made-to-order items

Deliverable: Inventory model document with pool structure, per-SKU buffer calculations, and sync frequency assignments.

### Step 3 — Build Pricing Architecture

Define cross-channel pricing rules that prevent parity violations:

**Anchor pricing model:**
- Designate one price as the anchor (usually DTC or MAP price)
- Define allowed differentials per channel: Amazon (anchor ± 0%), Walmart (anchor ± 0%), TikTok Shop (anchor - 5% max), DTC (anchor + 0-10% with free shipping offset)
- Document MAP/MSRP constraints by brand or category
- Create a pricing parity compliance matrix showing which channels monitor each other

**Promotion pricing rules:**
- Coupon vs. list price reduction: which channels allow each, and how they affect parity
- Flash sale protocol: which channels need advance notification, which need temporary price matching
- Bundle and kit pricing: how to price channel-exclusive bundles without triggering parity alerts
- Clearance sequencing: which channel gets markdowns first, how quickly others must follow

**Fee-inclusive pricing:**
- Calculate true margin per channel after fees, shipping, and returns
- Build a per-channel P&L template at the SKU level
- Identify SKUs that are unprofitable on specific channels

Deliverable: Pricing rule document with anchor prices, channel differentials, promotion protocols, and per-channel margin analysis.

### Step 4 — Map Listing Content Strategy

Define which content fields are identical, adapted, or unique per channel:

**Field-level content mapping:**

| Field | Amazon | Shopify DTC | Walmart | TikTok Shop | eBay |
|---|---|---|---|---|---|
| Product title | SEO-optimized, 200 char max | Brand-forward, shorter | Walmart SEO rules | Short, engaging | eBay best practices |
| Bullet points | 5 keyword-rich bullets | Benefit-focused prose | Walmart key features | Not applicable | Item specifics |
| Description | A+ Content / EBC | Brand storytelling | Rich media shelf | Short video-friendly | HTML listing |
| Images | White background main, 7+ images | Lifestyle-forward | White background required | Vertical video + images | Gallery format |
| Price display | List price, deal price | Compare-at pricing | Everyday low price | Promotional pricing | Auction or fixed |
| Shipping info | FBA or seller-fulfilled | Custom shipping rules | WFS or seller | Platform shipping | eBay shipping options |

**Content sync rules:**
- Identical everywhere: UPC/EAN, weight, dimensions, safety warnings, compliance data
- Adapted per channel: titles (SEO vs. brand), descriptions (length and format), images (aspect ratio and background)
- Unique per channel: platform-specific enhanced content (A+ Content, Walmart Rich Media, TikTok product videos)

**Content update propagation:**
- Define the source of truth for each field type
- Map the propagation path: which fields update automatically via sync tools, which require manual channel-specific editing
- Create a content change checklist: when you update a product, which channels need manual review

Deliverable: Content mapping matrix with field-level sync rules and update propagation workflow.

### Step 5 — Create Promotion Coordination Protocol

Build the pre-launch and post-launch checklist for cross-channel promotions:

**Pre-launch checklist (48-72 hours before):**
- Verify inventory covers projected promotion demand + buffer across all channels
- Check pricing parity implications: will the promotion on one channel trigger violations on others?
- Reserve promotion inventory to prevent other channels from selling it first
- Prepare channel notifications: some marketplaces require advance notice for significant price changes
- Stage listing updates: promotional imagery, badges, and copy changes ready per channel
- Configure low-stock auto-pause rules for non-promotion channels during the event

**During promotion:**
- Monitor real-time inventory across all channels (set alert thresholds at 25%, 10%, and 5% remaining)
- Watch for parity alerts from Amazon, Walmart, or other marketplace dashboards
- Track channel-specific conversion rates and velocity to adjust buffer allocation

**Post-promotion:**
- Reconcile actual vs. projected demand per channel
- Restore standard pricing within documented timeline
- Remove promotional content and badges from all channels
- Review any oversells, parity violations, or listing issues
- Update buffer calculations based on actual promotion performance data

Deliverable: Promotion coordination playbook with pre-launch, live, and post-promotion checklists.

### Step 6 — Define Exception Handling Procedures

Document response playbooks for the three most common sync failures:

**Oversell response (< 1 hour SLA):**
1. Identify which channel(s) took the oversold order(s)
2. Check if any fulfillable inventory exists (other warehouse, in-transit, FBA)
3. If fulfillable: expedite shipment, document extra cost
4. If not fulfillable: cancel with personalized apology + compensation offer (discount code, priority on restock)
5. Root cause analysis: was it a sync delay, buffer miscalculation, or manual error?
6. Adjust buffers and sync frequency to prevent recurrence

**Price parity violation response (< 4 hours):**
1. Identify which channel triggered the violation and why
2. Immediately correct the offending price
3. If Buy Box suppressed: submit a price match or contact Seller Support with correction evidence
4. Document which parity monitoring detected it and update the compliance matrix
5. Review promotion cascade rules to prevent recurrence

**Listing suspension response (< 24 hours):**
1. Identify the suspension reason (IP claim, policy violation, quality issue)
2. Assess cross-channel impact: is the same issue present on other channels?
3. Prepare appeal or correction per platform-specific process
4. Monitor sales impact on other channels from the suspended listing
5. Update compliance checklist to catch similar issues pre-listing

Deliverable: Exception handling playbook with response timelines, escalation paths, and root cause analysis templates.

### Step 7 — Build Reconciliation and Monitoring Dashboard

Design the ongoing monitoring and reconciliation system:

- Define reconciliation frequency: real-time dashboard + daily detailed reconciliation + weekly deep audit
- Key metrics to track: inventory drift (difference between expected and actual counts per channel), sync latency (time between source update and channel reflection), oversell rate, parity violation frequency, listing accuracy score
- Alert thresholds: inventory drift > 5 units, sync latency > 30 minutes, any parity violation, any oversell
- Weekly reconciliation review: compare projected vs. actual sales by channel, review buffer adequacy, identify sync failures
- Monthly sync health report: total oversells, parity violations, listing issues, manual intervention count, sync uptime percentage

Deliverable: Monitoring dashboard specification with metrics, alert thresholds, and reconciliation cadence.

## Examples

### Example 1 — DTC + Amazon + TikTok Shop Seller (Beauty Category)

**Input:** "We sell skincare on Shopify (60% of revenue), Amazon FBA (30%), and just launched TikTok Shop (10%). We oversold 3 times last month during a TikTok flash sale. Our inventory is in one warehouse plus FBA. We have 150 SKUs."

**Inventory model designed:**
- Hybrid pool: self-fulfilled pool (Shopify + TikTok Shop) + separate FBA allocation
- FBA replenishment triggers at 14-day cover based on Amazon velocity
- TikTok Shop buffer: 15% of available self-fulfilled stock reserved (volatile demand)
- Shopify buffer: 5% (controlled experience, can oversell-manage with backorder page)
- Low-stock rule: when self-fulfilled pool < 20 units, auto-pause TikTok Shop listing
- Sync frequency: real-time for self-fulfilled channels, 2x daily FBA reconciliation

**Pricing architecture applied:**
- Anchor price = Shopify DTC price
- Amazon: match DTC price (free shipping via FBA offsets DTC free shipping threshold)
- TikTok Shop: up to 10% below DTC via platform coupons only (not list price reduction) to avoid Amazon parity detection
- Flash sale protocol: 48-hour advance inventory reserve, real-time monitoring, auto-pause TikTok listing if stock < 30 units

### Example 2 — Wholesale Brand Expanding to DTC + Marketplaces (Home Goods)

**Input:** "We're a wholesale brand (80% revenue) adding Shopify DTC and Amazon. We have MAP pricing on all products. Our wholesale partners are nervous about us competing with them online. We have 400 SKUs and use NetSuite as our ERP."

**Inventory model designed:**
- Single pool in NetSuite as source of truth
- Channel allocation priority: wholesale commitments first, then DTC, then Amazon
- Amazon: FBA with dedicated allocation (30-day cover), not drawing from general pool
- DTC: real-time sync from NetSuite available-to-promise (ATP) quantity
- Buffer strategy: wholesale safety stock (negotiated minimums) protected from DTC/Amazon availability
- Sync: NetSuite → Shopify real-time via API, NetSuite → Amazon via daily FBA shipment planning

**Pricing architecture applied:**
- Anchor price = MAP (non-negotiable across all channels)
- DTC: MAP price + free shipping over $75 (effective 5-8% premium feel via shipping threshold)
- Amazon: MAP price with FBA Prime shipping as differentiator
- Wholesale: standard wholesale pricing (50% of MAP)
- No channel-exclusive discounts without MAP holder approval
- Bundle strategy: create DTC-exclusive bundles at slight savings vs. buying individually at MAP, since bundles aren't MAP-covered

## Common Mistakes

1. **Setting flat buffers across all channels** — giving every channel a 10% buffer regardless of penalty severity. Amazon can suspend your account for repeated oversells; your DTC site just shows "back in stock soon." Weight buffers by consequence.

2. **Ignoring pricing parity monitoring** — assuming marketplaces won't notice a 15% discount on your DTC site. Amazon and Walmart actively crawl competitor prices including your own website. Even coupon-based discounts can trigger alerts if the final checkout price is visible.

3. **Copy-pasting listings across channels** — taking your Amazon listing and putting it on Shopify or vice versa. Amazon titles are keyword-stuffed for A9; Shopify titles should be brand-forward for humans. Each channel has different content rules, character limits, and SEO requirements.

4. **Syncing too infrequently during promotions** — running hourly sync during a flash sale that sells 50 units per hour. During promotions, sync frequency should increase to real-time or near-real-time on all participating channels.

5. **No promotion coordination protocol** — launching a sale on one channel without checking inventory availability across all channels or reviewing pricing parity implications. Every promotion needs a pre-launch checklist covering inventory, pricing, and content across all channels.

6. **Choosing sync tools before defining requirements** — signing up for ChannelAdvisor or Sellbrite because a competitor uses it, without mapping your specific channel mix, SKU count, sync frequency needs, and integration requirements. Evaluate tools against your documented requirements matrix.

7. **Manual reconciliation only** — relying on a person to check inventory counts across channels every morning. By the time they find a discrepancy at 9 AM, overnight orders may have already caused oversells. Automated drift detection with alerts is essential.

8. **No exception handling playbooks** — knowing what to do when everything works but having no documented procedure for oversells, parity violations, or listing suspensions. These happen regularly in multichannel selling; the response speed determines the business impact.

9. **Treating all SKUs the same** — applying the same sync frequency, buffer size, and monitoring intensity to a $5 accessory and a $500 hero product. Segment SKUs by velocity, margin, and strategic importance, then allocate sync resources accordingly.

10. **Forgetting channel-specific compliance rules** — each marketplace has unique rules about product data requirements, image specifications, pricing display, and seller performance metrics. A sync plan must include a compliance layer that validates content and pricing before pushing to each channel.

## Resources

- [Output Template](references/output-template.md) — Structured template for the complete multichannel sync plan deliverable
- [Inventory Buffer Calculator Guide](references/inventory-buffer-guide.md) — Framework for calculating SKU-level buffers by channel risk and velocity
- [Pricing Parity Compliance Guide](references/pricing-parity-guide.md) — Rules and workarounds for Amazon, Walmart, and marketplace pricing policies
- [Quality Checklist](assets/quality-checklist.md) — Pre-delivery checklist covering completeness, accuracy, and actionability
