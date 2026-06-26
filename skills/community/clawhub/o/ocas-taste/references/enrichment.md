# Entity Enrichment

How Taste enriches raw venue and item names into taste-relevant profiles.

## Why enrichment matters

A raw signal like "visited Nopa" or "ordered from Tartine" is just an identifier. To build a meaningful taste model and generate useful recommendations, Taste needs to know *what kind of place* Nopa is — its cuisine, price point, neighborhood, vibe. Enrichment turns identifiers into profiles that the recommendation engine can reason over.

Without enrichment, Taste can only say "you visited Nopa 4 times." With enrichment, it can say "you gravitate toward California-Mediterranean restaurants in the $$$  range in NoPa/Divisadero — you might like Rich Table."

## When to enrich

After promoting an ExtractionRecord to a ConsumptionSignal, check the associated ItemRecord. If `enriched: false`, queue it for enrichment. Enrichment happens as part of the `taste.enrich.item` command, which can be called:
- Automatically after `taste.scan` for newly created items
- Manually for any item in the model

## Enrichment sources (in order)

1. **Google Maps** — primary source. Look up the venue/item on Google Maps and extract structured attributes (cuisine, price level, rating, neighborhood, category, etc.)
2. **Web search** — backup. If Google Maps data is insufficient or the item isn't a physical venue (e.g., Amazon products), use web search to fill gaps.

## What to extract per domain

### Restaurants

| Attribute | Source | Description |
|-----------|--------|-------------|
| `cuisine[]` | Google Maps categories, web | e.g., ["japanese", "izakaya"], ["italian", "pizza"] |
| `price_level` | Google Maps | 1 (budget) to 4 (fine dining) |
| `neighborhood` | Google Maps address | e.g., "Mission", "Hayes Valley", "NoPa" |
| `city` | Google Maps address | e.g., "San Francisco", "Oakland" |
| `vibe[]` | Google Maps reviews summary, web | e.g., ["casual", "lively"], ["intimate", "romantic"] |
| `rating` | Google Maps | Numeric rating |
| `maps_place_id` | Google Maps | For future lookups and dedup |
| `seasonal_menu` | Web search | Whether the venue has a seasonal/rotating menu (relevant for re-recommendation exception) |

### Hotels

| Attribute | Source | Description |
|-----------|--------|-------------|
| `hotel_class` | Google Maps, web | Star rating (1-5) |
| `style[]` | Web search, reviews | e.g., ["boutique", "design"], ["resort", "spa"] |
| `neighborhood` | Google Maps address | Local area name |
| `city` | Google Maps address | City name |
| `price_tier` | Google Maps, web | budget, mid, upscale, luxury |
| `rating` | Google Maps | Numeric rating |
| `maps_place_id` | Google Maps | For future lookups |

### Products (Amazon, etc.)

| Attribute | Source | Description |
|-----------|--------|-------------|
| `category` | Web search, product page | e.g., "kitchen appliance", "book", "electronics" |
| `brand` | Extraction data, web | Brand name |
| `price_tier` | Order amount vs category median | budget, mid, premium |

### Food delivery items (DoorDash, Instacart, Good Eggs)

For delivery orders, enrich the *restaurant or store*, not individual menu items:
- DoorDash: enrich the restaurant (same as restaurant enrichment above)
- Instacart: enrich the store (e.g., "Whole Foods" → organic/premium grocery, neighborhood)
- Good Eggs: enrich the producer/farm when identifiable, otherwise the category

## Enrichment workflow

1. Look up the item name + city on Google Maps
2. Extract available attributes from the Maps result
3. If key attributes are missing (especially cuisine, price_level for restaurants), run a web search
4. Update the ItemRecord metadata with enriched attributes
5. Set `enriched: true` and `enriched_at` to current timestamp
6. After enrichment, evaluate whether new LinkRecords should be created between this item and other enriched items sharing attributes (same cuisine, same neighborhood, same price tier, etc.)

## Link generation from enrichment

When an item is enriched, compare its attributes against other enriched items to create or strengthen LinkRecords:

- **same_cuisine**: Two restaurants sharing a cuisine type
- **same_neighborhood**: Two venues in the same neighborhood
- **same_price_tier**: Venues at the same price level
- **same_style**: Hotels with overlapping style tags
- **cross_domain**: A restaurant and a travel destination linked by cuisine/culture (e.g., Japanese restaurant visits → Japan travel suggestion)

Link strength is proportional to the number of shared attributes. Two restaurants sharing cuisine + neighborhood + price level get a stronger link than two sharing only cuisine.

## Re-enrichment

Items may be re-enriched if:
- `enriched_at` is older than 180 days (attributes may have changed)
- The item has missing key attributes that a new lookup might fill
- The user manually requests re-enrichment

Re-enrichment overwrites stale attributes but preserves `first_seen` and `visit_dates`.
