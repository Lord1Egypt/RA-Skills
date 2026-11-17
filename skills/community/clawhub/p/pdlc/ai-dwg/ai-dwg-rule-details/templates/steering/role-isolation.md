<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: role-isolation.md

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Team Context + Methodology | date: {generation-date} -->

# Role Isolation

## Roles in Development Workflow

<!-- begin: AP-sourced -->

| Role | Responsibilities | MUST NOT |
|------|-----------------|----------|
| Architect | Define architecture, approve ADRs, review boundary changes | Write feature code without ADR for decisions |
| Developer | Implement per steering rules, write tests | Make arch decisions without ADR, violate boundaries |
| QA | Define test scenarios, verify acceptance criteria | Skip security tests, approve without verification |
| Security | Review auth/authz changes, validate security rules | Block non-security PRs, override architect |
| PM | Define requirements, prioritize, accept deliverables | Dictate technical approach |

<!-- end: AP-sourced -->

## AI Role (During AI-DLC v1 Sessions)

<!-- begin: AP-sourced -->

| AI MUST | AI MUST NOT |
|---------|------------|
| Follow ALL steering files | Invent patterns outside steering |
| Ask when unclear | Assume when rules conflict |
| Match coding-standards.md | Use patterns from other projects |
| Respect module boundaries | Create cross-module deps without flagging |
| Log deviations | Silently deviate |
| Complete one task fully before next | Start multiple tasks in parallel |

<!-- end: AP-sourced -->

## Segregation of Duties

<!-- begin: AP-sourced -->

| Decision Type | Approved By |
|--------------|-------------|
| Architecture decisions | Architect |
| Code changes | Peer + CODEOWNER |
| Security-sensitive changes | Security role |
| Steering file changes | Architect / Tech Lead |
| DoD exceptions | Tech Lead (documented) |
| Scope changes | PM + Architect |

<!-- end: AP-sourced -->
```

## Filling: Refer to `mapping/team-to-agreements.md` (Target 2).
