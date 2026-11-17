<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: brownfield-patterns.md (Conditional Steering File)

**Trigger:** AI-ADLC input mode was "Brownfield" (from `adlc-state.md` → `Input Mode: Brownfield`) OR Mode 3 Brownfield Overlay detected existing codebase with legacy integration context.

**Purpose:** Provide prescriptive rules for working alongside, extending, or migrating from an existing system. These rules constrain how developers interact with legacy boundaries, ensure characterization testing before changes, and enforce migration guardrails.

---

## Template

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Brownfield Strategy ADR + Integration Architecture (Legacy Patterns) | date: {generation-date} -->

# Brownfield Patterns — {System Name}

## Brownfield Context

**Strategy:** {from Brownfield Strategy ADR — e.g., Strangler Fig / Module Extract / Extend In-Place}
**Existing system:** {from AP — name, technology, relationship}
**Transition phase:** {current phase — e.g., Phase 2: Build + Route}
**Coexistence duration:** {from AP — estimated parallel operation period}

---

## Anti-Corruption Layer (ACL) Rules

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| BF-ACL-01 | ALL interactions with the legacy system MUST go through the Anti-Corruption Layer — NEVER call legacy APIs directly from business logic |
| BF-ACL-02 | The ACL translates BOTH directions: our domain model → legacy format (outbound) AND legacy format → our domain model (inbound) |
| BF-ACL-03 | ACL adapters are stateless — pure translation with NO business logic inside |
| BF-ACL-04 | ACL interfaces are defined in OUR domain language, not legacy terminology — the rest of our system never sees legacy concepts |
| BF-ACL-05 | Each legacy integration point has its own adapter class/module — do NOT share adapters across different legacy APIs |
| BF-ACL-06 | ACL code lives in a dedicated module: `{from AP — e.g., src/infrastructure/legacy-adapters/}` — clearly separated from domain code |
| BF-ACL-07 | When the legacy system is decommissioned: replace the ACL adapter with a direct implementation — the interface STAYS the same |

<!-- end: AP-sourced -->

---

## Characterization Testing

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| BF-CHAR-01 | NEVER modify, extend, or replace a legacy integration point without characterization tests covering its OBSERVED behavior |
| BF-CHAR-02 | Characterization tests verify what the legacy system ACTUALLY does (not what documentation says it does) — document discovered behavior |
| BF-CHAR-03 | Capture at minimum: happy path responses, error responses, edge cases, timeout behavior, and partial failure modes |
| BF-CHAR-04 | Characterization tests run in CI — they serve as regression detection for the legacy boundary |
| BF-CHAR-05 | When writing new code that replaces legacy behavior: the new implementation MUST pass all characterization tests before go-live |
| BF-CHAR-06 | Undocumented legacy behavior discovered during characterization: log in `management_framework/Issue_Log.md` and decide: replicate or fix |

<!-- end: AP-sourced -->

---

## Legacy API Compatibility

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| BF-API-01 | {from AP — e.g., All existing API endpoints consumed by the legacy system MUST remain operational during transition — zero breaking changes} |
| BF-API-02 | New API versions can be introduced alongside legacy endpoints — but legacy endpoints are NOT removed until all consumers migrate |
| BF-API-03 | Response format changes to legacy-consumed endpoints require explicit consumer notification + migration period (minimum {from AP — e.g., 2 sprints}) |
| BF-API-04 | API routing between legacy and new system is controlled by {from AP — e.g., feature flags / reverse proxy rules / header-based routing} |
| BF-API-05 | Monitor legacy API usage — track which consumers still call old endpoints to plan decommission timeline |

<!-- end: AP-sourced -->

---

## Data Migration Guardrails

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| BF-DATA-01 | Database migrations MUST be backward-compatible — the legacy system must continue functioning after migration runs |
| BF-DATA-02 | Data coexistence strategy: {from AP — e.g., shared database / event-based sync / dual-write} — follow the pattern defined in the Brownfield Strategy ADR |
| BF-DATA-03 | NEVER migrate data without a validated rollback plan — test rollback in staging BEFORE production |
| BF-DATA-04 | Large data migrations: run in batches with progress tracking — NEVER lock tables for extended periods |
| BF-DATA-05 | Data validation after migration: row counts, referential integrity, business rule verification — automated comparison against source |
| BF-DATA-06 | Legacy data that doesn't fit the new model: transform during migration via explicit mapping rules — NEVER silently drop or truncate |
| BF-DATA-07 | Migration scripts are versioned, idempotent, and logged — every migration records: start time, end time, rows affected, validation result |

<!-- end: AP-sourced -->

---

## Strangler Fig Boundaries

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| BF-STR-01 | {from AP — e.g., Feature routing decisions are controlled by configuration (feature flags or proxy rules) — NOT by code branches} |
| BF-STR-02 | Each migrated feature is independently deployable — migration of feature A does NOT depend on migration of feature B |
| BF-STR-03 | Rollback granularity: individual features can be routed back to legacy without affecting other migrated features |
| BF-STR-04 | Before routing production traffic to new implementation: verify equivalent behavior via shadow traffic or parallel comparison |
| BF-STR-05 | Monitor BOTH legacy and new paths during transition: compare latency, error rate, and response correctness |
| BF-STR-06 | Decommission trigger per feature: {from AP — e.g., 4 weeks with 0 traffic to legacy path AND no reported issues} |

<!-- end: AP-sourced -->

---

## Transition Phase Rules

<!-- begin: AP-sourced -->

### Current Phase: {from AP — Phase N: Name}

| Rule | Standard |
|------|----------|
| BF-PHASE-01 | Code changes in this phase are scoped to: {from AP — e.g., new module only / integration layer only / specific bounded contexts} |
| BF-PHASE-02 | Legacy code modifications: {from AP — e.g., NOT allowed in this phase / allowed for bug fixes only / allowed with characterization tests} |
| BF-PHASE-03 | Phase completion criteria: {from AP — e.g., all features in scope routed to new system + 2 weeks stability} |
| BF-PHASE-04 | Phase gate: {from AP — e.g., team review + stakeholder sign-off before proceeding to next phase} |

<!-- end: AP-sourced -->

---

## Anti-Patterns (DO NOT)

1. **DO NOT** modify legacy code "just to make integration easier" — use the ACL
2. **DO NOT** assume legacy behavior based on documentation — verify with characterization tests
3. **DO NOT** share database transactions across legacy and new system boundaries
4. **DO NOT** deploy legacy and new system changes in the same release (unless tightly coupled by design)
5. **DO NOT** remove legacy code or endpoints until decommission criteria are met AND verified
6. **DO NOT** skip the parallel comparison phase — "it works in staging" is insufficient for production cutover
7. **DO NOT** introduce direct dependencies from new code to legacy internal types/schemas — always use the ACL
8. **DO NOT** treat brownfield as "greenfield but skip some stages" — the constraints are fundamentally different
```

---

## Filling Instructions

This template is populated by `mapping/brownfield-to-steering.md`.

**Source artifacts:**
- Brownfield Strategy ADR (transition strategy, phases, boundaries)
- Integration Architecture — Legacy Patterns section (ACL, strangler fig, data sync)
- `adlc-state.md` → `Input Mode: Brownfield` confirmation
- Data Architecture (data migration approach, coexistence strategy)
- Security Architecture (legacy system access patterns)

**Cross-references after generation:**
- Verify ACL module path matches `module-structure.md`
- Verify API compatibility rules consistent with `api-standards.md`
- Verify data migration rules consistent with `database-rules.md`
- Verify phase rules consistent with `project-governance.md`

**Generation trigger:**
- CONDITIONAL: Only generate when `adlc-state.md` shows `Input Mode: Brownfield` OR Mode 3 overlay is active with legacy context in the AP
- If AP has no brownfield context (pure greenfield) → SKIP this file entirely

**Depth adaptation:**
- Minimal: ACL rules + characterization testing + data migration basics (~15 rules)
- Standard: Full structure as defined above (~30 rules)
- Comprehensive: Full + legacy system behavior catalog + migration runbook template + rollback decision matrix + compliance implications per phase
