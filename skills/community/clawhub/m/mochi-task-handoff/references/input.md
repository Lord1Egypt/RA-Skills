# Action contract

save: id, goal, completed/next/blocked/constraints (optional string arrays), files (optional workspace-relative paths). Each save increments revision and preserves the previous checkpoint in local history. load: id; exports handoff.md, JSON and HTML with source hash checks. list: saved checkpoints. Does not read or message other agents.

## Request example

```json
{
  "action": "save",
  "id": "demo-task",
  "goal": "Finish the demo report",
  "completed": [
    "Collected inputs"
  ],
  "next": [
    "Review conclusions"
  ],
  "files": [
    "samples/demo.txt"
  ]
}
```

## Runtime and boundaries

Python 3.10+ standard library. Paths must be relative to the active workspace; absolute paths, parent traversal, symbolic links and junctions are rejected. This is a path guard, not OS-level isolation: retain the host container/sandbox. A helper field does not grant permission to access another account or send information.

A checkpoint is context, not proof that unfinished work is complete. Recheck stale inputs. No autonomous scheduling, cross-agent access, prompt-file replacement or external messaging is performed.
