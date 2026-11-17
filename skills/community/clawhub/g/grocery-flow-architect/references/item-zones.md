# Item→Zone Matcher Data & Extension Rules

The canonical table embedded in `grocery_flow.py` (`ITEM_ZONES`). Zones are
conventional grocery-store departments; your store map decides which of
them exist for you and in what order.

## Canonical zones (16)

produce, bakery, deli, dairy, meat, seafood, frozen, pantry, breakfast,
beverages, snacks, household, health, baby, pet, floral

## Matching pipeline (in order)

1. **Learned items win.** Anything you answered manually for this store is
   stored in the store JSON and matched first, forever.
2. **Prefix conventions.** `frozen X` → frozen, `canned/jarred/bottled/dried
   X` → pantry, `fresh X` → produce — BEFORE any other rule. So "frozen
   peas" is frozen even though "peas" alone is produce.
3. **Exact + hyphen/space variants.** `ice cream` ↔ `ice-cream`.
4. **Head-noun rule.** Multi-word unknowns match their last word:
   "cherry tomatoes" → tomatoes → produce; "dish soap" → soap → health.
5. **Substring scan (last resort).** Only words longer than 3 chars.

## Normalization

- lowercase, punctuation stripped
- plural → singular (tomatoes→tomato, berries→berry, loaves→loaf via
  the -ies/-es/-s rules in `norm_item`)
- multiple spaces collapsed

## Extending the table

Add items to the zone blobs in `ITEM_ZONES` — lowercase, hyphenated
multi-word items, one entry per synonym. Rules of thumb:

- Add the form YOU write in lists ("greek yogurt", not "yogurt, greek
  style")
- Regional names belong in the blob too (courgette alongside zucchini,
  aubergine alongside eggplant, coriander alongside cilantro)
- Brand names usually fail the matcher — put `[zone]` hints in the list
  line instead: `fairlife milk [dairy]`

## Aliases

`ZONE_ALIASES` rewrites canonical zones to common store-zone names
(vegetables→produce, freezer→frozen, paper-goods→household...). Extend
when your store calls a zone something the matcher doesn't know.

## When the matcher asks

The `route` command asks interactively (in a TTY) for unplaced items and
persists the answer in that store's `learned` map. Non-interactive runs
(pipes, cron) print an `[?? unplaced]` section instead — re-run
interactively once to teach those items.

## Known limits

- Same item, different zone per store (eggs: dairy aisle vs. dairy case
  by bakery in some EU shops) — that's why learning is per-store.
- Loose produce vs. packaged: some stores split. If yours does, make
  them two zones in your map ("produce-bulk", "produce-packed").
- The matcher never overrides your zone ORDER; it only assigns items to
  zones that exist in your map. An item whose zone isn't in your store
  stays unplaced (correct: you don't know where your store hides it).
