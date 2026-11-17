# Formula Lineage and Computation Evidence

## 1. Select the model before tracing

A question about a computed value may concern three different producers:

| Target | Correct identity | Evidence to inspect |
|---|---|---|
| Excel Sheet formula | `worksheet_name` and A1 cell | `mbs formula lineage` |
| Base column Formula | `table_id`, `field_id`, record identity | validation, persisted-formula readback, and recalculation evidence |
| Worksheet SQL Config | result worksheet and raw SQL config | stored SQL, preview, and materialization evidence |

Do not send a Base `field_id` to the A1 lineage command, and do not explain a
SQL Config result as though it were an ordinary formula cell.


## Public command discovery

This reference does not define a command tree or flag contract. Before
generating a lineage or Formula command, inspect the installed public surface:

```bash
mbs --help
mbs range --help
mbs formula --help
mbs sql --help
```

Use nested `--help` for the selected public leaf. Do not generate hidden
compatibility commands.

## 2. Sheet formula lineage

`mbs range lineage` is read-only A1-style dependency tracing for Sheet
targets and SQL result cells that the service exposes as cells.

```bash
mbs range lineage --target "https://www.maybe.ai/docs/spreadsheets/d/<DOC_ID>?gid=<GID>" --range C2 --format tree --output yaml
mbs range lineage --target "https://www.maybe.ai/docs/spreadsheets/d/<DOC_ID>?gid=<GID>" --range C2:E2 --format node
```

`--range` accepts a concrete A1 address such as `C2` or an A1 range such as
`C2:E2`; `range lineage --cell` is not accepted. Use `--format tree` for a
human explanation and `--format node` for a graph.

A tree result normally contains:

- `target`, `lineage`, and nested `depends_on`
- Sheet cells/ranges, column headers, and ordinary formula text
- an optional `produced_by` Worksheet SQL Config node
- SQL fingerprints, dependencies, and last-run state where SQL Config lineage
  is available

The trace is read-only. Read source values separately with
`range read` or `table sample`.

## 3. Base column Formula evidence

Base Formula evidence is not an A1 dependency graph, and compile output alone
does not prove that a Formula was persisted or executed. Resolve the stable
`table_id` and `field_id`, then inspect the public Formula leaves before use:

```bash
mbs formula validate --help
mbs formula set --help
mbs formula read --help
mbs formula recalculate --help
```

For a supported Base Formula workflow, retain all of the following evidence:

1. Validation output for the intended formula and target field.
2. The successful persistence result from `formula set` (when a write was
   requested).
3. Persisted-formula readback that identifies the target field and stored
   expression.
4. Recalculation result, including execution status and any field errors.
5. A representative record read only as value evidence after recalculation.

If public `formula validate`, `formula set`, `formula read`, or `formula
recalculate` help does not cover the requested Base behavior, report a
capability gap. Do not substitute a cell lineage query, a range formula, a
row-2 template, or a hidden compatibility command.

## 4. Worksheet SQL Config lineage

For an SQL-produced result, inspect the stored config and the materialized
output first:

```bash
mbs sql config get --doc-id <DOC_ID> --worksheet-name <SQL_RESULT_SHEET> --output json
mbs sql preview --doc-id <DOC_ID> --worksheet-name <SQL_RESULT_SHEET> --sql-file query.sql --output table
mbs sql overwrite --doc-id <DOC_ID> --worksheet-name <SQL_RESULT_SHEET> --confirm-overwrite
```

Then use A1 lineage only when the target is a Sheet/SQL-result cell:

```bash
mbs formula lineage --doc-id <DOC_ID> --worksheet-name <SQL_RESULT_SHEET> --cell C2 --format tree
```

Trace the `worksheet_sql_config`/SQL dependency nodes back to source
worksheets or Base tables. The authoritative query text is raw SQL in SQL
Config, not a cell formula.

## 5. Recovery

1. If workbook inspection and worksheet listing do not reveal the engine and
   object identity, stop and resolve it before tracing or writing.
2. If a Sheet A1 trace returns a source cell rather than a formula, inspect
   nearby cells and the source data.
3. If Base results are stale, obtain validation, persisted-formula readback,
   and recalculation evidence; a table sample alone cannot show whether
   recalculation ran.
4. If SQL output is stale or incomplete, inspect the saved config, preview the
   exact raw SQL, and validate the materialization result.
5. Existing legacy SQL wrapper cells are migration-only objects. Do not edit
   them through formula commands; use the SQL migration workflow.
