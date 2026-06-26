# memory-referee

**ontology** and **Proactive Agent** give agents the ability to remember more. **memory-referee** is designed to work alongside skills like ontology and Proactive Agent to give that memory a cleaner foundation to stand on — deduplicating entities, resolving naming conflicts, separating facts from goals from speculation, archiving stale records, and enforcing consistent schemas.

---

> **Built with [Saturnday](https://www.saturnday.dev) — AI-specific governance for AI-generated code.**
>
> While governing the build of memory-referee, Saturnday caught the kinds of mistakes AI coders routinely ship: `.env` patterns that could expose API keys, deduplication logic that could silently drop memory records, fake tests that passed while verifying almost nothing, and runtime validation gaps that would let malformed records corrupt downstream decisions.
>
> That is the difference between AI-generated code and governed AI-generated code.
> [www.saturnday.dev](https://www.saturnday.dev)

---

## Installation

```sh
npm install
npm run build
```

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

## Input format

Each record in the input array must include:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `string` | yes | Unique record identifier |
| `kind` | `string` | yes | `fact`, `goal`, or `speculation` |
| `entity` | `string` | yes | The entity this record describes |
| `content` | `string` | yes | The record's content |
| `timestamp` | `string` | yes | ISO 8601 date string |
| `provenance` | `object` | yes | `{ sourceId, sourceLabel, capturedAt }` — pass as a single object; the skill wraps it into an array internally to support merged records that accumulate multiple sources |
| `tags` | `string[]` | no | Optional tags |

## Development

```sh
npm test          # run tests
npm run typecheck # type-check without emit
npm run build     # compile to dist/
```

## Trade-offs

- **Similarity threshold is fixed at 0.8** — deduplication uses Jaccard word-overlap similarity. Records must share at least 80% of their word vocabulary to be merged. Lower than that and they are kept separate for conflict detection to inspect.
- **In-process only** — the adjudication pipeline runs entirely in memory. For very large record sets (> 100k records) a streaming or batched approach would be more appropriate.
- **No persistence** — the skill adjudicates a snapshot and returns results; it does not maintain a live memory store or handle incremental updates.

## Limitations

- Contradiction detection is heuristic-based (negation proximity + numeric divergence) and will produce false positives when a negation word appears near a shared entity name across unrelated records. Semantic antonym detection is not implemented in v1.
- Provenance is preserved as-is from input; the skill does not re-verify or enrich source metadata.
- Staleness is determined by timestamp age against a fixed 30-day TTL; context-dependent staleness (e.g. a goal that was completed) is not inferred automatically.

## Non-goals

- Not a vector database or embedding-based semantic search layer.
- Not a long-term persistence store; use a dedicated memory backend for that.
- Not a general-purpose ETL pipeline; designed specifically for OpenClaw agent memory records.
- Not responsible for fetching or writing records to external systems.
