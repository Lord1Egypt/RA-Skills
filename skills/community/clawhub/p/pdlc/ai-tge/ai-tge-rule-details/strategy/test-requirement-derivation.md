<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Test Requirement Derivation

## Stage: 3 of 12
## Phase: 🔵 STRATEGY
## Execution: ALWAYS

---

## Purpose

Transform the Architecture Commitment Inventory (Stage 2) into a structured **Test Register** — every required test linked to its source commitment, classified by the three-dimensional taxonomy (Level × Type × Technique), and ready for risk scoring. This is where architectural promises become test obligations.

The two-source model applies here: architecture-derived requirements PLUS universal baseline requirements combine to form the complete register.

---

## Depth Adaptation

| Depth | Derivation Scope | Register Detail |
|-------|-----------------|----------------|
| **Minimal** | Core commitments only. Apply baseline to major component types. Produce flat register with: Commitment ID, Test Name, Level, Type, Source, Status. Skip sub-type detail. | 1 test per simple commitment; 2-3 per complex (API, security) |
| **Standard** | All commitments. Full baseline application. Register includes: all taxonomy dimensions, risk score placeholder, linked components. Each API endpoint gets 2-4 tests; each integration gets 3 tests. | Full three-dimensional classification per entry |
| **Comprehensive** | All commitments + story-derived + cross-reference enrichment. Register includes: detailed assertions, test preconditions, data requirements, dependency notes. Multiple tests per commitment where architecture warrants. | Detailed entries with assertion descriptions and precondition notes |

---

## MANDATORY: Stage Sub-Role — Systems Engineer

During THIS stage, ALSO adopt the mindset of a **Systems Engineer**. This does NOT replace your primary role (Senior QA Engineer / Test Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think about the system as interconnected components — a test for one commitment may reveal dependencies on others
- Apply the derivation mapping table mechanically first (architecture → test type), then review for completeness
- Ensure every commitment produces at LEAST one register entry — zero-test commitments indicate a derivation gap
- Consider boundary conditions: where component A meets component B is where integration tests live

### Anti-Patterns for This Stage
- Do NOT derive tests for things the architecture didn't commit to (that's invention, not derivation)
- Do NOT produce a flat list of tests without classification — every entry needs Level × Type × Source
- Do NOT skip baseline application — even well-documented architectures have gaps that baseline catches
- Do NOT duplicate entries — if architecture-derived and baseline point to the same test, link them ("satisfied by")

### Quality Check
A good output at this stage sounds like:
- "Derived 67 test requirements from 47 commitments: 28 Architecture-derived, 24 Baseline-applied, 15 Story-derived. Distribution: 38% Unit, 31% Integration, 19% System, 12% Acceptance. 5 baseline entries satisfied by existing architecture entries (linked, not duplicated)."

---

## Step-by-Step Execution

### Step 1: Load Required Context

Before derivation, load:
1. Architecture Commitment Inventory from Stage 2 (`.governance/test/architecture-commitments.md`)
2. `common/two-source-model.md` — baseline catalog and resolution rules
3. `common/test-taxonomy.md` — classification dimensions and mapping table

---

### Step 2: Architecture-Derived Derivation

For each commitment in the inventory, apply the **Primary Mapping Table** from `test-taxonomy.md`:

| AP Artifact Type | Derivation Rule | Tests Per Commitment |
|-----------------|----------------|:--------------------:|
| API endpoint | Contract test (request + response schema) + error test per documented error code + auth test if protected | 2-5 |
| Security ADR (authentication) | Auth valid test + auth invalid test + token expiry test | 2-3 |
| Security ADR (authorization) | Role-access test per role × resource combination | 1-N (per role) |
| Component design (business rule) | Unit test per rule + boundary test for edge cases | 2-3 |
| Component design (state machine) | Transition test per valid transition + rejection test per invalid | N+M |
| Integration (external system) | Connectivity + error handling + timeout test | 3 |
| Integration (async messaging) | Publish + consume + dead-letter test | 3 |
| Data model (entity) | CRUD cycle + validation test + constraint test | 2-4 |
| Data model (migration) | Up + down + data preservation test | 2-3 |
| NFR (performance SLA) | Load test at stated threshold | 1-2 |
| NFR (reliability) | Failure + recovery test | 1-2 |
| User story (acceptance criteria) | 1 acceptance test per criterion | 1 per AC |
| Configuration | Valid + invalid + default test | 3 |

**For each derived test, record:**
```markdown
| Commitment ID | Test Level | Test Type | Sub-Type | Test Name | Source | Status |
```

- **Status:** Set to `Required` (not yet checked against codebase)
- **Source:** `Architecture`
- **Classification:** Apply Level × Type × Sub-Type per taxonomy rules

---

### Step 3: Baseline Application

After architecture derivation, apply the built-in baseline from `two-source-model.md`:

**For each component type detected in the project:**

1. **Identify matching baseline rules** — which BASE-* rules apply?
2. **Check for "satisfied by"** — does an architecture-derived entry already cover this baseline?
3. **Register new entries** — for baselines NOT satisfied by architecture entries
4. **Link satisfied entries** — mark baseline as "Satisfied by: {architecture entry ID}"

**Resolution logic:**
```
FOR each baseline rule in two-source-model.md:
  IF component type exists in project:
    FOR each instance of that component:
      IF architecture-derived test covers this concern:
        → Mark baseline as "Satisfied by {ARCH-ID}" (no duplicate entry)
      ELSE:
        → Register new entry with Source = "Baseline", ID = BASE-*
```

---

### Step 4: Story-Derived Tests (Conditional)

**Execute IF:** User stories with acceptance criteria exist (in aidlc-docs or AP)
**Skip IF:** No user stories available

For each user story:
1. Extract every acceptance criterion
2. Each criterion becomes ONE acceptance test
3. Register entry format: `STORY-{story_id}-AC{n}`
4. Level = Acceptance, Type = Functional, Sub-Type = Workflow
5. Source = Story

**Deduplication:** If a story acceptance criterion maps to the same concern as an architecture-derived test, link them rather than duplicating. The architecture entry takes precedence for classification; the story entry confirms business value alignment.

---

### Step 5: Compile the Test Register

Assemble all derived entries into the register format:

```markdown
# Test Register

**Generated:** {ISO timestamp}
**Engine:** AI-TGE v1.0.0
**Mode:** {mode}
**Depth:** {depth level}
**Total Entries:** {N}

## Register Summary

| Metric | Count |
|--------|:-----:|
| Architecture-derived | {n} |
| Baseline-applied | {n} |
| Story-derived | {n} |
| Baseline satisfied by architecture | {n} (linked, not counted separately) |
| **Total unique test requirements** | **{N}** |

## Distribution by Level

| Level | Count | Percentage | Target (pyramid) |
|-------|:-----:|:----------:|:----------------:|
| Unit | {n} | {n}% | {target from depth}% |
| Integration | {n} | {n}% | {target}% |
| System | {n} | {n}% | {target}% |
| Acceptance | {n} | {n}% | {target}% |

## Full Register

| ID | Commitment | Level | Type | Sub-Type | Test Name | Source | Risk Score | Status |
|:--:|:----------:|:-----:|:----:|:--------:|-----------|:------:|:----------:|:------:|
| {auto} | {commit_id} | {level} | {type} | {subtype} | {descriptive name} | {source} | _[pending Stage 6]_ | Required |
```

**Risk scores are LEFT BLANK** in this stage — they are calculated in Stage 6 (Risk Scoring). Mark as `_[pending Stage 6]_`.

---

### Step 6: Validate Register Quality

Before presenting, run these checks:

| Check | What to Verify | Action if Failed |
|-------|---------------|-----------------|
| Every commitment has ≥1 test | No commitment in inventory has zero register entries | Derive missing entry or justify exemption |
| No duplicate tests | Same commitment + same test name = duplicate | Merge duplicates; keep the more specific entry |
| Classification valid | Level × Type combination is valid per taxonomy rules | Correct per taxonomy (e.g., Unit+Performance → System+Performance) |
| Baseline coverage complete | All applicable baseline rules applied for detected components | Add missing baseline entries |
| Source traceability intact | Every entry links to a commitment ID, baseline rule, or story | Fix broken links |
| No invented tests | Every entry traces to a specific source — no "I think we should test X" | Remove unsourced entries; if valid, mark Source = Manual and note rationale |

---

### Step 7: Present for Review

```markdown
## Review: Test Register (Baseline)

I've derived the test register from your architecture commitments + universal baseline.

**Total test requirements:** {N}
- Architecture-derived: {n}
- Baseline-applied: {n}
- Story-derived: {n}

**By test level:**
- Unit: {n} ({n}%)
- Integration: {n} ({n}%)
- System: {n} ({n}%)
- Acceptance: {n} ({n}%)

**Baseline enrichment:** {n} entries where baseline adds coverage the architecture didn't explicitly call for

**Key derivation highlights:**
- {API-001}: POST /users → 4 tests (contract, validation error, auth required, response schema)
- {SEC-001}: JWT authentication → 3 tests (valid, invalid, expired)
- {INT-001}: Payment gateway → 3 tests (connectivity, error handling, timeout)

**Full register saved to:** `.governance/test/test-register.md`

---

**Your response:**
- (a) **Approve** — these are the right tests to require; proceed
- (b) **Add requirements** — I know of additional tests needed
- (c) **Remove requirements** — some derived tests are unnecessary (explain which)
- (d) **Reclassify** — some tests are at the wrong level/type
- (e) **Override baseline** — I want to exclude specific baseline rules (with rationale)
```

---

## Gate

**This stage has a GATE.** Do not proceed to Stage 4 until the user confirms the test register represents the correct set of required tests. The register is the source of truth for all coverage tracking and debt scoring — errors here persist through the entire observation phase.

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Test Register | `.governance/test/test-register.md` | Master register — maintained throughout engine lifecycle |
| Updated state file | `.governance/test/tge-state.md` | Stage 3 complete; register stats populated |

---

## Stage Completion Criteria

| Check | Pass Criteria |
|-------|---------------|
| Two-source model applied | Both architecture-derived AND baseline rules used |
| All commitments covered | Every inventory item has ≥1 register entry |
| Classification complete | Every entry has Level + Type + Sub-Type |
| No duplicates | Zero duplicate entries in register |
| Baseline resolution applied | "Satisfied by" links where architecture covers baseline |
| Register stats calculated | Total, by-level, by-source counts accurate |
| User approved | Register confirmed as correct test obligations |
| State file updated | Stage 3 = complete; register stats in state |
