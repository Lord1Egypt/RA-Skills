# Phase 2: Ecosystem Mapping

**Goal**: For every symbol imported or used in the source project, find its target-language
equivalent and document the equivalence type, precision delta, and any gaps.

The output is a complete `ecosystem-map.yaml` that Phase 4 will use as a lookup table.
AI must never guess an equivalence in Phase 4 — it must be in this map first.

---

## ⛔ No Silent Batch Confirmation

**Confirming a mapping without evidence of research is task fraud.**

Every entry that moves from `NEEDS_REVIEW` to `CONFIRMED` must have its
`confirmation_evidence` field populated. This field can ONLY be filled by
actually looking up the source symbol's behavior AND the target equivalent's behavior.

An AI that batch-converts NEEDS_REVIEW → CONFIRMED without populating evidence
fields has not done the work. This is detectable and will cause P4 structural errors.

---

## Entry Criteria

- `phases.P1_asset_scan: DONE`
- `asset-inventory.yaml` has `depends_on_ecosystem` populated for all source files

## Exit Criteria

- Every unique symbol has an entry in `ecosystem-map.yaml`
- Every entry has `status: CONFIRMED` or `status: GAP_ACCEPTED`
- Every CONFIRMED entry has `confirmation_evidence` populated (not empty)
- Every GAP_ACCEPTED entry has `compensation_strategy` and `gap_notes` populated
- AI Self-Verification Protocol completed and reported
- `phases.P2_ecosystem_map: DONE`, `phases.P3_ipo_analysis: IN_PROGRESS`

---

## Symbol Extraction

### Step 1: Collect all unique symbols

Aggregate all values from `depends_on_ecosystem` across the entire `asset-inventory.yaml`.
Deduplicate. Sort by category: types first, then stdlib, then third-party.

Also do a **deep scan** of each source file to find:
- Module-level type aliases
- Implicit behavior dependencies (dict ordering, integer overflow behavior)
- Precision-sensitive operations (float division, bit shifts)
- Platform-specific behaviors (path separators, encoding defaults)

### Step 2: Classify and Research

Use the language pair module as primary reference.
For each symbol NOT in the language pair module, research from first principles:

1. What does this symbol guarantee (semantics, precision, ordering, memory layout)?
2. Does the target have a native equivalent with identical guarantees?
3. If not, what is the closest and what is the gap?
4. Can a third-party package close the gap?

---

## Confirmation Evidence Protocol (Anti-Cheating)

Every entry that reaches `status: CONFIRMED` must include:

```yaml
- id: "numpy.float64"
  ...
  status: CONFIRMED
  confirmed_by: "AI"
  confirmation_evidence:
    source_behavior: "IEEE 754 double-precision; supports NaN/Inf; numpy broadcasting"
    target_behavior: "f64 in Rust: IEEE 754 double-precision; no broadcasting semantics"
    equivalence_rationale: "Bit-width and IEEE 754 conformance match; broadcasting gap documented in gap_notes"
    verified_from: "numpy docs §3.1 + rust f64 reference + source file entropy.py line 12"
```

**`confirmation_evidence` is mandatory for every CONFIRMED entry.**

An entry with empty `confirmation_evidence` is considered `NEEDS_REVIEW` regardless of its `status` field.
P2 cannot be marked DONE if any CONFIRMED entry has empty evidence.

For GAP_ACCEPTED entries, replace `confirmation_evidence` with:

```yaml
  gap_acceptance_evidence:
    gap_description: "specific, precise description of what is missing"
    compensation_strategy: "exact implementation plan in target language"
    human_decision: "if applicable — user decision reference"
    verified_from: "source and target docs consulted"
```

---

## Equivalence Classification Rules

### Structural equivalence
Same data representation, same algorithm complexity, same precision, same ordering,
same error semantics. Requires verification of ALL five criteria.

### Behavioral equivalence (acceptable)
Observable inputs → outputs are identical, but internal structure differs.
Must document the internal difference in `gap_notes`. Must still populate `confirmation_evidence`.

### Partial equivalence (use with caution)
Covers the common case but has documented edge cases.
Must verify that source project does NOT exercise the edge cases.
Requires evidence that the source was checked.

### None (no equivalent)
Must have `compensation_strategy`. Always triggers BLOCKED — human decides.

---

## Critical Categories to Research and Evidence

### Numeric Types and Precision

For every numeric type: bit width, signed/unsigned, overflow behavior,
float NaN/Inf handling, division-by-zero behavior. All must be in `confirmation_evidence`.

### Collections and Ordering

Ordering guarantees, mutability, memory layout. Especially: does the source rely on
dict insertion order? Does any algorithm depend on set iteration order?

### Randomness (High Risk)

If source uses RNG:
- What algorithm? (Python default: Mersenne Twister)
- Is bit-identical output required?
- Evidence must show the source algorithm was identified

### Concurrency Model

Map: threads, async/await, locks, channels, atomics.
Note paradigm differences and their implication for control flow.

---

## AI Self-Verification Protocol

**Before marking P2 DONE**, the AI must run and report all three checks:

### Check 1: Evidence Coverage

```
CHECK 1 — Confirmation Evidence Coverage:
  total_entries: <N>
  CONFIRMED_with_evidence: <N>
  CONFIRMED_missing_evidence: <X>   ← must be 0
  GAP_ACCEPTED_with_evidence: <N>
  GAP_ACCEPTED_missing_evidence: <Y>   ← must be 0
  NEEDS_REVIEW_remaining: <Z>   ← must be 0
  action: <re-researched X entries / none required>
```

### Check 2: Behavioral Consistency Spot-Check

Randomly select 5 CONFIRMED entries.
For each, the AI must write — from memory, without re-reading docs —
what specific behavior difference (if any) exists between source and target.
Generic or vague answers indicate the mapping was not actually researched.

```
CHECK 2 — Spot-Check (5 random CONFIRMED entries):
  entry_1: <id> → source_behavior: <specific> | target_behavior: <specific> | delta: <none/described>
  entry_2: ...
  entry_3: ...
  entry_4: ...
  entry_5: ...
  spot_check_result: PASS / FAIL
  action: <re-researched X entries / none required>
```

### Check 3: Gap Completeness

For every `equivalence_type: none` entry:
- Is `compensation_strategy` specific enough to implement? (not just "rewrite in Go")
- Is it actionable without further research?

```
CHECK 3 — Gap Compensation Completeness:
  none_equivalence_entries: <N>
  GAP_ACCEPTED_with_specific_strategy: <N>
  GAP_ACCEPTED_with_vague_strategy: <X>   ← must be 0
  action: <refined X strategies / none required>
```

**All three checks must pass before `phases.P2_ecosystem_map` is set to DONE.**
The verification report must appear in the AI's response before the status update.

---

## Gap Resolution Strategies

When a gap is found, evaluate in order:

1. **Direct equivalent** — target stdlib has it; use it
2. **Third-party package** — well-maintained package fills the gap; add to `new_dependencies`
3. **Custom shim** — write a small wrapper; document in `compensation_strategy` with specific API
4. **Algorithm restructure** — document restructuring plan in `compensation_strategy`
5. **Human decision required** — none viable → BLOCK

---

## Update State

After each batch of entries:
```yaml
stats:
  ecosystem_entries_total: <n>
  ecosystem_entries_done: <confirmed + gap_accepted>
  ecosystem_entries_blocked: <n>
```

At phase exit (only after Self-Verification Protocol passes):
```yaml
phases:
  P2_ecosystem_map: DONE
  P3_ipo_analysis: IN_PROGRESS
meta:
  new_dependencies: [<list all target packages added>]
```

---

## Phase Exit: Trigger PGR-2

When you believe P2 is complete, do NOT mark it DONE yet.

Load `references/phase-gate-review.md` and run PGR-2 using the audit criteria defined there.
Only set `phases.P2_ecosystem_map: DONE` after PGR-2 passes with zero findings.

The PGR-2 loop will:
1. Verify every import/symbol from translate-strategy source files has an ecosystem-map entry
2. Verify no entries remain at `status: NEEDS_REVIEW`
3. Verify every CONFIRMED entry has non-empty `confirmation_evidence.source_behavior` and `target_behavior`
4. Verify every entry has `equivalence_type` set
5. Verify no orphan entries reference symbols not found in source files
6. Fix any findings autonomously and re-audit from scratch until zero findings remain

`phases.P2_ecosystem_map: DONE` is set by PGR-2 as its final action — never set it directly.
