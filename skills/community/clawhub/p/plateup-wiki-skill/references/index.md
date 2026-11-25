# Reference Index

Records use English names or stable IDs as canonical identifiers. Follow the bilingual display rules in [SKILL.md](../SKILL.md) and use the glossary for translation status.

| User asks about | Read |
|---|---|
| A dish, ordered preparation steps and timing, variants, required tools | [recipes.yaml](recipes.yaml) |
| An ingredient and which dishes use it | [recipes.yaml](recipes.yaml) and [ingredients.yaml](ingredients.yaml) |
| Appliance function, cost when known, upgrade path, automation | [appliances.yaml](appliances.yaml) |
| Card effect, prerequisite, setting, Heat/Chill | [cards.yaml](cards.yaml) |
| Achievement unlock condition or strategy | [achievements.yaml](achievements.yaml) |
| Customer phase, patience duration, queue/weather modifier | [customers.yaml](customers.yaml) |
| Bilingual game term or preferred Chinese rendering | [terms.yaml](terms.yaml) |
| Field meanings and structured-data coverage limits | [data-schema.md](data-schema.md) |

## Data Conventions

- `id` and English names are canonical; Chinese names are presentation labels.
- `null` means not confirmed in the captured source. Do not substitute a guessed value.
- Source URLs and retrieval dates are recorded per file. For current-version rules, check the live wiki or release notes. When relying on the offline snapshot, state its date and version when recorded.
- Community-guide strategies are labeled as guide/player advice and should not be presented as official mechanics.
