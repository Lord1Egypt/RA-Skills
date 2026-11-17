# themealdb — recipes (test endpoint with key "1")

## What this source has

TheMealDB is a crowdsourced recipe database — a few thousand recipes with ingredients, measurements, instructions, category (Beef, Chicken, Vegetarian...), area/cuisine (American, Italian, Thai...), tags, YouTube link, and an image URL per recipe. Each meal has a numeric `idMeal`. Coverage is light compared to commercial recipe sites — think sample dataset, not exhaustive.

Use TheMealDB for: random recipe ideas, simple ingredient/cuisine search, building a quick demo app. Not a substitute for serious recipe coverage.

## Auth

| | |
|---|---|
| Required | none (free uses key `"1"`) |
| Account | optional (Patreon-tier API key for full features) |

The free key `"1"` is hard-coded into the URL and works only against the demo "test" endpoints — those wrap the public sample dataset. Premium features (image filters, list-by-letter on full corpus) require the patron-tier key.

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | no documented cap on the test endpoint |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `search` | Search by name (or first letter) | `s` (name) or `f` (first letter) |
| `lookup` | Look up by meal ID | `i` |
| `random` | Random meal | none |
| `categories` | List meal categories | none |

## Worked examples

```bash
# Search by name
python3 scripts/reach.py query themealdb search '{"s": "carbonara"}'

# Search by first letter
python3 scripts/reach.py query themealdb search '{"f": "a"}'

# Random meal
python3 scripts/reach.py query themealdb random '{}'

# Meal by ID
python3 scripts/reach.py query themealdb lookup '{"i": "52772"}'

# All categories
python3 scripts/reach.py query themealdb categories '{}'
```

## Response shape

```json
{
  "meals": [
    {
      "idMeal": "52772",
      "strMeal": "Teriyaki Chicken Casserole",
      "strCategory": "Chicken",
      "strArea": "Japanese",
      "strInstructions": "...",
      "strMealThumb": "https://...",
      "strTags": "Meat,Casserole",
      "strYoutube": "https://...",
      "strIngredient1": "soy sauce",
      "strIngredient2": "...",
      "strMeasure1": "3/4 cup",
      "strMeasure2": "...",
      "strSource": "...", "strImageSource": null,
      "dateModified": null
    }
  ]
}
```

If no match: `{meals: null}` (note: `null`, not an empty array).

## Pitfalls

- **`meals: null` for no-match**, not `[]`. Always check before iterating.
- **Ingredients are flattened into 20 numbered slots.** `strIngredient1`...`strIngredient20`, paired with `strMeasure1`...`strMeasure20`. Empty unused slots may be `""` or `null`. Loop over the range and skip empties.
- **Free key is `"1"`** — hard-coded in the base URL. Premium endpoints (image filter, list-by-letter on full corpus) require a paid Patreon key, which the test endpoint does not honor.
- **No cuisine taxonomy beyond `strArea`** — single string per meal. Don't expect multi-tag classification.
- **Category list** only carries names + thumbnails + descriptions — to get meals in a category, use `filter.php?c=<category>` (not currently wrapped here).
- **Coverage is a sample.** A few hundred meals; many common dishes are absent. For broad recipe coverage, look elsewhere.
- **Test data is static.** Recipes don't update meaningfully — same dataset month-to-month.

## Source links

- API docs: https://www.themealdb.com/api.php
- Public test endpoints: https://www.themealdb.com/api/json/v1/1/
- Patron access: https://www.themealdb.com/api.php (lower section)
