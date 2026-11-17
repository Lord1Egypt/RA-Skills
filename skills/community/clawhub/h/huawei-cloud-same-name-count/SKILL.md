---
name: huawei-cloud-same-name-count
description: |
  Query same-name population counts (同名人数 / 重名查询). Given a name, a single
  call returns how many people share that name in a bundled, reproducible sample
  dataset; the result can be narrowed with --gender and/or --province and is then
  broken down by gender and province. When nothing matches, an explicit message is
  printed — the query never fails silently. Output is readable Markdown by default,
  with plain-text and JSON alternatives. Implemented with the Python 3 standard
  library only; it does not call the Huawei Cloud CLI, any Huawei Cloud SDK, or any
  REST API, and it touches no cloud resource.
  Triggers include: "查询同名人数", "同名同姓查询", "姓名重名", "重名查询",
  "同名查询", "查同名", "同名人数", "same name count", "name duplicate count",
  "count same name", "how many people share this name".
tags: [devtools, same-name, count, query, utility]
---

# Same-Name Count Query

## Overview

This skill answers the question **"how many people share this name?"** for a given
name. A single call reads a bundled, **reproducible** sample dataset
(`scripts/data.json`, sample/demo data) and returns:

- **同名人数合计 (total)** — the number of people with that name.
- **可选分维度统计 (optional breakdown)** — the same total split **by gender** and
  **by province**.

`--name` is required; `--gender` (男/女) and `--province` are optional filters. When
they are supplied, both the total and every breakdown count cover **only** the
matching records.

- **One call → one answer** — a self-contained same-name count for the given name.
- **Filterable** — `--gender` / `--province` narrow the query; breakdowns are always
  reported for the matched records.
- **Never silent** — a name that is absent from the dataset, or a filter that
  excludes every record, returns an explicit message (Markdown/text print it; JSON
  carries it in `message` with `matched=false`).
- **Self-contained** — pure Python 3 standard library, no network, no credentials.
- **Demo data only** — the dataset is a bundled sample fixture for a reproducible
  offline demo, not an authoritative population register; it can be replaced with
  `--data`.

## Prerequisites

- **Python 3.8+** available as `python3` (or `python`) on `PATH`.
- No Huawei Cloud credentials, CLI (KooCLI), SDK, or network access are needed; this
  skill is entirely local.
- `scripts/data.json` must be present (it ships with the skill) unless a custom
  dataset is supplied with `--data`.

## Workflow

1. **Load the dataset** — `load_data()` reads `scripts/data.json` and returns the
   `genders` / `provinces` lists plus the `records` (each `{"name", "gender",
   "province", "count"}`); `--data` may override it with a custom JSON file of the
   same shape.
2. **Normalize the filters** — `normalize_gender()` / `normalize_province()` map a
   label or alias (e.g. `male` → 男, `广东省` → 广东) to a canonical value; an unknown
   value is rejected with exit code `2`.
3. **Query and aggregate** — `query(name, gender, province, data)` keeps the records
   whose name (and gender/province) match, sums their `count` into a total, and builds
   the by-gender / by-province breakdowns. When nothing matches, it returns
   `matched=false` plus an explicit `message` (and, when the name exists but the filter
   excluded all rows, the dimensions the name does have).
4. **Render** — `render_markdown()` / `render_text()` / `render_json()` turn the result
   into readable output (Markdown by default).
5. **Emit** — the result goes to standard output, or to a file when `--output` is given.

## Core Commands

```bash
# Default: same-name count for one name (Markdown)
python3 scripts/query.py --name 张伟

# Narrow by gender and/or province
python3 scripts/query.py --name 张伟 --gender 男
python3 scripts/query.py --name 李娜 --province 广东

# JSON (machine-readable, for piping into other tools)
python3 scripts/query.py --name 刘洋 --format json

# Aliases and case-insensitivity
python3 scripts/query.py --name 王伟 --gender male
python3 scripts/query.py --name 王伟 --province 广东省

# Discover what the dataset supports
python3 scripts/query.py --list-provinces
python3 scripts/query.py --list-genders

# Use a custom dataset and write the result to a file
python3 scripts/query.py --name 张伟 --data /path/to/dataset.json --output result.md

# A name with no record prints an explicit no-result message (exit 0)
python3 scripts/query.py --name 不存在的名字

# Run the bundled unit tests
python3 -m unittest discover -s tests -v
```

The command-line entry point is `scripts/query.py`; the built-in
`scripts/data.json` is what the examples above read by default.

## Parameter Confirmation

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| `--name` | Yes* | Name to look up (*required unless `--list-*` is used) | — |
| `--gender` | No | Filter by gender (`男`/`女`, or `male`/`female`) | all |
| `--province` | No | Filter by province (`广东`, `广东省`, …) | all |
| `--format` | No | Output format: `markdown`, `text`, or `json` | `markdown` |
| `--data` | No | Path to a custom dataset JSON | `scripts/data.json` |
| `--output` | No | Write the result to a file instead of stdout | stdout |
| `--list-provinces` | No | Print the supported provinces and exit | off |
| `--list-genders` | No | Print the supported genders and exit | off |

## Reference Documents

| Document | Description |
|----------|-------------|
| [references/usage-guide.md](references/usage-guide.md) | Command recipes, filter rules, no-result behaviour, extending the dataset |
| [references/verification-method.md](references/verification-method.md) | How the skill is verified (offline unit tests + spot checks) |
| [references/acceptance-criteria.md](references/acceptance-criteria.md) | Acceptance criteria and out-of-scope items |
| [references/dataflow-diagram.md](references/dataflow-diagram.md) | Mermaid data flow diagram |
| [references/iam-policies.md](references/iam-policies.md) | Permission notes (none required) |

## Notes

- The query is read-only with respect to the cloud: it reads only its local dataset and
  writes only to standard output or a user-chosen `--output` file.
- The counts are **sample/demo figures** from a bundled fixture; they are not an
  authoritative population register and must not be presented as official statistics.
- A query that returns no match is a **valid, explicit result** (exit code `0`): the
  message states whether the name is absent or the filter excluded every record.
- To expand coverage, add `{"name", "gender", "province", "count"}` entries to the
  `records` array in `scripts/data.json` (and list any new province in `provinces`). No
  code change is required.