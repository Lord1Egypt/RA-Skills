# Workbook Inspection Reference

Use this short reference to identify a workbook and its worksheets before an
unfamiliar read or write. It is an inspection aid, not a command map and not a
replacement for a bounded data read.

## Discover public inspection commands

The installed CLI is authoritative. Start with public help, then inspect the
specific leaves you intend to run:

```bash
mbs --help
mbs workbook --help
mbs workbook inspect --help
mbs worksheet --help
mbs worksheet list --help
```

Generate only commands that appear in public help. Use nested `--help` for
any public leaf before relying on its flags. Do not generate hidden
compatibility commands.

## Minimal inspection workflow

```bash
mbs workbook inspect --doc-id <DOC_ID> --output json
mbs worksheet list --doc-id <DOC_ID> --output json
```

Use the inspection response and worksheet list to resolve the workbook,
worksheet name, `gid`, engine, and any stable Base table identity exposed by
the current CLI. Then choose the narrowest public follow-up:

- For a Sheet grid, do a bounded `range read` and retain its worksheet locator.
- For a persistent Sheet table or Base table, use `table inspect`, `table
  schema`, and a bounded `table sample` after resolving the stable table
  identity.
- For Formula work, use the public `formula` leaf help to choose validation,
  persistence, readback, or recalculation rather than inferring support from
  the workbook-level response.

Do not infer exact headers, row counts, record IDs, or data values from
inspection alone.

## Verify a native worksheet import

Run the public `worksheet import` flow with its documented verification option.
Use `workbook inspect` plus `worksheet list` afterward only to confirm the
created worksheet's identity and engine. For a large Base source, preserve the
import operation's own row-count and verification evidence; a default bounded
read does not prove copy completeness.

## Recovery

- `403`: confirm `MAYBEAI_API_TOKEN` and document access.
- Missing worksheet: rerun `workbook inspect` and `worksheet list`, then use
  the exact returned worksheet name or `gid`.
- Missing Base table identity: stop before mutation and resolve the table with
  public `table` discovery/inspection help. Once known, target `table inspect`
  with `?tid=<TABLE_ID>` or `?table=<TABLE_NAME>`; its dimensions metadata is
  not a substitute for `table schema` or `table read`.
- If the installed help differs from this reference, follow the installed
  public help and report any required unsupported operation as a capability
  gap.
