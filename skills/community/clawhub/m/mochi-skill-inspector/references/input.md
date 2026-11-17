# Action contract

inspect: file (workspace-relative ZIP). Limits: 16 MiB compressed, 32 MiB uncompressed, 2000 entries, 4 MiB per file; encrypted entries, links, duplicate names and traversal are rejected. Findings contain rule, file and line, not secret-bearing source excerpts. Reports are review indicators, not a malware verdict.

## Request example

```json
{
  "action": "inspect",
  "file": "samples/demo-skill.zip"
}
```

## Runtime and boundaries

Python 3.10+ standard library. Paths must be relative to the active workspace; absolute paths, parent traversal, symbolic links and junctions are rejected. This is a path guard, not OS-level isolation: retain the host container/sandbox. A helper field does not grant permission to access another account or send information.

Do not install or execute an inspected package as part of inspection. Indicators can be false positives and static checks can miss harmful behaviour. A clean report is not approval or certification.
