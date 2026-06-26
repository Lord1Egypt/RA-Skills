# Summary Generator Pattern

Use this pattern to create live summaries without confusing them for canon.

## Goal
Generate compact current-state views from upstream sources while keeping them clearly derived and rebuildable.

## Appropriate use cases
Use generated summaries for:
- queue state
- alert state
- health snapshots
- recent run outcomes
- compact digests of noisy logs
- operator dashboards

Do not use generated summaries as the primary home for durable doctrine.

## Inputs
A summary generator should read from authoritative sources such as:
- logs
- queue/task state
- monitoring outputs
- daily notes
- project artifacts
- system state files

## Output characteristics
A good generated summary is:
- compact
- timestamped
- explicit about what it summarizes
- clear about current state vs durable lesson
- rewriteable in place when representing current truth

## Recommended output sections
When useful, structure summaries like this:

### 1. Current state
What is true right now?

### 2. Evidence / provenance
What sources were summarized?

### 3. Risks / caveats
What parts are uncertain, stale, or weakly inferred?

### 4. Promotion candidates
What recurring lessons might deserve elevation into doctrine later?

## Truthfulness rules
- Mark summaries as derived state.
- Do not let transient red/yellow/green states become durable canon automatically.
- Distinguish observed facts from weak inference.
- Prefer rewriting current-state summaries instead of appending infinite history unless history is the artifact.

## Example pattern
A health summary might include:
- active alerts
- last successful checks
- most recent failures
- timestamps for freshness
- note that the summary is derived from logs and health outputs

## Promotion boundary
A summary can nominate durable lessons, but it should not silently convert them into doctrine.
Promotion should happen through a separate review step or memory-maintenance flow.

## Lightweight automation idea
A future summary helper can:
- read current inputs
- rewrite a compact state file
- emit a small list of promotion candidates

It should not directly edit hot canon unless the surrounding system explicitly authorizes that step.
