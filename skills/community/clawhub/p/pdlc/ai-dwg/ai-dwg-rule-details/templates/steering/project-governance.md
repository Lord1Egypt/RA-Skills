<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: project-governance.md

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Infrastructure & Deployment + Team Context | date: {generation-date} -->

# Project Governance

## Sprint Cadence

<!-- begin: AP-sourced -->
- Sprint length: {duration}
- Planning: {when}
- Daily standup: {time}
- Review: {when}
- Retrospective: {when}
<!-- end: AP-sourced -->

## Quality Gates

<!-- begin: AP-sourced -->
| Gate | Requirement | Enforced By |
|------|-------------|-------------|
| PR Approval | {n} reviewers + CODEOWNER | Git platform |
| CI Pass | Lint + Test + Build + Security | CI pipeline |
| DoD Verified | All DEFINITION_OF_DONE items checked | Reviewer |
| Security Review | Required for auth/data changes | Security role |
<!-- end: AP-sourced -->

## Escalation

<!-- begin: AP-sourced -->
| Situation | Action | Timeline |
|-----------|--------|----------|
| Blocker | Escalate to tech lead | Within {hours} |
| Architecture deviation needed | ADR required | Before implementation |
| Security concern | Flag immediately | Do not proceed until resolved |
| Scope creep detected | Discuss with PM | Before accepting |
<!-- end: AP-sourced -->

## Decision Making

<!-- begin: AP-sourced -->
- Architecture decisions: ADR process (evaluate options → recommend → approve)
- Technology additions: ADR + team discussion
- Process changes: Retro action items → team agreement
<!-- end: AP-sourced -->
```

## Filling: Refer to `mapping/team-to-agreements.md` (Target 7).
