# thecocktaildb — cocktails (test endpoint with key "1")

## What this source has

TheCocktailDB is the cocktail sibling of TheMealDB — same shape of API, same author. A few hundred cocktails with ingredients, measurements, instructions, glass type, alcoholic/non-alcoholic flag, category (Ordinary Drink, Cocktail, Shot...), tags, image URL. Each drink has a numeric `idDrink`.

Use TheCocktailDB for: cocktail recipe lookup, random drink ideas, simple ingredient search. Same caveat as TheMealDB — sample dataset, not exhaustive.

## Auth

| | |
|---|---|
| Required | none (free uses key `"1"`) |
| Account | optional (Patreon for full features) |

The free key `"1"` is built into the base URL. Premium endpoints (image variants, list-by-multi-ingredient) require the patron-tier key.

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | no documented cap on the test endpoint |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `search` | Search drinks by name (or first letter) | `s` or `f` |
| `lookup` | Look up by drink ID | `i` |
| `random` | Random cocktail | none |

## Worked examples

```bash
# Search by name
python3 scripts/reach.py query thecocktaildb search '{"s": "margarita"}'

# Random drink
python3 scripts/reach.py query thecocktaildb random '{}'

# Drink by ID
python3 scripts/reach.py query thecocktaildb lookup '{"i": "11007"}'

# Search by first letter
python3 scripts/reach.py query thecocktaildb search '{"f": "g"}'
```

## Response shape

```json
{
  "drinks": [
    {
      "idDrink": "11007",
      "strDrink": "Margarita",
      "strCategory": "Ordinary Drink",
      "strAlcoholic": "Alcoholic",
      "strGlass": "Cocktail glass",
      "strInstructions": "Rub the rim of the glass with the lime slice...",
      "strDrinkThumb": "https://...",
      "strIngredient1": "Tequila", "strIngredient2": "Triple sec", "strIngredient3": "Lime juice", "strIngredient4": "Salt",
      "strMeasure1": "1 1/2 oz ", "strMeasure2": "1/2 oz ", "strMeasure3": "1 oz ",
      "strTags": "IBA,ContemporaryClassic", "dateModified": "..."
    }
  ]
}
```

No match → `{drinks: null}`.

## Pitfalls

- **`drinks: null` for no match.** Same as TheMealDB — `null`, not `[]`.
- **Ingredients flattened to `strIngredient1`..`strIngredient15`.** Loop and skip empties (`""` or `null`).
- **`strMeasure*` may have trailing whitespace** — `"1 1/2 oz "` (with the trailing space). Strip before display.
- **`strAlcoholic` values** are `"Alcoholic"`, `"Non alcoholic"`, or `"Optional alcohol"`. Note "Non alcoholic" without the hyphen.
- **No multi-ingredient filter on free tier.** Patron-only.
- **Coverage is a small curated set.** Don't expect every cocktail you've heard of.
- **Search by first letter (`f`)** returns a list of all drinks starting with that letter from the sample set.

## Source links

- API docs: https://www.thecocktaildb.com/api.php
- Public test endpoints: https://www.thecocktaildb.com/api/json/v1/1/
- Patron access: https://www.thecocktaildb.com/api.php
