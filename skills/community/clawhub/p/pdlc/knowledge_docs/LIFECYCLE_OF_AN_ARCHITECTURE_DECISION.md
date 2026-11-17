# Lifecycle of an Architecture Decision

**Purpose:** Traces how an architecture decision (ADR) moves from proposal through acceptance, propagation into the workspace and governance, and eventual supersession — showing how one decision ripples through the entire AI-* chain over time.

---

## The Complete Lifecycle

```
PROPOSED ──→ ACCEPTED ──→ PROPAGATED ──→ ENFORCED ──→ ┬── STABLE (indefinite)
                                                        ├── REVISED ──→ (re-propagated)
                                                        └── SUPERSEDED ──→ ARCHIVED
```

---

## States

### 1. Proposed (Under Discussion)

**Trigger:** AI-ADLC reaches a stage requiring a technology/pattern decision.

**What happens:**
- Options identified (minimum 2)
- Trade-off analysis performed
- ADR document created with Status: `Proposed`
- Presented at stage gate for human review

**Duration:** Minutes to hours (within one AI session typically).

### 2. Accepted (Gate Approved)

**Trigger:** Human approves the decision at the stage gate.

**What happens:**
- ADR Status → `Accepted`
- Decision recorded in `adlc-state.md` (ADR count incremented)
- Architecture artifacts updated to reflect the decision
- Downstream decisions may now proceed (unlocked by this decision)

**What it enables:** Other stages that depend on this decision can now run (e.g., data architecture requires database decision first).

### 3. Propagated (Flows Downstream)

**Trigger:** AI-DWG reads the Architecture Package containing the accepted ADR.

**What happens:**
- AI-DWG translates the decision into steering file content
  - ADR-003 (PostgreSQL + Redis) → `data-standards.md` with caching rules
  - ADR-005 (REST + header versioning) → `api-standards.md` with versioning rules
- Workspace structure may change (new folders, new configs)
- Templates generated to match the decision

**Result:** The decision is now embedded in the development workspace as operational rules.

### 4. Enforced (Governance Active)

**Trigger:** AI-GCE reads the steering files (which were derived from the ADR).

**What happens:**
- Governance rules derived from the steering (which was derived from the ADR)
- Hooks generated to enforce the decision's implications
- Compliance scoring includes adherence to this decision's constraints

**Traceability chain:**
```
ADR-003 (Database: PostgreSQL + Redis)
    → data-standards.md (steering: "Cache invalidation MUST use TTL pattern")
        → DATA-01 (rule: "Redis keys MUST have TTL configured")
            → data-cache-check.json (hook: fires on Redis config files)
```

### 5. Stable (Indefinite)

**State:** Decision is accepted, propagated, enforced, and not being challenged. The normal state for most decisions.

**Duration:** Months to years (most ADRs remain stable for the life of the project).

### 6. Revised (Decision Changed)

**Trigger:** New information, changed constraints, or team experience reveals a better option.

**What happens:**
- Original ADR marked as `Superseded by ADR-{N}`
- New ADR created with Status: `Accepted`
- Re-propagation cascade:
  ```
  New ADR accepted
      → AI-ADLC state updated
      → AI-DWG Mode 2 (reconcile workspace)
          → Steering files updated
          → AI-GCE re-derives rules
              → New enforcement matches new decision
  ```
- Migration ADR may be needed (transition from old to new)

**Key principle:** Revision is not failure — it's learning. ADRs expect to be superseded when context changes.

### 7. Superseded (Replaced)

**Trigger:** A new ADR explicitly replaces this one.

**What happens:**
- Status → `Superseded`
- `Superseded By: ADR-{N}` field added
- The old ADR remains in the record (audit trail, historical context)
- Previous rules derived from this ADR → deprecated when re-derivation runs
- Future readers see: "This was our decision then; this is our decision now"

### 8. Archived (Project Complete)

**Trigger:** Project enters maintenance mode or is decommissioned.

**What happens:**
- ADRs remain as historical record
- No active enforcement (project not under active development)
- Available for reference if project is revived or forked

---

## The Propagation Cascade (Detailed)

When an ADR is accepted, this cascade happens:

```
TIME →

T0: ADR-007 accepted ("Switch from REST to GraphQL for client API")
    │
T1: AI-ADLC artifacts updated (API Architecture doc revised)
    │
T2: AI-DWG Mode 2 triggered
    ├── api-standards.md regenerated (GraphQL rules replace REST rules)
    ├── New steering: graphql-standards.md generated (conditional trigger met)
    ├── Old steering: rest-only-patterns.md flagged obsolete
    └── Signal sent to AI-GCE
    │
T3: AI-GCE re-derivation triggered
    ├── API-01 (contract-first) re-derived (now references GraphQL schema, not OpenAPI)
    ├── API-02 (versioning) re-derived (schema evolution, not URL versioning)
    ├── Old REST-specific hooks deprecated
    └── New GraphQL-specific hooks generated
    │
T4: AI-TGE register updated
    ├── Old REST endpoint tests → Deprecated
    ├── New GraphQL query/mutation tests → Added as gaps
    └── Risk score recalculated
    │
T5: Team informed (new steering appears in next session)
```

---

## Decision Categories and Their Propagation Depth

| ADR Category | Propagation Reach | Why |
|-------------|:--:|-----|
| Tech stack (language, framework) | Full chain | Affects naming, testing, structure, governance |
| Database strategy | Medium | Affects data steering, some test requirements |
| API style | Full chain | Affects steering, hooks, tests, workspace structure |
| Security model | Full chain | Affects security steering, all security rules |
| Deployment pattern | GCE only (Tier 3) | Affects deployment governance |
| Internal component pattern | Minimal | Affects only that module's steering |

---

## Related Documents

| Document | Location |
|----------|----------|
| Anatomy of an ADR | `knowledge_docs/ANATOMY_OF_AN_ADR.md` |
| How to Handle Architecture Changes Mid-Project | `knowledge_docs/HOW_TO_HANDLE_ARCHITECTURE_CHANGES_MID_PROJECT.md` |
| Pattern: Gate Before Transition | `knowledge_docs/PATTERN_GATE_BEFORE_TRANSITION.md` |
| Pattern: Downstream Signaling | `knowledge_docs/PATTERN_DOWNSTREAM_SIGNALING.md` |
| When to Trigger Re-Derivation | `knowledge_docs/WHEN_TO_TRIGGER_REDERIVATION.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
