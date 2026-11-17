# Engine Selection When Creating Data Products

Choose the target model before creating a worksheet, table, or query output.
The models may coexist in one workbook but do not share a write API.

## Discover the public command surface first

Do not treat this reference as a command tree or a flag contract. Before
constructing a command, inspect the installed public surface and the relevant
leaf help:

```bash
mbs --help
mbs table --help
mbs sql --help
mbs worksheet --help
mbs formula --help
```

Generate only commands shown by those public help screens and their nested
`--help` output. Use nested `--help` for the selected public leaf before
relying on flags or payload shape. Do not generate hidden compatibility
commands, even when an older script or integration still accepts them.

| Need | Create/use | Identity after creation |
|---|---|---|
| Visual report, merged cells, charts, images, or visible formulas | Excel Sheet | `worksheet_name`, `gid`, A1 addresses |
| Flat operational records and field-level computation | Base Table | `table_id`, `field_id`, record key/`record_id` |
| Persisted derived result from a query | Worksheet SQL Config or supported SQL materialization | result worksheet/table and raw SQL config |

## Base Table

For a new durable Base handoff table, use the public `table create` flow when
its documented arguments cover the requested rows and schema. Capture the
returned table and field identities, then use `table inspect`, `table schema`,
and a bounded `table sample` to verify the result.

The canonical response operation is `table.create` for every public creation
source: a local frame, a SQL query result, or a worksheet range. Source
selection does not produce source-specific operation IDs.

Do not update a Base table by writing a range, running a keep-headers refresh,
or preserving a row-2 formula template. For later writes, select only a public
record operation shown by the current `mbs table --help` and confirm its
semantics with the leaf help before constructing the payload.

For derived SQL output, use public `mbs sql materialize`. Discover the exact
materialization options with:

```bash
mbs sql materialize --help
```

`sql materialize` is only a replacement when its documented destination,
identity, schema, and persistence semantics satisfy the requested durable Base
table outcome. If it cannot create or target the required Base table with the
required name/schema, report a **capability gap** instead of substituting a
hidden command or claiming that SQL materialization is equivalent.

For Base Formula work, use public formula validation, persisted-formula
readback, and recalculation evidence. Do not use compile output by itself as
proof that a Formula field was persisted or executed.

## Worksheet SQL Config

Use this when the query itself must remain visible, auditable, and refreshable
as a distinct producer. Discover the supported SQL-config and materialization
leaves before use:

```bash
mbs sql --help
mbs sql config --help
mbs sql materialize --help
```

SQL Config takes raw SQL; it is not a Formula field and it must not be created
as a legacy cell SQL wrapper. If a requested materialization destination is not
supported by the public `sql materialize` help, report the capability gap.

## Excel Sheet

Use Sheet only for layout-oriented outputs. Discover the public worksheet,
range, and formula leaves first; for example, inspect `mbs formula set --help`
before writing a formula.

```bash
mbs worksheet create --doc-id <DOC_ID> --name <REPORT_WORKSHEET> --output json
mbs range write --doc-id <DOC_ID> --worksheet-name <REPORT_WORKSHEET> --range A1:D20 --values <VALUES_JSON> --verify
mbs formula set --doc-id <DOC_ID> --worksheet-name <REPORT_WORKSHEET> --cell E2 --expression '=<FORMULA>' --language excel
mbs formula recalculate --doc-id <DOC_ID> --worksheet-name <REPORT_WORKSHEET>
mbs range inspect --doc-id <DOC_ID> --worksheet-name <REPORT_WORKSHEET>
```

After creation, inspect the workbook and list its worksheets with the public
inspection flows:

```bash
mbs workbook inspect --doc-id <DOC_ID> --output json
mbs worksheet list --doc-id <DOC_ID> --output json
```

If the result is Base-backed, stop using A1/range or cell-formula instructions
and switch to the Base verification runbook.
