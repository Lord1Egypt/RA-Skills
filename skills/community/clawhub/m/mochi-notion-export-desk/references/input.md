# Action contract

index: file (ZIP exported as Markdown & CSV). Limits 16 MiB compressed/32 MiB uncompressed/2000 members/4 MiB per member. Rejects traversal, symlink, encryption and duplicate paths. Reads .md and .csv; records skipped attachments and HTML/nested ZIPs rather than pretending they were converted. Outputs notion-index.md and JSON/HTML metadata. Nothing is extracted into original paths.

## Request example

```json
{
  "action": "index",
  "file": "samples/notion.zip"
}
```

## Runtime and boundaries

Python 3.10+ standard library. Paths must be relative to the active workspace; absolute paths, parent traversal, symbolic links and junctions are rejected. This is a path guard, not OS-level isolation: retain the host container/sandbox. A helper field does not grant permission to access another account or send information.

In Notion use the page menu → Export → Markdown & CSV, then provide the resulting ZIP. Follow current official help at https://www.notion.com/help/export-your-content . This is an offline export reader, not an API connector, permission migration or full-fidelity backup.
