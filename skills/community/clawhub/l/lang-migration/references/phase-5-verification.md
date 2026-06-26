# Phase 5: Verification

**Goal**: Confirm that every translated function satisfies its IPO specification through
structural review and real-data behavioral testing. No mocks. No workarounds.

Verification has two tracks, both mandatory:
- **Track A: Structural Review** — does the code match the IPO registry?
- **Track B: Behavioral Testing** — does the code produce correct output on real data?

---

## Entry Criteria

- `phases.P4_translation: DONE`
- Target project compiles without errors

## Exit Criteria

- Every function has passed both Track A and Track B
- All test fixtures produce identical outputs (within documented precision delta)
- `phases.P5_verification: DONE`

---

## ⛔ Entry Guard: P4 Completeness Check

Before starting P5:

```
P5 ENTRY CHECK:
  Scan ipo-registry.yaml:
    - entries_with_empty_target_lines: <N>   ← must be 0
    - entries_still_TODO: <N>                ← must be 0
  
  If either count > 0: P4 is incomplete. Return and finish.
```

---

## Track A: Structural Review

For each function, compare the target implementation against its IPO registry entry.
This is a mechanical checklist — do not use judgment to "accept" deviations; flag them.

### Checklist per function

- [ ] **Step count**: Does the target have the same number of logical steps as `process.steps`?
- [ ] **Step order**: Are the steps in the same order?
- [ ] **Magic numbers**: Is every magic number a named constant with the correct value?
- [ ] **Invariants**: Is every `inferred_invariant` present as a comment or debug assertion?
- [ ] **Side effects**: Are all documented side effects present? Are there any *undocumented* side effects?
- [ ] **Error conditions**: Does the target raise/return errors in the same conditions?
- [ ] **Ecosystem refs**: Is the `compensation_strategy` applied wherever `equivalence_type != structural`?

### Structural Review Outcome

- **PASS**: All checklist items confirmed
- **MINOR_DEVIATION**: One or two items differ but the difference is explainable and documented → acceptable, append note to `translation_notes`
- **FAIL**: Step missing, step reordered, magic number value changed, or undocumented side effect → must return to P4

---

## Track B: Behavioral Testing

### Source: original test suite

The primary test source is the source project's existing test suite, migrated in P4.
These tests use the **original test fixtures** (direct_use files) — no new data is generated.

**Zero tolerance for mock**: If a test would require mocking to pass, do not mock it.
Instead:
1. Document what real environment/dependency is needed
2. Set `status: BLOCKED` with `human_input_required` describing what is needed
3. The test remains in the suite; it must pass when the dependency is available

### Test Output Evidence (Anti-Cheating)

"Tests pass" is not a valid completion statement. The AI must show actual test output.

After running tests, output the following in the response:

```
TEST OUTPUT EVIDENCE:
  command_run: "<exact command executed>"
  exit_code: <0 = pass, non-zero = fail>
  output_excerpt: |
    <actual test runner output — first 30 lines>
  passed: <N>
  failed: <N>
  skipped: <N>
  blocked_real_deps: <N>
```

If the AI says "tests pass" without providing TEST OUTPUT EVIDENCE, the claim is unverified.
The human must request the actual output before accepting P5 as complete.

### Differential Testing

For each function with deterministic inputs and outputs:

1. Run the source implementation on a set of test inputs → record ground truth outputs
2. Run the target implementation on the same inputs
3. Compare outputs

```bash
# In full_mode, automate this:
python scripts/run_differential.py \
  --source-fn "src/core/entropy.py::calculate_entropy" \
  --target-fn "src/core/entropy.rs::calculate_entropy" \
  --fixtures "tests/fixtures/"
```

### ⛔ Stateful / Accumulating Function Differential Testing

For functions that maintain internal state or accumulate output across multiple calls
(identified by `side_effects` containing "mutates self.", "appends to", "increments counter"):

**Standard differential testing is insufficient** — a snapshot at turn N may match even
when the delta between N-1 and N is wrong (the classic B1/B2 drift pattern).

**Mandatory protocol:**

1. Run the source implementation for **N iterations** (N ≥ 20, or 2× the largest `magic_number` cycle in the IPO entry)
2. Record the **incremental delta** at each iteration: `delta_i = output_i − output_{i-1}`
3. Run the target implementation for the same N iterations
4. Compare deltas iteration-by-iteration — not just the final snapshot

```
STATEFUL DIFFERENTIAL EVIDENCE:
  function: "<fn_id>"
  iterations_run: <N>
  source_delta_at_N:  "<value or structure>"
  target_delta_at_N:  "<value or structure>"
  drift_detected: true / false
  first_divergence_at_iteration: <i>   # if drift_detected
```

If `drift_detected: true` → this is a `side_effect_dropped` root cause (see retrospective protocol).

### ⛔ Boundary-Value Testing for Numeric Threshold Constants

For any function whose IPO registry `magic_numbers` contains an `iteration_limit` or `threshold` type:

**Mandatory**: test at exactly `value - 1`, `value`, and `value + 1`.

```
BOUNDARY TEST EVIDENCE:
  function: "<fn_id>"
  magic_number_tested: <value>     # e.g. 65 (turn cadence)
  source_at_N_minus_1: "<behavior>"  # e.g. "no callback triggered"
  source_at_N:         "<behavior>"  # e.g. "ask_user called"
  source_at_N_plus_1:  "<behavior>"  # e.g. "no callback triggered"
  target_at_N_minus_1: "<behavior>"
  target_at_N:         "<behavior>"
  target_at_N_plus_1:  "<behavior>"
  boundary_match: true / false
```

If `boundary_match: false` → the magic number was not correctly applied.
Root cause category: `magic_number_decontextualized` or `control_flow_collapsed`.

**When to apply**: check the IPO entry's `magic_numbers` before writing tests. If ANY entry
has `type: iteration_limit` or `type: threshold`, boundary testing is mandatory.
This test cannot be skipped by claiming "the happy path covers it."

### Precision Tolerance

For floating-point comparisons:
- If `precision_delta: none` in ecosystem map → exact equality required (bitwise for same-precision types)
- If `precision_delta: narrower` or `wider` → use the tolerance documented in ecosystem map
- Never set tolerance wider than documented without human approval

### Non-Deterministic Functions

For functions with `non_deterministic: true`:
- Test that outputs fall within the documented statistical distribution
- Do NOT compare individual values against source output
- Document the test strategy in `translation_notes`

---

## Verification Matrix

Maintain a verification record. After each function passes both tracks, update `ipo-registry.yaml`:

```yaml
translation_status: DONE
verification:
  structural: PASS
  behavioral: PASS
  behavioral_test_file: "tests/test_entropy.rs"
  notes: ""
```

---

## Regression Strategy + TDD Retrospective Protocol

When a Track A structural deviation or Track B test failure is found:

### ⛔ STEP 0: Bug Triage — Mandatory Before Any Fix

**Do not touch the target code until triage is complete.**

A failing test or structural deviation has four possible root locations.
Misidentifying the location leads to fixing the wrong thing — or deleting
correct code that faithfully mirrors the source.

Execute this triage sequence in order. Stop at the first conclusive answer.

---

#### Triage Step T1: Map the failure to the IPO registry

```
T1 TRIAGE:
  failing_function: "<fn_id in ipo-registry.yaml>"
  failing_step:     "<which process.step does the mismatch correspond to?>"
  ipo_source_lines: "<source_lines from that step>"
  target_matches_ipo_step: true / false
```

- If `target_matches_ipo_step: false` → **Translation Error** — target deviates from IPO spec → go to Step 1 (Fix)
- If `target_matches_ipo_step: true` → target code is correct per IPO spec → continue to T2

---

#### Triage Step T2: Read the actual source lines

Using `ipo_source_lines`, read the SOURCE file at those exact lines.

```
T2 TRIAGE:
  source_file_read: "<file>:<line_start>-<line_end>"
  source_behavior: "<what the source code does at those lines>"
  target_behavior: "<what the target code does>"
  source_matches_target: true / false
```

- If `source_matches_target: true` → **Source-Faithful Behavior** — the target correctly reproduces source behavior; the test expectation may be wrong → go to T3-ANNOTATE
- If `source_matches_target: false` → The IPO registry recorded wrong lines (`ipo_source_lines_wrong`) → flag and go to Step 1 (Fix with retrospective category `ipo_source_lines_wrong`)

---

#### Triage Step T3: Investigate the consumer / caller path

Before concluding anything is wrong, verify:

```
T3 TRIAGE:
  callers_checked: ["<file>:<fn> calls this function"]
  test_fixture_format_correct: true / false   # does fixture match target lang format?
  caller_passes_correct_args: true / false
  test_exercises_correct_behavior: true / false
  consumer_path_verdict: CONSUMER_ERROR / ECOSYSTEM_DIFFERENCE / CONFIRMED_TRANSLATION_ERROR
```

- `CONSUMER_ERROR` — the bug is in the caller, test fixture, or test assertion — fix the consumer, not the function
- `IMPLICIT_CAPABILITY_ASSUMPTION` — the source design relied on a capable consumer (strong model, smart runtime) that the target consumer lacks; the translated function is correct, but the integration layer needs to make the implicit contract explicit (e.g., add a code_run example to a system prompt, add an explicit trigger rule). Fix in the integration layer, **not** in the translated function. Document the assumed capability in the IPO registry `inferred_invariants`.
- `ECOSYSTEM_DIFFERENCE` — the difference is a known and documented gap — verify compensation strategy is applied correctly; if yes, update test expectation to match target semantics
- `CONFIRMED_TRANSLATION_ERROR` — none of the above apply; the function itself is wrong → go to Step 1 (Fix + retrospective)

---

#### T3-ANNOTATE: Source-Faithful Behavior Resolution

When T2 confirms the target faithfully reproduces source behavior:

1. **Add a comment in the target code** at the relevant line(s):
   ```go
   // SOURCE-FAITHFUL: <description of behavior>
   // Source: <source_file>:<line_range> — matches Python behavior exactly.
   // If this behavior needs to change, change the source first and re-run P3.
   ```

2. **Add a `known_source_behaviors` entry to the IPO registry**:
   ```yaml
   known_source_behaviors:
     - desc: "<what this behavior does>"
       source_file: "<file>"
       source_lines: "<start>-<end>"
       intentional: true     # true = deliberate design; false = source has a bug we're faithfully reproducing
       annotation_added: true
       annotation_location: "<target_file>:<line>"
   ```

3. **If `intentional: false`** (source has a genuine bug being faithfully reproduced):
   - Do NOT silently fix it in the target — that creates behavioral divergence
   - Set `current_task.status: BLOCKED` with `human_input_required: "Source has bug at <lines>. Fix source and re-run P3? Or accept known deviation?"`
   - Wait for human decision before proceeding

4. **Fix the test** (if source-faithful is the verdict):
   - Update the test assertion to match source semantics
   - Add a comment in the test: `// Source-faithful: tests source behavior, not ideal behavior`

5. **No retrospective entry is required** for source-faithful resolutions — they are not translation errors.

---

### Step 1: Diagnose
- **Track A failure**: which IPO checklist item failed? Which step/magic_number/invariant?
- **Track B failure**: binary search to identify which IPO process step produces wrong output; add intermediate value logging

Check in order:
1. Does the error originate in a dependency function? (re-verify callees first)
2. Does ecosystem-map show a gap that was documented but not applied?
3. Was an inferred invariant from P3 not reflected in the translation?

### Step 2: Fix

Apply the minimal correct fix. Do not refactor unrelated code during a test fix.

### Step 3: MANDATORY — TDD Retrospective (see `references/tdd-retrospective.md`)

After every fix — without exception — run the four-step retrospective:

```
ROOT CAUSE ANALYSIS → write RCA entry to retrospective-checklist.yaml
CHECKLIST RULE      → "Whenever [pattern], check for [property]"
SCOPE SCAN          → define search pattern BEFORE scanning; classify all hits
CONSISTENT FIX      → same fix strategy for all FIXED instances
```

### Step 4: Re-run Full Test Suite

After the retrospective scope fixes are applied, re-run the **complete** test suite —
not just the originally failing test. A scope-scan fix may introduce a new failure
in a related component.

```bash
go test ./...     # full suite
go vet ./...      # structural check
```

If new failures appear: each triggers its own independent retrospective.
Do not batch multiple failures into one retrospective entry.

### Step 5: Retrospective Checklist Gate (end of P5)

Before marking P5 DONE, read all entries in `retrospective-checklist.yaml` and output
the Checklist Summary (defined in `references/tdd-retrospective.md`).

---

## Final Phase Checklist

Before marking P5 DONE:

- [ ] All functions: `translation_status: DONE`
- [ ] All functions: `verification.structural: PASS`
- [ ] All functions: `verification.behavioral: PASS` (or `BLOCKED` with documented real dependency)
- [ ] Every Track B failure went through Bug Triage (T1→T2→T3) before any fix was applied
- [ ] Every `source_faithful_behavior` finding has a `SOURCE-FAITHFUL` comment in target code AND `known_source_behaviors` entry in IPO registry
- [ ] Every `consumer_error` finding has its fix in the caller/test, NOT in the translated function
- [ ] No `known_source_behaviors` with `intentional: false` is unresolved (must be BLOCKED or human-approved)
- [ ] Target project builds cleanly (no warnings treated as errors)
- [ ] Original CI pipeline (adapted) passes on the target project
- [ ] `migration-state.yaml` final stats are updated
- [ ] `decisions_log` includes all human decisions made during the migration
- [ ] `retrospective-checklist.yaml` complete; Checklist Summary output in response
- [ ] Ecosystem-map entries updated where `ecosystem_map_update_required: true`
- [ ] A `MIGRATION_NOTES.md` is written at the target project root documenting:
  - Source project and version
  - Target language and toolchain version
  - All `GAP_ACCEPTED` entries and their compensation strategies
  - All behavioral equivalence decisions
  - Known limitations vs source
  - Retrospective summary: most common root cause category and improvement suggestion

---

## Phase Exit: Trigger PGR-5

When you believe P5 is complete, do NOT mark it DONE yet.

Load `references/phase-gate-review.md` and run PGR-5 using the audit criteria defined there.
Only set `phases.P5_verification: DONE` after PGR-5 passes with zero findings.

The PGR-5 loop will:
1. Verify every ipo-registry entry has TEST OUTPUT EVIDENCE (actual runner output shown in session)
2. Verify every retrospective entry from P5 is `status: RESOLVED` or `status: DEFERRED` with a documented reason
3. Verify the Gap Report (P6) has been run and its output is present in the session response showing TRUE 1:1 COMPLETION
4. Verify the gap report shows `d5.accidental_gaps == 0`
5. Verify the Final Retrospective Checklist Summary has been output in the session response
6. Fix any findings autonomously and re-audit from scratch until zero findings remain

`phases.P5_verification: DONE` is set by PGR-5 as its final action — never set it directly.
After PGR-5 passes, the migration is complete.
