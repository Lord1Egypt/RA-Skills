<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: module-structure.md

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Component Design (C4 L3) | date: {generation-date} -->

# Module Structure

## Architecture Style
{style} — {description}

## Modules
<!-- begin: AP-sourced -->
| Module | Responsibility | Bounded Context | Owner |
|--------|---------------|-----------------|-------|
| `{module}` | {responsibility} | {context} | {owner} |
| `shared` | Cross-cutting utilities | Platform | {architect} |
<!-- end: AP-sourced -->

## Dependency Rules
<!-- begin: AP-sourced -->
### Allowed
| From | Can Depend On | Reason |
|------|---------------|--------|
| {module-a} | `shared` | Shared kernel |
| ... | ... | ... |

### Forbidden
| From | MUST NOT Depend On | Reason |
|------|-------------------|--------|
| Any | Another module's internals | Encapsulation |
| ... | ... | ... |
<!-- end: AP-sourced -->

## Layer Rules (If Applicable)
<!-- begin: AP-sourced -->
| Layer | Can Reference | MUST NOT Reference |
|-------|---------------|-------------------|
| domain/ | Nothing | infrastructure/, api/ |
| application/ | domain/ | infrastructure/ directly |
| infrastructure/ | domain/, application/ | Other module's infra |
| api/ | application/ | domain/ directly |
<!-- end: AP-sourced -->

## Public Interface Convention
Every module exposes via single barrel file (`index.{ext}`).
Other modules import ONLY from barrel — never internal paths.

## Anti-Patterns
1. NO circular dependencies
2. NO bypassing barrel imports
3. NO business logic in shared/
4. NO god modules
```

## Filling: Refer to `mapping/components-to-structure.md` (Target 3).
