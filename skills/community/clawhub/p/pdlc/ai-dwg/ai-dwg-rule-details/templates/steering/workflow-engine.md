<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: workflow-engine.md (CONDITIONAL)

**Generate IF:** Component Design includes workflow/state-machine component.

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Component Design (workflow component) | date: {generation-date} -->

# Workflow Engine Standards

## Workflow Model
**Engine:** {from AP — e.g., custom state machine / Temporal / Camunda}
**Storage:** {where workflow state lives}
**Execution:** {sync / async / event-driven}

## Rules
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| WF-01 | All business workflows defined as state machines with explicit states + transitions |
| WF-02 | State transitions: validate preconditions BEFORE transition — reject invalid |
| WF-03 | Workflow definitions: stored as configuration — not hardcoded in business logic |
| WF-04 | Audit: every state transition logged (who, when, from-state, to-state, reason) |
| WF-05 | Timeout: define max time per state — escalate or auto-transition on expiry |
| WF-06 | Versioning: workflow definition changes don't break in-flight instances |
| WF-07 | Visualization: workflow definitions exportable for diagramming |
| WF-08 | Tenant-scoped: workflow instances belong to a tenant (if multi-tenant) |
| WF-09 | Idempotent transitions: re-applying same transition = no-op (not error) |
| WF-10 | Recovery: crashed workflow instances resume from last persisted state |
<!-- end: AP-sourced -->

## State Machine Pattern
<!-- begin: AP-sourced -->
- States: named, finite, documented
- Transitions: named, guarded (preconditions), audited
- Actions: side effects triggered on enter/exit/transition
- Events: external triggers that cause transitions
<!-- end: AP-sourced -->
```

## Filling: Derive from Component Design workflow component section.
