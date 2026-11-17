<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: domain-context.md

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Component Design (C4 L3) | date: {generation-date} -->

# Domain Context

## System Domain

**Domain:** {high-level domain}
**Subdomain classification:** {per bounded context below}

## Bounded Contexts

<!-- begin: AP-sourced -->

| Context | Responsibility | Module(s) | Type |
|---------|---------------|-----------|:----:|
| {context-a} | {responsibility} | `{module}` | Core |
| {context-b} | {responsibility} | `{module}` | Supporting |
| ... | ... | ... | ... |

<!-- end: AP-sourced -->

## Context Map

<!-- begin: AP-sourced -->
{ASCII or description of upstream/downstream relationships}

| Upstream | Downstream | Relationship | Pattern |
|----------|-----------|:------------:|---------|
| {ctx-a} | {ctx-b} | Customer-Supplier | {ACL/Events/API} |
| ... | ... | ... | ... |
<!-- end: AP-sourced -->

## Ubiquitous Language

<!-- begin: AP-sourced -->

### {Context A}

| Term | Definition | NEVER Call It |
|------|-----------|--------------|
| {term} | {precise definition} | {wrong synonyms} |
| ... | ... | ... |

### {Context B}

| Term | Definition | NEVER Call It |
|------|-----------|--------------|
| ... | ... | ... |

<!-- end: AP-sourced -->

## Cross-Context Disambiguation

<!-- begin: AP-sourced -->

| Term | In {Context A} | In {Context B} | Rule |
|------|---------------|---------------|------|
| {term} | {meaning-a} | {meaning-b} | {how to resolve} |
<!-- end: AP-sourced -->

## Domain Rules (Invariants)

<!-- begin: AP-sourced -->

| # | Context | Rule | Enforcement |
|---|---------|------|-------------|
| DR-1 | {ctx} | {invariant statement} | {code/DB/both} |
| ... | ... | ... | ... |
<!-- end: AP-sourced -->

## Entity Ownership

<!-- begin: AP-sourced -->

| Entity | Owning Context | Others See As |
|--------|:--------------:|--------------|
| {entity} | {context} | {ID-only / event / read-only} |
| ... | ... | ... |

Rules:
1. ONLY owning context may CREATE/UPDATE/DELETE
2. Others reference by ID only
3. Cross-context data needs → events or API query
<!-- end: AP-sourced -->

## Naming Enforcement

| Rule | Example |
|------|---------|
| Code uses EXACT domain terms | `Incident` not `Ticket` |
| Folders match context terms | `incident-management/` not `ticketing/` |
| DB tables use domain terms | `incidents` not `tickets` |
| API endpoints use domain terms | `/incidents` not `/tickets` |
| Events use context prefix | `IncidentManagement.IncidentCreated` |
```

## Filling: Refer to `mapping/components-to-domain-context.md`.
