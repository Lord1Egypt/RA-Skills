# usda_fooddata — USDA FoodData Central (authoritative US nutrition)

## What this source has

USDA FoodData Central (FDC) merges several USDA nutrition datasets:
- **Foundation Foods**: research-grade nutrient profiles for raw and minimally processed foods.
- **SR Legacy**: Standard Reference, the historical canonical USDA nutrient database.
- **Survey (FNDDS)**: foods consumed in NHANES dietary surveys, with portion-size data.
- **Branded Foods**: ~1.5M packaged products from manufacturer label submissions.
- **Experimental Foods**: in-progress research data.

Each food has an FDC ID (integer, the canonical key) plus optionally a UPC (for branded), an NDB number (legacy), and a data type tag indicating which dataset it came from. Nutrient values include the value, unit, derivation method, and standard error where available.

Use USDA FoodData for: authoritative US nutrition data on raw foods (broccoli, salmon, oats), portion sizes from dietary surveys, branded products via label data. Pair with `open_food_facts` for international branded packaged goods.

## Auth

| | |
|---|---|
| Required | yes |
| Env var | `USDA_KEY` |
| Account URL | https://api.nal.usda.gov/fdc/ |
| Plan tier | free |

Reach is authorized to register at the URL above using `<agent-email>`. See `references/account_provisioning.md`. The signup is via api.data.gov — same key works for many federal APIs (NASA, govinfo).

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | 1,000 req/hour per key |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `search` | Search foods | `query` |
| `food` | Fetch one food by FDC ID | `fdc_id` |
| `foods` | Bulk fetch by FDC IDs (POST) | `fdcIds` (array) |

## Worked examples

```bash
# Search for "raw broccoli"
python3 scripts/reach.py query usda_fooddata search '{
  "query": "raw broccoli",
  "dataType": ["Foundation", "SR Legacy"],
  "pageSize": 25
}'

# Fetch one food
python3 scripts/reach.py query usda_fooddata food '{
  "fdc_id": 170379,
  "format": "full"
}'

# Bulk fetch
python3 scripts/reach.py query usda_fooddata foods '{
  "fdcIds": [170379, 173944, 169414],
  "format": "abridged"
}'

# Search constrained to branded foods with a specific nutrient floor
python3 scripts/reach.py query usda_fooddata search '{
  "query": "greek yogurt",
  "dataType": ["Branded"],
  "pageSize": 50
}'
```

## Response shape

- `search`: `{totalHits, currentPage, totalPages, foods: [{fdcId, description, dataType, gtinUpc, brandOwner, brandName, ingredients, marketCountry, foodCategory, publishedDate, foodNutrients: [{nutrientId, nutrientName, nutrientNumber, unitName, value}, ...], finalFoodInputFoods, foodMeasures, packageWeight}, ...]}`.
- `food` (single): `{fdcId, description, dataType, foodNutrients: [{nutrient: {id, number, name, unitName}, amount, dataPoints, derivationCode, ...}], foodPortions: [{id, amount, modifier, gramWeight, sequenceNumber}], inputFoods: [...], publishedDate, foodAttributes, ...}` — schema varies by `dataType`.
- `foods`: array of food objects, same shape as single `food`.

## Pitfalls

- **FDC ID is canonical**, not NDB number. Older USDA tools used 5-digit NDB numbers; FDC introduced new IDs. Both can coexist but FDC ID is the modern key.
- **Schema differs by `dataType`.** Foundation has `inputFoods` and `nutrientConversionFactors`; Branded has `gtinUpc`, `brandOwner`, `ingredients`. Always branch on `dataType`.
- **Nutrient ID numbers are stable.** Common ones: 1003 protein, 1004 fat, 1005 carbohydrate, 1008 energy (kcal), 1093 sodium, 1087 calcium. Look up the full list at `/nutrients`.
- **Per-100g vs per-portion.** `foodNutrients[].value` is per 100g of the food (or per 100mL for liquids). To convert to per-serving, multiply by `(servingSize / 100)` using `foodPortions`.
- **Branded foods have label-derived values.** Manufacturer-submitted, less rigorous than Foundation/SR Legacy. Same nutrient may differ across brands of the same food.
- **`dataType` filter is an array** — pass as a JSON array, not a comma-separated string.
- **`format` controls verbosity.** `abridged` is much smaller and usually enough; `full` includes all nested input foods, derivation codes, etc.
- **`api.data.gov` shared rate limit.** A single api.data.gov key shares its 1000/hour quota across NASA, USDA, govinfo, and other federal APIs.

## Source links

- API docs: https://fdc.nal.usda.gov/api-guide.html
- Data dictionary: https://fdc.nal.usda.gov/portal-data/external/dataDictionary
- Sign-up: https://fdc.nal.usda.gov/api-key-signup.html
