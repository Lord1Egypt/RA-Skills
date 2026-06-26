# OBSERVABILITY AND FEEDBACK CLOSED-LOOP

Observability is not logging. It is the closed loop that feeds harness failures back
into harness improvements. The target of analysis is always the harness, never the model.

---

## EXECUTION TRACKING

Every cycle produces an execution trace in docs/generated/tool-logs/:
  - One entry per tool call (metadata only -- see tools/execution-protocol.md)
  - One cycle summary in docs/status/CYCLE-NNN.md

The cycle summary records:
  - Tasks attempted, completed, failed
  - Tool calls made per agent (counts only, no payloads)
  - Duration per phase
  - Test results (aggregate counts + coverage)
  - Abnormalities detected
  - Avg-ctx-tokens-per-gap (context efficiency metric)
  - Gap-closed-rate (quality metric)

### Queryable trace filesystem

All tracking logs and tool-log entries are stored as grep-able plaintext files.
The harness-improvement agent (Phase 6) navigates them selectively:

  Find high-iteration WUs (scope too large?):
    Search DISPATCH-TRACK-NNN.md for lines containing "ITER-3", "ITER-4", or "ITER-5"

  Find high-context steps (context rule violated?):
    Search DISPATCH-TRACK-NNN.md for "Ctx-used" entries where the percentage is 40 or above

  Find recurring reviewer failures (review scope gap?):
    Search DISPATCH-TRACK files for entries where L2 or L3 status is "fail"

  Find repeated failure types across cycles (constraint gap?):
    Search MEMORY.md for lines containing "Harness Cause:"

The agent reads selectively. It does NOT ingest full tracking files.
Full files exist in the filesystem for diagnosis; the agent retrieves what it needs.
This is the key design: filesystem-as-feedback-channel, not prompt-as-feedback.

---

## QUALITY CATEGORIZATION

After each VERIFY phase, categorize every output:

TIER 1 -- Critical (block cycle advance):
  - Failing tests
  - Security scan findings
  - Reviewer veto

TIER 2 -- High (address this cycle):
  - Coverage below threshold
  - Performance regression
  - Constraint violation

TIER 3 -- Medium (backlog with priority score):
  - Code smell / dead code
  - Doc gaps
  - Minor reviewer comments

TIER 4 -- Low (GC agent, next cycle):
  - Style inconsistencies
  - Optimization opportunities
  - Refactoring candidates

Only Tier 1 blocks cycle advance. Tier 2-4 are scored and queued.

---

## ABNORMALITY DETECTION

Trigger debugger_agent immediately on:
  - Any test that was passing and is now failing (regression)
  - Any tool call that returns an unexpected structure
  - A sub-agent that produces output not matching its EXPECTED OUTPUT field
  - The same failure appearing in tool-logs more than once
  - A cycle that takes more than 2x its historical average duration
  - An agent that exceeds its context limit without triggering the 40% rule

Do not continue the cycle on abnormality. Stop, diagnose, write MEMORY.md entry, then
decide: fix in this cycle, or checkpoint and escalate to human.

---

## FEEDBACK CLOSED-LOOP

This is the most important part of observability. When a failure occurs:

WRONG QUESTION: "Why did the model get this wrong?"
RIGHT QUESTION:  "What was missing from the harness that allowed this to happen?"

Harness gap categories:
  MISSING CONSTRAINT  -- a rule that would have prevented this does not exist
  MISSING TEST        -- a test that would have caught this was not written
  MISSING CONTEXT     -- the agent lacked information it needed (context engineering gap)
  MISSING TOOL        -- the agent could not verify something it needed to verify
  MISSING REVIEW      -- the review cycle did not catch this (review scope gap)
  MISSING CHECKPOINT  -- a context reset lost state that should have been persisted

For every failure, identify the harness gap category and create the missing element.
Record the gap category in MEMORY.md. Update references/constraints.md if it is a
MISSING CONSTRAINT.

---

## HARNESS IMPROVEMENT CYCLE

At the end of every 5 cycles, run a harness review:

1. Aggregate CYCLE-NNN.md summaries
2. Identify the most frequent gap categories
3. Draft harness improvements (new constraints, tests, or context rules)
4. Surface to human for approval (P6 gate)
5. Apply approved improvements to this skill's reference files (append-only)
6. Commit changes to the skill under docs/harness-improvements/

The harness should become measurably more effective over time.
Track: regression rate, average cycle duration, context resets per cycle.

---

## COST TRACKING

Token usage and cost are tracked per-cycle. See runtime/cost-tracking.md.

Cost-per-gap is a primary efficiency metric. Rising cost-per-gap signals harness
bloat (too many retries, too much context per gap, sub-optimal agent routing).
Connect cost data to the feedback closed-loop: if cost-per-gap is increasing,
analyze whether the harness is introducing unnecessary overhead.
