<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: generated
---
# Template: DEFINITION_OF_DONE.md

```markdown
<!-- AI-DWG generated | source: Quality Attributes + multiple AP sources | date: {generation-date} -->

# Definition of Done

A task is DONE when ALL applicable items pass. No exceptions.

## Code Quality
- [ ] Follows coding-standards.md
- [ ] Respects module-structure.md boundaries
- [ ] Domain terminology from domain-context.md
- [ ] Error handling per error-handling.md
- [ ] No new lint warnings
- [ ] No TODO/FIXME without ticket

## Testing
- [ ] Unit tests for new/changed logic
- [ ] All tests pass
- [ ] Integration tests for API/service changes
- [ ] Coverage: {target — does not decrease}
- [ ] Edge cases covered

## Security
- [ ] No secrets in code (DATA-06)
- [ ] Input validated (SEC-01)
- [ ] Auth checked for new endpoints (AUTHZ-05)
- [ ] No sensitive data in logs (SENS rules)
- [ ] Tenant scoping verified (if multi-tenant)

## Observability
- [ ] Logging for significant operations
- [ ] Correct log levels
- [ ] No sensitive data in logs

## Database (if schema changes)
- [ ] Migration created + tested
- [ ] Naming conventions followed
- [ ] Indexes for new queries
- [ ] Tenant scoping on new tables

## API (if endpoint changes)
- [ ] Follows api-standards.md
- [ ] Error format standard
- [ ] OpenAPI docs updated
- [ ] Pagination applied

## Documentation
- [ ] Code comments for complex logic
- [ ] README updated if setup changed
- [ ] API docs updated
- [ ] ADR if architecture decision made

## Review & Merge
- [ ] PR template completed
- [ ] Required approvals received
- [ ] CI passes
- [ ] No merge conflicts
- [ ] Branch up-to-date
```

## Filling: Refer to `mapping/quality-to-dod.md`.
