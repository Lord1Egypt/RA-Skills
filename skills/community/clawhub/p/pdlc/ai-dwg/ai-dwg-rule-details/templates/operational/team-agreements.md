<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: generated
---
# Template: TEAM_AGREEMENTS.md

```markdown
<!-- AI-DWG generated | source: Team context + Methodology | date: {generation-date} -->

# Team Agreements

## Working Model

- **Autonomy mode:** {Autopilot / Supervised}
- **Review standard:** {n} peer + CODEOWNER
- **Ownership:** {collective / strong per module}
- **Pair programming:** {when/if practiced}

## Communication

- Async-first: document decisions in ADRs/tickets
- Blockers: escalate within {hours}
- Architecture questions: check steering files first

## Quality Standards

- "Done" = passes DEFINITION_OF_DONE.md — no negotiation
- Tech debt: log as tickets — never ignore
- Refactoring: allowed in task scope; major = ADR

## Meetings

| Ceremony | Cadence | Duration | Purpose |
|----------|---------|:--------:|---------|
| {Planning} | {cadence} | {time} | Plan sprint work |
| {Standup} | Daily | {time} | Sync + blockers |
| {Review} | {cadence} | {time} | Demo completed work |
| {Retro} | {cadence} | {time} | Process improvement |

## Conflict Resolution

1. Technical disagreement → data/evidence wins
2. Architecture disagreement → ADR process (evaluate options)
3. Process disagreement → retro action item
4. Unresolved → tech lead decides (documented)
```

## Filling: Refer to `mapping/team-to-agreements.md` (Target 1).
