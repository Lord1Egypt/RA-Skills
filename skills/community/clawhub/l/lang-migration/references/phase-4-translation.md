# Phase 4: Translation

**Goal**: Translate every source function into the target language following the IPO registry
as the specification. Structural equivalence is mandatory unless the ecosystem map explicitly
documents a gap requiring behavioral equivalence.

**Primary rule**: Translate the IPO registry entry, not the source code directly.
The source code may be consulted for clarification, but the IPO entry is the contract.

---

## ⛔ Entry Guard: P3 Quality Check

Before starting P4, verify that P3 was genuinely completed:

```
P4 ENTRY CHECK:
  Sample 10 random ipo-registry.yaml entries.
  For each, confirm:
    - At least one step has non-empty source_lines? YES/NO
    - At least one magic_number has non-zero source_line? YES/NO (or no magic numbers)
    - inferred_invariants have [inferred from: ...] brackets? YES/NO (or none)

  If ANY sampled entry fails: P3 is incomplete.
  Action: Return to P3 and re-analyze failing entries before proceeding.
```

**Do not start P4 if the entry check reveals empty source_lines fields.**
A P3 with empty fields was batch-fabricated and will produce structurally wrong translations.

---

## Entry Criteria

- `phases.P3_ipo_analysis: DONE`
- `ipo-registry.yaml` has no entries with `translation_status: BLOCKED`
- P4 Entry Guard passed (sampled entries have non-empty `source_lines`)

## Exit Criteria

- Every function in `ipo-registry.yaml` has `translation_status: DONE`
- Every translated function has `target_lines` populated in its registry entry
- All target files compile without errors
- All `adapt`-strategy files are updated
- Dependency manifest for target is written
- `phases.P4_translation: DONE`, `phases.P5_verification: IN_PROGRESS`

---

## Translation Order

Follow the dependency order from the `calls` graph in `ipo-registry.yaml`:
1. Translate leaf functions first (those with empty `calls` lists)
2. Translate callers only after all their callees are `DONE`
3. Within a dependency level, translate in file order

This guarantees that when you write a caller, the callee API is already finalized.

---

## Structural Equivalence Rules

### Algorithm Steps → Control Flow

Every step in `process.steps` must have a visible counterpart in the target code.
Do not merge steps. Do not reorder steps.

```
Source step 1: "filter values below epsilon"
Source step 2: "compute -sum(p * log_b(p))"
Source step 3: "return scalar"

Target must have:
  Step 1 → filter loop or iterator with condition
  Step 2 → sum computation
  Step 3 → return statement
```

### Magic Numbers → Named Constants

Every magic number from the IPO registry must become a named constant in the target:

```rust
// NOT this:
if p < 1e-10 { continue; }

// THIS:
const PROBABILITY_EPSILON: f64 = 1e-10;  // floor to prevent log(0), see IPO registry
if p < PROBABILITY_EPSILON { continue; }
```

The constant name should reflect its purpose, not its value.

### Inferred Invariants → Comments or Debug Assertions

Every inferred invariant must be preserved as either:
- A `debug_assert!` / debug assertion (when it can be checked cheaply)
- A `// INVARIANT:` comment (when it cannot be checked at runtime)

```rust
// INVARIANT: caller guarantees sum(data) ≈ 1.0 (not validated; matches source behavior)
debug_assert!(!data.is_empty(), "entropy input must be non-empty");
```

### Ecosystem Gap Resolution

Before translating any function, check its `ecosystem_refs` against `ecosystem-map.yaml`.
For each referenced symbol:

- `equivalence_type: structural` → use target equivalent directly
- `equivalence_type: behavioral` → use target equivalent; add a comment referencing the gap entry
- `equivalence_type: partial` → use target equivalent; add `// PARTIAL EQUIVALENCE: <gap_notes>`
- `equivalence_type: none` → use `compensation_strategy` from ecosystem map

---

## Anti-Patterns (Prohibited)

These patterns are explicitly forbidden. If you find yourself doing any of these, stop and rethink:

| Anti-pattern | Why forbidden |
|---|---|
| Using `todo!()` / `unimplemented!()` in logic paths | Structural hole; not a real translation |
| Wrapping everything in a `catch_all` / generic error | Hides error semantics from IPO registry |
| Calling the equivalent of `eval()` to avoid translation | Structural equivalence violated |
| Implementing a mock that returns hardcoded values | Explicitly prohibited by project policy |
| Merging two IPO steps into one "clever" idiom | Structural equivalence violated |
| Changing the algorithm for performance during P4 | P4 is for correctness; optimization is post-P5 |
| Omitting a magic number (using the literal instead) | Magic numbers must become named constants |

---

## Handling the `adapt` Strategy

For each `adapt` file (build configs, CI, manifests):

1. Read the source file completely
2. Identify all language-specific content (package names, build commands, tool names)
3. Replace using ecosystem-map lookups
4. Keep all structure, comments, and non-language-specific content
5. Do not remove any pipeline step or build target — only update the implementation

---

## File-by-File Workflow

For each file with `migration_strategy: translate`:

1. Create target file at `target_path`
2. Add appropriate file header comment
3. Translate each function in dependency order
4. After each function, update `ipo-registry.yaml`:
   ```yaml
   translation_status: DONE
   target_impl_file: "src/core/entropy.rs"
   target_lines: "15-42"        # MANDATORY — must be populated; empty = not done
   ```
5. Verify the file compiles before moving to the next file

**`target_lines` is mandatory.** An entry with `translation_status: DONE` but empty
`target_lines` is considered incomplete and will be flagged in P5.

---

## Blocking Rules

Block when:
- An IPO step has no clear target-language representation and the ecosystem map does not cover it
- A `compensation_strategy` in the ecosystem map is ambiguous — requires clarification before coding
- The target code would require `unsafe` (Rust) or equivalent; human must approve unsafe blocks
- A function's behavior depends on an inferred invariant that seems wrong upon implementation

---

## Fix Protocol: TDD Retrospective Required

When any compilation error, `go vet` warning, or structural mismatch is found and fixed:

```
ERROR FOUND → fix applied → MANDATORY: TDD Retrospective Protocol
                            (see references/tdd-retrospective.md)

Step 1 ROOT CAUSE ANALYSIS
  - Phenomenon: exact error, file, line
  - Root cause category (ecosystem_gap_unapplied | semantic_contract_lost | ...)
  - Root cause: structural reason — not "I forgot X"

Step 2 CHECKLIST ENTRY
  - Write entry to migration_workspace/retrospective-checklist.yaml
  - checklist_rule: "Whenever [pattern], check for [property]"

Step 3 SCOPE SCAN  ← define search pattern BEFORE scanning
  - grep/search entire target codebase for the same root cause pattern
  - Classify each hit: FIXED | OK | DEFERRED

Step 4 CONSISTENT FIX
  - Apply identical fix strategy to all FIXED instances
  - Re-run: go build ./... + go vet ./... (full build, not just current file)
  - If new errors appear: each triggers its own retrospective
```

Only after these four steps: continue to the next translation unit.
A fix without a retrospective is a local patch. A fix with a retrospective is a systemic improvement.

---

## Dependency Manifest

After all source files are translated, write the target's dependency manifest:
- Start from the `new_dependencies` list in `ecosystem-map.yaml`
- Add the target language's standard toolchain requirements
- Pin versions (use the most recent stable version as of the migration date)
- Record the manifest path in `migration-state.yaml`

---

## Phase Exit: Trigger PGR-4

When you believe P4 is complete, do NOT mark it DONE yet.

Load `references/phase-gate-review.md` and run PGR-4 using the audit criteria defined there.
Only set `phases.P4_translation: DONE` after PGR-4 passes with zero findings.

The PGR-4 loop will:
1. Verify every translate-strategy asset has a corresponding target file on disk
2. Verify every ipo-registry entry with `translation_status: DONE` has non-empty `target_lines`
3. Verify all retrospective entries with `ecosystem_map_update_required: true` have been applied to `ecosystem-map.yaml`
4. Verify the Retrospective Checklist Summary has been output in the session response
5. Run the target language build command (`go build ./...`, `cargo build`, etc.) and verify clean exit
6. Fix any findings autonomously and re-audit from scratch until zero findings remain

`phases.P4_translation: DONE` is set by PGR-4 as its final action — never set it directly.
