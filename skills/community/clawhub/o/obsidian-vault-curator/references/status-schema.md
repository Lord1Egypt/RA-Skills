# Status schema

Use a small controlled schema. Expand only when repeated real use shows a gap.

## Core fields

```yaml
status: needs-review
doc_kind: reference
topic:
canonical: false
canonical_for: []
supersedes: []
superseded_by: []
last_verified:
review_after:
review_state: unreviewed
confidence: low
```

## Allowed values

### `status`

- `current` — currently valid or leading
- `historical` — no longer leading, but still worth keeping
- `concept` — target state, proposal, idea, or design direction
- `needs-review` — unclear, conflicting, or not yet checked
- `reactivatable` — not active now, but likely worth reviving later

### `doc_kind`

- `reference`
- `howto`
- `explanation`
- `tutorial`
- `research`
- `adr`
- `log`
- `index`
- `concept`

Note: `concept` exists in both lists on purpose. `status: concept` means the note describes a future state. `doc_kind: concept` describes its writing genre. They are independent.

### `review_state`

- `unreviewed`
- `reviewed`
- `conflict`
- `migrate-plan-ready`
- `migrated`

### `confidence`

- `low`
- `medium`
- `high`

## Rules

- Keep `status` separate from `doc_kind`.
- When ambiguity matters in prose, name the field explicitly, for example `status: concept`.
- Prefer one canonical page per topic cluster.
- Use `superseded_by` on old pages and `supersedes` on the new leading page.
- If you cannot justify `current`, use `needs-review` first.
- If dates matter, write real dates instead of vague words like "latest".

### `topic` rule

Use one short kebab-case slug per topic cluster. Adopt the slug already used elsewhere in the vault when one exists. If no slug exists yet, leave the field blank rather than inventing one without main-agent confirmation.

### `confidence` rule

Use `low` when the evidence is one shallow signal or inference. Use `medium` when at least two independent signals agree. Use `high` only when the note's live state was directly verified within the current pass. Default to `low` under uncertainty.

## Examples

### Current reference page

```yaml
status: current
doc_kind: reference
topic: openclaw
canonical: true
canonical_for:
  - OpenClaw Runtime
last_verified: 2026-05-11
review_state: reviewed
confidence: high
```

### Historical page preserved for context

```yaml
status: historical
doc_kind: howto
topic: openclaw
superseded_by:
  - "[[OpenClaw Runtime & Konfiguration]]"
review_state: reviewed
confidence: medium
```

### Future-state note

```yaml
status: concept
doc_kind: explanation
topic: yuna-public
review_state: unreviewed
confidence: medium
```

`status` and `doc_kind` are independent. A future-state note can also use `doc_kind: concept` when that is the best fit.

### Unclear note waiting for triage

```yaml
status: needs-review
doc_kind: research
review_state: unreviewed
confidence: low
```
