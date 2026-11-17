# How AI-TGE Test Governance Works

**Purpose:** Explains how AI-TGE's hybrid engine derives test requirements from architecture, maps them to a structured register, observes AI-DLC v1 execution for coverage, and scores test debt risk — governing WHAT must be tested without writing test code.

---

## What AI-TGE Does

AI-TGE is a hybrid test governance engine with two operational phases:
1. **Strategy Phase** — derive what tests MUST exist based on architectural commitments
2. **Observation Phase** — track what actually gets tested during AI-DLC v1 execution

It answers: "Given what we designed, what MUST be tested? Is it being tested? What's the risk of gaps?"

```
ARCHITECTURE PACKAGE (from AI-ADLC)
+ DEVELOPMENT WORKSPACE (from AI-DWG)
        │
        ▼
┌─────────────────────────────────────────────────────────────────────┐
│  AI-TGE STRATEGY PHASE (Stages 1-6)                                  │
│                                                                      │
│  Read AP → Derive Requirements → Classify → Prioritize → Register   │
└─────────────────────────────────────────────────────────────────────┘
        │
        ▼
TEST STRATEGY + TEST REGISTER (what MUST be tested)
        │
        ▼ (during AI-DLC v1 delivery)
┌─────────────────────────────────────────────────────────────────────┐
│  AI-TGE OBSERVATION PHASE (Stages 7-12)                              │
│                                                                      │
│  Track execution → Map coverage → Score gaps → Report debt           │
└─────────────────────────────────────────────────────────────────────┘
        │
        ▼
COVERAGE REPORTS + DEBT SCORECARD + DEFECT LOG
```

**Hard boundary:** AI-TGE governs tests — it does NOT write them. It identifies what must exist, tracks what does exist, and scores the risk of gaps.

---

## The Two-Source Model

Like AI-GCE, AI-TGE derives requirements from two sources:

### Source 1: Architecture-Derived (from AP)

Every architectural commitment implies test requirements:

| AP Artifact | Derived Test Requirements |
|------------|--------------------------|
| API contracts | Contract tests (consumer-driven), endpoint validation tests |
| Security architecture | Auth boundary tests, penetration test plan, injection prevention |
| Integration map | Integration tests for each external dependency |
| ADR decisions | Decision validation tests (does the implementation honor the decision?) |
| Performance NFRs | Performance/load test requirements |
| Data architecture | Data integrity tests, migration tests, consistency checks |
| Component boundaries | Unit tests at boundary interfaces |

### Source 2: Built-In Baseline (universal minimums)

Even without a rich AP, universal testing standards apply:

| Baseline Rule | What It Requires |
|--------------|-----------------|
| Every public function has a test | Minimum unit test presence |
| Error paths are tested | Not just happy-path coverage |
| Regression test for every bug fix | No bug recurs without a safety net |
| New endpoints have request validation tests | Input safety |
| Authentication flows are tested | Critical path coverage |
| Build must run tests | CI includes test execution |

---

## The Test Register

The central artifact — a structured inventory of ALL test requirements:

```markdown
# Test Register

| ID | Source | Requirement | Level | Type | Technique | Status | Risk |
|----|--------|-------------|-------|------|-----------|--------|------|
| TR-001 | API-Architecture §3.2 | GET /users returns paginated results | Integration | Functional | Architecture-Derived | Covered | - |
| TR-002 | Security Architecture §4.1 | JWT validation rejects expired tokens | Unit | Non-Functional | Architecture-Derived | Gap | High |
| TR-003 | Baseline B-003 | Error responses follow standard format | Unit | Functional | Baseline | Covered | - |
| TR-004 | ADR-005 (Event Sourcing) | Events are immutable after persistence | Integration | Structural | Architecture-Derived | Gap | Critical |
```

Each entry is classified on three ISTQB dimensions:
- **Level:** Unit / Integration / System / Acceptance
- **Type:** Functional / Non-Functional / Structural
- **Technique:** Architecture-Derived / Baseline / Story-Derived / Manual

---

## The Four Operating Modes

| Mode | Input Available | Behavior |
|------|----------------|----------|
| **Full Chain** | AP + DW + AI-DLC v1 state | Full derivation + continuous observation |
| **Architecture Only** | AP only (no workspace yet) | Derive test strategy pre-implementation |
| **Brownfield** | Existing workspace + existing tests | Scan existing tests, map against requirements, find gaps |
| **Observation Only** | Active AI-DLC v1 session | Track what's being tested in real-time, flag gaps |

Mode is auto-detected based on what's available — no manual configuration needed.

---

## Strategy Phase (Stages 1-6)

### Stage 1: Workspace Detection
- Detect AP (`adlc-state.md`), DW (`.kiro/steering/workspace-rules.md`), AI-DLC v1 state
- Determine operating mode based on what's found
- Read depth level from predecessor state

### Stage 2: Architecture Reading
- Parse all AP artifacts (API contracts, ADRs, security, integrations, components)
- Extract every testable commitment ("the system MUST...", "the API SHALL...")
- Catalog NFRs (performance, security, availability)

### Stage 3: Test Requirement Derivation
- Transform architectural commitments into test requirements
- Apply ISTQB taxonomy (Level × Type × Technique)
- Assign unique IDs (TR-NNN)
- Link each requirement to its source (traceability)

### Stage 4: Brownfield Assessment (if existing tests)
- Scan test directories for existing tests
- Map existing tests to derived requirements
- Identify: Covered (test exists) / Gap (no test) / Excess (test without requirement)
- Build baseline state

### Stage 5: Strategy & Pyramid Generation
- Design test pyramid proportions (unit > integration > system > acceptance)
- Set coverage thresholds per level
- Identify priority order (risk-first, not alphabetical)
- Produce the Test Strategy document

### Stage 6: Risk Scoring & Prioritization
Score each gap using four factors (1-5 each):

| Factor | What It Measures |
|--------|-----------------|
| Architectural Risk | How critical is this component to system integrity? |
| Blast Radius | If this breaks, how much else breaks? |
| Logic Complexity | How complex is the untested logic? |
| Change Frequency | How often is this code modified? |

**Risk Score = AR × BR × LC × CF** (max 625, presented as High/Medium/Low bands)

---

## Observation Phase (Stages 7-12)

Runs continuously alongside AI-DLC v1 delivery:

### Stage 7: State Observation
- Monitor AI-DLC v1 session artifacts (specs, code, tests produced)
- Detect when new tests are written

### Stage 8: Story Acceptance Mapping
- When AI-DLC v1 implements a story, map its acceptance criteria to register entries
- Update coverage status (Gap → Covered when test confirmed)

### Stage 9: Coverage Reporting
- Periodic coverage reports: what's tested, what's not, trend over time
- Commitment-based coverage (not just line coverage): "75% of architectural commitments verified"

### Stage 10: Architecture Reconciliation
- When AP changes (AI-ADLC re-run), update register accordingly
- New requirements added, obsolete ones marked Deprecated
- Gap list refreshed

### Stage 11: Defect Logging
- Track defects found during delivery
- Correlate with test gaps ("this defect was in an untested area — confirming gap risk")
- Feed back into risk scoring (defect in an area → risk score increases)

### Stage 12: Debt Prioritization
- Produce Test Debt Scorecard: ranked list of test gaps by risk
- Recommend sprint allocation for test writing
- Track improvement over time

---

## Key Principle: Govern, Don't Write

AI-TGE tells you:
- ✅ "TR-004 requires an integration test for event immutability — currently a Gap with Critical risk"
- ❌ It does NOT write the test

The development team (via AI-DLC v1) writes tests. AI-TGE ensures the RIGHT tests get written for the RIGHT reasons, and tracks whether they actually exist.

---

## Output Artifacts

| Artifact | Purpose | Updated When |
|----------|---------|-------------|
| `test-strategy.md` | Test approach, pyramid, thresholds | Strategy phase (Stage 5) |
| `test-register.md` | Full register of requirements + status | Continuously (every observation cycle) |
| `coverage-report.md` | Current coverage state + trends | Periodically (configurable) |
| `debt-scorecard.md` | Ranked test gaps by risk | After risk scoring (Stage 6, 12) |
| `defect-log.md` | Defects found + gap correlation | When defects are reported |
| `tge-state.md` | Session continuity + mode + progress | After every stage |

---

## Related Documents

| Document | Location |
|----------|----------|
| How Test Strategy Works | `knowledge_docs/HOW_TEST_STRATEGY_WORKS.md` |
| How GCE Derivation Pipeline Works | `knowledge_docs/HOW_GCE_DERIVATION_PIPELINE_WORKS.md` |
| How ADLC Progressive Decomposition Works | `knowledge_docs/HOW_ADLC_PROGRESSIVE_DECOMPOSITION_WORKS.md` |
| Why Testing Strategy Matters | `knowledge_docs/WHY_TESTING_STRATEGY_MATTERS.md` |
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
