# Influencer Attribution Guide

## Why Attribution Is Broken (and How to Fix It)

Standard influencer attribution fails for three reasons:
1. **Platform self-reporting** — TikTok and Instagram report conversions using their own attribution windows (often 7-day click, 1-day view), which double-count conversions attributed to other channels.
2. **Discount code sharing** — Codes spread to coupon sites within hours of going live, inflating a creator's attributed orders.
3. **Last-click bias** — Customers who discover a product through an influencer post but buy days later via Google search get attributed to paid search, not the creator.

---

## UTM Parameter Setup

### Recommended UTM Structure
```
utm_source=influencer
utm_medium=[platform]        (tiktok / instagram / youtube / pinterest)
utm_campaign=[campaign-name]
utm_content=[creator-handle]
utm_term=[post-type]         (video / reel / story / pin)
```

### Example URL
```
https://yourbrand.com/products/widget?utm_source=influencer&utm_medium=tiktok&utm_campaign=q2-launch&utm_content=creatorA&utm_term=video
```

### Shopify Setup
1. Create a URL with UTM parameters for each creator.
2. Share the UTM link in the creator brief — they put it in bio link or link sticker.
3. In Shopify Analytics → Sessions by UTM source → filter by `utm_content=[handle]` to pull creator-specific sessions and conversions.

---

## Unique Discount Code Strategy

### Best Practices
- Use creator-specific codes (e.g., `CREATORNAME15`) rather than generic campaign codes.
- Set a single-use-per-customer limit where possible to reduce sharing impact.
- Generate codes with a 2–4 week expiry tied to the campaign window.
- Track code redemptions in your ecommerce backend, not in the influencer platform.

### Hybrid Attribution (Most Accurate)
Combine UTM sessions with discount code orders:
- **UTM orders**: customers who clicked the link and purchased (with or without the code)
- **Code orders**: customers who used the discount code but may not have clicked the UTM link
- **Union = Total attributed orders** (deduplicate by order ID)

---

## Detecting Discount Code Leakage

### Quick Check Process
1. Search `"[DISCOUNT_CODE]" site:retailmenot.com` — if it appears, leakage is confirmed.
2. Repeat for: honey.com, joinhoney.com, couponbirds.com, dealspotr.com, groupon.com.
3. Check code usage velocity: if 80% of redemptions happen in the first 3 hours after posting (before broader reach), that's natural. If usage spikes on days the creator didn't post, leakage is occurring.

### Leakage Factor Calculation
```
Leakage Factor = (Code Uses Not Attributable to Creator Audience) / Total Code Uses

Conservative estimate:
- 1–2 coupon sites found → apply 15% leakage factor
- 3–4 coupon sites found → apply 25% leakage factor
- 5+ sites or code on Honey extension → apply 40% leakage factor

Adjusted Revenue = Raw Attributed Revenue × (1 − Leakage Factor)
```

---

## Multi-Touch Attribution Model

### Recommended: Time-Decay Model
Gives full credit to the converting touch, partial credit to earlier touches within 30 days.

| Touch Order | Days Before Conversion | Credit Weight |
|-------------|----------------------|---------------|
| Last touch (converter) | 0 | 100% |
| 2nd-to-last touch | 1–7 days prior | 40% |
| 3rd touch | 8–14 days prior | 20% |
| Earlier touches | 15–30 days prior | 10% |

### Practical Assisted Conversion Credit (Simpler)
If you can't implement full multi-touch, use a flat 20% assisted revenue credit for any creator whose UTM appears in the session path of a customer who later converts through another channel within 30 days.

Pull this from Google Analytics 4: Explore → Path Exploration → filter conversion paths that include your influencer UTM parameters.

---

## Platform-Specific Attribution Notes

### TikTok
- TikTok Pixel uses 7-day click / 1-day view windows — will overcount.
- Use Shopify backend as source of truth. TikTok numbers are for reach/awareness context only.
- Stories expire in 24h; link-in-bio performance decays quickly. Measure orders within 72h of post going live.

### Instagram
- Reels can have long tails (2–4 weeks of continuous traffic). Use 30-day UTM window.
- Story swipe-ups convert faster (within 24–48h). Use shorter attribution window.
- Instagram Shopping tags track add-to-cart but not always conversion — verify against Shopify.

### YouTube
- Long-form videos have the longest attribution tails (60–90 days not uncommon for review content).
- Description links with UTM are the most reliable attribution; pinned comment links are secondary.
- YouTube Analytics → Traffic Sources → External → filter by your domain to see click-through volume.

### Pinterest
- Pins are evergreen; use a 90-day attribution window.
- Pinterest Ads Manager conversion tracking is more accurate than organic pin analytics.
- If creator uses affiliate links (LTK, ShopMy), get their affiliate dashboard data directly.
