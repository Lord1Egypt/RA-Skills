# TDD Retrospective Protocol

**Trigger**: After fixing ANY failing test, compilation error, structural deviation, or
behavioral discrepancy — in P4 or P5, without exception.

**Core principle**: Every bug is a symptom of a bug *class*. Fixing one instance without
understanding and scanning for the class is incomplete work.

The protocol has four mandatory steps:

```
Step 1: ROOT CAUSE ANALYSIS   — understand WHY it happened, not just WHAT happened
Step 2: CHECKLIST ENTRY       — persist the root cause as a reusable rule
Step 3: SCOPE SCAN            — find every other instance of the same root cause
Step 4: CONSISTENT FIX        — fix all instances; update checklist with findings
```

These four steps are not optional when a fix is applied. A fix without a retrospective
is a local patch. A fix with a retrospective is a systemic improvement.

---

## The Retrospective Checklist File

Every fix adds one entry to `migration_workspace/retrospective-checklist.yaml`.
This file accumulates over the entire migration and becomes the authoritative
"lessons learned" record for this language pair and project.

At P5 completion, this file is the primary artifact for preventing the same class
of errors in future migrations to the same target language.

```yaml
# retrospective-checklist.yaml
# Auto-grows as fixes are applied during P4/P5.
# Each entry = one root cause class, not one bug instance.

meta:
  project: ""
  lang_pair: ""
  generated_at: ""
  total_entries: 0
  total_instances_found: 0
  total_instances_fixed: 0

entries: []
# Each entry: see schema below
```

---

## Root Cause Analysis Framework

When a fix is applied, the AI must answer four questions before writing the entry.
These questions force abstraction from symptom to root cause:

### Q1: Phenomenon (现象)
*What was observed?* — the specific test failure, compile error, or behavioral
discrepancy. Be concrete: file name, line number, error message.

### Q2: Root Cause (根因)
*Why did this happen at the structural level?* — not "I forgot to handle X" but
"the translation pattern for Y does not preserve Z property."

Root causes always belong to one of these categories:

| Category | Description | Example |
|---|---|---|
| `ecosystem_gap_unapplied` | A known gap in ecosystem-map.yaml was not applied during translation | dict ordering gap documented but map used anyway |
| `semantic_contract_lost` | Source type's implicit contract not preserved | Python int unbounded → Go int64 overflow not guarded |
| `invariant_not_transferred` | An inferred invariant from P3 not reflected in target | "input non-empty" invariant, no guard in translation |
| `magic_number_decontextualized` | A constant was translated without its meaning | `1e-10` became `0.0000000001` with no named constant |
| `control_flow_collapsed` | Two IPO steps were merged or reordered | filter-then-map became one expression losing step separation |
| `error_class_narrowed` | Source raised specific exception; target uses generic error | `ValueError` → generic `error` losing error type information |
| `side_effect_dropped` | A documented side effect was not replicated | cache mutation, global state write |
| `ipo_source_lines_wrong` | P3 source_lines were incorrect; translation based on wrong understanding | wrong line range → different algorithm segment translated |
| `test_fixture_mismatch` | Test fixture format changed between source and target | binary fixture loaded differently |
| `consumer_error` | Bug is in caller, test fixture, or test assertion — not in the translated function | test passes wrong arg type; fixture uses Python dict where Go expects slice |
| `source_faithful_behavior` | Behavior matches source exactly; the assumption that it's a bug is wrong | Source returns nil on cache miss; test expected error — source is correct by design |
| `implicit_capability_assumption` | Source design assumes consumer has implicit inference ability (e.g. strong LLM, runtime with smart defaults); target consumer lacks it and needs explicit guidance | Python conductor relies on Claude inferring "call GET /chat when unread>0"; Go target runs Qwen3.5 which needs an explicit code_run example to trigger the same action |
| `other` | Root cause does not fit above — describe precisely |

**⛔ Special resolution path for `source_faithful_behavior`, `consumer_error`, and `implicit_capability_assumption`:**

These three categories do NOT trigger the standard Fix → Scope Scan → Consistent Fix loop.
They are resolved differently:

- `source_faithful_behavior`: add `SOURCE-FAITHFUL` comment in target; add `known_source_behaviors` entry to IPO registry; fix the test assertion; if source has a genuine bug, BLOCK for human decision. **No code change to the translated function.**
- `consumer_error`: fix the caller, test fixture, or test assertion only. **No code change to the translated function.** Add a retrospective entry explaining what the consumer got wrong, so future test migrations avoid the same mistake.
- `implicit_capability_assumption`: the translated function is correct; the gap is that the source design relied on a capable consumer (strong model, smart runtime) that the target's consumer does not have. Fix by making the implicit contract explicit in the integration layer (system prompt, config, documentation) — **not** by changing the translated function's logic. Document the assumption in the IPO registry under `inferred_invariants`: `"consumer (model/runtime) can infer X from context without explicit instruction [inferred from: source design + known model capability gap]"`.

The retrospective entry is still required for all three categories — it documents what happened, prevents the same misdiagnosis in future, and may reveal a pattern in how the integration layer needs to be strengthened for the target environment.

### Q3: Generalization (泛化规律)
*What is the general pattern this root cause represents?* — stated as a rule:
"Whenever [pattern X], check for [property Y]."

This is the sentence that goes into the checklist.

### Q4: Scope (排查范围)
*Where else in the codebase could this root cause have produced the same error?*
Define the search pattern before scanning — do not scan first and classify later.

---

## Retrospective Entry Schema

```yaml
entries:
  - id: "RCA-001"                    # auto-incremented, never reused
    discovered_phase: "P5"           # P4 | P5
    discovered_at: "2026-05-15"
    
    # Step 1: Root Cause Analysis
    phenomenon: |
      Track B test test_loop_tool_order FAILED.
      Expected tool execution order: [search, read, write]
      Actual execution order:        [write, read, search]
      File: internal/loop/loop.go, test: tests/test_loop.go:88
    
    root_cause_category: ecosystem_gap_unapplied
    root_cause: |
      Python dict preserves insertion order (3.7+). The ecosystem-map entry for
      "dict[K,V]" documents this gap and specifies IndexMap/[]Entry as compensation.
      The translation used map[string]ToolHandler instead of []ToolEntry, silently
      losing the ordering contract. The gap was known; it was not applied.
    
    fix_applied: |
      Replaced map[string]ToolHandler with []ToolEntry{name, handler} slice in
      AgentLoop.toolRegistry. Updated all 3 call sites to use slice lookup.
      internal/loop/loop.go lines 34-67, 112, 198.
    
    # Step 2: Checklist Entry
    checklist_rule: |
      After translating any Python dict: verify whether the caller code depends on
      iteration order. If dict.keys(), dict.items(), or dict.values() is iterated
      in source with order-sensitive logic, use []Entry slice or IndexMap — never
      map[K]V. Check ecosystem-map entry for the specific dict usage before translating.
    
    # Step 3: Scope Scan
    generalization: "Python dict with order-sensitive iteration translated to Go map"
    scope_scan_query: "grep -rn 'map\\[string\\]' internal/ --include='*.go'"
    scope_scan_results:
      - path: "internal/loop/loop.go"
        verdict: FIXED
        notes: "toolRegistry — iteration order mattered"
      - path: "internal/memory/keychain/keychain.go"
        verdict: FIXED
        notes: "lookupChain iterates in registration order — same issue"
      - path: "internal/frontends/conductor/conductor.go"
        verdict: OK
        notes: "frontendRegistry — only Get/Set, no iteration in source"
      - path: "internal/plugins/langfuse/langfuse.go"
        verdict: OK
        notes: "eventBuffer — source also used unordered set"
    
    # Step 4: Consistent Fix
    instances_found: 4
    instances_fixed: 2
    instances_ok: 2
    status: RESOLVED
    
    # Optional: ecosystem-map correction
    ecosystem_map_update_required: true
    ecosystem_map_note: |
      The entry for 'dict[K,V]' compensation_strategy should be strengthened:
      add explicit instruction to check iteration usage at each call site, not
      just at the type-mapping level. Filed as improvement for next migration.
```

---

## Scope Scan Protocol

The scope scan is the highest-value part of the retrospective.
It must be done in this order — never reversed:

### Step A: Define the search pattern BEFORE scanning

Write the search query based on the root cause, not based on what you expect to find.

```
Root cause: "Python dict with insertion-order-dependent iteration"
↓
Search pattern: grep for map[string]* in target + cross-reference against
               source files where .items()/.keys() were iterated in loops
```

Do not write the search pattern after scanning. That produces confirmation bias.

### Step B: Scan comprehensively

In full_mode:
```bash
# Example: find all Go maps that might correspond to Python dicts
grep -rn "map\[string\]" internal/ --include="*.go" -l

# Then for each file found, check the source equivalent:
grep -n "\.items()\|\.keys()\|\.values()\|for.*in.*dict" genericagent/<source_equivalent>
```

Do NOT stop scanning when you find one instance. Complete the full scan before fixing anything.

### Step C: Classify each finding

For each file found by the scan:
- `FIXED` — same root cause, fix required, applied
- `OK` — root cause pattern present but does not apply here (explain why)
- `DEFERRED` — applies but blocked by missing real dependency (document)

The `OK` classification requires a written justification. "I checked and it's fine" is not a classification.

### Step D: Apply fixes consistently

All `FIXED` instances must use the same fix strategy. Do not fix the same root cause
with different approaches in different files — this creates maintenance inconsistency
and makes future bugs harder to trace.

---

## Integration with P4 and P5

### In P4 (Translation)

When a file fails to compile or `go vet` reports an error after translation:

```
COMPILE/VET ERROR → fix → trigger Retrospective Protocol
                           ↓
                    write RCA entry → scope scan → consistent fix → update checklist
```

Do not continue to the next file until the retrospective is complete for the current error.

### In P5 (Verification)

When a Track A structural review or Track B test reveals a discrepancy:

```
DISCREPANCY FOUND → fix → trigger Retrospective Protocol
                          ↓
                   write RCA entry → scope scan → consistent fix → update checklist
                   
Retrospective complete → re-run the full test suite (not just the failing test)
                       → if new failures appear, each triggers its own retrospective
```

**Always re-run the full suite after a retrospective fix**, not just the originally failing test. A scope-scan fix may have introduced a new failure in a related component.

---

## Checklist Review at Phase Gates

At the END of P4 and the END of P5, the AI must:

1. Read the full `retrospective-checklist.yaml`
2. For each entry with `ecosystem_map_update_required: true` — update `ecosystem-map.yaml`
3. Output a **Checklist Summary** in the response:

```
RETROSPECTIVE CHECKLIST SUMMARY (end of P5):
  total_rca_entries:       <N>
  total_instances_found:   <N>
  total_instances_fixed:   <N>
  
  By root_cause_category:
    ecosystem_gap_unapplied:    <N>   ← most common? consider strengthening P2
    semantic_contract_lost:     <N>   ← consider strengthening P3 IPO inputs
    invariant_not_transferred:  <N>
    magic_number_decontextualized: <N>
    control_flow_collapsed:     <N>
    error_class_narrowed:       <N>
    other:                      <N>
  
  PATTERN INSIGHT:
    Most common category: <category>
    This suggests the lang-pair module for <pair> should be strengthened
    with explicit guidance on: <specific guidance>
  
  ecosystem_map_updates_applied: <N>
  lang_pair_module_improvements_suggested: <Y/N>
```

This summary is the primary mechanism for improving the language pair modules over time.
If `ecosystem_gap_unapplied` is the most common category across multiple migrations,
the `python-go.md` module's gap documentation needs to be more explicit.

---

## The Meta-Goal: Self-Improving Methodology

The retrospective checklist is not just a record of what went wrong.
It is the primary input for improving the methodology itself.

Each entry that identifies a recurring pattern contributes to:
- Stronger language pair modules (pre-documented gaps)
- Better P3 IPO analysis rules (invariants to always look for)
- Better P2 ecosystem mapping (gaps to always research)

A mature migration methodology has a large, specific retrospective history.
A new methodology has none. The checklist is how the methodology grows up.
