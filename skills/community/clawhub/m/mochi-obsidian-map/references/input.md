# Action contract

map: directory (vault subdirectory inside the current workspace). Scans <=2000 .md files, skips fenced code, resolves [[Note#Heading|alias]] by relative path, root path or unique basename. Reports ambiguous note names and missing headings. Does not support block IDs, plugin syntax or non-Markdown attachments. No files are renamed or edited.

## Request example

```json
{
  "action": "map",
  "directory": "samples/vault"
}
```

## Runtime and boundaries

Python 3.10+ standard library. Paths must be relative to the active workspace; absolute paths, parent traversal, symbolic links and junctions are rejected. This is a path guard, not OS-level isolation: retain the host container/sandbox. A helper field does not grant permission to access another account or send information.

Ask for a selected vault copied or mounted into the active workspace. Do not scan another user’s home directory. This helper does not synchronize Obsidian or modify notes.
