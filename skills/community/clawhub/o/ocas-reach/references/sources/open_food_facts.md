# open_food_facts — crowdsourced packaged-food database (barcode → nutrition)

## What this source has

Open Food Facts is the Wikipedia of packaged food: ~3M products contributed by users worldwide, keyed by EAN/UPC barcode. Each product carries name, brand, categories, ingredients (raw text + parsed allergens), nutrition facts per 100g/100ml AND per serving, Nutri-Score, NOVA classification, eco-score, packaging materials, country of sale, additives list, label claims (organic, fair trade, etc.).

Coverage is heaviest in Western Europe (especially France, where the project originated). North American and Asian product coverage is improving but spotty. Data quality varies — some entries are photos-only with most fields empty; others are exhaustive.

Use Open Food Facts for: barcode lookup, ingredient/allergen analysis, comparing similar products. Pair with `usda_fooddata` for authoritative US nutrition data on raw foods (USDA covers raw ingredients better; OFF covers branded packaged goods better).

## Auth

| | |
|---|---|
| Required | none |
| Account | not needed |

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | 100 req/min recommended; bulk dumps preferred for analytics |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `barcode` | Fetch a product by EAN/UPC | `barcode` |
| `search` | Search products by name/brand/category | `search_terms` |

## Worked examples

```bash
# Barcode lookup (Nutella 750g)
python3 scripts/reach.py query open_food_facts barcode '{"barcode": "3017620422003"}'

# Search by product name
python3 scripts/reach.py query open_food_facts search '{
  "search_terms": "oat milk",
  "page_size": 20
}'

# Filter to a category
python3 scripts/reach.py query open_food_facts search '{
  "search_terms": "yogurt",
  "tagtype_0": "categories",
  "tag_contains_0": "contains",
  "tag_0": "yogurts",
  "page_size": 25
}'
```

## Response shape

- `barcode`: `{status, status_verbose, code, product: {product_name, brands, categories_tags, ingredients_text, allergens_tags, nutriments: {energy-kcal_100g, fat_100g, saturated-fat_100g, carbohydrates_100g, sugars_100g, fiber_100g, proteins_100g, salt_100g, sodium_100g, ...}, nutriscore_grade, nova_group, ecoscore_grade, image_url, ingredients: [{id, text, percent_estimate, vegan, vegetarian}, ...], packaging_tags, countries_tags, additives_tags, labels_tags, ...}}`. `status: 1` = found, `status: 0` = not found.
- `search`: `{count, page, page_count, page_size, products: [...same product schema...], skip}`.

## Pitfalls

- **Barcode is canonical** but format varies — UPC-A (12 digits) for US goods, EAN-13 (13 digits) for European. The API generally accepts both forms; leading zeros sometimes matter (`0001234...` ≠ `1234...`).
- **Product completeness is uneven.** Always check that the field you need is present before reading. `nutriments` may exist but be empty; `ingredients_text` may be `""`.
- **Nutriment field names embed units.** `energy-kcal_100g`, `fat_serving`, `sodium_unit`. The `_100g` suffix is the per-100g value; `_serving` is per-serving (when serving size is recorded); `_value`/`_unit` give the raw field.
- **`*_tags` arrays are normalized**, language-prefixed identifiers like `en:peanuts` or `fr:produits-laitiers`. Strip the prefix for display.
- **Nutri-Score and NOVA may be missing.** Computed scores depend on having enough data; absent score ≠ "good" or "bad".
- **`status: 0` (not found) is common.** Especially for North American or Asian products. Fall back to `search` or `usda_fooddata`.
- **Multilingual fields.** Many strings are stored in language-suffixed keys: `product_name_en`, `product_name_fr`. The unsuffixed `product_name` is the project's "main language" pick.
- **Search field syntax is legacy CGI.** Filtering uses awkward `tagtype_N`/`tag_contains_N`/`tag_N` triples (up to N=2). The newer v2 search supports cleaner JSON filters but isn't fully wrapped here.

## Source links

- API docs: https://openfoodfacts.github.io/openfoodfacts-server/api/
- Data fields list: https://wiki.openfoodfacts.org/Data_fields
- Terms: https://world.openfoodfacts.org/terms-of-use
