# Legacy SQL Formula Showcase

This reference is retained only for older workbooks that already contain legacy SQL formula cells. Do not use it to create new SQL outputs.

For new work, use Worksheet SQL Config:

```bash
mbs sql config set --doc-id <DOC_ID> --worksheet-name Report --sql-file report.sql --auto-refresh
mbs sql preview --doc-id <DOC_ID> --worksheet-name Report --sql-file report.sql --output table
mbs sql overwrite --doc-id <DOC_ID> --worksheet-name Report --confirm-overwrite
```

## Legacy Compatibility

Older workbooks may have a formula cell at the top-left of a SQL result block. The modern system should preserve those cells when reading or exporting existing workbook data, but new CLI/UI/API paths should not create or edit them.

Use this document only to:

- recognize an existing legacy SQL formula result block
- explain why an old workbook still has a formula producer
- migrate old cells into Worksheet SQL Config with explicit preview/commit

Migration commands:

```bash
mbs sql migration preview --doc-id <DOC_ID>
mbs sql migration commit --doc-id <DOC_ID> --candidate-id <CANDIDATE_ID> --allow-manual-candidates
```

Run preview first. Commit modifies registry/config state and should be run only in the operator-approved migration window.

## Reading Existing Legacy Outputs

For an existing legacy workbook, use normal read/lineage commands:

```bash
mbs formula read --doc-id <DOC_ID> --worksheet-name Report --range A1:A1 --output json
mbs range read --doc-id <DOC_ID> --worksheet-name Report --range A1:E20 --output table
mbs range lineage --target "https://www.maybe.ai/docs/spreadsheets/d/<DOC_ID>?gid=<GID>" --range B2 --format tree --output yaml
```

If the visible result is stale, prefer migrating to Worksheet SQL Config and refreshing through `mbs sql overwrite`.
