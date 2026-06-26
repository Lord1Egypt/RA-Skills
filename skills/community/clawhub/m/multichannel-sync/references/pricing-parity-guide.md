# Pricing Parity Compliance — Reference Guide

## What Pricing Parity Means

Pricing parity is the expectation (or contractual requirement) that a product's price on one sales channel doesn't undercut its price on another. Major marketplaces actively monitor your pricing across the web, including your own DTC site, and will penalize listings that violate their pricing policies.

## Platform-Specific Parity Rules

### Amazon
**Policy:** Amazon's Fair Pricing Policy prohibits pricing that is "significantly higher than recent prices offered on or off Amazon." In practice, Amazon monitors your prices on your own website, Walmart, eBay, and Google Shopping.

**What triggers enforcement:**
- Your DTC site shows a lower price (including after coupon/discount codes if the discounted price is visible in structured data or Google Shopping feeds)
- Another marketplace has a lower list price
- Your price is significantly higher than other sellers of the same product

**Consequences:**
- Buy Box suppression (your listing shows "See All Buying Options" instead of "Add to Cart")
- Featured Offer removal
- In severe/repeated cases: listing suppression or account-level warnings

**Workarounds that comply with policy:**
- Use Amazon coupons (clip-to-save) rather than reducing list price — these don't affect the reference price for parity monitoring
- Use Subscribe & Save discounts (Amazon considers these a separate program)
- DTC promotions via one-time-use email codes that aren't visible to crawlers
- Loyalty program pricing that requires account login to view
- Bundle or kit products exclusive to your DTC site (bundles are considered different products)

### Walmart
**Policy:** Walmart's pricing algorithm actively price-matches against Amazon and other retailers. They may automatically reduce your item's price (if using Walmart Repricer) or suppress your listing if your price is too high relative to competitors.

**What triggers enforcement:**
- Price higher than Amazon for the same item
- Price higher than other Walmart sellers
- Price set below their profitability threshold after Walmart's fee structure

**Consequences:**
- Listing unpublished or suppressed
- Item flagged as "price issue" in Seller Center
- Reduced search visibility

**Workarounds that comply with policy:**
- Match Amazon's price as your baseline
- Use Walmart's Reduced Price badge for temporary promotions
- Offer free shipping or faster shipping as a value differentiator rather than price cuts
- Create Walmart-exclusive bundles at different price points

### TikTok Shop
**Policy:** TikTok Shop is less mature on parity enforcement but does have policies against misleading pricing and requires that sale prices represent genuine reductions.

**Key considerations:**
- Flash sale pricing can be aggressive without parity risk (TikTok is less monitored by Amazon/Walmart)
- However, if your TikTok Shop prices appear in Google Shopping feeds, Amazon may detect them
- Creator commission structures effectively lower your price — factor this into parity calculations
- TikTok Shop affiliate pricing (where creators take a commission) is generally not treated as a price reduction by other platforms

### eBay
**Policy:** eBay doesn't enforce pricing parity as aggressively, but their Best Match algorithm favors competitive pricing.

**Key considerations:**
- eBay promotions (Markdown Manager, Promoted Listings) are self-contained
- Auction-style listings are inherently variable and don't trigger parity concerns
- Fixed-price listings should stay within your parity framework

## Building a Parity Compliance Matrix

Create a matrix showing which channels monitor which, and what triggers action:

| Your Channel | Monitored By | Detection Method | Trigger | Response Time |
|---|---|---|---|---|
| DTC website | Amazon, Walmart | Web crawlers, Google Shopping feed | Lower visible price | 24-48 hours |
| Amazon | Walmart | Direct price comparison | Higher price than Amazon | Immediate (automated) |
| TikTok Shop | Amazon (indirect) | Google Shopping feed | Lower price visible | 24-72 hours |
| eBay | Amazon (limited) | Sporadic monitoring | Significantly lower price | Variable |

## Promotion Pricing Decision Tree

When planning a promotion on any channel, follow this decision tree:

1. **Will the discounted price be visible to web crawlers?**
   - Yes (list price reduction, visible coupon) → check parity matrix for monitoring channels
   - No (email-only code, login-required pricing) → lower parity risk, proceed with standard checks

2. **Which channels might detect this price?**
   - Amazon monitors: your DTC site, Walmart, Google Shopping
   - Walmart monitors: Amazon, your DTC site

3. **For each monitoring channel, what's the consequence?**
   - Buy Box loss: can you afford reduced sales on Amazon for the promotion duration?
   - Listing suppression: will the promotion revenue offset lost marketplace sales?

4. **Mitigation options:**
   - Match the promotional price on monitoring channels
   - Use non-visible discount methods (coupons, loyalty pricing)
   - Time promotions when marketplace sales are naturally lower
   - Run promotions as channel-exclusive bundles instead of single-product discounts

## Fee-Adjusted Pricing Framework

True parity should account for total customer cost, not just list price:

| Component | Amazon | DTC (Shopify) | Walmart | TikTok Shop |
|---|---|---|---|---|
| List price | $50.00 | $50.00 | $50.00 | $47.50 |
| Shipping | Free (Prime) | $5.95 (or free over $75) | Free (WFS) | Free |
| Platform fees | 15% ($7.50) | 2.9% + $0.30 ($1.75) | 12% ($6.00) | 5% ($2.38) |
| FBA/fulfillment | $5.50 | $4.00 (3PL) | $4.50 (WFS) | $4.00 (self) |
| Returns cost | ~$2.00 (avg) | ~$3.00 (avg) | ~$2.00 (avg) | ~$1.50 (avg) |
| **Net margin** | **$35.00** | **$35.30** | **$37.50** | **$39.62** |

Use this framework to ensure pricing parity doesn't mean margin parity — adjust prices so margins are sustainable on each channel while maintaining compliant list prices.

## Parity Monitoring Tools

- **Prisync / Competera:** automated competitive price monitoring across channels
- **Seller Snap / BQool:** Amazon-specific repricing tools with parity awareness
- **Manual monitoring:** weekly spot-checks of your own listings across all channels (search your UPC on Google Shopping)
- **Google Alerts:** set alerts for your product names + "price" to catch unexpected price appearances

## Common Parity Mistakes

1. **Assuming coupons are invisible:** many coupon codes, especially those shared on deal sites, become visible to crawlers within hours.

2. **Forgetting Google Shopping:** your DTC site's structured data feeds directly into Google Shopping, which Amazon's crawlers monitor. If your sale price shows in structured data, Amazon sees it.

3. **Ignoring shipping in parity calculations:** a $45 product with $5 shipping on your DTC site is effectively the same as $50 with free shipping on Amazon — but crawlers may flag the $45 list price.

4. **Running channel-exclusive promotions without parity review:** every promotion on any channel needs a 30-second parity check: "Will this price appear anywhere that my other channels monitor?"

5. **Not having a response plan:** when a parity violation triggers Buy Box suppression, response speed matters. Have a documented procedure to correct prices and submit appeals within hours, not days.
