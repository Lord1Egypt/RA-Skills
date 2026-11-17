# Action contract

record: id, situation, correction, evidence (required strings), tags (optional string array). Duplicate IDs are rejected. resolve: id, verification (required). review: query (optional substring). Records stay local in .mochilab/; resolve appends verification history and review exports JSON/HTML. No hooks or policy files are changed.

## Request example

```json
{
  "action": "record",
  "id": "demo-command",
  "situation": "Demo flag failed",
  "correction": "Read the CLI help first",
  "evidence": "Synthetic exit code 2",
  "tags": [
    "demo"
  ]
}
```

## Runtime and boundaries

Python 3.10+ standard library. Paths must be relative to the active workspace; absolute paths, parent traversal, symbolic links and junctions are rejected. This is a path guard, not OS-level isolation: retain the host container/sandbox. A helper field does not grant permission to access another account or send information.

Only save corrections the user has asked to retain. Do not sweep chats or credentials, install hooks, rewrite system guidance, or claim one successful example proves a universal rule.
