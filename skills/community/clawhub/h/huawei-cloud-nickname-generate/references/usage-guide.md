# Usage Guide

## Quick start

```bash
python3 scripts/generate_nickname.py --seed 20240501
```

Prints one Markdown nickname assembled from a random style and length bucket to stdout.

## Common variations

```bash
# Plain text
python3 scripts/generate_nickname.py --seed 42 --count 2 --format text

# JSON (machine-readable, for piping into other tools)
python3 scripts/generate_nickname.py --seed 42 --count 5 --format json

# Force a style (aliases accepted, case-insensitive)
python3 scripts/generate_nickname.py --style cute
python3 scripts/generate_nickname.py --style 文艺

# Force a length bucket
python3 scripts/generate_nickname.py --style 文艺 --length 长
python3 scripts/generate_nickname.py --length short

# A batch of ten, reproducible
python3 scripts/generate_nickname.py --seed 7 --count 10

# See what the pool supports
python3 scripts/generate_nickname.py --list-styles
python3 scripts/generate_nickname.py --list-lengths

# Write to a file
python3 scripts/generate_nickname.py --seed 7 --count 5 --output nicknames.md
```

## Styles and length buckets

The built-in pool is tagged with four styles and three length buckets:

- Styles: `中性` (neutral), `文艺` (artsy/literary), `可爱` (cute), `简约` (minimal).
- Length buckets (character count of the assembled nickname):
  - `short` (短): 2–3 characters, patterns `core` and `prefix + core`.
  - `medium` (中): 4–6 characters, patterns `modifier + core`, `prefix + modifier + core`,
    `modifier + core + suffix`.
  - `long` (长): 7–10 characters, patterns `prefix + modifier + core + suffix`,
    `modifier + modifier + core + suffix`, `prefix + modifier + modifier + core + suffix`.

`--style` and `--length` accept either the Chinese label or an ASCII alias; matching is
case-insensitive. An unknown value is rejected with exit code `2` and a message listing
the valid choices.

## Slots and patterns

Each nickname is a concatenation of morphemes drawn from these slots:

| Slot | Label | Character width | Examples |
|------|-------|-----------------|----------|
| `prefix` | 前缀 | 1 | 小, 阿, 星, 甜, 青 |
| `modifier` | 修饰 | 2 | 薄荷, 星河, 软糖, 极简 |
| `core` | 主体 | 2 | 小猫, 鲸鱼, 星辰, 岛屿 |
| `suffix` | 后缀 | 2 | 同学, 酱酱, 骑士, 一梦 |

A **pattern** is an ordered list of slots (e.g. `["modifier", "core", "suffix"]`). The
pattern chosen fixes the nickname length, which is why length filtering is deterministic.

## Filtering behaviour

When a style is given, each slot is filtered to morphemes that carry that style. If a slot
has no morpheme for the requested style, that slot is relaxed (any morpheme is allowed) and
the affected nickname is recorded under `fallbacks` (`strict=false` in JSON). With the
built-in pool every style covers every slot, so a strict (unrelaxed) match is always
possible; relaxation only matters with a custom, narrower pool.

## Reproducibility

- Passing `--seed <int>` makes the output deterministic: the same seed, style and length
  always produce the same nicknames.
- Omitting `--seed` still works; the generator picks a random seed and prints it
  (`Seed: <n>` when writing to a file, `随机 seed <n>` in the body), so the run can be
  reproduced later with `--seed <n>`.

## Extending the pool

`scripts/nickname_data.json` holds the morpheme pools and the length/pattern table. Add
`{"name", "styles"}` entries to a slot array; keep at least one morpheme per style in every
slot used by a pattern so a strict match stays possible. To add a new length bucket, add an
entry under `lengths` with `label`, `min`, `max`, and one or more `patterns`. No code change
is required. A completely different pool can be supplied with `--data /path/to/data.json`,
which uses the same shape.