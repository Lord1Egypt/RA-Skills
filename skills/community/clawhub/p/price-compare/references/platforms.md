# Price Compare — Platform Reference

## Platform Profiles

### Amazon
- **URL pattern:** `https://www.amazon.com/s?k={product}&s=price-asc-rank`
- **Strengths:** Largest selection, Prime shipping, massive review base, frequently used as price anchor
- **Weaknesses:** Fake "was" discounts (list price often inflated), search results polluted by sponsored products, same product listed by many sellers at different prices
- **Best for:** Books, tech accessories, consumables, anything with many reviews
- **Search tip:** Add `&s=price-asc-rank` for cheapest first; use `&rh=p_85%3A2470955011` to filter Marketplace sellers
- **Gotcha:** Always check "Used" / "New" toggle; check the "All prices" section on the deal page; Amazon's "was $X" is almost never real

### Walmart
- **URL pattern:** `https://www.walmart.com/search?q={product}`
- **Strengths:** Often undercuts Amazon on essentials & groceries, free 2-day shipping (no membership needed), easy returns, "Rollback" deals are real discounts
- **Weaknesses:** Search quality lower than Amazon, fewer reviews, inventory less reliable
- **Best for:** Household essentials, groceries, toys, basic electronics
- **Search tip:** Filter by price range and sort by "Price + Shipping: low to high"; Walmart+ members get free delivery (factor this into total cost)

### Target
- **URL pattern:** `https://www.target.com/s?searchTerm={product}`
- **Strengths:** Clean UI, same-day pickup (Drive Up), Circle membership deals, RedCard 5% off, well-curated brand selection
- **Weaknesses:** Generally slightly higher prices without Circle deals, smaller catalog than Amazon/Walmart
- **Best for:** Home goods, baby products, seasonal decor, when you want fast in-store pickup
- **Search tip:** Filter by RedCard pricing if available; check Circle offers before buying; Circle offers can sometimes be stacked with other discounts

### Best Buy
- **URL pattern:** `https://www.bestbuy.com/site/searchpage.phtml?st={product}`
- **Strengths:** Expert reviews, open-box deals (like new condition at discount), price match guarantee, bundles, installation services
- **Weaknesses:** Very limited to electronics and appliances; mostly full retail pricing
- **Best for:** TVs, laptops, phones, cameras, appliances, gaming consoles
- **Search tip:** Check "New & Open Box" filter to see refurbished/discounted units; look for "Deal of the Day"; open-box items are often 15-30% off and fully tested

### eBay
- **URL pattern:** `https://www.ebay.com/sch/i.html?_nkw={product}&_sop=15`
- **Strengths:** Best prices on used/refurbished goods, auctions, "Best Offer" negotiation, massive selection of vintage/rare items
- **Weaknesses:** Condition varies wildly, shipping costs can offset savings, no instant delivery, risk of misrepresentation
- **Best for:** Refurbished electronics, vintage items, parts, textbooks, used sporting gear
- **Search tip:** Filter by "Used" / "Seller Refurbished"; sort by price + factor in shipping; check seller rating (95%+ preferred); look for "eBay Authentic Guarantee" badge for electronics

### Temu
- **URL pattern:** `https://www.temu.com/search_result.html?search_key={product}`
- **Strengths:** Consistently the lowest prices on most goods due to direct-from-manufacturer supply chain and heavy subsidies; enormous catalog; frequent flash sales and coupons; 90-day free returns
- **Weaknesses:** Quality is hit-or-miss on unbranded items; shipping is slow (7–21 days) unless paying for faster options; many products are unbranded knockoffs or generic; no review transparency (reviews are often incentivized)
- **Best for:** Non-critical consumables, accessories, home décor, trendy gadgets, sports equipment (especially generic/unbranded)
- **Search tip:** Filter by "4.5+ stars"; use coupon codes (often auto-applied); compare against branded equivalents on Amazon before buying; check the "Similar" tab for cheaper alternatives
- **Gotcha:** "Almost out of stock" is often a dark pattern — ignore it. Compare photos with Amazon listing to spot cheap imitations.

### Costco
- **URL pattern:** `https://www.costco.com/search?search={product}`
- **Strengths:** Often the absolute lowest unit price for bulk/household items; very reliable for electronics (authorized dealer); Kirkland Signature brand is high quality for low price; 2% annual Executive Member reward (up to $1000/year)
- **Weaknesses:** Membership required (~$60-120/year); limited to Costco's curated selection; large minimum pack sizes; online price may differ from in-warehouse price
- **Best for:** Bulk groceries, household paper goods, electronics (TVs, laptops), appliances, contact lenses, tires
- **Search tip:** Check if the price shows "Executive Member price" (extra 2% off); compare online vs. in-warehouse prices; Costco's electronics prices are often below market

### Kroger
- **URL pattern:** `https://www.kroger.com/search?query={product}`
- **Strengths:** Strong on groceries, household essentials, and pharmacy; digital coupons stack with sale prices; Boost by Kroger ($59/year) gives 5% off fuel + 10% off most items; fresh food prices are competitive
- **Weaknesses:** Non-grocery selection is limited; online delivery fees apply without subscription; regional availability varies
- **Best for:** Groceries, fresh food, household essentials, prescriptions
- **Search tip:** Always load digital coupons before shopping; Boost by Kroger membership dramatically changes the value equation; check "Fuel savings" calculator

### Google Shopping
- **URL pattern:** `https://www.google.com/shopping?q={product}&hl=en`
- **Strengths:** Aggregates all major retailers in one view, shows price history, easy comparison, pulls reviews from multiple sources
- **Weaknesses:** Redirects to other sites (doesn't purchase), results can include smaller/less reputable shops, tax not always shown
- **Best for:** One-stop overview, checking if current price is a good deal vs. history, finding the overall lowest price across the web
- **Search tip:** Click "Price history" link when visible; filter by star ratings; ignore results from unknown resellers

---

## Google Shopping Price History Guide

| Indicator | Meaning | Action |
|-----------|---------|--------|
| "Typically $220" | Stable price over 90 days | Price is reliable — this is the real market value |
| "↓ Good time to buy — down 20% from average" | Genuine sale below market | 🟢 Good time to buy |
| "↗ Price has gone up 15% in 30 days" | Price rising | ⚠️ Not the best time — wait if possible |
| "→ Stable — within normal range" | Normal fluctuation | Price is fair |
| "Was $X, now $Y" with X >> market avg | Fake anchor price | 🚩 Ignore X, compare Y to typical market price |
| No price history shown | Can't verify | ⚠️ Use other trust signals (reviews, seller type) |

---

## Platform Selection Guide

| Product Category | First Choice | Second Choice | Budget Pick |
|-----------------|-------------|---------------|-------------|
| Electronics (TVs, laptops, phones) | Best Buy | Amazon | Costco |
| Household essentials | Walmart | Kroger | Temu |
| Books | Amazon | eBay (used) | Walmart |
| Used / Refurbished electronics | eBay | Best Buy (open-box) | Amazon |
| Toys | Target | Costco | Temu |
| Groceries | Kroger | Walmart | Costco (bulk) |
| Appliances | Best Buy | Costco | Amazon |
| Clothing & Fashion | Target | Amazon | Temu |
| Sports & Outdoors | Amazon | Costco | Temu |
| Beauty & Personal Care | Target | Kroger | Amazon |

---

## Output Flags

| Flag | Meaning |
|------|---------|
| 🔥 Best Price | Lowest total cost (price + shipping) |
| ⭐ Best Value | Best price-to-quality ratio considering reviews and shipping |
| ⚡ Fastest | Fastest shipping available (same-day/next-day) |
| ♻️ Best Used/Refurb | eBay or Best Buy open-box, verified seller |
| 💸 Budget Pick | Temu unbranded — cheapest but lower quality assurance |
| 🛡️ Authenticated | eBay Authentic Guarantee or similar verification |
| 🎯 Bulk Pick | Costco — best per-unit price for multi-packs |
