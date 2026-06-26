# SELF-IMPROVEMENT ENGINE

Every failure is an opportunity to improve the harness. Every 5 cycles, the harness
proposes and evaluates improvements to itself. This is not optional.

---

## THE RULE

Every failure must produce at least one of:
- A new constraint appended to references/constraints.md
- A new test in tests/
- A new documentation entry in docs/

A failure that produces none of these is an incomplete cycle.

---

## HARD LIMITS ON SELF-IMPROVEMENT

The self-improvement engine may never:
- Modify SKILL.md, CONFIG.yaml, or any file under agents/, runtime/, or tools/
  EXCEPTION: Phase 6 harness-variant search (see below) may propose variants for
  human approval -- approved variants are applied by the human, not autonomously.
- Delete or overwrite existing entries in references/constraints.md
- Relax or remove an existing constraint (only humans may do this)
- Change retry limits, loop mode, or parallelism settings
- Grant itself or any agent additional permissions

Self-improvement is append-only and additive for constraints.
Harness variants are proposed and human-approved before application.

---

## PART 1: TRACE-BASED FAILURE ATTRIBUTION (every cycle, Phase 5)

When a failure occurs, the debugger or harness-improvement agent must NOT only read
MEMORY.md. It must query raw execution traces to find the causal chain.

### What to query

The following files are queryable via search_code and read_file:
  docs/generated/tool-logs/       -- raw tool call metadata per cycle
  docs/status/DISPATCH-TRACK-*.md -- per-WU, per-iteration status entries
  docs/status/RESEARCH-TRACK-*.md -- sub-researcher step log
  docs/status/PLAN-TRACK-*.md     -- gap planner step log
  docs/status/CYCLE-*.md          -- completed cycle summaries

### Attribution protocol

For each failure:
1. Find the DISPATCH-TRACK entry for the failing WU and iteration
2. Trace backward: which earlier harness decision contributed to this failure?
   Not just "what failed" -- which step, which rule, which structural choice
3. Identify the harness gap category (from runtime/observability.md)
4. Propose the smallest harness change that would have prevented it

Attribution questions to answer:
  - Was this a scope problem? (WU too large, sub-researcher saw too much)
  - Was this a context problem? (agent held too many files, quality degraded)
  - Was this a feedback problem? (reviewer summary lost a diagnostic detail)
  - Was this a sequencing problem? (two WUs should have been serialized)
  - Was this a constraint gap? (a rule should exist but does not)

Record the attribution in the MEMORY.md entry under a "Harness Cause:" field.

---

## PART 2: CONTEXT-EFFICIENCY METRIC (every cycle, Phase 6)

Track two metrics per cycle, not one:

METRIC 1 -- Gap-closed rate: gaps resolved / gaps attempted
METRIC 2 -- Context efficiency: average context tokens consumed per resolved gap

Both metrics are recorded in docs/status/CYCLE-NNN.md.
Both are tracked across cycles in docs/status/EFFICIENCY-HISTORY.md (append-only).

### Efficiency targets

Context efficiency degrades when:
  - WUs are too large (implementer reads many files)
  - Reviewer layers read full plans instead of excerpts
  - Feedback documents contain prior-iteration history
  - Sub-researchers cover too many files per scope

If context-tokens-per-gap increases cycle-over-cycle for 2 consecutive cycles:
  => trigger a harness-variant search targeting context reduction (Part 3)

EFFICIENCY-HISTORY.md format (one row per cycle):
  ```
  Cycle | Gaps-attempted | Gaps-closed | Avg-ctx-tokens-per-gap | Trend
  NNN   | N              | N           | N                      | up/down/flat
  ```

---

## PART 3: HARNESS-VARIANT SEARCH (every 5 cycles, Phase 6)

Based on the Meta-Harness principle: treat the harness itself as a searchable artifact.
Propose variant harness rules, evaluate them on a test task, keep the better performer.

### Process

1. The harness-improvement agent reads:
   - All CYCLE-NNN.md summaries (the full history, not just the last cycle)
   - EFFICIENCY-HISTORY.md (context and quality trend)
   - All MEMORY.md entries since the last variant search
   - Raw DISPATCH-TRACK files for cycles with the worst efficiency scores
     (read selectively via grep -- do not ingest all at once)

2. The agent identifies the 1-2 harness rules most likely causing degraded performance.
   It uses trace-based attribution (Part 1 protocol) applied to cycle-level data.

3. The agent proposes exactly 2 harness variants:
   - VARIANT-A: targets quality (gap-closed rate improvement)
   - VARIANT-B: targets efficiency (context-tokens-per-gap reduction)

   Each variant is a specific proposed change to one reference file only:
     - A new entry in references/constraints.md, OR
     - A modified scope rule in one agent file, OR
     - A changed threshold in CONFIG.yaml (e.g., WU file limit, feedback token cap)
   
   Written to: docs/harness-improvements/VARIANT-NNN-A.md and VARIANT-NNN-B.md

   VARIANT format:
   ```
   # VARIANT-NNN-<A|B>
   Target:       quality | efficiency
   Proposed change: <exact text to add or modify in which file>
   Rationale:    <which trace evidence justifies this -- cite specific CYCLE or TRACK entries>
   Expected effect: <what metric should improve and by how much>
   Risk:         <what could get worse>
   ```

4. HUMAN GATE (Gate 4 from autonomy-rules.md):
   Surface both variants to human with a recommendation.
   Human selects one, both, or neither.
   Human applies the approved change (agents do not self-modify protected files).

5. After human applies a variant, the next cycle tracks whether the expected effect occurred.
   Record outcome in EFFICIENCY-HISTORY.md.

### Variant search scope limits

The proposer reads DISPATCH-TRACK files selectively:
  - Search for lines containing "ITER-3", "ITER-4", or "ITER-5" to find high-iteration WUs
  - Search for "Ctx-used" entries where the value is 40% or above
  - Search for entries where L2 or L3 status is "fail" to find reviewer-layer patterns
Never ingest a full tracking file. Navigate it like a filesystem: locate by keyword, then read.

---

## IMPROVEMENT TRIGGERS SUMMARY

| Signal | Action | Where |
|--------|--------|-------|
| Any test failure | Trace-based attribution => constraint or test | Part 1 |
| Context efficiency degrading 2 cycles | Trigger variant search | Part 2+3 |
| Same MEMORY.md failure type twice | Mandatory Prevention Rule | Part 1 |
| Security scan finding | New security rule in constraints.md | Part 1 |
| Every 5 cycles | Harness-variant search | Part 3 |
| Doc gap discovered | Immediate doc update | Phase 5 |

---

## PART 4 -- SELF-ASSESSMENT (every cycle)

After each cycle, run the self-assessment protocol (runtime/self-assessment.md).
The 0-25 score feeds into the feedback closed-loop:
- Score trend tracked in EFFICIENCY-HISTORY.md
- Low scores (<15) trigger harness-variant search
- Critical scores (<10) halt the loop and surface to human
