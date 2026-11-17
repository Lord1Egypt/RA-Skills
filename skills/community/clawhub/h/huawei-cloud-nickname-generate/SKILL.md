---
name: huawei-cloud-nickname-generate
description: |
  Randomly generate one nickname, or a de-duplicated batch, (随机昵称). A single call
  assembles each nickname from a built-in Chinese morpheme pool: a *pattern*
  (e.g. modifier + core) fixes the structure, an optional **style** (中性 / 文艺 / 可爱 /
  简约) filters every slot to morphemes carrying that style, and an optional **length**
  bucket (short / medium / long — 短 / 中 / 长) selects patterns whose character count
  fits the bucket. `--count` controls how many are returned (default 1, max 20) and the
  batch never repeats a name; `--seed` makes any run reproducible (auto-generated seeds
  are printed). Output is readable Markdown by default, with plain-text and JSON
  alternatives, and `--output` writes to a file. Implemented with the Python 3 standard
  library only; it does not call the Huawei Cloud CLI, any Huawei Cloud SDK, or any REST
  API, and it touches no cloud resource.
  Triggers include: "随机昵称", "生成昵称", "昵称生成", "起个昵称", "随机生成昵称",
  "取名字", "生成一批昵称", "nickname generate", "random nickname", "nickname generator",
  "generate a nickname", "batch nicknames".
tags: [devtools, nickname, generator, python, utility]
---

# Nickname Generator

## Overview

This skill produces **random nicknames (随机昵称)**. Each name is assembled from a
built-in pool of Chinese morphemes (`scripts/nickname_data.json`):

- A **pattern** fixes the structure — e.g. `core` (主体), `prefix + core`,
  `modifier + core` (修饰 + 主体), or `modifier + core + suffix` (主体 + 后缀).
- An overall **style** (中性 / 文艺 / 可爱 / 简约) can be forced; when given, every slot is
  filtered to morphemes that carry that style, so the result really fits the requested
  style whenever the pool has a matching morpheme.
- A **length** bucket (short / medium / long = 短 / 中 / 长) can be forced; each bucket
  selects the patterns whose total character count falls inside it.

- **One call → one nickname** by default; `--count N` returns a batch.
- **Batch is de-duplicated** — no name repeats within one run (a shortfall, if the pool
  is exhausted, is reported rather than silently repeating).
- **Reproducible** — passing `--seed` makes a run deterministic; when omitted, a random
  seed is chosen and printed so the run can be reproduced later.
- **Self-contained** — pure Python 3 standard library, no network, no credentials.
- **Demo content only** — output is a generated nickname suggestion, not a checked or
  registered handle; uniqueness/trademark/sensitive-word checks are out of scope.

## Prerequisites

- **Python 3.8+** available as `python3` (or `python`) on `PATH`.
- No Huawei Cloud credentials, CLI (KooCLI), SDK, or network access are needed; this
  skill is entirely local.
- `scripts/nickname_data.json` must be present (it ships with the skill) unless a custom
  pool is supplied with `--data`.

## Workflow

1. **Load the morpheme pool** — `load_data()` reads `scripts/nickname_data.json` and
   returns the `styles` list, the `lengths` buckets (each with its character-count range
   and pattern list), and the per-slot `parts` (`prefix` / `modifier` / `core` /
   `suffix`, each morpheme carrying its `name` and `styles`); `--data` may override it
   with a custom JSON file of the same shape.
2. **Resolve the frame** — `generate_nicknames(count, seed, style, length)` picks a style
   and a length bucket with `random.Random(seed)` when they are not given on the command
   line (marking their `*_source` as `random`), or normalizes the CLI values (aliases and
   case-insensitive matching; `*_source = cli`).
3. **Assemble each nickname** — a pattern is chosen for the bucket, and one morpheme per
   slot is drawn from the pool filtered by the chosen style. A slot with no strict style
   match is relaxed and recorded under `fallbacks`. The batch is de-duplicated.
4. **Render** — `render_markdown()` / `render_text()` / `render_json()` turn the result
   into readable output (Markdown by default).
5. **Emit** — the result goes to standard output, or to a file when `--output` is given.

## Core Commands

```bash
# Default: one Markdown nickname, reproducible with the given seed
python3 scripts/generate_nickname.py --seed 20240501

# A de-duplicated batch of 5, as JSON
python3 scripts/generate_nickname.py --seed 42 --count 5 --format json

# Force a style (aliases accepted, case-insensitive)
python3 scripts/generate_nickname.py --seed 7 --count 3 --style cute
python3 scripts/generate_nickname.py --seed 7 --style 文艺

# Force a length bucket (short / medium / long or 短 / 中 / 长)
python3 scripts/generate_nickname.py --seed 9 --style 文艺 --length 长 --count 3

# Plain text
python3 scripts/generate_nickname.py --seed 42 --count 2 --format text

# List the styles / length buckets the pool supports
python3 scripts/generate_nickname.py --list-styles
python3 scripts/generate_nickname.py --list-lengths

# Use a custom pool and write the result to a file
python3 scripts/generate_nickname.py --data /path/to/nickname_data.json --output nicknames.md

# Run the bundled unit tests
python3 -m unittest discover -s tests -v
```

The command-line entry point is `scripts/generate_nickname.py`; the built-in
`scripts/nickname_data.json` is what the examples above read by default.

## Parameter Confirmation

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| `--count` | No | Number of nicknames to generate; must be `1`–`20` | `1` |
| `--seed` | No | Integer seed for reproducible output | random (printed) |
| `--style` | No | Force a style: `中性` (neutral), `文艺` (artsy), `可爱` (cute), `简约` (minimal); aliases accepted | random |
| `--length` | No | Force a length bucket: `short` (短, 2–3 chars), `medium` (中, 4–6), `long` (长, 7–10) | random |
| `--format` | No | Output format: `markdown`, `text`, or `json` | `markdown` |
| `--data` | No | Path to a custom morpheme-pool JSON | `scripts/nickname_data.json` |
| `--output` | No | Write the result to a file instead of stdout | stdout |
| `--list-styles` | No | Print the available styles and exit | off |
| `--list-lengths` | No | Print the available length buckets and exit | off |

`--count` above the maximum (`20`) or below `1` is rejected with exit code `2`.

## Reference Documents

| Document | Description |
|----------|-------------|
| [references/usage-guide.md](references/usage-guide.md) | Command recipes, reproducibility rules, styles/length buckets, extending the pool |
| [references/verification-method.md](references/verification-method.md) | How the skill is verified (offline unit tests + spot checks) |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria and out-of-scope items |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/iam-policies.md](references/iam-policies.md) | Permission notes (none required) |

## Notes

- The generator is read-only with respect to the cloud: it reads only its local pool and
  writes only to standard output or a user-chosen `--output` file.
- The generated nickname is **sample/demo content**: a random suggestion, not a checked or
  registered handle (no uniqueness / trademark / sensitive-word validation).
- To expand the pool, add `{"name", "styles"}` entries to a slot array in
  `scripts/nickname_data.json`; keep at least one morpheme per style in every slot used by
  a pattern so a strict (unrelaxed) match stays possible. No code change is required.