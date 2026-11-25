---
name: marketplace-price-check
description: Work out what an item really sells for on Facebook Marketplace in a given city - fair price range, median, underpriced listings and listings to avoid - from live public listings via SocialAPIs. Use when the user asks what something is worth, whether a listing is a good deal, how to price an item they want to sell, or wants resale / flipping research in a local market.
---

# Marketplace price check

Answer "what does this go for around here?" with numbers from current Facebook Marketplace listings, not guesses.

Needs `SOCIALAPIS_API_KEY`. Auth, parameters and errors are in the `socialapis` skill ([endpoint reference](https://github.com/SocialAPIsHub/skills/blob/main/skills/socialapis/references/endpoints.md)); if the SocialAPIs MCP tools are connected, use `facebook_marketplace` instead of raw HTTP.

## Ask first (only what's missing)

- The item, as specific as possible: model, size, storage, year ("iPhone 15 Pro 256GB", not "iPhone").
- The city (and country if the name is ambiguous) and a radius. Default 40 km.
- Condition if it matters: new, used_like_new, used_good, used_fair.
- Is the user **buying** (find deals) or **selling** (set a price)? It changes the output.

## Budget

Every call is 1 credit. A normal check is 4 to 8 credits: 1 for coordinates, 2 to 4 search pages, 1 to 3 listing details. Say the estimate before starting if the user's balance is low (`/usage` is free).

## Steps

1. **Location.** `/facebook/marketplace/city-coordinates?city=<city>&country=<country>&exactly_one=true` and keep the latitude and longitude.
2. **Collect comparables.** `/facebook/marketplace/search` with `query`, the coordinates, `filter_radius_km`, `exact_match=true` for model numbers, and `commerce_search_and_rp_condition` if given. Sort `CREATION_TIME_DESCEND` so the sample is current. Follow `end_cursor` until you have about 30 to 60 listings or there are no more pages.
3. **Clean the sample.** This is the step that makes the answer trustworthy:
   - Parse `price` strings (`"$15,900"`, `"1.200 €"`) into numbers; keep the currency.
   - Drop listings that aren't the item: accessories, cases, "for parts", "broken", "trade only", bundles, different storage or model. Read titles; when unsure, drop it.
   - Drop placeholder prices (0, 1, 123, 1234, 9999) and duplicates (same title + price + photo).
   - Report how many you dropped and why.
4. **Compute.** On the cleaned prices: count, median, 25th and 75th percentile (the "fair range"), min and max. Split by condition if there are at least 5 per condition.
5. **Spot outliers.** Listings below the 25th percentile by more than 20% are "worth a look"; open the top 1 to 3 with `/facebook/marketplace/listing?listing_id=…` and read the description and photos count.
6. **Seller check (only for shortlisted deals).** `/facebook/marketplace/seller?seller_id=<seller.id from the listing>`: join date, rating, reviews. A brand-new account plus a far-below-market price is a red flag, not a deal.

## Warning signs to call out

- Price far below the 25th percentile with a new or reviewless seller.
- Description asks to move off Facebook, pay by gift card, wire or crypto, or ship-only for an item usually picked up locally.
- Stock photos only, or the same photo on several listings.
- "Price is firm, deposit first".

Say these are signals, not proof.

## Output

```
## <item> in <city> (<radius> km), <date>

Fair range: <p25> - <p75> <currency>   Median: <median>   Sample: <n> listings (<dropped> removed: <reasons>)

| Condition | Listings | Median | Range (p25-p75) |
|---|---|---|---|

### Worth a look   (buying)    /    Price it at   (selling)
| Title | Price | vs median | Seller (joined, rating) | Link |

### Skip
<listings with warning signs, one line each, why>

Notes: asking prices, not sold prices; Marketplace shows what's listed today.
```

For a seller: suggest a list price just under the median for a quick sale, or near the 75th percentile if their item is in better condition than most of the sample, and say which.

## Be honest about the data

- These are **asking** prices. Sold prices aren't public. Say so in the output.
- Small samples (under 10 after cleaning) give a rough range only; say "rough".
- Don't contact sellers or post anything; this skill only reads public listings.
