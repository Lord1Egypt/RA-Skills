# Reference Index

All structured records use English item/card names as canonical identifiers. Follow the bilingual terminology rule in `SKILL.md`; translations marked suggested are not official localizations.

| User asks about | Read |
|---|---|
| A dish, cooking steps, variants, required tools | [recipes.yaml](recipes.yaml) |
| Recipe steps in ordered, searchable form with source text and classified time roles | [recipe-steps.yaml](recipe-steps.yaml) |
| An ingredient and which dishes use it | [ingredients.yaml](ingredients.yaml) |
| Appliance function, cost when known, upgrade path, automation | [appliances.yaml](appliances.yaml) |
| Card effect, prerequisite, setting, Heat/Chill | [cards.yaml](cards.yaml) |
| Achievement unlock condition or strategy | [achievements.yaml](achievements.yaml) |
| Customer phase, patience duration, queue/weather modifier | [customers.yaml](customers.yaml) |
| Bilingual game term or preferred Chinese rendering | [terms.yaml](terms.yaml) |
| Field meanings and structured-data coverage limits | [data-schema.md](data-schema.md) |

## Data Conventions

- `id` and English names are canonical; Chinese names are presentation labels.
- `null` means not confirmed in the captured source. Do not substitute a guessed value.
- Source URLs and retrieval dates are recorded per file. For current-version rules, check the live wiki/release notes.
- Community-guide strategies are labeled as guide/player advice and should not be presented as official mechanics.
