<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: coding-standards.md

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Technology Stack + Component Design | date: {generation-date} -->

# Coding Standards

## Language Conventions

<!-- begin: AP-sourced -->
{Technology-specific conventions — derived from framework + language choice}
- File naming: {convention}
- Exports: {convention}
- Typing: {strict/partial — from AP}
<!-- end: AP-sourced -->

## Code Patterns

<!-- begin: AP-sourced -->
| Pattern | Usage | Example |
|---------|-------|---------|
| Dependency Injection | {framework DI approach} | {brief example} |
| Repository Pattern | Data access abstraction | {brief} |
| Service Pattern | Business logic encapsulation | {brief} |
| {additional patterns from AP} | ... | ... |
<!-- end: AP-sourced -->

## File Organization

<!-- begin: AP-sourced -->
{Module/layer structure conventions — from component design}
- One class per file
- Co-locate tests with source (or separate — per AP)
- Barrel exports from module index
<!-- end: AP-sourced -->

## Import Rules

<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| CS-IMP-01 | Import from module barrel (index) — never from internal paths |
| CS-IMP-02 | Import order: framework → external → internal → relative |
| CS-IMP-03 | No circular imports — enforced by linter |
<!-- end: AP-sourced -->

## Async Patterns

<!-- begin: AP-sourced -->
{From technology stack — async/await, Promises, Observables, etc.}
<!-- end: AP-sourced -->

## Anti-Patterns

<!-- begin: AP-sourced -->
1. {technology-specific anti-patterns}
2. ...
<!-- end: AP-sourced -->
```

## Filling: Refer to `mapping/team-to-agreements.md` (Target 3).
