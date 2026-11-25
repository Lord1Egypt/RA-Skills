# Structured Data Schema

Use English names or stable IDs as canonical keys. Chinese names are display labels; consult [terms.yaml](terms.yaml) and preserve the distinction between `community` and `suggested` translations.

## Recipe records

[recipes.yaml](recipes.yaml) stores `base_recipes` with nested `variants` and `extras`, plus `side_and_course_workflows`. Records use stable IDs and may include prerequisites, ingredients, equipment, common preparation in `base`, and ordered `steps`. Some nested entries have only a name and ID. Check the base recipe for shared steps or ingredients without assuming a variant keeps every ingredient. Read the steps to distinguish cooking times, extra time for a cooking stage, prep or portioning times, burn delays, and stated totals. Leave missing or ambiguous times unknown.

## Appliance records

[appliances.yaml](appliances.yaml) keeps blueprint upgrade edges in `upgrade_paths`. `linear` contains one-step routes without a cycle. `entry_points` lists the confirmed one-action results leading into multistep routes; `followup` contains the later transitions. `partially_documented_entries` records a route shown in the upgrade diagram but does not establish the full set of first outcomes. Stop at a repeated blueprint when describing a cycle. `cost` is the blueprint price when available; `free_at_run_start` is separate. A `patience_duration_multiplier` scales phase duration, not depletion speed.

`catalog_by_category` confirms catalog membership. `attributes_status: name_only` marks entries with no collected mechanics; `partial_verified` means some fields have a source and others may still be unknown. `null` is unknown.

## Ingredient mappings

Search `ingredients` on base recipes, variants, extras, and side or course workflows. Merge results with `additional_uses` in [ingredients.yaml](ingredients.yaml), whose lists point to stable recipe IDs, and deduplicate by ID. `wiki_only_uses` names uses without a local recipe record; `extras_and_equipment` records optional add-ons and serving equipment. A match by itself does not establish quantity, optionality, or required equipment; check the recipe steps and prerequisites.

## Cards

`cards.yaml` groups cards by type. Distinguish prerequisite from `blocked_by`; repeated names require type and prerequisite as part of identity. Record numeric group, patience, money, and XP modifiers independently when supported by the source; retain prose `effect` as a readable summary.

## Achievements

`achievements.yaml` keeps English achievement names as keys. Separate unlock condition from strategy. Mark Steam guide observations as guide claims or player advice, and do not elevate them to verified wiki mechanics.

## Customer phases

`customers.yaml` records phase baselines, modifiers, queue rules, and pathing separately. Durations are seconds. Keep phase duration distinct from patience depletion speed; `Thinking` and `Eating` are not failure patience bars.

## Provenance

Each topic file should include source page(s), retrieval date, and game-version context. If a value is unavailable, use `null` and state what source was checked rather than filling it from intuition.
