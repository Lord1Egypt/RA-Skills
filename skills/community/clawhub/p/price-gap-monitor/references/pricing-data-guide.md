# Pricing Data Collection Guide

How to collect, normalize, and validate pricing data from ecommerce marketplaces for the Price Gap Monitor skill.

---

## Data Collection Principles

### What counts as "visible public data"

Visible public data is anything a regular shopper can see by visiting a marketplace without special tools, API access, or insider accounts:

- Listed prices on search results pages
- Product detail page prices
- Visible coupons, promo badges, Lightning Deal prices
- Shipping costs shown on the listing
- Seller names and rating counts
- Review counts and star ratings
- "Best Seller" or category rank badges (when displayed)
- Stock status messages ("Only 3 left", "In Stock")

### What is NOT visible public data

Do not claim access to or fabricate:

- Historical price charts (unless provided by a visible tool like CamelCamelCamel)
- Internal Best Seller Rank (BSR) numbers not shown on the page
- Actual unit sales volumes
- Advertising spend or ACoS of competitors
- Supplier costs or margin data of competitors
- Conversion rates of competitor listings
- Internal marketplace algorithm scores

---

## Collection Methods

### Method 1: Browser-based collection

When browser tools are available, follow this sequence:

1. **Search query setup**: Use the exact product name, model number, or category keyword the user provided. Do not modify the search terms unless the user agrees.

2. **Result page capture**: Record the first 10-20 organic results. Note:
   - Position in results (rank)
   - Whether the listing is "Sponsored" or organic
   - Title (first 80 characters)
   - Price as displayed
   - Any coupon or promo badge text
   - Seller name
   - Rating count (number of reviews)
   - Star rating
   - Prime/free shipping badge

3. **Product page deep-dive** (for Mode A): Navigate to 3-5 key competitor listings. Record:
   - Full price breakdown (base + shipping)
   - Available variants and their prices
   - Buy Box seller and "Other sellers" if visible
   - Any quantity discount tiers
   - Product dimensions/weight for shipping normalization

4. **Timestamp**: Record the UTC time of each page visit. Marketplace pages can change within hours due to dynamic pricing.

### Method 2: User-provided snapshot processing

When the user provides price data:

1. **Validate completeness**: Check that each competitor entry has: price, platform, date collected, and product identifier.
2. **Check freshness**: Flag any data older than 7 days as potentially stale.
3. **Verify consistency**: Look for obvious errors (e.g., prices that seem too low or too high for the category).
4. **Request missing fields**: If critical data is missing, ask the user to provide it before proceeding.

---

## Price Normalization

### Currency normalization

- Always convert to the user's operating currency.
- State the exchange rate used and the source (e.g., "USD/GBP 0.79 per xe.com on 2025-05-01").
- For rough comparisons, rounding to 2 decimal places is acceptable.

### Unit normalization

Common scenarios requiring normalization:

| Scenario | Normalization method |
|---|---|
| Multi-packs vs singles | Divide pack price by pack count for per-unit cost |
| Different sizes (oz, ml, g) | Calculate price per standard unit (per oz, per 100ml) |
| Bundle vs standalone | Separate bundle components and compare matching items |
| Subscription vs one-time | Compare one-time prices; note subscription discount separately |

### Landed cost calculation

Landed cost = product price + shipping cost + applicable import duties (if cross-border)

- For Prime/Walmart+ eligible items: shipping = $0 for members
- For non-member items: use displayed shipping cost
- If shipping says "calculated at checkout" and can't be determined: note as "shipping TBD" and exclude from landed cost comparison

### What to exclude from comparison

- **Clearly different products**: Different model, size, material, or generation
- **Used/refurbished listings**: Unless the user specifically asks to include them
- **Wholesale/bulk listings**: Unless the user is comparing at bulk level
- **International listings**: Unless cross-border comparison is the explicit goal

---

## Data Validation Checks

Before producing output, run these validation checks:

1. **Price sanity check**: Is any price less than 20% of the category average? If so, flag as potential error, counterfeit risk, or loss leader.

2. **Seller legitimacy**: Does the seller have fewer than 10 ratings? Flag as new/unestablished seller — their pricing may not reflect stable market conditions.

3. **Listing accuracy**: Does the listing title match the actual product being compared? Keyword-stuffed titles can mislead.

4. **Promo timing**: Are Lightning Deals or flash sales active? Note the expected end time if visible.

5. **Stock availability**: Is the item actually in stock? "Currently unavailable" listings should be excluded from active pricing comparisons.

6. **Rating count context**: A listing with 50,000 reviews at $14.99 represents a different competitive threat than one with 12 reviews at the same price. Include rating counts as context.

---

## Refresh Recommendations

| Scenario | Recommended refresh interval |
|---|---|
| Pre-launch pricing research | Weekly until launch, then daily for first 2 weeks |
| Stable market monitoring | Bi-weekly or monthly |
| Active price war detected | Every 24-48 hours |
| Seasonal/promotional period | Daily during the promotional window |
| Post-price-change verification | 24 hours after your own price change |

Always recommend a specific next-check date based on the scenario detected.
