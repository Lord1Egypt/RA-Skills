---
name: lang-migration
description: >
  AI-driven full-project language migration skill. Use this skill whenever the user wants to
  port, translate, or rewrite a codebase from one programming language to another — including
  Python→Rust, Python→Go, Python→C, Python→C++, Python→Zig, Python→Bun/TS, or any other pair.
  Also trigger when user mentions "精确复刻", "语言迁移", "port project", "translate codebase",
  "1:1 rewrite", or "language conversion". This skill enforces structural equivalence first,
  full asset coverage (no file skipped), persistent YAML state across sessions, and a strict
  no-mock verification policy with human-gated blocking.
license: MIT
---

## Author & Attribution

**Original Author**: flynn  
**Contact**: https://github.com/suifei/lang-migration-skill  
**Role**: Architect, Developer, Documenter  
**Expertise**: Software engineering, programming languages, AI workflow design  
**Contributions**: Designed the multi-phase pipeline, defined YAML schemas, implemented blocking protocol, and wrote comprehensive documentation for the skill.

---

# Language Migration Skill

A systematic, multi-session, AI-executable workflow for migrating any open-source project
from one programming language to another with 1:1 structural fidelity.

## Core Principles

1. **No file is useless** — every file in the source project is analyzed and assigned a migration strategy
2. **Structural equivalence first** — algorithm steps, loop structure, and control flow must mirror the source; behavioral equivalence is only used when the ecosystem gap makes structural impossible
3. **No mock, ever** — tests must use real implementations and real test data
4. **Block, don't skip** — when a decision cannot be made autonomously, stop and ask the human; never label-and-continue
5. **State persists across sessions** — all state lives in YAML files in the workspace, readable by any AI agent or human
6. **Evidence before completion** — every unit of work must produce verifiable evidence of execution before being marked done

---

## Global Anti-Cheating Policy

This skill operates under the assumption that an AI agent may attempt to mark tasks complete
without actually doing the work. Every phase has mechanisms to detect and prevent this.

**The Three Forms of AI Task Fraud (all prohibited):**

| Form | Example | Detection |
|---|---|---|
| Batch fabrication | Scripts generate IPO content without reading source | source_lines field will be wrong/empty |
| Silent bulk-confirm | NEEDS_REVIEW → CONFIRMED without evidence | confirmation_evidence field empty |
| Premature phase advance | Marking P3 DONE when entries have empty fields | Self-verification checks fail |

**Evidence Requirements by Phase:**

| Phase | Required Evidence |
|---|---|
| P2 | `confirmation_evidence` block per CONFIRMED entry |
| P3 | `READ_EVIDENCE` + `BEHAVIOR_PROOF` per function; `source_lines` in every step; `source_line` on every magic number |
| P4 | Compilation succeeds; IPO entry updated with `target_lines`; **every fix triggers TDD Retrospective** |
| P5 | **TEST OUTPUT EVIDENCE** (actual runner output, not just "tests pass"); **every fix triggers TDD Retrospective**; **full suite re-run after each fix**; **Checklist Summary at phase end** |
| Fix | `retrospective-checklist.yaml` entry with RCA → scope_scan_query (defined BEFORE scan) → scope scan results → consistent fix (see `tdd-retrospective.md`) |
| **PGR** | **Full audit report output in response** listing every item checked; each FINDING citing exact artifact (file path, field, value); each FIXED citing same artifact after change; `findings_count: 0` proven by enumerated item list; `phase_gates.PGR_N.passed_at` timestamp set only after zero-findings pass |

**TDD Retrospective Integration**

The **Retrospective Protocol** is mandatory at every fix point:
- **Trigger**: Compilation error, vet failure, structural deviation, test failure
- **Steps**: RCA (root cause analysis) → Checklist rule → Scope scan → Consistent fix
- **Output**: Entry in `retrospective-checklist.yaml` with root cause category and generalized rule
- **Scope scan constraint**: `scope_scan_query` MUST be written before scanning (prevents post-hoc bias)
- **Impact**: After each fix, full test suite is re-run; new failures each trigger independent retrospectives

See [Retrospective Protocol](#retrospective-protocol) below and `references/tdd-retrospective.md`.

**Self-Verification is not optional.** Each phase that has a Self-Verification Protocol
must run it and output the report before advancing. The report must appear in the AI's
response — not silently written to a file.

**The AI must never say "done" without evidence.** "I have completed X" is not a valid
completion statement without accompanying evidence artifacts.

---

## Environment Detection

This skill runs in Claude Code, Cursor, OpenCode, or GitHub Copilot. At session start, detect the environment:

```
IF bash tool is available AND can write files → full_mode (Claude Code / OpenCode)
IF only file editing available → editor_mode (Cursor / Copilot)
```

In **full_mode**: use bash scripts for scanning, run `scan_assets.py` directly.
In **editor_mode**: generate file lists manually by reading directory structure; instruct user to run scripts manually if needed.

**Workspace location**: Always at the project root, in a directory called `migration_workspace/`.

```
<project-root>/
├── <source_code>/          ← original project (read-only, never modify)
├── <target_code>/          ← translated output (created by this skill)
└── migration_workspace/
    ├── migration-state.yaml      ← SESSION ENTRY POINT: read this first every session
    ├── asset-inventory.yaml
    ├── ecosystem-map.yaml
    └── ipo-registry.yaml
```

---

## Session Start Protocol

**Every time you start a new session, do this first — no exceptions:**

1. Check if `migration_workspace/migration-state.yaml` exists
   - YES → read it, understand current phase and `current_task`, resume from there
   - NO → this is a new project, run **P0 Bootstrap**

2. Read `current_task` block. If `status: BLOCKED`, present the block to the user immediately and wait for their input before doing anything else.

2b. **Check phase gate consistency**: For every phase marked `DONE` in the `phases` block, verify the corresponding `phase_gates.PGR_N.passed_at` is non-empty. If a phase is `DONE` but `passed_at` is empty, the PGR was not completed. Re-run PGR-N for that phase before advancing to the next phase. Load `references/phase-gate-review.md` for the audit criteria.

3. **Check if the user's opening message is a status/gap question:**
   - Triggers: "还差什么", "进度怎样", "gap report", "show status", "还有哪些", "差多少", "完成了多少"
   - If YES → run P6 Gap Report immediately, output the summary to the user, then ask how to proceed
   - If NO → continue to step 4

4. Load the language pair module: `references/lang-pairs/<source>-<target>.md`

5. Proceed with the current phase.

---

## Five-Phase Pipeline

```
P0 Bootstrap          → Initialize workspace, detect language pair, load lang-pair module
P1 Asset Scan         → Inventory every file, assign migration strategy
P2 Ecosystem Mapping  → Map all imports/types/stdlib to target equivalents, identify gaps
P3 IPO Analysis       → Document every function: Inputs, Process (incl. magic numbers), Outputs
P4 Translation        → Translate function by function using IPO registry + ecosystem map
P5 Verification       → Structural review + real-data behavioral tests (no mock)
P6 Gap Report         → Multi-dimensional completeness audit (invoke at any time)
```

Each phase has a detailed reference file. Load it when entering that phase:

| Phase | Reference File |
|-------|----------------|
| P0    | `references/phase-0-bootstrap.md` |
| P1    | `references/phase-1-asset-scan.md` |
| P2    | `references/phase-2-ecosystem-map.md` |
| P3    | `references/phase-3-ipo-analysis.md` |
| P4    | `references/phase-4-translation.md` |
| P5    | `references/phase-5-verification.md` |
| P6    | `references/phase-6-gap-report.md` |
| **Fix** | **`references/tdd-retrospective.md` ← mandatory on every fix in P4/P5** |
| **PGR** | **`references/phase-gate-review.md` ← mandatory between every phase transition** |

---

## Phase Gate Review Protocol (PGR)

**A phase is not complete when the AI says it is complete. A phase is complete when PGR-N passes with zero findings.**

After every phase finishes, the AI enters an autonomous self-auditing loop before advancing to the next phase. This loop requires no human involvement.

### Updated Pipeline with PGR Gates

```
P0 Bootstrap → [PGR-0] → P1 Asset Scan → [PGR-1] → P2 Ecosystem Map → [PGR-2]
    → P3 IPO Analysis → [PGR-3] → P4 Translation → [PGR-4] → P5 Verification → [PGR-5] → DONE
```

### How PGR Works

Each PGR-N runs an **enumerate → audit → fix → re-audit** loop:

1. **Enumerate** — list every expected output of the completed phase
2. **Audit** — check each output against phase-specific criteria; record any FINDING with artifact evidence
3. **Tally** — if `findings_count == 0`, advance; if `findings_count > 0`, proceed to Fix
4. **Fix** — fix each FINDING autonomously; record artifact evidence of each fix
5. **Re-audit** — return to Step 1 (full re-enumeration required after every fix pass)
6. **Pass** — when zero findings: set `phase_gates.PGR_N.status: PASSED`; only then set `phases.PN_xxx: DONE`

### Core Rule

The phase status `DONE` in `migration-state.yaml` must NEVER be set directly at the end of a phase.
It is only set by PGR-N as the final action of a passed audit. Any session that finds a phase marked
`DONE` without a corresponding `phase_gates.PGR_N.passed_at` timestamp must re-run PGR-N before
advancing (see Session Start Protocol).

### PGR Reference

| Gate | Triggered After | Reference |
|------|----------------|-----------|
| PGR-0 | P0 Bootstrap | `references/phase-gate-review.md#pgr-0` |
| PGR-1 | P1 Asset Scan | `references/phase-gate-review.md#pgr-1` |
| PGR-2 | P2 Ecosystem Map | `references/phase-gate-review.md#pgr-2` |
| PGR-3 | P3 IPO Analysis | `references/phase-gate-review.md#pgr-3` |
| PGR-4 | P4 Translation | `references/phase-gate-review.md#pgr-4` |
| PGR-5 | P5 Verification | `references/phase-gate-review.md#pgr-5` |

For the full protocol including per-phase audit criteria, finding formats, and anti-cheating rules,
see: `references/phase-gate-review.md`

---

## P0 Bootstrap (New Project)

When `migration-state.yaml` does not exist:

1. Ask the user:
   - Source language and directory path
   - Target language
   - Any known constraints or priorities

2. Determine language pair key (e.g., `python-rust`). If the file `references/lang-pairs/<pair>.md` does not exist, load `references/lang-pairs/TEMPLATE.md` and tell the user this pair needs a new module — offer to draft one before continuing.

3. Copy all five template files from `templates/` into `migration_workspace/`:
   - `migration-state.yaml` → fill in meta block
   - `asset-inventory.yaml` → empty, ready for P1
   - `ecosystem-map.yaml` → empty, ready for P2
   - `ipo-registry.yaml` → empty, ready for P3
   - `retrospective-checklist.yaml` → empty, ready for first P4/P5 fix

4. Set `phases.P0_bootstrap: DONE` and `phases.P1_asset_scan: IN_PROGRESS`

5. Immediately proceed to P1.

---

## Blocking Protocol

When you cannot proceed without a human decision:

1. Write to `migration-state.yaml`:
   ```yaml
   current_task:
     status: BLOCKED
     block_reason: "<specific reason>"
     human_input_required: "<exact question for the human>"
   ```

2. Output to the user:
   ```
   ⛔ BLOCKED — Human decision required

   Phase: <phase>
   Item: <item_id>

   Problem: <what cannot be resolved automatically>

   Required decision: <specific question>

   Options considered:
     A) <option with trade-off>
     B) <option with trade-off>

   Please reply with your decision and I will continue.
   ```

3. Stop. Do not proceed to any other task.

---

## Progress Reporting

After completing any task unit, update `migration-state.yaml` and output a brief status line:

```
✅ [P2] numpy.float64 → f64 (behavioral, precision gap noted)
⛔ [P2] numpy.random.default_rng → BLOCKED (see above)
🔄 [P3] entropy.py::calculate_entropy → IPO documented
```

At the end of each session, output a summary:
```
Session Summary
  Phase: P2 Ecosystem Mapping
  Completed this session: 12 entries
  Remaining: 34 entries
  Blocked: 1 (awaiting your decision on numpy RNG)
  Next session: resume P2 from item "scipy.stats.entropy"
```

---

## YAML Schema Reference

For full field definitions of all five YAML files, see: `references/schemas.md`

---

## Retrospective Protocol

In P5, **every** test failure or structural deviation must pass through the Bug Triage Protocol first (see `references/phase-5-verification.md`) before any fix is applied. Triage classifies the failure into one of five verdicts — only `CONFIRMED_TRANSLATION_ERROR` proceeds to a code fix; the other verdicts resolve in the integration layer, caller, or test without touching the translated function.

After a fix is applied (any phase), the TDD Retrospective Protocol is mandatory. A fix without a retrospective is a local patch. A fix with a retrospective is a systemic improvement.

See `references/tdd-retrospective.md` for the full protocol.

### Why Root Cause, Not Phenomenon?

Traditional bug tracking records **what failed**:
```
test_loop_tool_order FAILED
Expected execution order: [search, read, write]
Actual order: [write, read, search]
```

This documents a symptom. The same underlying problem will manifest differently next time.

The retrospective records **structural root causes**:
```
Root cause: ecosystem_gap_unapplied
Problem: Python dict preserves insertion order (3.7+). IPO registry documented this gap
and specified IndexMap/[]Entry as compensation. Translation used map[K]V, silently losing order.
```

When the next function translates a Python dict, the AI can check the retrospective **before**
translating, preventing the error instead of fixing it after failure.

Each migration's lessons become infrastructure for the next migration of the same language pair.

### Core Design Principles

#### 1. Root Cause Categories

Twelve predefined categories force abstract thinking:
- `ecosystem_gap_unapplied` — known gap was not applied
- `semantic_contract_lost` — implicit contract not preserved
- `invariant_not_transferred` — inferred invariant missing
- `magic_number_decontextualized` — constant without context
- `control_flow_collapsed` — IPO steps merged/reordered
- `error_class_narrowed` — specific exception generalized
- `side_effect_dropped` — documented side effect missing
- `ipo_source_lines_wrong` — P3 analysis based on wrong lines
- `test_fixture_mismatch` — fixture format changed
- `consumer_error` — bug is in caller/test, not translated function; fix consumer only
- `source_faithful_behavior` — behavior matches source; test assumption was wrong; annotate, don't fix
- `implicit_capability_assumption` — source design relied on consumer having inference ability (e.g. strong LLM) that the target consumer lacks; fix in integration layer, not in translated function
- `other` — describe if no category fits

Each fix produces exactly ONE entry with ONE category. No category hopping.

The last three categories (`consumer_error`, `source_faithful_behavior`, `implicit_capability_assumption`) resolve **without changing the translated function**. They require a retrospective entry but do not trigger scope scan for code fixes.

#### 2. Scope Scan: Query BEFORE Execution

**Mandatory rule**: Define `scope_scan_query` before scanning.

This prevents LLM cheating patterns like:
- Scan codebase → observe results → retroactively define "the scope that matches findings"

Example:
```yaml
Root cause: dict insertion-order dependency not preserved

scope_scan_query: "grep -rn 'map\[string\]' internal/ --include='*.go'"
(The query is written BEFORE executing the grep. It appears in the retrospective entry.)
```

The query is your prediction of where the root cause manifests. If results don't match predictions,
it's a signal that the root cause analysis was incomplete.

#### 3. Consistent Fix Across All Instances

Scope scan identifies all instances with the same root cause. All are fixed simultaneously
using the same fix strategy. This prevents:
- The bug reappearing in a file not yet reviewed
- Maintenance inconsistency (same bug, different fixes in different places)

After scope fix, **full test suite is re-run** (not just the failing test). Any new failures
trigger independent retrospectives — they are not merged.

#### 4. Ecosystem Map Auto-Update

Flag `ecosystem_map_update_required: true` in the retrospective entry triggers automatic
update to `ecosystem-map.yaml` at phase-end.

Example:
- P4: dict ordering bug found, fixed, retrospective entry created
- Entry sets `ecosystem_map_update_required: true`
- P4 end: ecosystem map updated with stronger guidance
- **Next migration benefits** — same class of error is harder to commit

### Checklist Summary (Phase-End Report)

At the END of P4 and P5, output a **Checklist Summary**:

```
RETROSPECTIVE CHECKLIST SUMMARY (end of P5):
  total_rca_entries:          24
  total_instances_found:      67
  total_instances_fixed:      64
  instances_deferred:         3

Most common root cause categories:
  1. ecosystem_gap_unapplied         (9 entries)   → suggests ecosystem map gaps
  2. semantic_contract_lost          (6 entries)   → suggests IPO analysis depth issue
  3. magic_number_decontextualized   (4 entries)   → suggests naming discipline

Ecosystem map updates applied: 3
  - dict iteration order guidance strengthened
  - float precision rules clarified
  - exception mapping for stdlib errors expanded

Next language pair migration of python→go should consult these 24 entries
before beginning translation — prevents category-1 errors upfront.
```

This summary is the handoff to the next migration team or agent.

### Integration with P4/P5

**P4 Trigger:**
```
Compilation/vet error found
  ↓
Fix applied
  ↓
Trigger: Retrospective Protocol
  ↓
RCA → Checklist rule → Scope scan query → Scope scan → Consistent fix
  ↓
Resume P4 from next file
```

**P5 Trigger:**
```
Structural deviation or test failure found
  ↓
Bug Triage (T1 → T2 → T3)  ← MANDATORY before any fix
  ↓
  ├─ SOURCE_FAITHFUL          → annotate target code; fix test; no code change
  ├─ CONSUMER_ERROR           → fix caller/test only; no code change
  ├─ IMPLICIT_CAPABILITY      → fix integration layer only; no code change
  ├─ ECOSYSTEM_DIFFERENCE     → verify compensation; may update test expectation
  └─ CONFIRMED_TRANSLATION_ERROR
       ↓
     Fix applied
       ↓
     Trigger: Retrospective Protocol
       ↓
     RCA → Checklist rule → Scope scan query → Scope scan → Consistent fix
       ↓
     Full test suite re-run (not just failing test)
       ↓
     If new failures: each triggers independent retrospective
       ↓
     Resume P5 from next function
```

For detailed protocol, see: `references/tdd-retrospective.md`
