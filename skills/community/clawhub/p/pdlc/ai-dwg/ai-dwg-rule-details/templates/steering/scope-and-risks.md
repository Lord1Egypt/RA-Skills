<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: scope-and-risks.md

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: System Context (C4 L1) + Architecture Workbook | date: {generation-date} -->

# Scope & Risks

## In Scope

<!-- begin: AP-sourced -->
This system provides:
- {module/capability from C4 L1 boundary — list all}
- ...

Modules: {list from module-structure.md}
<!-- end: AP-sourced -->

## Out of Scope

<!-- begin: AP-sourced -->
Explicitly NOT part of this system:
- {item from Architecture Vision exclusions}
- ...

Deferred to future versions:
- {deferred items if mentioned in AP}
<!-- end: AP-sourced -->

## Known Risks

<!-- begin: AP-sourced -->
| # | Risk | Impact | Likelihood | Mitigation |
|---|------|--------|:----------:|-----------|
| R1 | {from Architecture Workbook — open items/risks} | {impact} | {H/M/L} | {current approach} |
| ... | ... | ... | ... | ... |
<!-- end: AP-sourced -->

## Assumptions

<!-- begin: AP-sourced -->
| # | Assumption | If Wrong |
|---|-----------|----------|
| A1 | {from Architecture Workbook} | {consequence} |
| ... | ... | ... |
<!-- end: AP-sourced -->

## Constraints Reminder

See workspace-rules.md Constraints section for non-negotiable limitations.
```

## Filling: Refer to `mapping/team-to-agreements.md` (Target 8).
