# AUTONOMOUS LOOP

Each full pass is one cycle. Phases run sequentially.
Context budget is monitored at every phase boundary.
Every phase writes to its tracking log before and after.

---

## PHASE 0: SESSION INIT (every session start)

### Step 0a -- Platform prerequisite check (MUST complete before any repo access)

Before reading any file or calling any tool, verify the platform can enforce its
required protections. This is a blocking check -- if any item is unconfirmed, the
agent surfaces the gap to the human and waits for resolution or explicit override.

Check 1 -- Sensitive path blocking
  Verify: confirm with your platform administrator that the router is configured to
          block read calls matching the patterns in references/sensitive-paths.md.
  How to confirm without a live call: review the router's block-list configuration
          and confirm the patterns are present, OR check prior BLOCKED_READ log entries.
  If router blocking is unconfirmed: HALT. Surface to human.
    Message: "Cannot confirm platform enforces sensitive path blocking.
              See PLATFORM_REQUIREMENTS.md item 1. Verify router config before proceeding."

Check 2 -- Protected path write blocking
  Verify: confirm with your platform administrator that the router blocks write calls
          to the protected paths listed in tools/tool-router.md PROTECTED PATHS section.
  How to confirm: review router config for the protected path list, OR check prior
          BLOCKED_WRITE log entries from any previous session.
  If write blocking is unconfirmed: HALT. Surface to human.
    Message: "Cannot confirm platform enforces write blocking on protected harness files.
              See PLATFORM_REQUIREMENTS.md item 2. Verify router config before proceeding."

Check 3 -- Confirm loop mode and parallelism
  Read CONFIG.yaml loop_mode and max_parallel_agents.
  If loop_mode is "continuous" and this is the first cycle on this repo:
    Surface to human: "CONFIG.yaml is set to continuous mode. Is this intended?
                       Recommend single-pass for first cycle."
    Wait for explicit confirmation before proceeding.

Check 4 -- Confirm human gate availability
  Surface to human: session type, cycle number, and platform check results.
  Wait for explicit acknowledgment (on-start lifespan hook).
  This acknowledgment also serves as confirmation that human gates are operational.

If all checks pass: proceed to Step 0b.
If any check fails and human chooses to override: log override decision in
  docs/status/PROGRESS.md with timestamp and human's explicit acknowledgment.

### Step 0b -- Fast-path evaluation

Fast-path 1 -- Single-pass mode:
  If CONFIG.yaml loop_mode is "single-pass":
    Skip Phase 1 (research) unless gaps are explicitly provided.
    Skip Phase 2.5 (contract negotiation) -- use provided plan directly.
    Reduce agent pool to: implementer + reviewer only.
    Skip Phase 6 Steps 4-5 (variant search, observability review).

Fast-path 2 -- Resume from HANDOFF.md:
  If docs/status/HANDOFF.md exists and is recent (< 1 hour old):
    Skip Phase 0a checks (already verified in prior session).
    Skip Phase 1 (research) -- use research output referenced in HANDOFF.md.
    Skip Phase 2 (plan) -- use plan output referenced in HANDOFF.md.
    Go directly to the phase and step indicated in HANDOFF.md.
    Read MEMORY.md for entries newer than HANDOFF.md timestamp.

If no fast-path applies: proceed to Step 0c (standard init).

### Step 0c -- Context and state init

1. Read CLAUDE.md / AGENTS.md (base knowledge)
2. Read docs/status/PROGRESS.md -- is this a resumption?
3. Read docs/status/HANDOFF.md -- load checkpoint if resuming
4. Read MEMORY.md (failure patterns and prevention rules)
5. Read references/constraints.md (active prevention rules)
6. If resuming: read the relevant tracking log to find last completed step
   - Research interrupted => read RESEARCH-TRACK-NNN.md
   - Planning interrupted => read PLAN-TRACK-NNN.md
   - Implementation interrupted => read DISPATCH-TRACK-NNN.md
7. If already above 20% context from init reads: compact before proceeding

### Step 0d -- Storage format selection (before Phase 1)

Ask user: "How should research documentation be saved?"
  Options:
    A) Markdown files in docs/ folder (default)
    B) Obsidian LLM wiki
  IF user selects B: ask vault location. Record setting.
  This setting is used throughout all phases for output location.
  Record in PROGRESS.md: storage_format = <choice>, vault_path = <path or null>

LIFESPAN HOOK: on-start (combined with Check 4 above)
  Surface: session type, cycle number, checkpoint state, platform check results
  Wait: human acknowledgment before proceeding to Phase 1.

---

## PHASE 1: RESEARCH

Small-piece rule: Q-Agents and R-Agents cover at most 20 files each. Orchestrator
reads only compressed R-RECORDs, never raw source. See agents/researcher.md.

Orchestrator: researcher_agent (agents/researcher.md)

Phase A -- Q-Agent questioning:
  - Orchestrator scans full file structure
  - Spawns parallel Q-Agents (one per module boundary)
  - Each Q-Agent reads code, asks questions, performs web search if needed
  - Each Q-Agent produces Q-FINDINGS-NNN-<module>.md

GATE-R1 -- Research questions:
  Surface all Q-FINDINGS to human for review.
  Wait for human to answer questions and approve proceeding to R-Agent phase.
  If human requests changes: re-spawn Q-Agents with adjusted scope.

Phase B -- R-Agent recording:
  - Spawns paired R-Agents (1:1 with Q-Agents)
  - Each R-Agent receives Q-FINDINGS + human answers
  - Records facts + user vision verbatim
  - Each R-Agent produces R-RECORD-NNN-<module>.md

Phase C -- Aggregation:
  - Orchestrator reads all R-RECORDs
  - Cross-module integration analysis
  - Aggregates into RESEARCH-NNN.md

Phase D -- Tracking:
  - RESEARCH-TRACK-NNN.md updated at every step
  - HANDOFF.md written if context reset needed mid-research

Context check: at every agent aggregation boundary, check orchestrator
context. If above 40%: compact orchestrator context, keep only aggregated summaries.

Output: docs/status/RESEARCH-NNN.md (NO GAPS-NNN.md -- gap analysis is the planner's job)

---

## PHASE 2: PLAN

Small-piece rule: one gap planner per gap, receiving only the relevant research excerpt.
WUs are sized to fit in one implementer context window (3-5 files max). See agents/planner.md.

Orchestrator: planner_agent (agents/planner.md)

Phase 2.1 -- Design Discussion:
  - Planner spawns design discussion agents (one per subsystem if large/complex)
  - Each agent analyzes current vs desired state, identifies patterns, asks open questions
  - Each agent produces DESIGN-NNN-<scope>.md
  - PLAN-TRACK-NNN.md updated as each design completes

  GATE-P1 -- Design direction:
    Surface DESIGN-NNN-*.md to human.
    Wait for human to answer design questions and confirm direction.
    No outlining begins until human approves design direction.

Phase 2.2 -- Outline + Gap Analysis:
  - Planner spawns outline agents (one per change area if large/complex)
  - Each agent performs gap analysis (5 categories) and maps changes
  - Produces OUTLINE-NNN-<scope>.md and GAPS-NNN.md
  - PLAN-TRACK-NNN.md updated as each outline completes

  GATE-P2 -- Change outlines:
    Surface OUTLINE-NNN-*.md and GAPS-NNN.md to human.
    Wait for human to confirm scope and approve outlines.
    No master planning begins until human approves outlines.

Phase 2.3 -- Master Planning:
  - Classify gaps (SIMPLE/STANDARD/COMPLEX)
  - Spawn gap planners per non-SIMPLE gap
  - Each gap planner produces GAP-PLAN-NNN-XX.md
  - Consistency check, conflict resolution, scoring, prioritization
  - Produces MASTER-PLAN-NNN.md with prioritized execution queue

  GATE-P3 (on-plan-complete lifespan hook):
    Surface MASTER-PLAN-NNN.md to human.
    Wait for explicit approval (with any modifications) before Phase 2.5.
    Record approval timestamp in MASTER-PLAN-NNN.md.

Context check: at every agent completion boundary, check planner
context. If above 40%: compact, keep only summaries and prioritization.

---

## PHASE 2.5: CONTRACT NEGOTIATION AND WORKTREE (between Plan and Implement)

Before dispatching any implementer agents, the worktree is built and contracts are negotiated.

### Step 0 -- Worktree Agent
Spawn a single worktree agent to produce WORKTREE-NNN.md:
  - Reads MASTER-PLAN-NNN.md + all GAP-PLAN-NNN-XX.md
  - Builds dependency graph between WUs
  - Assigns execution slots with dependency ordering
  - Defines checkpoint boundaries
  - Output: docs/status/WORKTREE-NNN.md

The worktree provides the execution order for Phase 3.

### Step 1 -- Contract Proposal (implementer agent)
For each WU in MASTER-PLAN-NNN.md, a temporary implementer instance proposes:
  - What files will be created or modified (exact paths)
  - What the implementation approach will be (brief)
  - What "done" looks like: specific, testable acceptance criteria
  - What tests will be written and what they will verify

### Step 2 -- Contract Review (reviewer agent)
A reviewer instance evaluates the proposal:
  - Are the acceptance criteria specific enough to be unambiguous?
  - Does the scope match the WU piece contract from GAP-PLAN?
  - Are edge cases covered in the test plan?
  - Is the implementation approach sound?

### Step 3 -- Negotiation
If the reviewer identifies gaps in the proposal:
  - Reviewer writes specific concerns to the contract document
  - Implementer revises the proposal to address each concern
  - Repeat until reviewer approves OR escalation to human (rare)

### Step 4 -- Freeze
Once approved: CONTRACT-NNN-XX.md is written and FROZEN.
No scope changes without a new negotiation cycle.
The implementer dispatched for this WU MUST implement exactly what CONTRACT-NNN-XX.md says.

### Output
  docs/status/CONTRACT-NNN-XX.md per WU (see templates/contract.md format)

---

## PHASE 3: IMPLEMENT

Small-piece rule: each implementer instance handles one task (T-NNN) with 3-5 files max.
Each reviewer layer receives only the section it needs. Feedback capped at 500 tokens.
See agents/implementer.md, agents/reviewer.md, agents/dispatcher.md.

Orchestrator: dispatcher (agents/dispatcher.md)

For each GROUP in WORKTREE-NNN.md execution graph:
  For each WU in the group, read CONTRACT-NNN-XX.md (frozen done criteria) before dispatching.

  Phase B -- Parallel ITR execution:
    Spawn ITR group per WU (max: CONFIG.yaml max_parallel_agents).
    Each group runs the self-feedback loop:
      implement => test (isolated sandbox, various environments/edge cases) =>
      review (2-4 reviewers, clean-pass-only) =>
      feedback => loop until CLEAN PASS or on-error hook.
    DISPATCH-TRACK-NNN.md updated after every iteration of every group.
    Status reported to dispatcher after each cycle.
    Set a cron job to periodically check on subagent progress.
    If any agent is stuck for >10 minutes without output, log the issue,
    kill it, and spawn subagents to break the task into smaller pieces.
    Complex WUs: break into subtasks, spawn nested ITR group per subtask.

  Integration check:
    After GROUP completes: run GROUP's integration verification tests.
    If fail: debugger_agent + surface to human before next GROUP.

After ALL groups complete:
  Run cross-gap integration tests from MASTER-PLAN-NNN.md.

---

## PHASE 4: FINAL REVIEW

Agent: reviewer_agent (Final Review mode -- agents/reviewer.md)

Checks:
  - All gaps in GAPS-NNN.md have confirmed gap-closed criteria
  - Implementation coherent with RESEARCH-NNN.md integration map
  - No principle violations introduced
  - All done criteria across all WUs checked off
  - Cross-gap integration tests pass

Output: docs/status/FINAL-REVIEW-NNN.md

LIFESPAN HOOK: on-cycle-complete
  Surface FINAL-REVIEW-NNN.md to human.
  If PASS: cycle complete. Transition to maintenance or next cycle.
  If FAIL: list remaining issues. Human decides: new cycle or defer.

---

## PHASE 5: REFLECT

- Write MEMORY.md entries for every failure (EPISODIC type)
- Write CYCLE-NNN.md summary (docs/status/)
- Identify harness gap categories for recurring patterns
- Update references/constraints.md if Prevention Rule is needed (append-only)

---

## PHASE 6: IMPROVE

Step 1 -- Failure attribution (every cycle)
  Apply trace-based attribution per runtime/self-improvement.md Part 1.
  Read raw DISPATCH-TRACK and tool-log files for failed WUs via selective grep.
  Record "Harness Cause:" in every MEMORY.md failure entry.

Step 2 -- Context-efficiency tracking (every cycle)
  Compute avg-ctx-tokens-per-gap from DISPATCH-TRACK-NNN.md.
  Append to docs/status/EFFICIENCY-HISTORY.md.
  If efficiency degraded 2 cycles in a row: flag for variant search this cycle.

Step 3 -- Garbage collection (per gc_interval)
  Run garbage_collector_agent if gc_interval has elapsed (CONFIG.yaml).

Step 4 -- Harness-variant search (every 5 cycles, or when efficiency flag is set)
  Run per runtime/self-improvement.md Part 3:
    a. Agent reads CYCLE summaries and EFFICIENCY-HISTORY.md
    b. Agent greps DISPATCH-TRACK files for high-iteration and high-context WUs
    c. Agent proposes 2 variants (quality-target and efficiency-target)
    d. Variants written to docs/harness-improvements/VARIANT-NNN-*.md
  HUMAN GATE (Gate 4): surface variants to human for selection and application.

Step 5 -- Observability harness review (every 5 cycles)
  Run per runtime/observability.md harness-improvement cycle.

---

## LOOP CONDITION

Continue unless:
  - No gaps remain (transition to maintenance mode)
  - Human explicitly halts

In single-pass mode: stop after Phase 6, surface summary, wait for human go-ahead.

---

## COMPACT SUMMARY FORMAT

At each phase transition, write a one-entry compact summary to PROGRESS.md:

  ```
  [YYYY-MM-DD HH:MM] CYCLE-NNN PHASE-N: <phase name>
  Status: complete | in-progress | blocked
  Output: <primary artifact produced>
  Next: <next phase or action>
  Key findings: <one sentence -- most important thing from this phase>
  ```

This ensures PROGRESS.md is always a readable compact state of the cycle,
not a raw dump of all activity.
