# Action contract

entity: id, type (identifiers), name, source, properties (optional object <=20 KB). Existing ID updates that entity. relate: from, to, relation, source; both nodes must exist. query: id, depth (0..4, default 1), capped at 1000 reachable nodes. export: all nodes and edges. Cycles are supported, not inferred as errors.

## Request example

```json
{
  "action": "entity",
  "id": "demo-project",
  "type": "project",
  "name": "Demo project",
  "source": "User supplied demo"
}
```

## Runtime and boundaries

Python 3.10+ standard library. Paths must be relative to the active workspace; absolute paths, parent traversal, symbolic links and junctions are rejected. This is a path guard, not OS-level isolation: retain the host container/sandbox. A helper field does not grant permission to access another account or send information.

Use only user-authorized information in the active agent workspace. Ask before storing sensitive personal details. Relations are supplied facts, not inferred employment, trust or eligibility decisions.
