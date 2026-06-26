# Phase Gate Review (PGR) Protocol

**PGR is the mandatory autonomous self-auditing loop that runs between every phase transition.**

A phase is not complete when the AI says it is complete.
**A phase is complete when PGR-N passes with zero findings.**

No human involvement is required or permitted inside a PGR loop. The AI audits its own work,
finds gaps, fixes them, and re-audits — autonomously — until the finding count reaches zero.

---

## Why PGR Exists

Each phase has exit criteria. Without PGR, an AI can mark a phase DONE the moment the last
task appears finished, without checking whether the sum of all outputs meets the stated criteria.
PGR closes this gap by requiring a systematic, exhaustive audit before the phase status changes.

The same anti-cheating principles that govern individual tasks apply here:
- The AI must never claim zero findings without running the audit
- Every finding must have artifact evidence (a specific file, field, line number)
- A fix is only valid when the artifact evidence changes — not when the AI says it changed

---

## Universal PGR Loop Algorithm

This algorithm is identical for every PGR-N. Only the audit criteria differ per phase (see below).

```
PHASE-N FINISHES
  ↓
[ENTER PGR-N]
  ↓
Step 1: ENUMERATE
  Load the PGR-N audit criteria from this document.
  Enumerate every item that must be checked (files, YAML entries, field values, etc.).
  Record the total item count.
  ↓
Step 2: AUDIT
  For each item in the enumerated list:
    Run the specified check.
    If check PASSES: mark item OK.
    If check FAILS: record a FINDING with format:
      FINDING [N]: <item_id> — <check_name> — <specific failure description>
      Evidence: <exact file path, field, value, or line that is wrong>
  ↓
Step 3: TALLY
  Output the PGR-N Audit Report (see format below).
  IF findings_count == 0:
    → Advance to "ZERO FINDINGS" path below.
  IF findings_count > 0:
    → Advance to "FIX" path below.
  ↓
Step 4 (FIX path): FIX
  For each FINDING in order:
    Apply the fix described in the "What 'fixed' means" section for PGR-N.
    Record: FIXED [N]: <item_id> — <what was changed> — <artifact evidence of fix>
  increment iteration_count
  increment findings_resolved by count of findings just fixed
  Update migration-state.yaml:
    phase_gates.PGR_N.iteration_count: <new count>
    phase_gates.PGR_N.findings_resolved: <cumulative count>
    phase_gates.PGR_N.status: IN_PROGRESS
  → Return to Step 1 (ENUMERATE). A new full audit pass is required — not just re-checking fixed items.
  ↓
Step 5 (ZERO FINDINGS path): PASS
  Output final PGR-N report with zero findings.
  Update migration-state.yaml:
    phase_gates.PGR_N.status: PASSED
    phase_gates.PGR_N.passed_at: "<ISO 8601 timestamp>"
    phase_gates.PGR_N.last_report: "<one-line summary>"
  Set phases.PN_xxx: DONE in migration-state.yaml.
  Proceed to the next phase.
```

**Critical rule**: After any fix, the ENTIRE audit must be re-run from Step 1 — not just the
previously-failing items. A fix to one item may invalidate another item's prior PASS result.

---

## Zero Findings — What It Means and How to Prove It

"Zero findings" means:

1. Every item in the enumerated list was checked against the specified check.
2. Every check produced a PASS result with artifact evidence (not just the AI's assertion).
3. The audit report lists `findings_count: 0` with the enumerated item count > 0.

**Zero findings cannot be claimed by:**
- Saying "I reviewed everything and it looks good"
- Running a partial audit and extrapolating
- Re-reading the same file that produced a previous PASS without re-executing the check

**Zero findings IS proven by:**
- Outputting the full audit report in the response, listing every item checked
- Each item showing its check result and the specific artifact that confirmed PASS
- `findings_count: 0` in the tally

---

## PGR Audit Report Format

Output this report in the AI's response at the end of every audit pass. Also store the
one-line summary in `migration-state.yaml` under `phase_gates.PGR_N.last_report`.

```
PGR-N AUDIT REPORT (iteration <K>)
  phase:              P<N> <phase_name>
  items_enumerated:   <total item count checked>
  items_passed:       <count>
  findings_count:     <count>   ← must be 0 to advance

  FINDINGS:
    FINDING [1]: <item_id> — <check_name> — <specific failure>
                 Evidence: <file:line or field:value>
    FINDING [2]: ...
    (none if zero findings)

  FIXES APPLIED THIS ITERATION:
    FIXED [1]: <item_id> — <what changed> — <artifact>
    FIXED [2]: ...
    (none on first-pass zero-finding run)

  RESULT: PASS / FINDINGS_REMAIN
```

---

## Anti-Cheating Rules for PGR

These rules are specific to the PGR process. General anti-cheating rules from SKILL.md also apply.

**Rule PGR-AC-1: No self-certification without artifact evidence.**
The AI must not write `findings_count: 0` and then list no items checked. Every PASS requires
the specific artifact (field value, file existence confirmation, line content) that proved it.

**Rule PGR-AC-2: Full re-audit after every fix.**
Returning to Step 2 after a fix (skipping Step 1 re-enumeration) is prohibited. The item list
may have changed (e.g., a fix adds new entries that now also need checking).

**Rule PGR-AC-3: Findings must reference specific artifacts.**
`FINDING [1]: asset-inventory.yaml — purpose field empty` is NOT sufficient.
`FINDING [1]: asset-inventory.yaml entry path=src/core/entropy.py — purpose field — value is ""` IS sufficient.
Vague findings cannot be verified fixed.

**Rule PGR-AC-4: Fix evidence must reference the same artifact.**
`FIXED [1]: asset-inventory.yaml entry src/core/entropy.py — purpose set to "Computes Shannon entropy over a probability distribution"` is the correct format.
"Fixed the empty purpose field" is not sufficient.

**Rule PGR-AC-5: iteration_count > 1 is not a failure.**
Multiple iterations are expected and correct. They mean the AI found and fixed real issues.
An iteration_count of exactly 1 with a complex phase output should be treated with suspicion.

**Rule PGR-AC-6: PGR status cannot be set to PASSED by skipping phases.**
If a phase status is set to DONE without a corresponding `phase_gates.PGR_N.status: PASSED`,
the session start protocol must detect this and re-run PGR-N before proceeding.

---

## PGR-0: Audit Criteria (after P0 Bootstrap)

### Expected Outputs

The five template files copied to `migration_workspace/` with meta blocks filled.

### Checks

**Check PGR-0-A: Template files exist**
- Verify these five files exist:
  - `migration_workspace/migration-state.yaml`
  - `migration_workspace/asset-inventory.yaml`
  - `migration_workspace/ecosystem-map.yaml`
  - `migration_workspace/ipo-registry.yaml`
  - `migration_workspace/retrospective-checklist.yaml`
- PASS: all five files exist on disk
- FINDING format: `PGR-0-A: migration_workspace/<filename> does not exist`

**Check PGR-0-B: Meta block filled**
- Read `migration_workspace/migration-state.yaml`
- Verify these fields are non-empty strings:
  - `meta.source_lang`
  - `meta.target_lang`
  - `meta.source_dir`
  - `meta.target_dir`
  - `meta.lang_pair_module`
  - `meta.project_name`
- PASS: all fields non-empty
- FINDING format: `PGR-0-B: migration-state.yaml meta.<field> is empty`

**Check PGR-0-C: lang_pair_module resolves to an existing file**
- Read `meta.lang_pair_module` value (e.g., `python-rust`)
- Check that `references/lang-pairs/<value>.md` exists
- PASS: file exists
- FINDING format: `PGR-0-C: references/lang-pairs/<value>.md does not exist — lang_pair_module value may be wrong`

**Check PGR-0-D: source_dir and target_dir documented**
- Verify `meta.source_dir` is a non-empty path string
- Verify `meta.target_dir` is a non-empty path string
- PASS: both non-empty
- FINDING format: `PGR-0-D: migration-state.yaml meta.<field> is empty`

**Check PGR-0-E: P0 phase status**
- Verify `phases.P0_bootstrap: DONE` in migration-state.yaml
- PASS: value equals `DONE`
- FINDING format: `PGR-0-E: phases.P0_bootstrap = <value>, expected DONE`

### What "fixed" means for PGR-0

- Missing file: copy the template from `templates/` and fill all required fields
- Empty meta field: ask the user for the value; do not guess
- Wrong lang_pair_module: correct the key to match an existing file, or create a new lang-pair module
- Wrong phase status: set `phases.P0_bootstrap: DONE` only after all other checks pass

---

## PGR-1: Audit Criteria (after P1 Asset Scan)

### Expected Outputs

A complete `asset-inventory.yaml` where every source file has a classified entry.

### Checks

**Check PGR-1-A: No missing files**
- Run `find <source_dir> -type f | sort` to get the current file list
- Compare against all `path` values in `asset-inventory.yaml`
- PASS: every file in the find output has a corresponding entry
- FINDING format: `PGR-1-A: source file <path> not in asset-inventory.yaml`

**Check PGR-1-B: purpose field non-empty and non-placeholder**
- For every entry in `asset-inventory.yaml`, check `purpose` field
- FAIL if: empty string, `"TBD"`, `"TODO"`, `"placeholder"`, or any variant
- PASS: every entry has a specific, meaningful purpose description
- FINDING format: `PGR-1-B: asset-inventory.yaml entry path=<path> — purpose is empty or placeholder: "<value>"`

**Check PGR-1-C: migration_strategy confirmed**
- For every entry, check `migration_strategy` field
- FAIL if: empty string, or still contains `# AUTO-CLASSIFIED` comment marker
- PASS: every entry has an explicit strategy value from the allowed set
- FINDING format: `PGR-1-C: asset-inventory.yaml entry path=<path> — migration_strategy is unconfirmed: "<value>"`

**Check PGR-1-D: status field set**
- For every entry, verify `status` is one of `DONE`, `BLOCKED`, `IN_PROGRESS`
- FAIL if: empty or value not in allowed set
- FINDING format: `PGR-1-D: asset-inventory.yaml entry path=<path> — status is "<value>"`

**Check PGR-1-E: by_strategy counts match actuals**
- Read the `by_strategy` summary block in `asset-inventory.yaml`
- Count actual entries per strategy value in the entries list
- PASS: counts match exactly
- FINDING format: `PGR-1-E: by_strategy.<strategy> shows <X> but actual count is <Y>`

**Check PGR-1-F: Re-scan for new files**
- Run `scan_assets.py` (or equivalent find command) again
- Diff result against current inventory
- PASS: no new files detected
- FINDING format: `PGR-1-F: new file detected since last scan: <path>`

### What "fixed" means for PGR-1

- Missing file entry: add entry with full classification (type, purpose, strategy, status)
- Empty/placeholder purpose: read the file; write a specific one-line purpose description
- Unconfirmed strategy: apply the strategy decision tree from `references/phase-1-asset-scan.md`
- Wrong counts: recount and update the `by_strategy` block
- New file found: classify and add entry; update counts

---

## PGR-2: Audit Criteria (after P2 Ecosystem Map)

### Expected Outputs

A complete `ecosystem-map.yaml` with every import/symbol confirmed or gap-accepted.

### Checks

**Check PGR-2-A: All source symbols are mapped**
- Scan every source file that has `migration_strategy: translate` in the inventory
- Extract all imports and symbols used
- Cross-reference against `ecosystem-map.yaml` entry IDs
- PASS: every symbol found in source has an entry
- FINDING format: `PGR-2-A: symbol <symbol> used in <file>:<line> has no ecosystem-map entry`

**Check PGR-2-B: No NEEDS_REVIEW entries remaining**
- Scan all entries in `ecosystem-map.yaml`
- FAIL if any entry has `status: NEEDS_REVIEW`
- FINDING format: `PGR-2-B: ecosystem-map.yaml entry id=<id> still has status: NEEDS_REVIEW`

**Check PGR-2-C: CONFIRMED entries have non-empty evidence**
- For every `status: CONFIRMED` entry:
  - Verify `confirmation_evidence.source_behavior` is non-empty
  - Verify `confirmation_evidence.target_behavior` is non-empty
- FINDING format: `PGR-2-C: ecosystem-map.yaml entry id=<id> — confirmation_evidence.<field> is empty`

**Check PGR-2-D: equivalence_type set on every entry**
- For every entry, verify `equivalence_type` is one of: `structural`, `behavioral`, `partial`, `none`
- FAIL if: empty string or missing field
- FINDING format: `PGR-2-D: ecosystem-map.yaml entry id=<id> — equivalence_type is empty`

**Check PGR-2-E: No orphan entries**
- For every entry in ecosystem-map.yaml, verify the source symbol it maps exists in at least one source file
- PASS: all entries reference symbols actually used in the source
- FINDING format: `PGR-2-E: ecosystem-map.yaml entry id=<id> — source symbol <sym> not found in any source file`

### What "fixed" means for PGR-2

- Missing symbol: research the symbol and add a complete entry with confirmation_evidence
- NEEDS_REVIEW remaining: research and confirm or GAP_ACCEPT with evidence
- Empty evidence: look up source and target documentation; populate both fields specifically
- Empty equivalence_type: determine and set the correct classification
- Orphan entry: remove if truly unused, or verify the symbol IS used (grep may have missed it)

---

## PGR-3: Audit Criteria (after P3 IPO Analysis)

### Expected Outputs

A complete `ipo-registry.yaml` with every function documented and every field populated.

### Checks

**Check PGR-3-A: All translate-strategy functions are in registry**
- For every source file with `migration_strategy: translate`:
  - Extract all function/method definitions
- Cross-reference against entries in `ipo-registry.yaml`
- FAIL if any function is missing AND its `translation_status != SKIP`
- FINDING format: `PGR-3-A: function <source_file>::<fn_name> not in ipo-registry.yaml (not marked SKIP)`

**Check PGR-3-B: Every entry has at least one process step with source_lines**
- For every entry in ipo-registry.yaml:
  - Verify `process.steps` is non-empty
  - Verify at least one step has non-empty `source_lines`
- FINDING format: `PGR-3-B: ipo-registry.yaml entry id=<id> — no step has source_lines populated`

**Check PGR-3-C: Every magic number has non-zero source_line**
- For every `magic_numbers` item across all entries:
  - Verify `source_line` is not 0 and not empty
- FINDING format: `PGR-3-C: ipo-registry.yaml entry id=<id> magic_number value=<val> — source_line is 0 or empty`

**Check PGR-3-D: Every inferred_invariant has evidence bracket**
- For every `inferred_invariants` string across all entries:
  - Verify it contains `[inferred from:` substring
- FINDING format: `PGR-3-D: ipo-registry.yaml entry id=<id> invariant "<text>" — missing [inferred from: ...] bracket`

**Check PGR-3-E: No entry has translation_status: DONE**
- P3 populates the registry but does NOT translate; no entry should have `translation_status: DONE`
- FINDING format: `PGR-3-E: ipo-registry.yaml entry id=<id> has translation_status: DONE — P3 must not set DONE`

**Check PGR-3-F: Spot-check 5 random entries**
- Select 5 random entries from ipo-registry.yaml
- For each, re-read the actual source file for that function
- Verify that `first_statement` and `last_statement` (from READ_EVIDENCE) match actual file content
- PASS: both match for all 5 entries
- FINDING format: `PGR-3-F: entry id=<id> — first_statement "<recorded>" does not match actual line <N>: "<actual>"`

**Check PGR-3-G: Branch coverage — steps_count ≥ branch_count**
- For every entry in ipo-registry.yaml that has a `READ_EVIDENCE.branch_count` recorded:
  - Count the number of entries in `process.steps`
  - Verify `steps_count >= branch_count`
- A collapsed entry is one where multiple conditional branches were merged into a single step
- FINDING format: `PGR-3-G: entry id=<id> — steps_count=<s> < branch_count=<b>; branches collapsed`

**Check PGR-3-H: Post-construction call-site scan**
- For every entry whose `outputs` section describes a returned object or struct:
  - Identify all direct callers of this function in the source project
  - Verify each caller has an IPO entry in ipo-registry.yaml
  - Verify each caller's `side_effects` includes any `obj.attr = X` assignments made immediately after the call
- FINDING format: `PGR-3-H: caller <file>::<fn> calls <callee> but has no IPO entry / missing post-construction side_effects`

### What "fixed" means for PGR-3

- Missing function: run Phase 3 analysis protocol for that function (READ_EVIDENCE + BEHAVIOR_PROOF + fill entry)
- Missing source_lines: re-read source function; fill step source_lines with exact line range
- Missing source_line on magic number: re-read source; find the literal; record exact line
- Missing invariant bracket: re-read source and callers; write specific evidence for the invariant
- Entry marked DONE: set back to `TODO`; translation happens in P4
- Mismatched spot-check: re-analyze the specific function from scratch
- Collapsed branches (PGR-3-G): re-read source function; expand steps to one-step-per-branch; record each branch's source_lines
- Missing post-construction side_effects (PGR-3-H): read call sites; add `side_effects` entries to caller IPO; add `translation_notes` to callee IPO

---

## PGR-4: Audit Criteria (after P4 Translation)

### Expected Outputs

Every translate-strategy asset has a target file; every function is translated; build passes clean.

### Checks

**Check PGR-4-A: Every translate-strategy asset has a target file**
- For every entry in asset-inventory.yaml with `migration_strategy: translate`:
  - Verify the `target_path` file exists on disk
- FINDING format: `PGR-4-A: asset <path> has strategy=translate but target file <target_path> does not exist`

**Check PGR-4-B: Every DONE function has non-empty target_lines**
- For every ipo-registry.yaml entry with `translation_status: DONE`:
  - Verify `target_lines` is non-empty
- FINDING format: `PGR-4-B: ipo-registry.yaml entry id=<id> has translation_status: DONE but target_lines is empty`

**Check PGR-4-C: Retrospective ecosystem map updates applied**
- Read all entries in `retrospective-checklist.yaml`
- For every entry with `ecosystem_map_update_required: true`:
  - Verify the corresponding ecosystem-map.yaml entry has been updated
- FINDING format: `PGR-4-C: retrospective entry id=<id> has ecosystem_map_update_required: true but ecosystem-map.yaml entry id=<eco_id> was not updated`

**Check PGR-4-D: Retrospective Checklist Summary output**
- Verify the Retrospective Checklist Summary (defined in `references/tdd-retrospective.md`) has been output in the session response
- If it has not been output: trigger it now as part of the fix step
- FINDING format: `PGR-4-D: Retrospective Checklist Summary not yet output for P4`

**Check PGR-4-E: Build passes clean**
- Run `go build ./...` (Go), `cargo build` (Rust), `npm run build` (TypeScript/Bun), or equivalent for target language
- PASS: exit code 0, no errors
- FINDING format: `PGR-4-E: build failed — <compiler output excerpt>`

### What "fixed" means for PGR-4

- Missing target file: translate the asset using IPO registry (full Phase 4 protocol)
- Empty target_lines: locate the translated function in target file; record actual line range
- Unapplied ecosystem map update: apply the update from the retrospective entry to ecosystem-map.yaml
- Missing Checklist Summary: generate and output the summary now
- Build failure: diagnose and fix the compilation error; trigger TDD Retrospective if a code fix is applied

---

## PGR-5: Audit Criteria (after P5 Verification)

### Expected Outputs

Every function verified structurally and behaviorally; gap report run; retrospective complete.

### Checks

**Check PGR-5-A: Every function has TEST OUTPUT EVIDENCE**
- For every ipo-registry.yaml entry:
  - Verify `verification.behavioral` is `PASS` or `BLOCKED` (with documented real dependency)
  - Verify the session response contains TEST OUTPUT EVIDENCE block (actual runner output)
- FINDING format: `PGR-5-A: entry id=<id> has no behavioral verification result; TEST OUTPUT EVIDENCE not shown`

**Check PGR-5-B: All P5 retrospective entries are resolved**
- Read all entries in `retrospective-checklist.yaml` created during P5
- Verify every entry has `status: RESOLVED` or `status: DEFERRED` with a non-empty `deferred_reason`
- FINDING format: `PGR-5-B: retrospective-checklist.yaml entry id=<id> has status <value> — not RESOLVED or DEFERRED with reason`

**Check PGR-5-C: Gap Report (P6) has been run**
- Verify `references/phase-6-gap-report.md` protocol has been executed
- Verify the gap report output is present in the session response showing TRUE 1:1 COMPLETION
- FINDING format: `PGR-5-C: Gap Report (P6) not yet run or output not present in response`

**Check PGR-5-D: No accidental gaps**
- Read the gap report output
- Verify `d5.accidental_gaps == 0` (all gaps are intentional or documented)
- FINDING format: `PGR-5-D: gap report shows d5.accidental_gaps = <N> — must be 0`

**Check PGR-5-E: Final Retrospective Checklist Summary output**
- Verify the Final Retrospective Checklist Summary (P5-end version) has been output in the session response
- FINDING format: `PGR-5-E: Final Retrospective Checklist Summary not yet output for P5`

### What "fixed" means for PGR-5

- Missing TEST OUTPUT EVIDENCE: re-run the test suite; output TEST OUTPUT EVIDENCE block
- Unresolved retrospective entry: complete the RCA → checklist rule → scope scan → fix sequence; set status to RESOLVED
- Gap Report not run: run P6 Gap Report protocol now; output the full report
- Accidental gaps found: return to the relevant phase (P4 or P3) to close the gap; re-run verification
- Missing Checklist Summary: generate and output the summary now
