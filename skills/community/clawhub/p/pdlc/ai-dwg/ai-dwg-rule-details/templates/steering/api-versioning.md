<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: api-versioning.md (CONDITIONAL)

**Generate IF:** API Architecture specifies multi-version strategy or deprecation lifecycle.

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: API Architecture (versioning) | date: {generation-date} -->

# API Versioning

## Strategy
**Method:** {URL path | header | query param}
**Current:** {v1}  |  **Planned:** {v2 when breaking changes needed}

## Rules
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| VER-01 | Versioning method: {method} |
| VER-02 | Breaking change = {definition} |
| VER-03 | Non-breaking (allowed): {list} |
| VER-04 | New version when: {criteria} |
| VER-05 | Max supported versions: {n} |
<!-- end: AP-sourced -->

## Deprecation Lifecycle
<!-- begin: AP-sourced -->
Active → Deprecated ({n} months) → Sunset (410 Gone)

| Phase | Duration | Support Level |
|-------|----------|--------------|
| Active | Until next version | Full |
| Deprecated | {months} | Security only |
| Sunset | After deprecation | Removed |
<!-- end: AP-sourced -->

## Migration Rules
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| VER-06 | Document ALL changes in migration guide |
| VER-07 | Deprecated endpoints return Sunset header |
| VER-08 | Never break active version |
| VER-09 | Consumer notification: {timeline} |
<!-- end: AP-sourced -->
```

## Filling: Refer to `mapping/api-to-steering.md` (Target 2).
