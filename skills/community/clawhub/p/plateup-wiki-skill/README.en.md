# PlateUp Wiki Skill

PlateUp Wiki Skill is a reference skill for **PlateUp!**, covering recipes, appliances, automation, cards, achievements, customer rules, and game terminology.

[中文说明](README.md)

## Features

- Chinese and English question support
- Recipes, variants, ingredients, and preparation steps
- Appliance properties, upgrade paths, and automation interactions
- Card effects, prerequisites, and achievement conditions
- Customer phases, patience rules, and queue mechanics
- Bilingual terminology with suggested translations for missing Chinese names
- Source and game-version tracking

## Language Rules

- Answers default to the language of the question. Explicit requests for another language, bilingual names, or translation take precedence.
- English answers use English game names only by default.
- Chinese answers use only the established Chinese name (`zh_status: community`) when one exists. Missing or suggested translations use `建议译名：中文（English Name）` and are never presented as official localizations.

## Repository Layout

```text
plateup-wiki-skill/
├── SKILL.md                  # Skill instructions
├── agents/openai.yaml         # Optional UI metadata
└── references/
    ├── index.md               # Query routing
    ├── recipes.yaml           # Recipes, variants, and preparation steps
    ├── appliances.yaml        # Appliances and automation
    ├── ingredients.yaml       # Supplemental ingredient mappings
    ├── cards.yaml             # Cards
    ├── achievements.yaml      # Achievements
    ├── customers.yaml         # Customer phases
    ├── terms.yaml             # Bilingual glossary
    └── data-schema.md         # Data conventions
```

## Installation for OpenClaw

Install from GitHub into your current OpenClaw workspace:

```bash
openclaw skills install git:syh31/plateup-wiki-skill@main
```

To invoke the skill explicitly in chat, use `$plateup-wiki-skill`, for example `$plateup-wiki-skill How do I make pizza?`.

## Installation for Hermes Agent

From the root of your local checkout, copy `SKILL.md` and `references/` into the default Hermes skill directory:

```bash
mkdir -p ~/.hermes/skills/plateup-wiki-skill/references
cp SKILL.md ~/.hermes/skills/plateup-wiki-skill/
cp -R references/. ~/.hermes/skills/plateup-wiki-skill/references/
hermes skills list
```

Once the skill appears in the list, enter `/plateup-wiki-skill How do I make pizza?` in Hermes chat. For a custom profile path, see the [Hermes skills documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills).

## ClawHub

To publish using [ClawHub's GitHub importer](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md#github-import), select a public repository you own that is not a fork. In the preview, check that the package includes the root `SKILL.md` and the `references/` directory.

ClawHub publishes skills under [MIT-0](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md#license). Before publishing, make sure you have the right to distribute the included material under that license. A link to the wiki or a community source does not grant redistribution rights.

## Data Sources

- [PlateUp! Official Wiki](https://wiki.plateupgame.com/)
- [PlateUp! Official Updates](https://www.plateupgame.com/updates/)
- [Bilibili terminology reference](https://www.bilibili.com/opus/709028087756488743)
- [Steam community achievement guide](https://steamcommunity.com/sharedfiles/filedetails/?id=3267294764)

Official Wiki and release notes are preferred for mechanics. Community sources are retained for translations, achievement guidance, or practical strategies and are labeled accordingly.

## Data Policy

- English names and stable IDs are canonical.
- `null` means that no verified value was collected.
- Unknown values are not filled by guesswork.
- Look up ingredients in the [recipe data](references/recipes.yaml) first, then use the [ingredient mappings](references/ingredients.yaml) for additional matches.
- `name_only` entries contain names without normalized mechanics.

## Status

This is a community-maintained reference skill and is not affiliated with or endorsed by PlateUp! or its developers.
