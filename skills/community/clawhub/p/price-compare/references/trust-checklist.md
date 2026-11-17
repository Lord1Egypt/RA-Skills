# Price Trust Checklist (Reviewer Pattern)

Use this checklist to score every price result before presenting it to the user. Score each signal, sum the points, then apply the final trust label.

---

## Trust Signals

### Positive Signals (+points)

| Signal | +Points | Why |
|--------|---------|-----|
| First-party / official store (Wilson.com, Best Buy, DICK'S) | +2 | Authentic, full warranty, real inventory |
| 4.5+ stars AND 500+ reviews | +1 | Popular, likely genuine |
| Price history shown on Google Shopping (stable / down) | +1 | Can verify it's a fair price |
| "Sale" confirmed by price history (was $X, now $Y, X was actually sold) | +1 | Real discount |
| Free shipping (especially over a reasonable threshold) | +1 | Reduces total cost uncertainty |
| Returns accepted (30+ days) | +1 | Risk-free to try |
| Seller/authenticity guarantee | +1 | Protects against counterfeits |
| Costco member price (confirmed) | +1 | Often genuinely cheaper with membership |
| eBay authenticated (eBay Authentic Guarantee badge) | +1 | Fake item = full refund |

### Negative Signals (−points)

| Signal | −Points | Why |
|--------|---------|-----|
| "Was $X, now $Y" where X > 30% above current market price | −2 | X was never really the price — dark pattern |
| No reviews / <10 reviews | −1 | Cannot verify quality |
| Generic/unbranded product on Temu | −1 | Quality not assured, easy to counterfeit |
| eBay seller rating <95% | −2 | High defect/misrepresentation rate |
| Used or refurbished (without grade disclosed) | −1 | Normal risk — acceptable if disclosed |
| "Only 2 left!" / countdown timer / stock pressure | −1 | Dark pattern — ignore these |
| Price < 30% of the average market price | −3 | Almost certainly fake, counterfeit, or dropshipped garbage |
| 1-star reviews mention "fake" or "counterfeit" | −2 | Possible counterfeit on platform |
| International seller with long shipping (no US stock) | −1 | Long wait, hard to return |
| Marketplace / third-party seller on Amazon | −1 | Amazon itself doesn't vet marketplace sellers |
| Price only available with coupon code (not shown) | −1 | "Discount" requires code user doesn't have |
| Cryptocurrency / non-standard payment only | −2 | High fraud risk |

### Neutral Signals (±0)

| Signal | Points | Note |
|--------|--------|------|
| Refurbished (grade A/B disclosed, seller rated 95%+) | ±0 | Acceptable if clearly disclosed |
| Bulk pricing (e.g., "buy 4 at $X each") | ±0 | Good for groups, but single unit price may differ |
| Membership-only price (Costco, Prime, Target Circle) | ±0 | Note which membership is needed |

---

## Score Interpretation

| Score Range | Label | Color | Action |
|------------|-------|-------|--------|
| +3 to +5 | 🟢 Reliable | Green | Show prominently, recommend |
| +1 to +2 | 🟡 Acceptable | Yellow | Show with a brief caveat note |
| 0 to -1 | 🟠 Caution | Orange | Show only if user is budget-sensitive, add warning |
| −2 or below | 🔴 Suspicious | Red | Skip or show only with strong warning + do not recommend |

---

## Platform-Specific Notes

### Amazon
- Amazon Marketplace sellers (fulfilled by Amazon) get +0; sold by Amazon directly gets +2
- Check the "New & Used" toggle — marketplace can show different (lower) prices
- "A variety of new" price = aggregated marketplace, not a single price

### eBay
- Only trust eBay if: seller 98%+, "eBay Authentic Guarantee" badge, or bulk buy from established seller
- Watch for "graded" items (PSA/BGS graded cards etc.) — these have legitimate high-value variants
- "Buy It Now" vs auction: auction end time matters, bid != final price

### Temu
- Anything under $5 is almost always generic/unbranded — accept as-is (no trust score fraud risk at that price)
- Review count on Temu is unreliable — many are incentivized reviews
- Best for: non-critical consumables, accessories, trendy gadgets where you don't care about brand
- Worst for: anything you rely on for safety (electronics with real safety certifications, baby products, anything ingestible)

### Google Shopping
- "Typically $X" = the price has been stable at X for 90+ days
- "↗ Price up 15% in 30 days" = the price is rising, not a great time
- "↓ Price down 20% from average" = a genuine sale, good time to buy
- Ignore results from unknown reseller brands — these are often affiliate aggregators

### Walmart
- "Rollback" = genuine temporary price reduction
- "Reduced" = may continue to reduce or go back up
- Walmart+ members get free delivery — factor in membership cost for true comparison

### Target
- RedCard (debit or credit) = 5% off + free shipping — worth noting if user has one
- Circle offers can stack — worth checking before recommending

---

## Worked Example — Basketball Trust Scoring

**Wilson NBA Official Game Ball @ Amazon (Marketplace, $195)**
- Third-party seller → +0
- 4.5 stars / 200 reviews → +1
- Price 11% below market ($195 vs $220) → +0 (could be real)
- "Was $280" listed → −2 (fake anchor — $280 was never real)
- Free shipping → +1
- **Total: +0 = 🟠 Caution** → Show with warning about marketplace seller

**Wilson NBA Official Game Ball @ DICK'S ($219.99, 11% off)**
- First-party retailer → +2
- 4.7 stars / 129 reviews → +1
- Price history confirms discount (was $250, now $219.99) → +1
- Free shipping + 90-day returns → +2
- **Total: +6 = 🟢 Reliable** → Show as primary recommendation

**Wilson-style ball @ Temu ($8.99, no brand)**
- Unbranded generic → −1
- No reviews visible → −1
- Price < 30% of market ($9 vs $220) → −3
- **Total: −5 = 🔴 Suspicious** → Skip or warn strongly
