---
name: plateup-wiki-skill
description: Answer questions about PlateUp! / 速速上菜 gameplay, recipes, appliances, cards, automation, achievements, and terminology in Chinese or English.
---

# PlateUp Wiki Skill

Use this skill for PlateUp! / 速速上菜 game-mechanics questions, item and recipe lookups, automation planning, achievement help, and English-Chinese terminology.

## Answer Language and Terms

- Match the explanation language to the user's message: Chinese for Chinese prompts, English for English prompts.
- For English prompts, show game terms in English only. Do not append Chinese names unless the user asks for bilingual output or translation help.
- For Chinese prompts, use the Chinese glossary name alone when `terms.yaml` marks it as an established/community translation (`zh_status: community`).
- For a glossary entry marked `zh_status: suggested`, or for an item absent from the glossary, retain the English original and show a clearly marked suggestion in Chinese: `建议译名：中文（English Name）`. Never present a suggestion as an official localization.
- Preserve the English name or stable English ID in structured data and when disambiguating similarly named cards/items. Use the display rule above only in the natural-language answer.
- Keep explanations concise and practical. For planning questions, state assumptions such as recipe, day, setting, group sizes, player count, and available appliances when they affect the answer.

## Sources and Versioning

- Use [references/index.md](references/index.md) to route to the relevant structured data file. Load only the needed topic for ordinary lookups.
- Use [references/terms.yaml](references/terms.yaml) for bilingual names and translation status; use [references/data-schema.md](references/data-schema.md) when extending or interpreting structured records.
- Before rendering a named game term, look it up by English name or stable ID in `terms.yaml`; apply `zh_status` to decide whether to show an established Chinese name or a marked suggestion.
- Prefer the structured YAML references for exact item, prerequisite, value, step, or condition lookups.
- For current-version behavior, recent patches, exact numerical rules, or conflicts between sources, check the relevant PlateUp! Wiki page. Prefer official wiki/release notes for mechanics; use community guides for practical strategies and label them as player advice.
- When sources disagree or a rule is version-sensitive, say which source/version supports the answer and avoid silently combining incompatible rules.
- Attribute non-obvious claims to the relevant wiki page or community guide. Do not invent certainty where the source is incomplete.

## Coverage

The references cover recipe workflows, ingredient mappings, appliance properties and upgrade paths, card effects and prerequisites, achievement conditions, and customer phases/patience. Some values remain explicitly unknown where the wiki snapshot did not provide them; consult the live wiki rather than inferring missing statistics.
