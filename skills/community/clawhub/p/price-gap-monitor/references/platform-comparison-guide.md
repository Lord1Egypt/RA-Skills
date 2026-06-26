# Platform Comparison Reference

Platform-specific pricing nuances for major ecommerce marketplaces. Use this reference when interpreting price gaps across platforms in the Price Gap Monitor skill.

---

## Amazon (US, UK, DE, JP)

### Pricing structure
- **Buy Box price**: The price shown on the main product page. May be from the brand owner, an authorized reseller, or a third-party seller.
- **Other Sellers**: Below the Buy Box, Amazon shows alternative offers. These are important for competitive context but often ignored.
- **Subscribe & Save**: Recurring delivery discount, typically 5-15% off. Note separately from one-time price.
- **Coupons**: Visible green badge on search results. Clip-to-apply. Reduces effective price.
- **Lightning Deals**: Time-limited (usually 6-12 hours). Show countdown timer and claimed percentage.
- **Prime exclusive price**: Some items show a lower price for Prime members only.

### Key normalization notes
- Always check whether Prime shipping is included (it usually is for Prime-eligible items).
- "List Price" with strikethrough is often inflated. Compare actual selling prices, not claimed discounts.
- Amazon's "Climate Pledge Friendly" or "Amazon's Choice" badges don't affect price but affect visibility.

### Data collection tips
- Search results show up to 48 items per page (desktop) or 16 (mobile).
- Sponsored listings appear at positions 1-3 and throughout. Always flag these.
- Category pages (Browse nodes) show different rankings than keyword search.

---

## Walmart (US)

### Pricing structure
- **Everyday Low Price**: Standard pricing philosophy. Less frequent promotions than Amazon.
- **Rollback**: Temporary price reduction, similar to a sale. Usually lasts 2-4 weeks.
- **Walmart+**: Free shipping for members on orders $35+. Similar to Prime for shipping.
- **Marketplace sellers**: Third-party sellers on Walmart.com may price differently from Walmart-direct items.

### Key normalization notes
- Walmart has a **Price Parity policy**: Marketplace sellers cannot price significantly higher on Walmart than on their own website or other marketplaces. This creates a pricing floor effect.
- Free 2-day shipping is common for Walmart-fulfilled items. Factor this into landed cost.
- Walmart's "Compare at" price is their version of a reference price — treat with same skepticism as Amazon's "List Price."

### Data collection tips
- Search results typically show 40 items per page.
- Walmart groups "Best Seller" and "Popular Pick" badges visibly.
- In-store vs online prices may differ. This skill only covers online prices.

---

## Temu

### Pricing structure
- **Flash sale pricing**: Temu frequently runs time-limited deals with significant discounts.
- **New user pricing**: First-time buyers see different (lower) prices. Always note if browsing as a new user.
- **Bundle deals**: "Buy 2, get X% off" is common. Normalize to single-unit price.
- **Free shipping**: Most items ship free with no minimum. This is a significant competitive advantage at low price points.

### Key normalization notes
- Temu prices are often 40-70% lower than Amazon/Walmart for comparable (not identical) products.
- Quality and brand positioning differ significantly. A $5 Temu item is not a direct competitor to a $25 branded Amazon item, even if the product category matches.
- Delivery times (7-15 days) vs Prime (1-2 days) represent different value propositions. Note this context.

### Data collection tips
- Temu's search results are heavily personalized. Results may vary between sessions.
- Product images and descriptions may be less standardized. Verify product match carefully.
- Rating systems differ — Temu uses a 5-star system but review volume is often lower.

---

## TikTok Shop

### Pricing structure
- **In-video pricing**: Products linked in TikTok videos may have creator-specific discount codes.
- **Shop tab pricing**: Standard marketplace pricing, comparable to Amazon.
- **Flash deals**: Time-limited promotions tied to live shopping events.
- **Creator commissions**: Built into the price. A $20 TikTok Shop item may include 10-20% creator commission.

### Key normalization notes
- TikTok Shop is newer than other platforms. Review counts and sales history are typically much lower.
- Pricing may be more volatile due to smaller seller base and frequent promotional events.
- Shipping is typically free for most items, fulfilled by the seller or TikTok's logistics.

### Data collection tips
- Product search on TikTok Shop is less mature than Amazon/Walmart. Results may be less relevant.
- Live shopping events can create temporary price spikes or drops.
- Verify that the product is actually available (not just shown in a video).

---

## eBay

### Pricing structure
- **Buy It Now**: Fixed price. Most comparable to other platform listings.
- **Auction**: Variable price. Not useful for competitive pricing analysis unless monitoring final sale prices.
- **Best Offer**: Listed price with negotiation option. Actual transaction prices may be 10-20% lower.
- **Promoted Listings**: Seller pays a commission for better visibility. Doesn't directly affect price but affects ranking.

### Key normalization notes
- eBay mixes new, refurbished, used, and parts listings. Always filter for "New" condition when comparing.
- Shipping costs vary widely. Some sellers use free shipping, others charge separately. Always calculate landed cost.
- eBay's "Sold" data (visible on completed listings) provides actual transaction prices — but accessing this requires specific searches.

### Data collection tips
- Use "Buy It Now" filter to exclude auctions.
- Sort by "Best Match" for organic ranking, "Price + Shipping: lowest first" for price analysis.
- eBay shows "X sold" counts on some listings — useful for volume context.

---

## Cross-Platform Comparison Checklist

When comparing prices across platforms, verify:

- [ ] Same product (not just same category)
- [ ] Same condition (new vs refurbished vs used)
- [ ] Same quantity (single vs multi-pack)
- [ ] Shipping costs included in comparison
- [ ] Temporary promos flagged and noted separately
- [ ] Currency converted if comparing across markets
- [ ] Platform-specific pricing policies noted (e.g., Walmart price parity)
- [ ] Review count and seller maturity included as context
- [ ] Delivery time differences noted (Prime 1-day vs Temu 10-day)
- [ ] Sponsored vs organic placement distinguished
