<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: generated
---
# Template: .github/pull_request_template.md

```markdown
## Summary
{Brief description}

## Type
- [ ] Feature (`feat`)
- [ ] Bug fix (`fix`)
- [ ] Refactor (`refactor`)
- [ ] Documentation (`docs`)
- [ ] Tests (`test`)
- [ ] Chore (`chore`)

## Related
- Ticket: {PROJ-XXX}
- Related PRs: {if any}

## Changes
- {Change 1}
- {Change 2}

## Checklist
- [ ] Follows workspace-rules.md
- [ ] Module boundaries respected (module-structure.md)
- [ ] Domain terminology correct (domain-context.md)
- [ ] Tests added/updated
- [ ] Error handling per error-handling.md
- [ ] No sensitive data in logs
- [ ] Tenant scoping applied (if applicable)
- [ ] API follows api-standards.md (if API changes)
- [ ] Migration included (if DB changes)
- [ ] Documentation updated (if needed)

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing: {describe}

## Screenshots (if UI)
{Before/After or N/A}
```

## Filling: Refer to `mapping/governance-derivation.md` (Target 4).
