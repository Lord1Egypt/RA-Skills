---
name: memory-referee
version: 1.0.0
description: Memory hygiene and adjudication layer for OpenClaw agent workflows. Deduplicates entities, resolves naming conflicts, separates facts from goals from speculation, archives stale records, enforces consistent schemas, detects contradictions, and preserves provenance. Complements ontology and Proactive Agent.
author: Saturnday
tags:
  - memory
  - hygiene
  - adjudication
  - deduplication
  - provenance
inputs:
  raw_records:
    type: array
    description: Array of raw memory records to adjudicate
    required: true
outputs:
  report:
    type: string
    description: Markdown adjudication report summarising all decisions
  result:
    type: object
    description: Structured JSON output with deduplicated, classified, and validated records
runtime: node
---

# memory-referee

**ontology** and **Proactive Agent** give agents the ability to remember more. **memory-referee** is designed to work alongside skills like ontology and Proactive Agent to give that memory a cleaner foundation to stand on — deduplicating entities, resolving naming conflicts, separating facts from goals from speculation, archiving stale records, and enforcing consistent schemas.

---

> Built with [Saturnday](https://www.saturnday.dev) — AI-specific governance for AI-generated code.
>
> While governing the build of memory-referee, Saturnday caught the kinds of mistakes AI coders routinely ship: `.env` patterns that could expose API keys, deduplication logic that could silently drop memory records, fake tests that passed while verifying almost nothing, and runtime validation gaps that would let malformed records corrupt downstream decisions.
>
> That is the difference between AI-generated code and governed AI-generated code.
> [www.saturnday.dev](https://www.saturnday.dev)

---

## When to Use

Invoke this skill whenever an agent's memory store may have accumulated:

- **Duplicate or near-duplicate records** that should be collapsed into a single canonical entry
- **Naming conflicts** where the same entity appears under multiple aliases
- **Mixed classification** — facts, goals, and speculation interleaved without clear labelling
- **Stale records** that have aged past their useful window and should be archived
- **Schema drift** — records that no longer conform to the expected structure
- **Contradictions** — two records that assert incompatible facts about the same entity

Use it after running ontology or Proactive Agent to clean up accumulated memory before passing it downstream.

## Inputs

Each record in `raw_records` must be a JSON object with the following fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | yes | Unique identifier for the record |
| `kind` | `string` | yes | One of `fact`, `goal`, or `speculation` |
| `entity` | `string` | yes | The entity this record is about |
| `content` | `string` | yes | The record's content |
| `timestamp` | `string` | yes | ISO 8601 date string |
| `provenance` | `object` | yes | Single provenance object: `{ sourceId, sourceLabel, capturedAt }`. The skill wraps this internally into an array to support merged records with multiple sources. |
| `tags` | `string[]` | no | Optional tags |

## Outputs

| Field | Type | Description |
|-------|------|-------------|
| `report` | `string` | Markdown adjudication report summarising all decisions |
| `result` | `object` | Structured JSON with deduplicated, classified, validated records |

## Usage

### CLI

```sh
echo '[{"id":"r1","kind":"fact","entity":"Alice","content":"Alice prefers dark mode","timestamp":"2026-03-27T00:00:00Z","provenance":{"sourceId":"s1","sourceLabel":"pref-log","capturedAt":"2026-03-27T00:00:00Z"}}]' | node dist/index.js
```

### Library

```typescript
import { main } from 'memory-referee';

const records = [
  {
    id: 'r1',
    kind: 'fact',
    entity: 'Alice',
    content: 'Alice prefers dark mode',
    timestamp: '2026-03-27T00:00:00Z',
    provenance: { sourceId: 's1', sourceLabel: 'pref-log', capturedAt: '2026-03-27T00:00:00Z' }
  }
];

const { markdown, json, report } = main(JSON.stringify(records));

console.log(markdown);  // human-readable adjudication report
console.log(json);      // structured JSON output
```
