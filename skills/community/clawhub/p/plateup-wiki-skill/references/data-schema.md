# Structured Data Schema

Use English names or stable IDs as canonical keys. Chinese names are display labels; consult [terms.yaml](terms.yaml) and preserve the distinction between `community` and `suggested` translations.

## Recipe records

`recipes.yaml` stores base recipes and nested variants/extras. Records use stable IDs, bilingual names, prerequisites, ingredients, equipment, and ordered preparation descriptions. Refer to `recipe-steps.yaml` for searchable step order, lexical action terms, and typed duration mentions. The prose in `recipes.yaml` remains the authoritative ordered procedure; do not infer missing inputs, outputs, or equipment from prose.

`recipe-steps.yaml` is a generated search index over those ordered step descriptions. `action_terms` are lexical matches and may include negated or descriptive mentions. `duration_mentions_seconds` preserves the extracted numeric list; `duration_details` aligns each value with a `role` and optional `label`. Roles include `cook_stage_increment`, `cook_duration`, `action_duration`, `burn_delay`, and `total_duration`; use `unknown` whenever wording is ambiguous. These records classify explicit time mentions only; they do not split compound prose into independently verified operations. Read `source_text` before giving a precise process answer.

## Appliance records

`appliances.yaml` separates upgrade paths, individual appliance records, general rules, and automation interactions. A name appearing in `catalog_by_category` only confirms catalog membership; it does not mean all properties are captured. Records may include verified cost, seats/capacity, quantity, modifiers, function, timing, burn behavior, interaction constraints, upgrade links, and `source_page`. Use `null` for unknown values.

Each appliance in the catalog has a bilingual display name. `attributes_status: name_only` marks entries with no collected mechanics; `partial_verified` means some fields have a source and other attributes may still be unknown. Do not treat null fields as appliance mechanics.

## Ingredient mappings

`ingredients.yaml` is an inverse index from ingredient to recipes. Treat recipe names as canonical English names and do not infer quantities or optionality from membership alone. Extras and serving equipment are recorded separately.

## Cards

`cards.yaml` groups cards by type. Distinguish prerequisite from `blocked_by`; repeated names require type and prerequisite as part of identity. Record numeric group, patience, money, and XP modifiers independently when supported by the source; retain prose `effect` as a readable summary.

## Achievements

`achievements.yaml` keeps English achievement names as keys. Separate unlock condition from strategy. Mark Steam guide observations as guide claims or player advice, and do not elevate them to verified wiki mechanics.

## Customer phases

`customers.yaml` records phase baselines, modifiers, queue rules, and pathing separately. Durations are seconds. Keep phase duration distinct from patience depletion speed; `Thinking` and `Eating` are not failure patience bars.

## Provenance

Each topic file should include source page(s), retrieval date, and game-version context. If a value is unavailable, use `null` and state what source was checked rather than filling it from intuition.
