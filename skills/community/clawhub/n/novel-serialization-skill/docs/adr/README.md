# Architecture decision records

An ADR records one decision, the context that made it necessary, and its
consequences — including the parts we accepted as costs. Decisions that are
still open do not get an ADR.

## Index

| Number | Title | Status |
|---|---|---|
| [0001](0001-reports-are-not-released.md) | Reports are not released | Accepted |
| [0002](0002-release-references-release.md) | Release files reference release files only | Accepted |
| [0003](0003-dual-track-chapter-naming.md) | Dual-track chapter naming | Accepted |

## Status values

- **Proposed** — under discussion, not yet applied.
- **Accepted** — in force. Changing it needs a new ADR that supersedes this one.
- **Superseded** — replaced; the header links to the replacement.
- **Deprecated** — no longer recommended, still tolerated in existing trees.

## Template

```markdown
# <Number>. <Title>

Date: YYYY-MM-DD
Status: Proposed | Accepted | Superseded | Deprecated

## Context

What forced the decision, and what constraints apply.

## Decision

What we chose, stated in the active voice.

## Consequences

What gets easier, and what we accept as a cost.
```
