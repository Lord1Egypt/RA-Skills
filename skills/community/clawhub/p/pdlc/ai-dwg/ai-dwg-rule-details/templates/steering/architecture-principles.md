<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: architecture-principles.md

## Template Structure

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Architecture Vision | date: {generation-date} -->

# Architecture Principles

## Vision

{vision-statement — verbatim from AP}

## Principles

<!-- begin: AP-sourced -->

### P1: {Principle Name}

**Statement:** {verbatim}

**Rationale:** {verbatim}

**Implications:**
- {development-implication-1}
- {development-implication-2}
- {code-review-implication}

**Violations look like:**
- {specific-anti-pattern-1}
- {specific-anti-pattern-2}

---

### P2: {Principle Name}

{repeat structure}

<!-- end: AP-sourced -->

## Quality Attributes

<!-- begin: AP-sourced -->

| Priority | Attribute | Target | Measurement |
|:--------:|-----------|--------|-------------|
| Critical | {attribute} | {target} | {verification} |
| High | {attribute} | {target} | {verification} |
| Medium | {attribute} | {target} | {verification} |
| Low | {attribute} | {target} | {verification} |

<!-- end: AP-sourced -->

## Constraints

<!-- begin: AP-sourced -->

| # | Constraint | Source | Impact on Architecture |
|---|-----------|--------|----------------------|
| C1 | {constraint} | {source} | {impact} |
| ... | ... | ... | ... |

<!-- end: AP-sourced -->

## Stakeholder Concerns

<!-- begin: AP-sourced -->

| Stakeholder | Concern | Architecture Response |
|-------------|---------|---------------------|
| {role} | {concern} | {response} |
| ... | ... | ... |

<!-- end: AP-sourced -->
```

## Filling Instructions

Refer to `mapping/vision-to-workspace-rules.md` (Target 2 section).
