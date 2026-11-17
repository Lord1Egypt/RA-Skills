---
name: huawei-cloud-outfit-generate
description: |
  Randomly generate one outfit-of-the-day (今日穿搭). A single call picks an overall
  style and a season, then draws exactly one item per category — 上装 (top) / 下装
  (bottom) / 鞋履 (footwear) / 配饰 (accessory) — from a built-in wardrobe, so the look
  is a complete, coherent outfit. The style and season can be forced with --style /
  --season (they filter each category to matching items), output is readable Markdown
  by default with plain-text and JSON alternatives, and a --seed value makes any run
  reproducible. Implemented with the Python 3 standard library only; it does not call
  the Huawei Cloud CLI, any Huawei Cloud SDK, or any REST API, and it touches no cloud
  resource.
  Triggers include: "随机穿搭", "今日穿搭", "生成穿搭", "今天穿什么", "穿搭建议",
  "随机生成一套穿搭", "穿搭生成", "outfit generate", "random outfit", "outfit of the day",
  "daily outfit", "outfit generator", "generate an outfit".
tags: [devtools, outfit, generator, python, utility]
---

# Outfit Generator

## Overview

This skill produces **one random outfit-of-the-day** per invocation. An overall
**style** and a **season** are chosen first, then each category — 上装 / 下装 / 鞋履 /
配饰 — is filled with one item drawn from a built-in wardrobe (`scripts/wardrobe.json`).
Every item is tagged with the styles and seasons it suits, so the result is a complete,
readable look that actually respects the requested style / season.

- **One call → one outfit** — a single, self-contained 今日穿搭 covering all four
  categories.
- **Conditional** — `--style` and `--season` filter each category to matching items
  (relaxed gracefully, with a note, only when the wardrobe has no strict match).
- **Reproducible** — passing `--seed` makes a run deterministic; when omitted, a random
  seed is chosen and printed so the run can be reproduced later.
- **Self-contained** — pure Python 3 standard library, no network, no credentials.
- **Demo data only** — the wardrobe is bundled sample data; the output is a generated
  suggestion, not real merchandising data.

## Prerequisites

- **Python 3.8+** available as `python3` (or `python`) on `PATH`.
- No Huawei Cloud credentials, CLI (KooCLI), SDK, or network access are needed; this
  skill is entirely local.
- `scripts/wardrobe.json` must be present (it ships with the skill) unless a custom
  wardrobe is supplied with `--wardrobe`.

## Workflow

1. **Load the wardrobe** — `load_wardrobe()` reads `scripts/wardrobe.json` and returns
   the `styles` / `seasons` lists plus the per-category item pools (each item carries a
   `name`, its `styles`, and its `seasons`); `--wardrobe` may override it with a custom
   JSON file of the same shape.
2. **Choose the look's frame** — `pick_outfit(seed, style, season, wardrobe)` selects a
   style and a season with `random.Random(seed)` (or uses the values given on the
   command line, marking their `*_source` as `cli`).
3. **Fill each category** — for every category, items matching both the chosen style and
   season are preferred; the season constraint is relaxed first, then the style one, and
   any relaxation is recorded in `fallbacks`. One item is drawn from the resulting pool.
4. **Render** — `render_markdown()` / `render_text()` / `render_json()` turn the outfit
   into readable output (Markdown by default).
5. **Emit** — the result goes to standard output, or to a file when `--output` is given.

## Core Commands

```bash
# Default: one Markdown outfit, reproducible with the given seed
python3 scripts/generate_outfit.py --seed 20240501

# Plain text
python3 scripts/generate_outfit.py --seed 42 --format text

# JSON (machine-readable, for piping into other tools)
python3 scripts/generate_outfit.py --seed 42 --format json

# Force a style and a season (both accept aliases; see the usage guide)
python3 scripts/generate_outfit.py --seed 7 --style casual --season autumn

# Chinese labels work too
python3 scripts/generate_outfit.py --seed 7 --style 简约 --season 冬

# List the styles / seasons the wardrobe supports
python3 scripts/generate_outfit.py --list-styles
python3 scripts/generate_outfit.py --list-seasons

# Use a custom wardrobe and write the outfit to a file
python3 scripts/generate_outfit.py --wardrobe /path/to/wardrobe.json --output outfit.md

# Run the bundled unit tests
python3 -m unittest discover -s tests -v
```

The command-line entry point is `scripts/generate_outfit.py`; the built-in
`scripts/wardrobe.json` is what the examples above read by default.

## Parameter Confirmation

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| `--seed` | No | Integer seed for reproducible output | random (printed) |
| `--style` | No | Force the outfit style (`casual/休闲`, `commute/通勤`, `sport/运动`, `vintage/复古`, `minimal/简约`) | random |
| `--season` | No | Force the season to dress for (`spring/春`, `summer/夏`, `autumn/秋`, `winter/冬`) | random |
| `--format` | No | Output format: `markdown`, `text`, or `json` | `markdown` |
| `--wardrobe` | No | Path to a custom wardrobe JSON | `scripts/wardrobe.json` |
| `--output` | No | Write the outfit to a file instead of stdout | stdout |
| `--list-styles` | No | Print the available styles and exit | off |
| `--list-seasons` | No | Print the available seasons and exit | off |

## Reference Documents

| Document | Description |
|----------|-------------|
| [references/usage-guide.md](references/usage-guide.md) | Command recipes, reproducibility rules, styles/seasons, extending the wardrobe |
| [references/verification-method.md](references/verification-method.md) | How the skill is verified (offline unit tests + spot checks) |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria and out-of-scope items |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/iam-policies.md](references/iam-policies.md) | Permission notes (none required) |

## Notes

- The generator is read-only with respect to the cloud: it reads only its local wardrobe
  and writes only to standard output or a user-chosen `--output` file.
- The outfit is **sample/demo content**: a random styling suggestion, not real
  merchandising or sizing data.
- Output ordering is fixed: 上装 → 下装 → 鞋履 → 配饰.
- To expand the wardrobe, add `{"name", "styles", "seasons"}` entries to a category array
  in `scripts/wardrobe.json`; keep at least a couple of items per style and season so a
  strict (unrelaxed) match stays possible. No code change is required.