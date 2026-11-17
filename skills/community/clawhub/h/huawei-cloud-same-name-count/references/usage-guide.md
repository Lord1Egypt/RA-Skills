# Usage Guide

## Quick start

```bash
python3 scripts/query.py --name 张伟
```

Prints the same-name count for `张伟` plus a by-gender / by-province breakdown as
Markdown.

## Common variations

```bash
# Narrow by gender
python3 scripts/query.py --name 张伟 --gender 男
python3 scripts/query.py --name 刘洋 --gender female   # alias, case-insensitive

# Narrow by province
python3 scripts/query.py --name 李娜 --province 广东
python3 scripts/query.py --name 李娜 --province 广东省  # trailing 省 handled

# Both filters
python3 scripts/query.py --name 李娜 --gender 女 --province 四川

# JSON (machine-readable, for piping into other tools)
python3 scripts/query.py --name 刘洋 --format json

# See what the dataset supports
python3 scripts/query.py --list-genders
python3 scripts/query.py --list-provinces

# Write to a file
python3 scripts/query.py --name 张伟 --output result.md
```

## Filters

- `--gender` accepts `男` / `女` (or the aliases `male` / `female`); matching is
  case-insensitive. An unknown value is rejected with exit code `2`.
- `--province` accepts the canonical province (e.g. `广东`) or a common alias /
  prefixed form (e.g. `广东省`). An unknown value is rejected with exit code `2`.
- The total and every breakdown count cover **only** the records that satisfy all
  supplied filters.

## No-result behaviour

A query that matches nothing is a **valid result**, not an error — the tool always
prints an explicit message (exit code `0`):

- The name is absent from the dataset:
  `未找到姓名「X」的同名记录：数据集中没有该姓名。`
- The name exists but the filter excluded every record:
  `未找到满足条件的记录：姓名「X」在数据集中存在，但没有 性别=女 的数据。` plus the
  dimensions the name does have.

In `--format json`, the same information is carried in `matched` (`false`) and
`message`, so scripts can branch without parsing prose.

## Reproducibility

The dataset (`scripts/data.json`) is a fixed fixture, so the same name + filters
always produce the same counts. Replace it with `--data /path/to/dataset.json`
(same shape) to use your own numbers.

## Extending the dataset

`scripts/data.json` holds `records` (`{"name", "gender", "province", "count"}`),
plus the `genders` / `provinces` lists. Add records (and list any new province in
`provinces`) to widen coverage; no code change is required.

> The bundled counts are **sample/demo figures**, not an authoritative population
> register.