---
name: maybeai-sheet-cli
description: Operates MaybeAI spreadsheets via the maybeai-sheet CLI — upload, inspect worksheets, read/write data, append or upsert rows, set formulas, trace lineage, and run SQL result sheets. Use when the user works with MaybeAI workbooks, spreadsheet doc IDs, worksheet gids, Excel import/export, table headers, formula cells, or SQL-over-sheet reports. Use sheet-dashboard for chart-heavy dashboards instead.
metadata:
  openclaw:
    requires:
      env:
        - MAYBEAI_API_TOKEN
    primaryEnv: MAYBEAI_API_TOKEN
    emoji: "📊"
    homepage: https://github.com/OmniMCP-AI/maybeai-uni
---

# MaybeAI Sheet CLI

Execute spreadsheet work through `maybeai-sheet`. Do not use curl, bash wrappers, or hand-built HTTP for operations the CLI covers.

**Prerequisites:** `MAYBEAI_API_TOKEN`, `maybeai-sheet` (`pip install maybeai-sheet-cli`)

## Quick start

```bash
maybeai-sheet sheet worksheets --doc-id <DOC_ID> --output table
maybeai-sheet sheet read --doc-id <DOC_ID> --gid <GID> --output table
maybeai-sheet sheet append --doc-id <DOC_ID> --gid <GID> --rows rows.json --verify
maybeai-sheet workbook create-from-file ./report.xlsx
```

- `--output table` for human inspection; `json` (default) for automation
- Targeting flags (`--doc-id`, `--gid`, `--worksheet-name`, `--output`) work at root, group, or command level
- Always pass a leaf subcommand (`read`, `headers`, `append`, …)

Command catalog: [references/cli-commands.md](references/cli-commands.md)

## Execution order

1. `maybeai-sheet <group> <command> --help` when flags are unclear
2. [references/cli-commands.md](references/cli-commands.md) for command lookup
3. Topic reference below for semantics, edge cases, and uncovered APIs
4. `maybeai-sheet raw post <path> --body body.json` only when no CLI command exists

## Critical rules

**Worksheet targeting.** Non-first worksheets MUST be named explicitly. Prefer `--worksheet-name`; use `--gid` for headers, append, and upsert. Without either, calls often hit the first worksheet. Details: [references/read-write.md](references/read-write.md)

**Manifest-first.** Before reads or writes on an unfamiliar workbook: `workbook manifest` or `sheet worksheets`, then pick worksheet/gid.

**Write priority.** `sheet upsert` → `sheet append` → `sheet write-range` → `raw post` (last resort).

**Verify after every write.** Use `--verify`, then `sheet read --output table`, or `sheet headers`.

**Data vs style.** Write data with CLI commands; apply styles/charts via `raw post`. See [references/charts-formatting.md](references/charts-formatting.md).

**SQL.** Compile before write: `raw post /api/v1/excel/sql/compile` then `sql/write_result`. See [references/formulas-sql.md](references/formulas-sql.md).

## Task routing

| Task | Start here |
|------|------------|
| Command flags and examples | [references/cli-commands.md](references/cli-commands.md) |
| Read/write targeting and API choice | [references/read-write.md](references/read-write.md) |
| Upload, export, sharing | [references/file-management.md](references/file-management.md) |
| Workbook semantic overview | [references/workbook-profile.md](references/workbook-profile.md) |
| Formulas and SQL result sheets | [references/formulas-sql.md](references/formulas-sql.md) |
| Formula dependency tracing | [references/lineage-trace.md](references/lineage-trace.md) |
| Charts, freeze panes, styles | [references/charts-formatting.md](references/charts-formatting.md) |
| Failures and recovery | [references/errors-recovery.md](references/errors-recovery.md) |
| Clickable cell refs in answers | [references/clickable-refs.md](references/clickable-refs.md) |
| Live `=SQL(...)` showcase | [references/sql-formula-showcase.md](references/sql-formula-showcase.md) |

## Workflows

### Inspect a workbook

```
- [ ] worksheets or workbook manifest
- [ ] headers on target gid
- [ ] read sample with --output table
```

```bash
maybeai-sheet sheet worksheets --doc-id <DOC_ID> --output table
maybeai-sheet sheet headers --doc-id <DOC_ID> --gid <GID>
maybeai-sheet sheet read --doc-id <DOC_ID> --gid <GID> --output table
```

### Upload and inspect

```
- [ ] create-from-file
- [ ] capture document_id from JSON output
- [ ] worksheets → headers → read sample
```

```bash
maybeai-sheet workbook create-from-file ./file.xlsx
maybeai-sheet workbook manifest --doc-id <DOC_ID>
maybeai-sheet sheet worksheets --doc-id <DOC_ID> --output table
```

### Sync rows by key

```
- [ ] confirm key column name
- [ ] upsert with --verify
- [ ] recalculate if downstream formulas exist
- [ ] read back target range
```

```bash
maybeai-sheet sheet upsert --doc-id <DOC_ID> --gid <GID> --key order_id --rows rows.json --verify
maybeai-sheet sheet recalculate --doc-id <DOC_ID> --worksheet-name <SHEET>
```

### SQL result sheet

```
- [ ] headers + read sample on source sheet
- [ ] sql/compile (raw post)
- [ ] sql/write_result (raw post)
- [ ] read result sheet
```

See [references/formulas-sql.md](references/formulas-sql.md).

### Trace formula lineage

```bash
maybeai-sheet raw post /api/v3/excel/formula/lineage_trace --body lineage.json --output yaml
```

See [references/lineage-trace.md](references/lineage-trace.md) for request body shape.

## Boundaries

- **Dashboard/chart layout** → use `sheet-dashboard`, not this skill
- **Uncovered APIs** (profile, SQL, lineage, charts, export) → `raw post` + topic reference above
- **Clickable refs** → only confirmed locations; see [references/clickable-refs.md](references/clickable-refs.md)
