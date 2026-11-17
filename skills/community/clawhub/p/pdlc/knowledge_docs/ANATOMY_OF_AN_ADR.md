# Anatomy of an ADR (Architecture Decision Record)

**Purpose:** Field-by-field breakdown of Architecture Decision Records produced by AI-ADLC — what each section means, when ADRs are created, how they propagate through the chain, and how to write a good one.

**Derived from:** Pattern: Gate Before Transition + Pattern: Downstream Signaling

---

## What an ADR Is

An Architecture Decision Record documents a significant design choice — the context that drove it, the options considered, the decision made, and the consequences. It's the permanent record of WHY the architecture is what it is.

```markdown
# ADR-003: Database Strategy

## Status
Accepted

## Date
2026-06-10

## Context
The system requires persistent storage for 3 bounded contexts with different 
access patterns: high-read user profiles, write-heavy event logs, and 
transactional order processing.

## Options Considered
1. Single PostgreSQL instance (all contexts)
2. PostgreSQL + Redis (hot cache for profiles)
3. PostgreSQL + EventStore + Redis (polyglot persistence)

## Decision
Option 2: PostgreSQL + Redis

## Rationale
- Option 1: simpler but profile reads would hammer the DB at scale
- Option 3: over-engineered for current scale; Event Sourcing not justified (ADR-002)
- Option 2: balances simplicity with performance for the dominant read pattern

## Consequences
- PostgreSQL is the primary store (ACID transactions for orders)
- Redis caches user profiles (TTL-based, eventual consistency acceptable)
- Team needs Redis operational knowledge (training planned)
- Data architecture must define cache invalidation strategy
- AI-DWG will generate: data-standards.md with Redis caching rules

## Supersedes
None

## Related
- ADR-002 (Event Sourcing declined — informs this decision)
- ADR-001 (Tech Stack — PostgreSQL selected there)
```

---

## Section-by-Section Reference

### Status

| Value | Meaning | When Set |
|-------|---------|----------|
| `Proposed` | Under discussion, not yet decided | When first written |
| `Accepted` | Decision made and approved at gate | After gate approval |
| `Superseded` | Replaced by a newer ADR | When architecture changes |
| `Deprecated` | No longer relevant (feature removed) | When context disappears |

### Date

ISO date when the decision was MADE (gate approved), not when the doc was first drafted.

### Context

**What to include:**
- The problem or question that required a decision
- Relevant constraints (budget, timeline, team skills, existing systems)
- Quality attributes that influenced the choice (performance, security, scalability)
- Assumptions that shaped the evaluation

**What NOT to include:**
- The solution (that's the Decision section)
- Generic architecture theory
- Content from prior ADRs (reference them instead)

### Options Considered

**Minimum: 2 options** (otherwise it wasn't a decision — it was inevitable).

For each option:
- Name/description (one line)
- Key advantages
- Key disadvantages
- Why it might be the right choice

**The rejected options matter.** Future developers who ask "why didn't we use X?" can find the answer here.

### Decision

One clear statement: "We chose Option {N}: {name}"

No hedging. No "we'll revisit." The decision is made. If conditions change, create a new ADR that supersedes this one.

### Rationale

**The most valuable section.** Explains WHY this option won over others:
- What made the winning option better for THIS project?
- What specific constraints eliminated other options?
- What trade-offs were accepted?

### Consequences

**Both positive and negative:**
- What this decision ENABLES (positive consequences)
- What this decision COSTS or CONSTRAINS (negative consequences)
- What OTHER decisions this forces or influences
- What downstream packages will derive from this (AI-DWG, AI-GCE)

### Supersedes / Superseded By

Creates a decision history:
```
ADR-003 (original) → Superseded by ADR-012 (revised database strategy)
```

When an ADR is superseded:
- Original ADR status → `Superseded`
- Add `Superseded By: ADR-012` field
- New ADR references the original in its Context

### Related

Links to ADRs that:
- Informed this decision (prior decisions that constrained options)
- Are affected by this decision (downstream ADRs that depend on this)
- Were made in the same decision cluster (e.g., tech stack + database + caching)

---

## When AI-ADLC Creates ADRs

| Stage | ADR Triggers |
|-------|-------------|
| Stage 6 (Technology Stack) | Framework, language, database, messaging, hosting |
| Stage 7 (Multi-Tenancy) | Isolation pattern, tenant routing, data segregation |
| Stage 8 (Security & Identity) | Auth model, encryption approach, trust boundaries |
| Stage 9 (Data Architecture) | Persistence strategy, caching, consistency model |
| Stage 10 (API Architecture) | API style (REST/GraphQL/gRPC), versioning strategy |
| Stage 11 (Integration) | Integration patterns, resilience approach |
| Stage 12 (Component Design) | Internal patterns (when extension rules demand it) |

**Rule:** Any decision where ≥2 viable options exist AND the choice has downstream consequences → ADR required.

---

## How ADRs Flow Through the Chain

```
AI-ADLC produces ADRs (recorded in adlc-state.md: ADR Count = N)
    │
    ├── AI-DWG reads ADRs → derives steering files from decisions
    │   (ADR-003 Database → data-standards.md with Redis caching rules)
    │
    ├── AI-GCE reads steering (derived from ADRs) → derives governance rules
    │   (data-standards.md → DATA-01: cache invalidation required)
    │
    └── AI-TGE reads ADRs → derives test requirements
        (ADR-003 → TR-015: Redis cache invalidation test required)
```

**Traceability chain:** ADR → Steering → Rule → Hook → Enforcement

---

## ADR Quality Checklist

Before an ADR passes its stage gate:

- [ ] Context explains the PROBLEM, not the solution
- [ ] ≥2 options considered with honest trade-off analysis
- [ ] Decision is one clear statement (not "we'll probably...")
- [ ] Rationale explains WHY this option won (not just what it does)
- [ ] Consequences include BOTH positive and negative
- [ ] Downstream impact identified (what other decisions/packages are affected)
- [ ] Related ADRs cross-referenced
- [ ] Status is `Accepted` (gate-approved)
- [ ] ADR number is sequential and tracked in state file

---

## Common ADR Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Only one option listed | Not a decision — it's a mandate | Find at least one alternative (even if clearly worse) |
| No consequences section | Can't assess downstream impact | Think: "what does this force/enable/constrain?" |
| Rationale just repeats the decision | Doesn't explain WHY | Ask: "why NOT the other options?" |
| Context includes the solution | Biases the options analysis | Move solution language to Decision section |
| Vague consequences ("may affect performance") | Not actionable | Be specific: "adds 50ms latency to profile reads" |
| No related ADRs | Decisions look isolated | Every ADR connects to at least one other (or to a requirement) |

---

## Related Documents

| Document | Location |
|----------|----------|
| How ADLC Progressive Decomposition Works | `knowledge_docs/HOW_ADLC_PROGRESSIVE_DECOMPOSITION_WORKS.md` |
| How to Design Architecture | `knowledge_docs/HOW_TO_DESIGN_ARCHITECTURE.md` |
| How to Choose Architecture Extensions | `knowledge_docs/HOW_TO_CHOOSE_ARCHITECTURE_EXTENSIONS.md` |
| Pattern: Gate Before Transition | `knowledge_docs/PATTERN_GATE_BEFORE_TRANSITION.md` |
| Pattern: Downstream Signaling | `knowledge_docs/PATTERN_DOWNSTREAM_SIGNALING.md` |
| Why Architecture Before Code Matters | `knowledge_docs/WHY_ARCHITECTURE_BEFORE_CODE_MATTERS.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
