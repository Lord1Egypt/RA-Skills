<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Domain Context — Derivation Logic

## Purpose

Derives domain context enforcement rules (DOM-*) from `domain-context.md`. Ensures code uses the correct ubiquitous language, respects bounded context boundaries, and follows domain rules.

---

## MANDATORY: Stage Sub-Role — Workspace Architect

During THIS activity, ALSO adopt the mindset of a **Workspace Architect**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in ubiquitous language: the domain glossary is the single source of truth for ALL entity, method, and variable names
- Enforce bounded context isolation: vocabulary from one context must NOT leak into another
- Treat domain-layer purity as architectural: zero infrastructure dependencies in the domain layer
- Ensure domain events use the EXACT names stated in domain-context.md — synonyms are violations
- Consider that AI is particularly prone to inventing "close enough" names — this hook prevents that drift

### Anti-Patterns for This Activity
- Do NOT allow AI to use synonyms or abbreviations not in the glossary (e.g., "usr" instead of "User")
- Do NOT conflate domain vocabulary enforcement (DOM-*) with file naming format (NC-*)
- Do NOT skip domain-layer-purity check — infrastructure dependencies in domain layer are architectural violations

### Quality Check
A good output from this activity sounds like:
- "DOM-01: Code uses stated entity names from glossary. Verification: no class/variable uses 'Ticket' when domain-context.md defines 'Incident'. Hook: domain-layer-purity.json (agentStop)."
- "DOM-05: Domain layer has ZERO infrastructure dependencies. Pattern: `src/modules/*/domain/**/*.ts`. Verification: no imports from `@nestjs/`, `typeorm`, or `node:` modules."

---

## Source: `domain-context.md`

| Section | Generated Rules |
|---------|----------------|
| Ubiquitous language glossary | DOM-01: Code uses stated entity/concept names — no synonyms or abbreviations |
| Bounded context boundaries | DOM-02: Each module stays within its bounded context vocabulary |
| Domain invariants | DOM-03: Stated invariants enforced in domain layer code |
| Domain events | DOM-04: Cross-context communication uses stated event names |
| DDD layer purity (if DDD) | DOM-05: Domain layer has ZERO infrastructure dependencies |

## Hook: `domain-layer-purity.json`

- **Event:** agentStop (Tier B)
- **Pattern:** Domain layer files (e.g., `**/domain/**/*.{ext}`)
- **Checks:** DOM-05 (no infra deps), DOM-01 (naming matches glossary)

## Tier: 1 (domain language is foundational — prevents AI from inventing wrong names from Day 0)
