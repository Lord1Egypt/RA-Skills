# Discussion Recovery and Task Design

## 1. Recover the discussion faithfully

Build a decision inventory before writing task documents:

| Type | Content | Source | State |
| --- | --- | --- | --- |
| Original user goal | Uncompressed requirements | task/thread/message | confirmed |
| User correction | Later adjustment to a proposal | task/thread/message | confirmed |
| Agent proposal | Suggestion not yet accepted | assistant message | proposed |
| Explicit rejection | Alternative rejected by the user | task/thread/message | rejected |
| Current fact | Code, data, or runtime evidence | path/commit/artifact | observed |

Only `confirmed` entries become frozen design. Keep `proposed` entries open even when they appear reasonable.

When context was compacted:

1. reread the source task when possible;
2. compare user messages with the corresponding assistant explanations to identify the final accepted version;
3. mark unavailable evidence and ask about high-impact gaps;
4. preserve every material requirement when restructuring long input.

## 2. Separate design categories

Classify each item as:

- **Frozen decision**: already confirmed and not changeable by the Worker.
- **Implementation detail**: locally decidable from current code and project conventions.
- **OPEN design gate**: unresolved and capable of changing product or task semantics.
- **Non-goal**: an explicit scope boundary.

Do not mix future optimization ideas into current acceptance criteria.

## 3. Material gates that require the user

### 3.1 Persistence and migration

Confirm at least:

- model, fields, and durable paths;
- latest-only versus compatible reads;
- write, atomicity, and recovery semantics;
- migration, backup, rollback, and old-data handling;
- identity, revision, visibility, and state-machine invariants.

### 3.2 Important APIs and tools

Confirm at least:

- name;
- caller and authorization;
- basic parameters and identity selector;
- return value or receipt;
- material error categories;
- whether the operation is a synchronous mutation, asynchronous task, or read-only query.

### 3.3 System behavior and safety boundaries

Confirm at least:

- decision ownership;
- concurrency, locking, stale-review, and retry semantics;
- external messages, deployment, deletion, migration, Release, push, and other side effects;
- whether failure preserves partial progress;
- which gates may be removed or combined and which must remain.

### 3.4 Bug-fix semantics

When current behavior conflicts with documentation but more than one correction is plausible, preserve failure evidence and ask the user to freeze the target behavior.

## 4. Work-item requirements

Each work item answers:

1. What is currently wrong or missing?
2. What is the target behavior?
3. Which production paths or execution steps change?
4. Which adjacent boundaries must remain unchanged?
5. What establishes the failure or baseline first?
6. Which validation assets change?
7. Which exact validation runs?
8. What evidence is sufficient for acceptance?
9. What must stop execution and trigger coordination?

Freeze the validation design before execution. If implementation reveals a missing impact path, update the design and matrix before running the additional validation.

Negative coverage follows the owned contract and realistic risk model. Do not invent validation obligations for extreme recursion, oversized payloads, impossible internal states, or lower-level library failures unless they are explicitly supported, realistically reachable, security-relevant, or observed. Record optional defense-in-depth separately instead of expanding the task's acceptance boundary.

## 5. Part boundaries

A sound part:

- has one coherent business outcome;
- can reach a closed validation result;
- does not depend on unfrozen behavior from an unfinished part;
- fits one Reviewer context;
- is not divided only by folders or desired commit count.

End every part with an integrated audit of the call chain, persistence, authorization and Agent surface, realistic negative cases, documentation, stale symbols and entry points, and rollback or cleanup.
