# Formula Lineage Trace Reference

## Contents

1. When to use this
2. What lineage does
3. Request
4. Response
5. Recommended workflows
6. Limitations and recovery

## 1. When to use this

Read this document when the user asks where a formula cell, computed column, or SQL formula result comes from.

Use lineage trace for questions like:

- why a target cell has a wrong or unexpected value
- which source columns feed a computed column
- whether a formula depends on another formula column
- how a `=SQL(...)` result cell maps back to source worksheet columns
- building a dependency graph for a target cell

Do not use it as a substitute for reading actual values. After lineage identifies relevant sheets and columns, use `excel-worksheet range read`, `excel-table sample`, or `db-table sample` when exact data values are needed.

## 2. What lineage does

`mbs formula lineage` is read-only formula dependency tracing.

It:

- accepts a workbook `document_id` or MaybeAI spreadsheet `uri`
- accepts one or more target cells
- requires each target to identify a worksheet by `worksheet_name` or `gid`
- traces ordinary Excel formula references such as `A2`, `A:A`, `A2:B10`, and cross-sheet references
- treats repeated row formulas as column lineage when appropriate
- traces supported `=SQL("...")` formulas through final SELECT outputs, CTEs, table aliases, joins, and source worksheet columns
- returns either a nested dependency tree or graph-style nodes and edges

## 3. Request

```bash
mbs formula lineage --doc-id <DOC_ID> --worksheet-name Report --cell C2 --format tree --output yaml
mbs formula lineage --url <MAYBE_SHEET_URL> --worksheet-name Report --cell C2 --format node
```

`--cell` must be an exact A1 cell such as `C2` or `AE2`. Do not pass only `C:C`.
Use `--format tree` by default; use `--format node` for graph rendering.

## 4. Response

Common top-level fields:

```json
{
  "success": true,
  "document_id": "<document_id>",
  "format": "tree",
  "results": []
}
```

With `format: "tree"`, each result contains:

- `target`: the requested target cell
- `lineage`: the traced dependency node
- nested `depends_on`: upstream dependencies
- optional `produced_by`: SQL formula producer for SQL result cells

Common node fields:

- `id`: stable node id when available
- `type`: node type
- `worksheet_name`: worksheet name
- `gid`: worksheet gid
- `cell`: concrete cell for cell-level nodes
- `range`: cell or column range
- `column`: header from row 1 when available
- `formula`: exact formula for formula-cell or SQL formula nodes
- `sample_formula`: sample formula for formula-column nodes
- `depends_on`: upstream dependencies

Common node types:

- `target_cell`: the requested target
- `formula_cell`: a formula in a single cell
- `formula_column`: a column-like repeated formula
- `source_cell`: non-formula source cell
- `source_column`: non-formula source column
- `sql_formula`: `=SQL(...)` formula producer
- `sql_result_cell`: output cell produced by a SQL formula
- `unresolved`: reference could not be resolved or trace limits were reached

Example `tree` response shape:

```json
{
  "success": true,
  "document_id": "<document_id>",
  "format": "tree",
  "results": [
    {
      "target": {
        "type": "target_cell",
        "worksheet_name": "Report",
        "cell": "C2",
        "range": "C2:C2",
        "column": "Category"
      },
      "lineage": {
        "type": "formula_column",
        "worksheet_name": "Report",
        "range": "C:C",
        "column": "Category",
        "sample_formula": "=XLOOKUP(A2,Products!A:A,Products!C:C,\"\")",
        "depends_on": [
          {
            "type": "source_column",
            "worksheet_name": "Report",
            "range": "A:A",
            "column": "SKU"
          },
          {
            "type": "source_column",
            "worksheet_name": "Products",
            "range": "C:C",
            "column": "Category"
          }
        ]
      }
    }
  ]
}
```

With `format: "node"`, the response omits `results` and returns:

- `nodes`: flat lineage nodes
- `edges`: dependency edges

Edge relations include:

- `produced_by`: target/result produced by a formula node
- `formula_depends_on`: ordinary formula dependency
- `sql_depends_on`: SQL expression dependency

Use `node` when a UI, graph renderer, or downstream tool needs stable ids and edges.

## 5. Recommended workflows

### Explain a wrong formula result

1. `mbs workbook list-worksheets` and a small `mbs excel-worksheet range read` to confirm the sheet name.
2. Call `mbs formula lineage --format tree`.
3. Walk `lineage.depends_on` and summarize the chain in business terms.
4. If a source column looks suspicious, use `mbs excel-worksheet range read` or table sample to inspect sample values.

### Build a dependency graph

1. Call `mbs formula lineage --format node`.
2. Render `nodes` by `id`.
3. Render `edges` by `from`, `to`, and `relation`.
4. Label nodes with `worksheet_name`, `column`, `cell`, and `sample_formula` or `formula`.

### Trace SQL formula output

1. Identify a result cell in the SQL output block, usually row 2 or below.
2. Call `mbs formula lineage` for that output cell.
3. Inspect `produced_by` to find the `sql_formula`.
4. Inspect `depends_on` to see source worksheet columns used for that output column.

## 6. Limitations and recovery

Important limits:

- `cell` must be a concrete A1 cell.
- Lineage traces formulas and references; it does not calculate or mutate values.
- Formula parsing focuses on A1-style references, ranges, column references, and cross-sheet references.
- SQL tracing supports the common worksheet SQL subset, including CTEs, aliases, final SELECT outputs, and FROM/JOIN sources. It is not a full SQL parser.
- Deep or huge graphs may return `unresolved` if trace limits are reached.
- External workbook references or references to missing sheets may return `unresolved`.

Recovery:

1. If the worksheet cannot be found, call `mbs workbook list-worksheets` and retry with the exact `worksheet_name` or `gid`.
2. If the target is not a formula, the result may be a `source_cell` or `source_column`; read nearby formulas if the user expected computation.
3. If SQL lineage is incomplete, inspect the SQL formula text and validate source headers with `mbs excel-table schema` or `mbs db-table schema`.
4. If lineage identifies the right columns but not the wrong values, switch to `mbs excel-worksheet range read` or table sample for exact source rows.
