<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: generated
---
# Template: templates/estimation-guide.md

```markdown
# Estimation Guide

## Size Scale

| Size | Effort | Complexity | Uncertainty | Typical Duration |
|:----:|:------:|:----------:|:-----------:|:----------------:|
| **S** | 1-2 hours | Single module, known pattern | Low | Half day |
| **M** | 4-8 hours | 1-2 modules, standard work | Low-Medium | 1 day |
| **L** | 2-3 days | Multiple modules, some design | Medium | 2-3 days |
| **XL** | 4-5 days | Cross-cutting, new patterns | High | 1 week |
| **XXL** | >5 days | Split this into smaller tasks | — | Split required |

## Size Indicators

### Small (S)
- Bug fix with clear root cause
- Add field to existing entity (API + DB + UI)
- Simple CRUD endpoint following existing pattern
- Configuration change
- Test addition for existing code

### Medium (M)
- New endpoint with business logic
- Integration with existing external service (pattern exists)
- New entity with standard CRUD
- Refactoring within one module
- Performance optimization (identified bottleneck)

### Large (L)
- New feature spanning 2+ modules
- New external integration (pattern doesn't exist yet)
- New workflow/state machine
- Significant refactoring crossing module boundaries
- Database migration with data transformation

### Extra-Large (XL)
- Cross-cutting concern (affects all modules)
- New bounded context / module creation
- Architecture pattern change within a module
- Major version upgrade of core dependency

## Multipliers

| Condition | Multiply By |
|-----------|:-----------:|
| First time using this pattern | ×1.5 |
| Involves security-sensitive code | ×1.3 |
| Requires database migration | ×1.2 |
| Cross-module dependency | ×1.3 |
| Unclear requirements | ×1.5 |
| No existing tests for area | ×1.3 |

## Rules

1. **XXL = must split** — nothing stays XXL; break into L or XL pieces
2. **Uncertainty adds size** — if you're not sure how to do it, size up
3. **Include testing** — estimates include writing tests (not just code)
4. **Include review time** — PR feedback cycle is part of the estimate
5. **Compare to past work** — "this is similar in size to {previous task}"
```
