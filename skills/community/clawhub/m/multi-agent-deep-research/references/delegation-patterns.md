# Delegation Patterns

## Use delegation only when it helps

- Use subagents when the user explicitly asks for multi-agent or parallel work.
- Delegate independent slices, not the critical synthesis step that the PM needs immediately.
- Keep the orchestrator local so scope, standards, and final judgment stay coherent.

## Recommended role menu

- `PM / Orchestrator`: freeze scope, assign work, maintain status, integrate outputs.
- `Source Scout`: collect primary and high-quality secondary sources.
- `Evidence Librarian`: normalize metadata, deduplicate, and approve/reject sources.
- `Claim Builder` or `Comparative Analyst`: convert source notes into dated, scoped claims.
- `Metrics Normalizer`: align definitions, units, and comparability.
- `Claim Auditor`: verify wording, dates, and evidence links.
- `Drafting Editor`: write from verified claims only.

Choose the smallest role set that fits the project.

## Ownership rules

- Assign each agent a narrow write scope by file path.
- State that other agents exist and that the agent must not revert their edits.
- Give the agent one task packet, one cutoff date, and one output contract.
- Keep each work block focused on one dimension, country, or artifact.

## Handoff contract

Require every agent to end with:

```md
done:
- completed work

verified:
- facts or files checked

open:
- unresolved issues

next:
- next role
- next files to read
```

## Anti-duplication rules

- Read the current source ledger and open questions before searching.
- If the agent finds something outside scope, log it under open questions instead of expanding the project ad hoc.
- Do not let two agents write the same summary or ledger at the same time.

## Good task packet shape

- Objective
- Deliverable
- Read set
- Write scope
- Cutoff date
- Source-quality rule
- Handoff target

## Bad task packet shape

- "Research everything about this topic"
- "Write whatever you think is important"
- "Use the whole project context"
