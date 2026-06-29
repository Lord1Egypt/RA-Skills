# MaybeAI Sheet CLI Plan

## Recommendation

Yes, a CLI is worth adding for the highest-frequency operations, especially:

- `workbook_manifest`
- `read_sheet`
- `read_headers`
- `list_worksheets`
- `append_rows`
- `update_range_by_lookup`
- `update_range`
- `clear_range`
- `write_new_worksheet`
- `formula_set`
- `formula_batch_set`
- `recalculate_formulas`
- `workbook_profile`
- `export`

It is **not** a good replacement for the entire API surface. The repo already shows a large endpoint set, so the right design is:

1. First-class commands for the common workflows
2. Stable shared flags for auth, workbook, and worksheet targeting
3. A generic `api` or `raw` command for less-used endpoints

That keeps the CLI small enough to publish and maintain.

## Why a CLI Helps

For common sheet work, the current `curl` scripts have three recurring costs:

- repeated auth and base URL boilerplate
- repeated `uri` and `gid` handling
- repeated JSON escaping for structured payloads

A CLI improves:

- usability for humans
- repeatability in scripts and CI
- discoverability through `--help`
- safer worksheet targeting through shared options

## Product Scope

Package name candidates:

- `maybeai-sheet`
- `maybeai-sheets`
- `maybe-sheet`

Recommended executable:

```bash
maybeai-sheet
```

Recommended Python baseline:

- Python `>=3.10`

Recommended implementation:

- `typer` for CLI
- `httpx` for HTTP client
- `pydantic` for payload validation
- `rich` for readable table / JSON output

## CLI Shape

```bash
maybeai-sheet [global options] <resource> <command> [command options]
```

Shared options (root, resource group, or leaf command):

- `--token` or env `MAYBEAI_API_TOKEN`
- `--base-url` default `https://play-be.omnimcp.ai`
- `--doc-id`
- `--url`
- `--uri`
- `--gid`
- `--worksheet-name`
- `--output json|table|yaml`
- `--verbose`
- `--timeout`

Examples of valid flag placement:

```bash
maybeai-sheet --doc-id <id> --output table sheet read --gid 3
maybeai-sheet sheet --doc-id <id> --gid 3 read --output table
maybeai-sheet sheet read --doc-id <id> --gid 3 --output table
```

A leaf subcommand is always required (`read`, `headers`, `worksheets`, …).

Resolution rules:

1. If `--uri` is provided, use it
2. Else if `--doc-id` is provided, build `https://www.maybe.ai/docs/spreadsheets/d/<doc_id>`
3. If `--gid` is provided, append `?gid=<gid>` where required
4. Prefer `--worksheet-name` for commands that support it

## Proposed Commands

### Read path

```bash
maybeai-sheet sheet read --doc-id <id> --worksheet-name Sheet1
maybeai-sheet sheet read --doc-id <id> --worksheet-name Sheet1 --range A1:C20
maybeai-sheet sheet read-many --doc-id <id> --targets targets.json
maybeai-sheet sheet named-range --doc-id <id> --name RevenueBlock
maybeai-sheet sheet headers --doc-id <id> --gid 0
maybeai-sheet sheet worksheets --doc-id <id>
maybeai-sheet sheet profile --doc-id <id> --force-refresh
```

### Write path

```bash
maybeai-sheet sheet append --doc-id <id> --gid 0 --rows rows.json
maybeai-sheet sheet upsert --doc-id <id> --gid 0 --key OrderID --rows rows.json
maybeai-sheet sheet write-range --doc-id <id> --worksheet-name Sheet1 --range A1:C3 --values values.json
maybeai-sheet sheet clear-range --doc-id <id> --worksheet-name Sheet1 --range A1:C3
maybeai-sheet sheet create-worksheet --doc-id <id> --name Summary --values values.json
maybeai-sheet sheet formula-set --doc-id <id> --worksheet-name Sheet1 --cell E2 --formula '=SUM(B2:D2)'
maybeai-sheet sheet formula-batch-set --doc-id <id> --operations ops.json --recalculate-mode worksheet
maybeai-sheet sheet recalculate --doc-id <id> --worksheet-name Sheet1
```

### File path

```bash
maybeai-sheet file upload ./report.xlsx
maybeai-sheet file export --doc-id <id> --out final.xlsx
maybeai-sheet file search "q2 forecast"
```

### Escape hatch

```bash
maybeai-sheet raw post /api/v3/excel/range/read --body body.json
```

The `raw` command prevents CLI growth from tracking every niche endpoint.

## Command Mapping

| CLI command | API endpoint |
|---|---|
| `workbook manifest` | `POST /api/v3/excel/workbook/manifest` |
| `workbook capabilities` | `POST /api/v3/excel/workbook/capabilities` |
| `sheet read` | `POST /api/v3/excel/range/read` |
| `sheet read-range` | `POST /api/v3/excel/range/read` |
| `sheet read-many` | `POST /api/v3/excel/range/read_many` |
| `sheet named-range` | `POST /api/v3/excel/named_range/read` |
| `sheet headers` | `POST /api/v3/excel/table/headers` |
| `sheet worksheets` | `POST /api/v3/excel/worksheet/list` |
| `sheet formulas` | `POST /api/v3/excel/formula/read` |
| `sheet append` | `POST /api/v3/excel/table/append_rows` |
| `sheet upsert` | `POST /api/v3/excel/table/upsert_rows` |
| `sheet write-range` | `POST /api/v3/excel/range/write` |
| `sheet clear-range` | `POST /api/v3/excel/range/clear` |
| `sheet create-worksheet` | `POST /api/v3/excel/worksheet/create` |
| `sheet formula-set` | `POST /api/v3/excel/formula/set` |
| `sheet formula-batch-set` | `POST /api/v3/excel/formula/batch_set` |
| `sheet recalculate` | `POST /api/v3/excel/formula/recalculate` |
| `sheet profile` | `POST /api/v1/excel/workbook_profile` |
| `file upload` | `POST /api/v1/excel/upload` |
| `file export` | `GET /api/v1/excel/export/{document_id}` |

## UX Rules

The CLI should encode the operational rules already documented in this repo:

1. Warn when neither `--worksheet-name` nor `--gid` is provided for worksheet-sensitive commands
2. Prefer `workbook manifest` before read/write commands when the target worksheet is not already known
3. Prefer `--worksheet-name` for `sheet read`, `sheet write-range`, and `sheet formula-set`
4. Prefer `--gid` for `sheet headers`, `sheet append`, and `sheet upsert`
5. Support `--verify` on write commands to automatically read back after write
6. Support `--dry-run` where payload generation can be previewed safely

Example:

```bash
maybeai-sheet sheet upsert \
  --doc-id $DOC_ID \
  --gid 0 \
  --key OrderID \
  --rows sales.json \
  --verify
```

## Suggested Package Layout

```text
src/maybeai_sheet/
  __init__.py
  cli.py
  config.py
  client.py
  models.py
  formatters.py
  commands/
    file.py
    sheet.py
    raw.py
tests/
pyproject.toml
README.md
```

## `pyproject.toml` Direction

Use a console script entry point:

```toml
[project]
name = "maybeai-sheet"
version = "0.1.0"
description = "CLI for common MaybeAI spreadsheet operations"
requires-python = ">=3.10"
dependencies = ["typer", "httpx", "pydantic", "rich"]

[project.scripts]
maybeai-sheet = "maybeai_sheet.cli:app"
```

Build backend:

- `hatchling` or `setuptools`

Recommended:

- `hatchling`

## Publish-to-PyPI Plan

### Phase 1

Build a thin MVP around the most-used read/write flows:

- `workbook manifest`
- `sheet read`
- `sheet headers`
- `sheet worksheets`
- `sheet append`
- `sheet upsert`
- `sheet write-range`
- `sheet clear-range`
- `sheet create-worksheet`
- `sheet formula-set`
- `sheet formula-batch-set`
- `sheet recalculate`
- `file upload`
- `file export`

### Phase 2

Add operator-safety and better UX:

- `--verify`
- `--output table`
- better error messages for auth and wrong-sheet targeting
- `sheet profile`

### Phase 3

Publish:

1. reserve package name on PyPI
2. add `pyproject.toml`
3. add README with install and auth setup
4. add tests for request construction
5. build with `python -m build`
6. publish with `twine upload dist/*` or trusted publishing

## What Not To Do

- Do not create one CLI command per endpoint on day one
- Do not force users to hand-build JSON strings for common commands
- Do not hide worksheet targeting semantics
- Do not publish before adding at least smoke tests for the common commands

## Bottom Line

Yes, a pip-published CLI is a good fit here, but only if it is opinionated around the top workflows and does not try to mirror the full backend surface.

The first command to optimize is `read_sheet`, followed by the table-safe write commands.
