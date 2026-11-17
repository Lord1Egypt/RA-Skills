<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: generated
---
# Template: templates/session-planning.md

```markdown
# Session Planning — {Task Title}

## Task
**Ticket:** {ticket-id}
**Type:** {feature / bugfix / refactor}
**Module(s):** {affected modules from module-structure.md}

## Steering Files to Load
- [ ] workspace-rules.md (always)
- [ ] module-structure.md (always)
- [ ] domain-context.md (always)
- [ ] coding-standards.md (always)
- [ ] {additional relevant steering files for this task}

## Acceptance Criteria
1. {criterion from ticket}
2. {criterion}
3. {criterion}

## Approach
1. {step 1 — what to implement first}
2. {step 2}
3. {step 3}

## Files to Create/Modify
| File | Action | Module |
|------|--------|--------|
| {path} | Create / Modify | {module} |
| ... | ... | ... |

## Test Plan
| Test Type | What to Test |
|-----------|-------------|
| Unit | {specific logic to test} |
| Integration | {API/service to test} |

## Risks / Questions
- {any uncertainty or clarification needed}

## DoD Verification
After implementation, verify against DEFINITION_OF_DONE.md.
```
