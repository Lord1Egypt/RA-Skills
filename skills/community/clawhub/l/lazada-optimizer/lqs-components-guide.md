# LQS Components Guide — What Moves Listing Quality Score

Lazada's Listing Quality Score (LQS) bands listings as Poor / To Improve / Good / Excellent and feeds search ranking. Work the components in this order — it reflects typical impact per hour of effort.

## 1. Required category attributes (highest impact)

- Unfilled REQUIRED attributes cap the LQS band outright.
- Filtered search runs on attributes: a missing "material" or "capacity" removes the listing from those filter results entirely — invisible, regardless of rank.
- Action: open the category tree in Seller Center, fill 100% of required AND recommended fields. Re-check after Lazada category-tree updates (quarterly is safe).

## 2. Title structure

- Formula: `Brand + Model + Key Spec + Category Keyword`, 60–120 characters.
- Penalized patterns: emoji/symbols (【】★), promo words (HOT, SALE, MURAH, BEST), all-caps runs, repeated keywords.
- One primary category keyword; the search engine derives the rest from attributes and description — stuffing adds penalty, not reach.

## 3. Images

- Minimum ≥800×800px (zoom requires ≥1000×1000). Target 8 slots:
  1. White-background main (product fills ~85% of frame, no text overlays)
  2–4. Lifestyle/context shots
  5. Size or spec infographic
  6. Feature close-up
  7. Comparison or what's-in-the-box
  8. Packaging/warranty card
- Main-image text overlays and watermarks are quality penalties in most categories.

## 4. Video

- 15–30 seconds, demonstrates the hero function in the first 5 seconds.
- Video presence improves both LQS and conversion; a clean phone-shot demo is sufficient. Vertical 9:16 preferred (feeds into Lazada's discovery surfaces).

## 5. Description keyword coverage

- Structured description with short sections/bullets; cover secondary keywords naturally (the ones not used in the title).
- Include: dimensions/specs table, usage scenarios, care/warranty, FAQ-style objections (battery life, sizing, compatibility).
- Lazada indexes description text for long-tail queries — duplicate-thin descriptions across SKU variants dilute this.

## 6. Price competitiveness signal

- LQS interacts with price position vs. category median; being a far outlier (high) suppresses impressions.
- Use Seller Center's price suggestion as a sanity bound, not a command — undercutting to the floor erodes campaign discount room (thresholds compute off your 30-day lowest).

## Diagnostic flow for a stagnant listing

```
Organic traffic flat ≥30 days
 ├─ LQS below "Good"? → fix components 1–5 above, in order
 ├─ LQS "Good"+ but low impressions? → check attribute-filter coverage,
 │   price-outlier position, and campaign participation (non-participants
 │   lose baseline rank during campaign months)
 ├─ Impressions OK but CTR low? → main image and price point
 └─ Clicks OK but no orders? → description gaps, reviews <4.0, chat
     response, shipping fee surprise at checkout
```

## What does NOT meaningfully move LQS

- Renaming the shop, decorative store banners, follower count
- Re-publishing the same listing repeatedly (resets review history — actively harmful)
- Buying traffic to the listing without fixing the above (conversion drops, which hurts rank)
