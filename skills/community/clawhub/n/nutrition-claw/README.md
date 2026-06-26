# nutrition-claw

A fully local, agent-friendly nutrition tracking CLI built for [openclaw](https://openclaw.ai) with [Bun](https://bun.sh) and TypeScript.

Track daily meals and ingredients, manage a personal food library, set nutrition goals, and search your history — all without sending a single byte to the cloud.

## Features

- **Meal & ingredient tracking** — log meals with multiple ingredients; totals are computed on the fly
- **Food library** — store nutrition data per unit (100g, 100ml, 1 tbsp, …) and auto-scale when logging
- **Goal tracking** — set daily targets (min/max) with instant feedback on every ingredient added
- **Semantic search** — find meals, ingredients, and foods by meaning using a local MiniLM model (no API key)
- **YAML output** — compact, human-readable, and easy to parse by agents
- **Fully offline** — all data lives in `~/.nutrition-claw/` as plain JSON files

## Installation

This package is published to [GitHub Packages](https://github.com/Pita/nutrition-claw/pkgs/npm/nutrition-claw). Install globally:

```bash
npm install -g @pita/nutrition-claw --registry=https://npm.pkg.github.com
```

Or configure npm once to always resolve the `@pita` scope from GitHub Packages:

```bash
echo "@pita:registry=https://npm.pkg.github.com" >> ~/.npmrc
npm install -g @pita/nutrition-claw
```

Then configure your goals (interactive wizard):

```bash
nutrition-claw configure
```

Or non-interactively (e.g. from an agent):

```bash
# Auto-calculated from body profile
nutrition-claw configure --sex male --age 30 --weight-kg 80 --height-cm 180 --activity moderate --goal lose --rate 0.5

# Manual
nutrition-claw configure --calories-kcal 2000 --protein-g 150 --carbs-g 250 --fiber-g 25 --fat-g 65
```

## Usage

```bash
nutrition-claw --help
```

All commands, flags, units, and examples are in the `--help` output. A quick overview:

| Command | What it does |
|---|---|
| `configure` | Set nutrition goals (interactive or non-interactive) |
| `goals get/set/delete` | Read or update individual goal values |
| `food add/get/list/update/delete/search` | Manage the reusable food library |
| `meal add/update/delete/list` | Log meals for a given date and time |
| `meal ingredient add/update/delete` | Add or adjust ingredients within a meal |
| `meal search` | Semantic search over meal names |
| `meal ingredient search` | Semantic search over ingredient names |
| `food search` | Semantic search over the food library |
| `summary` | Daily totals vs goals |
| `history` | Nutrient totals over a date range |

## Data

All data is stored locally in `~/.nutrition-claw/`:

```
~/.nutrition-claw/
  goals.json          # daily nutrition goals
  foods.json          # food library
  logs/               # one file per day (YYYY-MM-DD.json)
  vectors/            # local vector index for semantic search
```

The MiniLM embedding model is downloaded once on first search and cached locally.

## Requirements

- Node.js ≥ 18

> **Contributing / building from source:** [Bun](https://bun.sh) ≥ 1.0 is used to compile the TypeScript source (`npm run build`). It is not needed to run the installed package.

## License

MIT © Peter 'Pita' Martischka
