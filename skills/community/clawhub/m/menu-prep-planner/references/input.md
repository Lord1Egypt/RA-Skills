# Offline helper contract

Python 3.11+ standard library, no network, writes, credentials or external actions. Resolve paths from the installed skill directory.

```sh
python3 scripts/menu.py assets/example.json
```

Run the command from this skill directory, or resolve both paths absolutely. For real use point to a private input JSON file. Reads only the explicitly supplied file and prints derived JSON; errors go to stderr with exit code 2. No output file is created and the source is unchanged. The included [example](../assets/example.json) is fictional.

Schema 1: target_servings is positive, recipes is a list of unique id/base_servings/ingredients. Optional recipe target_servings sizes a dish for a subset. Quantities are nonnegative decimal strings or integers, not binary floats or fractions; normalize '1/2' to '0.5' explicitly first. Unknown quantity = null, reported separately. Ingredient keys are ingredient_id + preparation + base unit. Preparation must encode distinctions such as chopped, whole, salted and required allergen-specific substitutions.

Units accepted: g, kg, ml, l, each, tsp_us, tbsp_us, cup_us. US volume conversions are explicit; 'cup', 'oz' and mass-to-volume conversion are rejected. Output in g/ml/each may contain fractional values; purchase rounding is a separate human-reviewed step. Ingredient sums use Decimal arithmetic, not a recipe safety validator.

Pantry is a list using the same ingredient/preparation/quantity/unit keys plus reserved (in the same unit). Available = stock minus reserved. Reservations above stock fail. Do not duplicate the same physical stock as multiple rows. Unknown stock is omitted, never assumed available.

bookings is a list of unique id/resource/start/end. Explicit-offset ISO timestamps are mandatory; each resource represents one exclusive resource. Intervals are half-open: an end exactly at another start doesn't conflict. Different-resource and multi-temperature feasibility still need planning review. No IANA/DST validation or cooking-time optimization is performed.

Expected example: flour required 500 g, available 300 g, buy 200 g; salt unquantified; oven conflict reported. Output excludes arbitrary recipe/pantry metadata but is a private planning report, not guest-safe content certification.
