# PlateUp Wiki Skill

PlateUp Wiki Skill is an OpenClaw skill for **PlateUp!**, covering recipes, appliances, automation, cards, achievements, customer rules, and game terminology.

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

For English questions, the skill displays English game names only. For Chinese questions, established glossary translations are shown as Chinese only. Missing or suggested translations are shown as `建议译名：中文（English Name）` and are never presented as official localizations.

## Repository Layout

```text
plateup-wiki-skill/
├── SKILL.md                  # Skill instructions
├── agents/openai.yaml         # Optional UI metadata
└── references/
    ├── index.md               # Query routing
    ├── recipes.yaml           # Recipes and variants
    ├── recipe-steps.yaml      # Ordered step index
    ├── appliances.yaml        # Appliances and automation
    ├── ingredients.yaml       # Ingredient mappings
    ├── cards.yaml             # Cards
    ├── achievements.yaml      # Achievements
    ├── customers.yaml         # Customer phases
    ├── terms.yaml             # Bilingual glossary
    └── data-schema.md         # Data conventions
```

## Installation for OpenClaw

Copy or symlink this directory to an OpenClaw skill directory:

```bash
cp -R plateup-wiki-skill ~/.openclaw/skills/plateup-wiki-skill
```

After installation, invoke it explicitly with `$plateup-wiki-skill`, or let OpenClaw select it automatically for relevant PlateUp! questions.

## ClawHub

The repository root is ready to be packaged as a ClawHub skill. Keep `SKILL.md` at the package root and include the `references/` directory when publishing.

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
- Recipe prose remains available for traceability.
- `name_only` entries contain names without normalized mechanics.

## Status

This is a community-maintained reference skill and is not affiliated with or endorsed by PlateUp! or its developers.
