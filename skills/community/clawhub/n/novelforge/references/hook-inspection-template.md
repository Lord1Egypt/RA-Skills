# Story review report

```json
{
  "chapter": "v01-c001",
  "kind": "engine",
  "source_hash": "sha256",
  "result": "PASS",
  "checks": [
    {
      "rule": "continuity.relationship",
      "status": "PASS",
      "source": "settlement:v01-c000",
      "evidence": "relation.example remains consistent"
    }
  ]
}
```

Every failed check must identify the source field or chapter evidence that can
be inspected by a human.
