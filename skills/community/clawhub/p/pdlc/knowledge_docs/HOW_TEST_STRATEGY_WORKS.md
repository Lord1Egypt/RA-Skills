# How Test Strategy Works

**Purpose:** Explains how the AI-* Family produces and enforces a structured test strategy for your project — from architecture-driven derivation through continuous coverage governance — and how AI-TGE orchestrates this as a test governance companion alongside AI-DLC v1 delivery.

---

## What "Test Strategy" Means in This Context

A test strategy is not a document someone writes from scratch. It is **derived** — from architecture decisions, from tech stack choices, from project risk profile. The AI-* Family automates this derivation through AI-TGE (Test Governance Engine), ensuring your testing approach is:

- Traceable to architectural commitments (not invented ad-hoc)
- Prioritized by risk (not listed flat)
- Continuously tracked against actual test coverage
- Adaptive when architecture or scope changes

```
ARCHITECTURE DECISIONS       TECH STACK         PROJECT RISK PROFILE
   (from AI-ADLC)          (from AI-DWG)       (from complexity score)
         │                       │                       │
         └───────────┬───────────┘───────────────────────┘
                     ▼
            ┌──────────────────┐
            │   TEST STRATEGY   │ ← derived, not invented
            └──────────────────┘
                     │
         ┌───────────┼───────────────┐
         ▼           ▼               ▼
   Test Pyramid   Coverage Goals   Risk Priorities
   (types/ratios) (per commitment) (what matters most)
```

---

## Where Test Strategy Sits in the Chain

Test strategy is produced during AI-TGE's Strategy Phase and enforced during its Observation Phase. It operates alongside AI-DLC v1 as a companion:

```
AI-ADLC ─── designs architecture ──────────────────┐
                                                    │
AI-DWG ──── prepares workspace (incl. test tools) ──┼──► AI-TGE derives test strategy
                                                    │
AI-DLC v1 ──── builds software ◄── AI-TGE observes ───┘
                                    │
                                    ▼
                          Coverage tracked continuously
```

You don't need to run the full chain. AI-TGE adapts to whatever exists:

| What You Have | What AI-TGE Produces |
|---------------|---------------------|
| Full architecture + workspace + active build | Complete strategy + continuous observation |
| Architecture package only (pre-implementation) | Strategy + register (ready before code starts) |
| Existing codebase with existing tests | Brownfield assessment — maps existing tests to gaps |
| Running build with no prior governance | Observation-only — starts tracking immediately |

---

## The Two Sources of Test Requirements

Every test requirement comes from one of two sources:

### Source 1: Architecture-Derived

Your architecture makes promises. Each promise implies verification:

| Architectural Promise | Implied Test Requirement |
|----------------------|--------------------------|
| "The API validates input against the schema" | Schema validation test per endpoint |
| "Authentication uses JWT with 15-min expiry" | Token expiry enforcement test |
| "Services communicate via async events" | Event delivery + ordering tests |
| "The system handles 500 concurrent users" | Load test at 500 concurrent connections |
| "Data at rest is encrypted (AES-256)" | Encryption verification test |
| "Failed writes are retried 3 times" | Retry behavior test with failure injection |

### Source 2: Universal Baseline

Even without a rich architecture package, proven testing minimums apply:

| Baseline Rule | Rationale |
|--------------|-----------|
| Every public API endpoint has a request validation test | Prevents injection and malformed input |
| Error paths are tested (not just happy paths) | Most production bugs are in error handling |
| Every bug fix includes a regression test | Same bug never recurs |
| Authentication flows have end-to-end tests | Critical path — can't rely on unit mocks alone |
| Database migrations have rollback tests | Data loss prevention |
| External integrations have contract tests | Interface drift detection |

The two-source model ensures coverage even when your AP is thin — baseline requirements fill gaps automatically without replacing architecture-derived ones.

---

## The Test Pyramid: Ratios Derived from Architecture

AI-TGE doesn't impose a fixed pyramid ratio. It derives proportions from your architecture:

| Architecture Pattern | Resulting Pyramid Shape |
|---------------------|------------------------|
| Monolith with rich domain logic | Heavy unit layer (domain rules), moderate integration, minimal e2e |
| Microservices with many integrations | Moderate unit, heavy integration + contract tests, moderate e2e |
| Event-driven with eventual consistency | Moderate unit, heavy event/contract tests, e2e focused on sagas |
| Frontend-heavy with thin API | Unit for components, integration for API calls, e2e for user journeys |

The strategy document states the ratios AND the rationale — traceable to your specific architecture.

---

## How Coverage Is Measured

Traditional coverage measures lines-of-code. AI-TGE measures **commitment coverage** — whether the promises your architecture made are actually verified:

```
                    TRADITIONAL                    COMMITMENT-BASED
                    ───────────                    ────────────────
                    85% line coverage              75% commitment coverage
                    (but which lines?)             (which promises are verified?)

                    Says: "most code is tested"   Says: "3 of 4 API contracts
                    Doesn't say: "are the                have contract tests.
                    important things tested?"            1 gap: Payment API (Critical risk)"
```

Coverage is reported across multiple dimensions:

| View | Question Answered |
|------|-------------------|
| By commitment | "Which architectural promises are verified?" |
| By component | "Which components have adequate test coverage?" |
| By test type | "Do we have enough integration tests vs. unit tests?" |
| By risk level | "Are the highest-risk areas covered first?" |

---

## Risk-Based Prioritization

Not all test gaps are equal. AI-TGE scores each gap on four factors:

| Factor | What It Asks | Example |
|--------|-------------|---------|
| **Architectural Risk** | How critical is this to system integrity? | Payment processing = 5; admin settings page = 2 |
| **Blast Radius** | If this fails, how much else breaks? | Shared auth library = 5; isolated utility = 1 |
| **Logic Complexity** | How likely is a bug here? | Complex state machine = 5; simple CRUD = 2 |
| **Change Frequency** | How often is this modified? | Active feature = 5; stable infrastructure = 1 |

**Risk Score = AR × BR × LC × CF** → range 1–625

| Risk Band | Score | Recommended Action |
|-----------|:-----:|-------------------|
| Critical | 400–625 | Write these tests immediately |
| High | 150–399 | Include in current sprint |
| Medium | 50–149 | Schedule within 2 sprints |
| Low | 1–49 | Write when convenient |

This ensures your test-writing effort goes where it matters most — not alphabetically through a flat list.

---

## The Test Register

The register is the single source of truth for test accountability:

| ID | Source | Requirement | Level | Type | Status | Risk |
|----|--------|-------------|-------|------|--------|------|
| TR-001 | API Architecture §3 | Pagination returns correct page size | Integration | Functional | ✅ Covered | — |
| TR-002 | Security ADR-003 | JWT rejection on expiry | Unit | Non-Functional | ❌ Gap | Critical |
| TR-003 | Baseline B-003 | Error responses follow standard shape | Unit | Functional | ✅ Covered | — |
| TR-004 | ADR-005 (Events) | Events immutable after write | Integration | Structural | ❌ Gap | High |
| TR-005 | Story US-012 | User can reset password via email | Acceptance | Functional | ✅ Covered | — |

Every entry links back to its source — you always know WHY a test is required and WHAT architectural promise it verifies.

Classification uses ISTQB-standard taxonomy on three dimensions:
- **Level:** Unit / Integration / System / Acceptance
- **Type:** Functional / Non-Functional / Structural
- **Technique:** Architecture-Derived / Baseline / Story-Derived / Manual

---

## How Strategy Adapts to Depth

AI-TGE calibrates based on project complexity:

| Depth | Characteristics | What You Get |
|-------|----------------|-------------|
| **Minimal** | Small project, few integrations, clear scope | Strategy + register (lightweight) |
| **Standard** | Mid-size project, multiple services, moderate complexity | + Coverage reports + debt scoring + brownfield assessment |
| **Comprehensive** | Large project, many integrations, high risk, regulatory | + Full traceability + architecture reconciliation + story-level mapping |

Depth is auto-detected from project complexity (5 factors scored) but can be overridden: "Change depth to Comprehensive."

---

## Brownfield Projects: Assessment Before Strategy

For projects with existing tests, AI-TGE starts with assessment — it doesn't ignore what you've already built:

```
EXISTING TEST SUITE
       │
       ▼
┌──────────────────┐
│  SCAN & MAP       │ ← What tests exist? What do they cover?
└──────────────────┘
       │
       ▼
┌──────────────────┐
│  GAP ANALYSIS     │ ← What requirements have NO test?
└──────────────────┘
       │
       ▼
┌──────────────────┐
│  EXCESS DETECTION │ ← What tests exist WITHOUT a requirement? (orphans)
└──────────────────┘
       │
       ▼
┌──────────────────┐
│  PRIORITIZED GAPS │ ← Risk-scored list of what to write next
└──────────────────┘
```

Brownfield assessment is non-destructive: it maps and analyzes without modifying your existing tests.

---

## Continuous Observation During Delivery

Once AI-DLC v1 starts building features, AI-TGE switches to observation:

| Trigger | AI-TGE Action |
|---------|---------------|
| AI-DLC v1 completes a unit | Register the tests that should exist for that unit |
| A story is accepted | Verify acceptance criteria have corresponding tests |
| Architecture changes (AP update) | Reconcile register — add new requirements, deprecate old ones |
| A defect is found | Log it, correlate with test gaps, update risk scores |
| Coverage milestone reached | Produce coverage report with trend analysis |

Observation is **non-blocking** — it informs, reports, and scores. It never stops the build. It makes gaps visible so the team can act on them with full risk context.

---

## What the Strategy Contains

The test strategy document (`.tge/test-strategy.md`) produced by AI-TGE includes:

| Section | Content |
|---------|---------|
| Test Approach | Overall philosophy — risk-driven, architecture-traceable |
| Test Pyramid | Types and proportions, derived from your architecture |
| Test Types Required | Unit, integration, contract, e2e, performance, security — which ones apply and why |
| Coverage Goals | Per-commitment targets (not just a global percentage) |
| Test Data Strategy | How test data is managed (fixtures, factories, seeding) |
| Environment Requirements | What test environments are needed |
| Entry/Exit Criteria | What must pass before release (per test level) |
| Tool Selection | Testing tools matched to your tech stack (from DW) |
| Automation Approach | What's automated, what's manual, and why |
| Risk Allocation | Where test effort should concentrate first |

---

## Interaction with Other AI-* Family Members

| Package | Contributes To Test Strategy |
|---------|------------------------------|
| **AI-ADLC** | Produces the architecture that test requirements are derived from |
| **AI-DWG** | Configures the workspace with appropriate test tooling + generates `testing-strategy.md` steering |
| **AI-GCE** | Enforces test-related compliance rules (coverage thresholds, mandatory test types per tier) |
| **AI-TGE** | Derives the full strategy, maintains the register, tracks coverage, scores debt |
| **AI-DLC v1** | Consumes the strategy context — writes tests according to register requirements |
| **AI-POLC** | Produces stories with acceptance criteria that become story-derived test requirements |

---

## Key Principles

| Principle | In Practice |
|-----------|-------------|
| **Derive, don't invent** | Test requirements come from architecture + baseline, never from imagination |
| **Risk-first** | Always prioritize by impact, not by count or convenience |
| **Commitment-based** | Measure coverage against what was promised, not what was easy to test |
| **Non-destructive** | Assess without modifying; propose without forcing; mark without deleting |
| **Silent when complete** | When all commitments are verified, there's nothing to report |
| **Adaptive** | Works with whatever input exists — full chain, AP only, brownfield, or observation only |
| **Govern, don't write** | The strategy tells you WHAT to test and WHY — AI-DLC v1 handles the HOW |

---

## Related Documents

| Document | Location |
|----------|----------|
| How AI-TGE Test Governance Works | `knowledge_docs/HOW_TGE_TEST_GOVERNANCE_WORKS.md` |
| Why Testing Strategy Matters | `knowledge_docs/WHY_TESTING_STRATEGY_MATTERS.md` |
| How GCE Derivation Pipeline Works | `knowledge_docs/HOW_GCE_DERIVATION_PIPELINE_WORKS.md` |
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |
| Pattern: Two-Source Model | `knowledge_docs/PATTERN_TWO_SOURCE_MODEL.md` |
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |

---

*Knowledge Document | Created: 2026-06-11 | Updated: 2026-06-13 (rewritten per AI-TGE package) | Author: Maheri*

*Knowledge Document | Created: 2026-06-11 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
