# Claim Model

HAMMERRR treats every project statement as a claim until current evidence proves
otherwise.

## Claim Sources

- `PUBLIC_CONTRACT`: README, website, public docs, package metadata, public API docs.
- `OPERATIONAL_CONTRACT`: install docs, runbooks, CI, deployment docs, release process.
- `DESIGN_DECISION`: ADRs, architecture docs, intentional tradeoff records.
- `INTERNAL_INTENT`: comments, TODOs, internal notes, roadmap hints.
- `INFORMAL_CONTEXT`: memory, handoffs, chat summaries, old reports.

Public and operational contracts require the strongest proof. Informal context
is a search hint, not proof.

## Claim Fields

Track:

- claim id
- claim text
- source and authority
- expected runtime or operational effect
- enforcement path
- proof required
- truth status
- proof status
- confidence
- blocker, if any

## Required Judgment

Do not mark a claim false merely because it looks suspicious. Check whether an
ADR, config gate, environment mode, role boundary, or release target makes it
intentional.
