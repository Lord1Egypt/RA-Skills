<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# ADR-{NNN}: Brownfield Strategy — {System/Module Name}

**Status:** Proposed | Accepted | Deprecated | Superseded
**Date:** {YYYY-MM-DD}
**Deciders:** {Names/Roles — typically CTO, Tech Lead, Product Owner}
**Category:** Platform | Architecture

---

## Context

{Describe the existing system and the business driver for change. Include:
- What exists today (technology, age, state, known issues)
- What the business wants (new capability, modernization, replacement)
- Why the existing system can't simply stay as-is
- Team familiarity with the existing system
- Timeline and risk tolerance}

### Existing System Profile

| Aspect | Current State |
|--------|--------------|
| **System name** | {existing system name} |
| **Age** | {years in production} |
| **Technology** | {tech stack — language, framework, database} |
| **Size** | {approximate — LOC, modules, endpoints, tables} |
| **Health** | {Healthy / Aging / Legacy / Critical tech debt} |
| **Documentation** | {Well-documented / Partial / Undocumented} |
| **Test coverage** | {High (>70%) / Moderate (30-70%) / Low (<30%) / None} |
| **Active development** | {Active / Maintenance-only / Frozen} |
| **Data volume** | {approximate — rows, storage, growth rate} |
| **User base** | {who depends on it today} |

---

## Decision Drivers

- {Driver 1 — e.g., "New capability cannot be built within existing architecture limitations"}
- {Driver 2 — e.g., "Existing system must remain operational during transition (zero downtime requirement)"}
- {Driver 3 — e.g., "Team has limited knowledge of legacy codebase"}
- {Driver 4 — e.g., "Data migration complexity (X million records, Y relationships)"}
- {Driver 5 — e.g., "Budget constraint limits parallel development capacity"}
- {Principle reference — e.g., "P3: Operational Simplicity — must not increase operational burden during transition"}

---

## Considered Options

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **(a) Extend In-Place** | Add new functionality within the existing system architecture | No migration risk; immediate integration; uses existing knowledge | Inherits all technical debt; limited by legacy architecture; may not support new requirements |
| **(b) Strangler Fig** | Build new functionality alongside existing system; gradually route traffic/features to new; decommission old piece by piece | Low risk per increment; existing system stays operational; allows learning; reversible at each step | Longer timeline; dual maintenance during transition; requires routing/facade layer; integration complexity |
| **(c) Big Bang Replace** | Build complete replacement; switch over in one deployment | Clean architecture; no legacy compromise; fastest path to ideal state | High risk; long period with no delivery; "all-or-nothing" go-live; requires parallel operation for testing |
| **(d) Module Extract** | Extract specific bounded contexts from the existing system into new services/modules; keep the rest | Focused scope; incremental value; learns from each extraction | Requires clear module boundaries in legacy (often entangled); extraction is complex; testing both sides |
| **(e) Parallel Run + Migrate** | Build new system; run both in parallel comparing outputs; migrate data when confidence is high | Validates correctness before cutover; low user risk | Expensive (double infrastructure); complex data sync; long parallel period |

---

## Decision

**Chosen:** Option ({x}) — {Name}

{State the chosen approach clearly in 1-2 sentences.}

---

## Rationale

{Why is this the best option given the context and drivers? Connect the decision to specific constraints, risks, and team capabilities. Address why rejected options were not suitable.}

---

## Transition Architecture

### Boundary Definition

```
┌─────────────────────────────────────────────────────────────────┐
│                    TRANSITION STATE                               │
│                                                                   │
│  ┌──────────────────────┐     ┌──────────────────────────────┐  │
│  │   EXISTING SYSTEM    │     │       NEW SYSTEM/MODULE       │  │
│  │                      │     │                               │  │
│  │  {what stays}        │◄───►│  {what's new}                │  │
│  │                      │     │                               │  │
│  └──────────────────────┘     └──────────────────────────────┘  │
│              │                              │                      │
│              ▼                              ▼                      │
│  ┌──────────────────────┐     ┌──────────────────────────────┐  │
│  │   SHARED DATA        │     │   NEW DATA STORE             │  │
│  │   (existing DB)      │     │   (if applicable)            │  │
│  └──────────────────────┘     └──────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Integration During Transition

| Integration Point | Mechanism | Direction | Notes |
|------------------|-----------|:---------:|-------|
| {Point 1 — e.g., User authentication} | {e.g., Shared auth service / SSO} | Bidirectional | {e.g., Both systems use same identity provider} |
| {Point 2 — e.g., Shared data} | {e.g., API / Shared DB / Sync} | {direction} | {notes on data ownership} |
| {Point 3 — e.g., UI routing} | {e.g., Reverse proxy / Feature flag} | {direction} | {how users see one system} |

### Transition Phases

| Phase | Duration | What Happens | Success Criteria |
|-------|:--------:|-------------|-----------------|
| 1 — Characterize | {weeks} | Understand existing system behavior; add characterization tests; document interfaces | Legacy behavior documented; key tests green |
| 2 — Scaffold | {weeks} | Build new system/module structure; establish integration points with legacy | New system deploys; connects to legacy; no user impact |
| 3 — Build + Route | {weeks/months} | Implement new features; gradually route traffic/features to new system | Features working in new system; metrics comparable |
| 4 — Migrate | {weeks} | Move remaining functionality/data; decommission legacy components | All traffic on new system; legacy components shut down |
| 5 — Cleanup | {weeks} | Remove transition scaffolding; simplify architecture | No legacy references; clean architecture |

---

## Data Strategy

| Aspect | Approach |
|--------|----------|
| **Data ownership during transition** | {e.g., Legacy DB is source of truth until Phase 4 / Shared ownership with sync / New system owns new data immediately} |
| **Migration approach** | {e.g., Big-bang data migration at cutover / Incremental sync / Dual-write during transition} |
| **Rollback capability** | {e.g., Can revert to legacy within X hours / Point-of-no-return after data migration / Reversible at each phase} |
| **Data consistency during parallel** | {e.g., Eventual consistency via events / Strict sync / Read from one, write to both} |

---

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|:-----------:|:------:|-----------|
| Legacy system has undocumented behavior | High | Medium | Characterization tests before any changes; shadow traffic comparison |
| Data migration corrupts records | Medium | High | Dry-run migrations; row-count validation; rollback plan with time limit |
| Users confused by partial transition | Medium | Medium | Feature flags hide WIP; single entry point (reverse proxy); clear communication |
| Transition takes longer than planned | High | Medium | Each phase delivers value independently; can pause between phases |
| Integration between old and new is fragile | Medium | High | Anti-corruption layer (ACL); contract tests; monitoring on integration points |
| Team knowledge of legacy is insufficient | Medium | Medium | Pair programming; legacy documentation sprint; characterization tests as learning |

---

## Consequences

### Positive
- {What this enables — e.g., "New module can use modern architecture without legacy constraints"}
- {Benefit 2 — e.g., "Risk is contained per phase; no big-bang failure mode"}
- {Benefit 3 — e.g., "Team learns incrementally; can adjust approach based on early phases"}

### Negative
- {What trade-off is accepted — e.g., "Dual maintenance during transition increases operational cost"}
- {Limitation — e.g., "Some features will live in legacy for N months longer than ideal"}
- {Complexity — e.g., "Integration layer adds routing complexity"}

### Risks
- {What could go wrong — e.g., "Strangler fig takes longer than expected; legacy becomes harder to maintain"}
- {Mitigation — e.g., "Set phase deadlines; escalate if missed; consider accelerating decommission"}

---

## Success Metrics

| Metric | Target | Measured When |
|--------|:------:|:------------:|
| Legacy code percentage | Decreasing by {X%} per {period} | Monthly |
| New system feature velocity | Increasing after Phase 2 | Per sprint |
| Incident rate (transition-caused) | < {threshold} per phase | Per phase |
| Data consistency validation | 100% pass | Before each phase transition |
| User-visible downtime | 0 (zero-downtime transitions) | Per phase transition |

---

## Related

- ADR-{NNN}: {Technology Stack} — new system technology choices
- ADR-{NNN}: {Data Architecture} — data migration approach details
- Principle P{n}: {relevant principle — e.g., "Operational Simplicity"}
- Constraint C{n}: {relevant constraint — e.g., "Zero downtime during transition"}

---

## Usage Notes (For AI-ADLC)

**When to produce this ADR:**
- User indicates Mode D (Brownfield) in Requirements Ingestion
- Existing system is being extended, replaced, or modernized
- Multiple viable approaches exist for how to relate to the existing system

**This ADR is produced EARLY** (during Stage 3: Architecture Vision, or immediately after Stage 2 if brownfield mode is active) because the brownfield strategy fundamentally constrains all subsequent design decisions.

**After this ADR is accepted:**
- Architecture Vision may need additional constraints (e.g., "backward compatibility with legacy API")
- System Context (C4 L1) must show BOTH existing and new systems
- Container Design (C4 L2) must show transition-state containers (proxy/facade/ACL)
- Integration Architecture must include legacy integration patterns
- Data Architecture must address migration/coexistence strategy
