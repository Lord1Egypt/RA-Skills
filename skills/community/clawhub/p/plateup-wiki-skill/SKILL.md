---
name: plateup-wiki-skill
description: Answer questions about PlateUp! / 速速上菜 gameplay, recipes, appliances, cards, automation, achievements, and terminology in Chinese or English.
---

# PlateUp Wiki Skill

Use this skill for PlateUp! / 速速上菜 game-mechanics questions, item and recipe lookups, automation planning, achievement help, and English-Chinese terminology.

## Answer Language and Terms

- Match the language of the question itself. A Chinese question containing English game names still gets a Chinese answer. Follow explicit requests for a particular language, bilingual output, or translation.
- Look up names in [terms.yaml](references/terms.yaml) by Chinese name, alias, English name, or stable ID. Resolve shared names using the question's context and term category, then match the topic record by canonical name or ID. Ask a short clarification if multiple matches remain.
- In English answers, show only English game names by default. In Chinese answers, use only the Chinese glossary name when `zh_status` is `community`. If it is `suggested` or the term is missing, keep the English original and show `建议译名：中文（English Name）`, proposing a Chinese name if needed. A suggestion is not official localization.
- Use the glossary for display names and translation status; the topic files' `zh` fields are lookup hints. Keep English names and IDs as data keys.
- Keep explanations concise and practical. For planning questions, state assumptions such as recipe, day, setting, group sizes, player count, and available appliances when they affect the answer.

## References

Resolve these links relative to this `SKILL.md` and read only the files relevant to the question:

- [recipes.yaml](references/recipes.yaml): read `base` and `steps` on the relevant recipe and its nested records, or use `side_and_course_workflows`. Distinguish cooking, prep or portioning, time before burning, and any explicitly stated total. Check the base recipe when an extra changes only part of the workflow.
- [ingredients.yaml](references/ingredients.yaml): find matches in the recipe records' `ingredients`, then add `additional_uses` by recipe ID and deduplicate. List `wiki_only_uses` separately when relevant. Distinguish required ingredients, optional additions, and serving equipment; verify optionality in the steps.
- [appliances.yaml](references/appliances.yaml): appliance properties, automation, and `upgrade_paths`. Separate possible outcomes of one research action from later steps; mark a cycle at the first repeated node. `partially_documented_entries` shows one documented route without establishing all possible first outcomes. Distinguish blueprint prices from equipment supplied at the start, and patience duration from depletion rate.
- [cards.yaml](references/cards.yaml): card effects, prerequisites, and blockers.
- [achievements.yaml](references/achievements.yaml): unlock conditions and community guide advice.
- [customers.yaml](references/customers.yaml): customer phases, patience, queue rules, and modifiers.
- [index.md](references/index.md) and [data-schema.md](references/data-schema.md): topic index and field conventions.

## Sources and Versioning

- Use the local records for the documented version. For current behavior, recent patches, missing values, or conflicts between sources, check the relevant PlateUp! Wiki page or official release notes if available. Label community strategies as player advice.
- For offline answers, identify the relevant local snapshot by date and game version when recorded. If sources disagree, say which source/version supports each claim. Attribute non-obvious claims and leave unconfirmed values unknown.
