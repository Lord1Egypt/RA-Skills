# Leftover Chef 🍳

Turn random leftover ingredients into meals you can actually cook tonight.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## The Problem

People throw away food because they don't know what to cook with random leftover ingredients. A fridge with eggs, rice, and half an onion becomes food waste instead of fried rice.

## The Solution

**Leftover Chef** is an agent skill that takes a list of ingredients you already have and matches them against a database of **57 recipes**, ranking each by **how completely it uses what you've got**. Recipes you can make right now bubble to the top. Recipes that are one or two items short come next, with clear missing-ingredient warnings.

## Quick Start

```bash
# What can I cook with these?
python3 scripts/leftover_chef.py egg rice soy sauce garlic onion

# Get JSON output for programmatic use
python3 scripts/leftover_chef.py chicken potato carrot --json

# Show only recipes I can make 80%+ of
python3 scripts/leftover_chef.py tomato onion garlic basil --threshold 80

# Browse the database
python3 scripts/leftover_chef.py --list-ingredients
python3 scripts/leftover_chef.py --list-recipes
```

## Example Output

```
============================================================
  🍳 LEFTOVER CHEF
  Ingredients: egg, rice, soy sauce, garlic, onion
  Matches found: 57
============================================================

  ★ You have everything for these — cook now!
  1. Fried Rice  —  100% ingredients (5/5)
     ████████████████████
     Time: 20 min  Difficulty: easy  Cuisine: asian
     ✓ Have: rice, egg, soy sauce, garlic, onion
```

## Features

- **57 built-in recipes** across 10+ cuisines (Italian, Asian, Mexican, Indian, Middle Eastern, American, French, Greek, Spanish, British)
- **Fuzzy ingredient matching** — "eggs" matches "egg", "tomatoes" matches "tomato", synonyms understood
- **Usage ranking** — recipes sorted by what percentage of ingredients you have
- **Missing-ingredient warnings** — always see what you'd need to grab from the store
- **JSON mode** for integration with other tools
- **Threshold filtering** — only show recipes above a certain match quality
- **Stdlib only** — no pip installs, runs on any Python 3.6+

## How Matching Works

1. Your ingredients are **normalised** (lowercase, synonym resolution, singular/plural)
2. Each recipe ingredient is checked against your available set with **fuzzy string matching**
3. Recipes are scored: `usage_pct = (ingredients_you_have / total_ingredients) × 100`
4. Results sorted by usage percentage (descending), then by fewer missing items

## Recipe Database

The database (`scripts/recipes_db.json`) includes for each recipe:

- Name, ingredient list, time, difficulty, cuisine, servings
- Step-by-step cooking instructions

Recipes span from 5-minute smoothies to 2-hour beef stew, and from easy scrambled eggs to hard risotto and shepherd's pie.

## Files

| File | Description |
|------|-------------|
| `SKILL.md` | Skill definition and agent workflow |
| `scripts/leftover_chef.py` | Main matcher script |
| `scripts/recipes_db.json` | Recipe database (57 recipes) |
| `references/recipes.md` | Detailed cooking notes |
| `references/substitutions.md` | Common ingredient substitutions |

## License

MIT © Denis Voronin
