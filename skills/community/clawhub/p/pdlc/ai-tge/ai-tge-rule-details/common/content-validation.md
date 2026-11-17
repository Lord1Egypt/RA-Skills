<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Content Validation

## Purpose

Before creating or saving ANY test governance artifact, AI-TGE MUST validate its content against the rules in this document. Test governance artifacts have specific quality requirements — they must be traceable, risk-scored, and consistent with the architecture they govern.

---

## Validation Checklist (Apply to Every TGE Output)

### 1. Document Metadata

Every TGE output document MUST include:

- [ ] Document title (H1 heading)
- [ ] Document type (Strategy / Register / Coverage Report / Debt Scorecard / Defect Log)
- [ ] Generation timestamp (ISO 8601)
- [ ] Engine version (AI-TGE v1.0.0)
- [ ] Mode active when generated (Full Chain / Architecture Only / Brownfield / Observation Only)
- [ ] Depth level (Minimal / Standard / Comprehensive)

**Format:**
```markdown
# {Document Title}

**Type:** {Strategy / Register / Coverage Report / Debt Scorecard / Defect Log}
**Generated:** {YYYY-MM-DDTHH:MM:SSZ}
**Engine:** AI-TGE v1.0.0
**Mode:** {Full Chain / Architecture Only / Brownfield / Observation Only}
**Depth:** {Minimal / Standard / Comprehensive}
```

---

### 2. Traceability Checks

Every test requirement in the register MUST be traceable to a source:

| Check | What to Verify |
|-------|---------------|
| Source field populated | Every register entry has Source = Architecture / Baseline / Story / Manual / Reconciliation |
| Commitment ID links to real artifact | If Source = Architecture, the referenced AP artifact must exist |
| Baseline ID is valid | If Source = Baseline, the ID must match a rule in `two-source-model.md` |
| Story ID is valid | If Source = Story, the referenced story file must exist in aidlc-docs |
| Manual entries have rationale | If Source = Manual, a user-provided rationale must be present |
| No orphan entries | Every entry links to something; no "floating" requirements with no origin |

**If traceability fails:**
1. Flag to user: "Register entry {ID} has no valid source link. Was this derived from {X}?"
2. Do NOT include in coverage calculations until resolved
3. Mark as `Source: Unresolved` temporarily

---

### 3. Risk Score Validation

Every register entry with Status = Missing MUST have a valid risk score:

| Check | What to Verify |
|-------|---------------|
| All 4 factors scored | Architectural Risk × Blast Radius × Logic Complexity × Change Frequency |
| Each factor 1-5 | No factor outside the 1-5 range |
| Composite calculated correctly | Product of 4 factors (not sum) |
| Bucket assigned correctly | 400-625 = Critical, 150-399 = High, 50-149 = Medium, 1-49 = Low |
| Rationale provided for scores ≥4 | Any factor scored 4 or 5 must have a brief justification |

**Scoring integrity rules:**
- Never score ALL factors at 5 without justification (625 is the maximum — reserved for genuinely critical gaps)
- Never score ALL factors at 1 (if truly all-1, question whether the test is needed at all)
- Architectural Risk should be highest for: auth, data integrity, core business logic
- Blast Radius should be highest for: shared components, platform layers, API gateways
- Logic Complexity should be highest for: state machines, algorithms, concurrent operations
- Change Frequency should be highest for: actively developed code, feature-flagged areas

---

### 4. Classification Consistency

Every register entry must follow the taxonomy defined in `test-taxonomy.md`:

| Check | What to Verify |
|-------|---------------|
| Test Level valid | Must be one of: Unit / Integration / System / Acceptance |
| Test Type valid | Must be one of: Functional / Non-Functional / Structural |
| Sub-Type valid | Must match a sub-type under the chosen Type (see taxonomy) |
| Level matches scope | Unit = isolated; Integration = cross-boundary; System = full stack; Acceptance = business value |
| Type matches focus | Functional = correctness; Non-Functional = quality attribute; Structural = internal quality |
| No level/type mismatch | e.g., "Unit + Non-Functional + Performance" is invalid (performance requires system scope) |

**Common misclassification patterns to catch:**

| Wrong | Correct | Why |
|-------|---------|-----|
| Unit + Performance | System + Performance | Performance requires realistic load conditions (not isolated) |
| Acceptance + Security | System + Security | Security tests verify system-level controls, not user-facing business value |
| Unit + Contract | Integration + Contract | Contracts are between components (by definition cross-boundary) |
| Integration + Business Logic | Unit + Business Logic | Pure business rules are tested in isolation (no dependency needed) |
| System + Boundary | Unit + Boundary | Boundary/edge cases are best caught at the unit level |

---

### 5. Register Consistency Checks

The test register must be internally consistent:

| Check | What to Verify |
|-------|---------------|
| No duplicate entries | Same commitment + same test name = duplicate (merge or remove) |
| Status values valid | Required / Exists / Missing / Failing / Deprecated / Overridden |
| Deprecated entries excluded from coverage | Coverage % uses only active entries (not deprecated/overridden) |
| Commitment IDs unique per source | No two entries from the same AP artifact share the same commitment ID |
| Missing tests have risk scores | Every Missing entry has a valid composite risk score |
| Existing tests have verification note | How was existence confirmed? (file path, test name match, etc.) |

---

### 6. Coverage Report Validation

Coverage reports must be mathematically correct and multi-dimensional:

| Check | What to Verify |
|-------|---------------|
| Percentage calculation correct | Coverage = (Tests Existing / Tests Required) × 100 — exclude Deprecated and Overridden |
| Multiple views present | By commitment, by component, by test type, by risk level (minimum 3 views for Standard+) |
| No 100% claim without verification | If claiming 100% coverage on a commitment, every derived test must have Status = Exists |
| Gap identification specific | Don't say "coverage is low" — say "API-USERS endpoint missing contract tests for 3/5 error codes" |
| Trend data included (if prior reports exist) | Show delta: "Coverage improved from 42% → 58% since last report" |

---

### 7. Strategy Document Validation

The test strategy must be complete and actionable:

| Check | What to Verify |
|-------|---------------|
| Test pyramid ratios defined | Unit : Integration : System : Acceptance percentages |
| Test types relevant to project | Only include types that apply (don't list "Accessibility tests" if no UI exists) |
| Tools/frameworks identified | From DW tech stack — not invented (use what the workspace provides) |
| Coverage goals per level | Specific targets, not vague ("≥80% unit coverage" not "good coverage") |
| Entry/exit criteria defined | What must be true before tests can run; what must be true after |
| Test data strategy addressed | How test data is created, managed, and cleaned up |
| Automation approach stated | Which tests are automated vs. manual (and why) |

---

### 8. Defect Log Validation

Every defect entry must be complete:

| Check | What to Verify |
|-------|---------------|
| Defect ID unique and sequential | DEF-001, DEF-002, ... — no gaps, no duplicates |
| Severity assigned | Critical / High / Medium / Low |
| Category assigned | Functional / Performance / Security / Data / Integration |
| Linked Component present | Which architectural component is affected |
| Status valid | Open / Investigating / Fixed / Verified / Closed |
| Root Cause populated (when known) | Once investigation completes, root cause must be documented |
| Linked Test noted | Which test caught it, OR "manual discovery" if found outside testing |

---

### 9. Architecture Alignment

TGE outputs must be consistent with the Architecture Package they govern:

| Check | What to Verify |
|-------|---------------|
| Component names match AP exactly | If AP says "UserService" — register says "UserService" (not "User Service" or "users") |
| API endpoint paths match | If AP defines `POST /api/v1/users` — register uses the same path |
| ADR references valid | If citing ADR-003 — that ADR must exist in the AP |
| Integration names match | External system names consistent between AP and register |
| NFR values match | If AP says "p95 ≤ 200ms" — strategy/register uses the same target |
| Tech stack references accurate | Testing frameworks mentioned must match what DW actually provides |

**If misalignment found:**
1. Flag to user: "Register uses '{X}' but AP defines '{Y}'. Which is current?"
2. Update register to match AP (AP is authoritative for architecture naming)
3. If AP itself is wrong, recommend user update AP first, then reconcile

---

### 10. Depth Level Compliance

Output detail must match the active depth level:

| Artifact | Minimal | Standard | Comprehensive |
|----------|---------|----------|---------------|
| Test Strategy | 1-2 page summary; pyramid ratios; tool list | Full strategy; all sections from validation §7 | + detailed test data strategy; automation roadmap; environment plan |
| Test Register | Commitment + test name + status + source | + risk score + level/type + linked component | + detailed assertions + test preconditions + data requirements |
| Coverage Report | Single percentage + gap list | Multi-view (3+ dimensions) + trend | + traceability matrix + heat map by component + historical trend |
| Debt Scorecard | Risk buckets with counts | + individual scoring per missing test | + remediation suggestions + effort estimates + sprint mapping |
| Defect Log | Basic fields (ID, severity, status) | + linked component + root cause | + timeline + linked tests + regression prevention note |

---

### 11. Naming Conventions

| Rule | Example |
|------|---------|
| TGE output folder | `.governance/test/` (dotfolder, lowercase) |
| State file | `tge-state.md` (lowercase, hyphenated) |
| Strategy file | `test-strategy.md` (lowercase, hyphenated) |
| Register file | `test-register.md` (lowercase, hyphenated) |
| Coverage report | `coverage-report.md` (lowercase, hyphenated) |
| Debt scorecard | `debt-scorecard.md` (lowercase, hyphenated) |
| Defect log | `defect-log.md` (lowercase, hyphenated) |
| Commitment IDs | `{CATEGORY}-{NNN}` (e.g., API-001, SEC-003, DATA-012) |
| Baseline IDs | `BASE-{CATEGORY}-{NN}` (e.g., BASE-API-01, BASE-SEC-02) |
| Defect IDs | `DEF-{NNN}` (e.g., DEF-001, DEF-042) |
| Story references | `STORY-{ID}-AC{N}` (e.g., STORY-012-AC3) |

---

### 12. Placeholder Hygiene

TGE outputs should have MINIMAL placeholders — the engine derives content from existing sources:

| Acceptable Placeholders | Context |
|------------------------|---------|
| `_[Pending AP reconciliation]_` | AP changed but reconciliation not yet run |
| `_[Test existence unverified — scan needed]_` | Brownfield detected but not yet assessed |
| `_[Risk score pending — requires depth ≥ Standard]_` | Depth is Minimal; risk scoring not active |
| `_[Root cause: investigating]_` | Defect logged but root cause not yet determined |

**Unacceptable in TGE outputs:**
- `_[TBD]_` without explanation (must say why it's pending)
- Placeholder for a test requirement (either derive it or don't include it)
- Empty risk scores on Missing entries (if Missing → must be scored)
- Blank commitment IDs (every entry must be identified)

---

## Validation Failure Handling

If validation fails:

| Failure Type | Action |
|-------------|--------|
| Traceability broken | Alert user; mark entry as `Source: Unresolved`; exclude from coverage |
| Risk score invalid | Recalculate from factors; if factors missing, prompt user for assessment |
| Classification mismatch | Correct automatically if clear (e.g., Unit+Performance → System+Performance); flag if ambiguous |
| Duplicate entries | Merge (keep the one with more detail); alert user |
| AP alignment drift | Flag specific mismatches; update register to match current AP |
| Coverage math wrong | Recalculate from register data (register is source of truth) |
| Depth violation | Either upgrade output detail OR explain why depth was reduced |
| Missing metadata | Add metadata from state file (engine always knows current mode/depth/version) |

---

## Cross-Artifact Consistency

When multiple TGE artifacts reference each other:

| Reference | Source of Truth |
|-----------|----------------|
| Register entry count | `test-register.md` (actual entries counted) |
| Coverage percentage | Calculated from register (Exists / Required) |
| Risk score | `debt-scorecard.md` (latest scoring) |
| Defect count by severity | `defect-log.md` (actual entries counted) |
| Strategy tools/frameworks | `test-strategy.md` (derived from DW tech stack) |
| State statistics | Recalculated from artifacts (never manually maintained) |

**Rule:** State file statistics are DERIVED from artifacts, not the other way around. If state says "Coverage: 58%" but register calculation shows 62%, update state (register is authoritative).
