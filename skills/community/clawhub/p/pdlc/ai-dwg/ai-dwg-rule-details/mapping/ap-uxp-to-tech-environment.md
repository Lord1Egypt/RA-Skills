<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Architecture Package + UXP → architecture/technical-environment.md (ADLC CLUSTER)

## Purpose

Assembles the **Technical Environment Document** that AI-DLC v1 expects as one of its two primary human-authored inputs. This document answers "What tools and constraints define our build environment?" — combining technology decisions from AI-ADLC with frontend patterns from AI-UXD.

**Output:** `{workspace-root}/architecture/technical-environment.md`

**Condition:** Generate IF `adlc-state.md` is present (ADLC peer input detected).

**Enrichment:** If `uxd-state.md` is ALSO present, the Frontend Patterns section is enriched with design system references, component library specification, and token format.

**Cluster:** Tech (primary) + UX (frontend enrichment)

---

## MANDATORY: Stage Sub-Role — Systems Engineer

During THIS activity, ALSO adopt the mindset of a **Systems Engineer**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in constraints — the Technical Environment Document tells AI-DLC v1 what it CAN and CANNOT use
- Be specific — "PostgreSQL 16" not "a relational database"; "React 18 with TypeScript" not "a modern frontend"
- Include allow/disallow lists — AI-DLC v1 uses these to restrict tool selection during code generation
- Frontend patterns from UXD are equally authoritative as backend patterns from ADLC

### Anti-Patterns for This Activity
- Do NOT include product vision or user stories (that's `info/vision.md`)
- Do NOT be vague about technology choices — specificity is the point
- Do NOT omit the frontend section when UXD is present — it's a first-class part of the tech environment
- Do NOT duplicate full token definitions (those live in `design-system.md`) — reference the format and system name

---

## Source Inputs

### Primary: AI-ADLC → Architecture Package (AP)

| AP Document | What to Extract | Maps to Tech-Env Section |
|---|---|---|
| Technology Stack | Languages, frameworks, runtimes, versions | Tech Summary, Languages & Frameworks |
| Infrastructure & Deployment | Cloud services, deployment topology | Cloud Services (allow/disallow) |
| Security Architecture | Auth mechanisms, encryption, compliance | Security Requirements |
| API Architecture | API patterns, protocols | Architecture Patterns |
| Component Design (C4 L3) | Module patterns, layering | Architecture Patterns |
| Quality Attributes | Testing requirements, performance targets | Testing Requirements |
| ADRs | Key technology decisions with rationale | Referenced throughout |

### Enrichment: AI-UXD → UX Design Package (UXP) — IF PRESENT

| UXP Document | What to Extract | Maps to Tech-Env Section |
|---|---|---|
| Design System Document | Component library name, token format, design tool references | Frontend Patterns |
| Design Tokens Specification | Token delivery format (CSS vars / Style Dictionary / JSON) | Frontend Patterns |
| Component Inventory | Component architecture style (Atomic Design, etc.) | Frontend Patterns |
| Accessibility Baseline | WCAG level, testing tools | Testing Requirements (a11y subsection) |

---

## Target Structure: technical-environment.md

```markdown
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AI-ADLC Architecture Package + AI-UXD Frontend Patterns"
generatedOn: "{generation-date}"
ownership: hybrid
---

<!-- AI-DWG generated | source: AI-ADLC AP + AI-UXD UXP | date: {generation-date} -->

# Technical Environment Document

## Tech Summary
<!-- begin: AP-sourced -->
| Aspect | Decision |
|--------|----------|
| Primary Language | {language + version} |
| Backend Framework | {framework + version} |
| Frontend Framework | {framework + version} |
| Database | {database + version} |
| Cache | {cache technology} |
| Message Queue | {queue technology} |
| Cloud Platform | {cloud provider} |
| Container Runtime | {runtime} |
| CI/CD | {tool} |
<!-- end: AP-sourced -->

## Languages & Frameworks

### Allowed
<!-- begin: AP-sourced -->
| Technology | Version | Purpose | ADR |
|-----------|---------|---------|-----|
| {language} | {version} | {purpose} | {ADR-ref} |
| {framework} | {version} | {purpose} | {ADR-ref} |
| ... | ... | ... | ... |
<!-- end: AP-sourced -->

### Disallowed
<!-- begin: AP-sourced -->
| Technology | Reason | Alternative |
|-----------|--------|-------------|
| {tech} | {why not} | {use instead} |
| ... | ... | ... |
<!-- end: AP-sourced -->

## Cloud Services

### Allowed
<!-- begin: AP-sourced -->
| Service | Purpose | Constraints |
|---------|---------|-------------|
| {service} | {purpose} | {constraints} |
| ... | ... | ... |
<!-- end: AP-sourced -->

### Disallowed
<!-- begin: AP-sourced -->
| Service | Reason |
|---------|--------|
| {service} | {reason} |
| ... | ... |
<!-- end: AP-sourced -->

## Architecture Patterns
<!-- begin: AP-sourced -->
| Pattern | Scope | Rationale |
|---------|-------|-----------|
| {pattern — e.g., Layered Architecture} | {where applied} | {ADR reference} |
| {pattern — e.g., CQRS} | {where applied} | {ADR reference} |
| ... | ... | ... |
<!-- end: AP-sourced -->

## Frontend Patterns
<!-- begin: UXP-sourced (if UXD present) / AP-sourced (if UXD absent) -->

### IF UXD PRESENT:
| Aspect | Specification |
|--------|--------------|
| Component Library | {from UXP — design system name + architecture style} |
| Design Token Format | {from UXP — e.g., W3C Design Tokens / Style Dictionary JSON / CSS custom properties} |
| Token Delivery | {how tokens reach code — e.g., npm package / generated CSS / JSON import} |
| Component Architecture | {from UXP — e.g., Atomic Design: atoms → molecules → organisms} |
| State Management | {from AP Technology Stack} |
| Styling Approach | {from AP + UXP — e.g., CSS Modules with design tokens / Tailwind with token overrides} |
| Design System Reference | See `rules/design-system.md` for full token inventory and component rules |

### IF UXD ABSENT:
| Aspect | Specification |
|--------|--------------|
| UI Framework | {from AP Technology Stack} |
| State Management | {from AP Technology Stack} |
| Styling | {from AP Technology Stack} |
| Component Patterns | {from AP C4 L3 — if UI components described} |
<!-- end: UXP-sourced / AP-sourced -->

## Security Requirements
<!-- begin: AP-sourced -->
| Requirement | Specification |
|-------------|--------------|
| Authentication | {method + provider} |
| Authorization | {model — RBAC/ABAC/etc.} |
| Encryption at Rest | {algorithm} |
| Encryption in Transit | {TLS version} |
| Secrets Management | {approach} |
| Compliance | {standards — SOC2, HIPAA, etc.} |
<!-- end: AP-sourced -->

## Testing Requirements
<!-- begin: AP-sourced -->
| Level | Tool | Coverage Target |
|-------|------|-----------------|
| Unit | {tool} | {target} |
| Integration | {tool} | {target} |
| E2E | {tool} | {target} |
| Performance | {tool} | {SLO targets} |
| Security | {tool} | {scope} |
| Accessibility | {tool — from UXP if present} | {WCAG level} |
<!-- end: AP-sourced -->

## Example Code Patterns
<!-- begin: AP-sourced -->
{Placeholder for team + UXD-seeded code patterns — see examples/ directory}

Reference: `examples/` directory contains starter patterns for:
- API endpoint template
- Database query template
- UI component template (if frontend — seeded from UXP if present)
<!-- end: AP-sourced -->
```

---

## Transformation Rules

| Source | Output Section | Condition |
|--------|---------------|-----------|
| AP Technology Stack — full selections | Tech Summary + Languages & Frameworks (Allowed) | IF ADLC |
| AP Technology Stack — rejected alternatives | Languages & Frameworks (Disallowed) | IF ADLC |
| AP Infrastructure — cloud services | Cloud Services (allow/disallow) | IF ADLC |
| AP Component Design — patterns + layering | Architecture Patterns | IF ADLC |
| AP Security Architecture | Security Requirements | IF ADLC |
| AP Quality Attributes — test requirements | Testing Requirements | IF ADLC |
| UXP Design System — component lib + tokens | Frontend Patterns (enriched) | IF UXD |
| UXP Accessibility Baseline — tools + level | Testing Requirements (a11y row) | IF UXD |
| ADRs | Referenced throughout (rationale links) | IF ADLC |

### Key Rules

1. **Specificity over generality.** "PostgreSQL 16.2" not "SQL database." "React 18.3 with TypeScript 5.4" not "modern frontend."
2. **Allow/Disallow lists are AI-DLC v1 constraints.** AI-DLC v1 uses these to restrict its code generation — be explicit about what's forbidden.
3. **Frontend Patterns are first-class.** When UXD is present, the Frontend Patterns section is as detailed as Security Requirements. It's not a footnote.
4. **Don't duplicate design-system.md.** Reference it ("See design-system.md for full token inventory") — don't copy all tokens into this file.
5. **ADR references provide rationale.** Every major decision links to an ADR so AI-DLC v1 can understand WHY (helpful for edge cases during code generation).

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| ADLC present, UXD absent | Frontend Patterns section uses AP Technology Stack only. Less detailed but still valid. |
| UXD provides frontend framework that differs from ADLC | Cross-input conflict — surface via conflict gate. Do NOT proceed. |
| No cloud services in AP | Cloud Services section: "No cloud services specified — local development only" |
| AP has no explicit disallow list | Disallowed sections: "No explicit restrictions documented — use judgment" (flag for improvement) |
| UXD token format not recognized | Include as-is: "Token Format: {whatever UXD specified}" — implementation handles format translation |

---

## Output Validation

- [ ] Tech Summary covers all major technology categories
- [ ] All allowed technologies have version numbers
- [ ] Disallow lists are populated (even if brief)
- [ ] Frontend Patterns enriched with UXP content (if UXD present)
- [ ] Security section covers auth, encryption, compliance
- [ ] Testing section includes all levels + accessibility
- [ ] ADR references included for major decisions
- [ ] No product/vision content (that's vision.md)
- [ ] Provenance markers present throughout
