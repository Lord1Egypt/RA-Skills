# STATUS MANAGEMENT AND RECOVERY

State lives in the repo, never in the context window.
Every phase and every cycle step writes to a tracking log.
Recovery can resume from any interruption point.

---

## TRACKING LOG HIERARCHY

One tracking log per major phase, written append-only:

  docs/status/RESEARCH-TRACK-NNN.md   -- researcher phase steps and sub-agent status
  docs/status/PLAN-TRACK-NNN.md       -- planner phase steps and gap plan status
  docs/status/DISPATCH-TRACK-NNN.md   -- ITR group status, per WU, per iteration

  docs/status/PROGRESS.md             -- compact cycle-level summary (one entry per phase)
  docs/status/HANDOFF.md              -- context reset checkpoint (overwritten each reset)
  docs/status/CYCLE-NNN.md            -- completed cycle archive (one per cycle)
  docs/status/EFFICIENCY-HISTORY.md    -- context-tokens-per-gap and gap-closed-rate across cycles
  docs/status/CHECKLIST-NNN-XX.md     -- per-WU done criteria checklist (one per WU)

---

## TRACKING LOG ENTRY FORMAT (all phase logs)

Every entry appended to a tracking log uses this format:

  ```
  [YYYY-MM-DD HH:MM] <PHASE>-<STEP> | <AGENT> | Status: <started|completed|blocked|recovering>
  Detail: <what happened -- factual, one sentence>
  Sub-agents: <count active>
  Context: ~<XX>%
  Output: <artifact produced or "none">
  Error: <error description or "none">
  Next: <next step>
  ```

Entries are APPEND-ONLY. Never edit or delete past entries.
A missing entry means the step was not completed.
A "blocked" entry means the step needs attention before proceeding.

---

## RESEARCH TRACKING (RESEARCH-TRACK-NNN.md)

Written by the research orchestrator at:
  - Before each sub-researcher is dispatched (started entry)
  - After each sub-researcher returns a Module Report (completed entry)
  - When the integration analysis phase begins and ends
  - When the gap analysis phase begins and ends
  - On any interruption (HANDOFF.md also written)

Recovery use: find the last "completed" sub-researcher entry.
All modules listed in "completed" entries do not need re-analysis.
Remaining modules resume from where the log was interrupted.

---

## PLAN TRACKING (PLAN-TRACK-NNN.md)

Written by the central planner at:
  - Before each gap planner is dispatched
  - After each GAP-PLAN-NNN-XX.md is produced
  - When conflict resolution begins and ends
  - When MASTER-PLAN-NNN.md is written
  - When human approval is received

Recovery use: find the last completed gap plan.
All GAP-XX IDs in "completed" entries do not need re-planning.
Re-run only gap planners for gaps not yet in the log.

---

## DISPATCH TRACKING (DISPATCH-TRACK-NNN.md)

Written by the dispatcher at:
  - GROUP start
  - Each WU ITR iteration: after implement, after test, after review
  - WU completion (all done criteria checked off)
  - GROUP integration verification: start and result
  - Final review: start and result
  - Any on-error hook trigger

Entry fields specific to dispatch tracking:
  ```
  [YYYY-MM-DD HH:MM] GROUP-N | WU-XX | ITER-N | STEP: implement|test|review|feedback|done
  Status: started | completed | blocked | recovering
  L1: pass|fail|pending  L2: pass|fail|pending  L3: pass|fail|pending
  Tests: N passed, N failed, coverage=XX%
  Gap-closed: N/M criteria confirmed
  Queue remaining: <list of WU IDs not yet complete>
  Ctx-tokens: <approximate tokens consumed by this agent instance>
  Ctx-used: ~XX%
  Error: <error or "none">
  ```

Recovery use: find the last "completed" WU entry.
Find any WU with no "completed" entry -- resume from its last logged step.
Do not re-run iterations that already have approved REVIEW files.

---

## CHECKLIST FORMAT (docs/status/CHECKLIST-NNN-XX.md)

One file per WU. Written by dispatcher before spawning the first implementer.
Checked off by dispatcher after each successful ITR cycle.

  ```
  # CHECKLIST -- NNN-WU-XX
  Gap ref: GAP-XX
  Plan ref: GAP-PLAN-NNN-XX.md
  Created: YYYY-MM-DD HH:MM

  ## Done Criteria
  - [ ] All unit tests pass (listed in GAP-PLAN test plan)
  - [ ] All integration tests pass
  - [ ] Coverage >= 90% on changed files
  - [ ] Lint and pre-commit hooks pass
  - [ ] Reviewer L1 approved (plan alignment)
  - [ ] Reviewer L2 approved (gap validity + quality)
  - [ ] Reviewer L3 approved (coherence)
  - [ ] Gap-closed criterion 1: <specific condition>
  - [ ] Gap-closed criterion 2: <specific condition>

  ## Iteration History
  - Iter 1: [YYYY-MM-DD] <one-line result>
  - Iter 2: [YYYY-MM-DD] <one-line result>
  ```

The CHECKLIST is the definitive record of whether a WU is done.
Not the context window. Not the dispatcher's memory. The CHECKLIST file.

---

## HANDOFF FORMAT (docs/status/HANDOFF.md, overwritten each reset)

  ```
  # HANDOFF
  Written: YYYY-MM-DD HH:MM
  Reason: context-reset | session-end | sub-agent | compact

  ## Active Phase
  Phase: research | plan | implement | final-review | reflect
  Cycle: NNN
  Tracking log: docs/status/<PHASE>-TRACK-NNN.md

  ## Last Completed Step
  Step: <exact step description from tracking log>
  Log entry timestamp: YYYY-MM-DD HH:MM

  ## Next Step
  <exact next action for the resuming agent -- be specific>

  ## Active Constraints
  <list prevention rules from references/constraints.md active this session>

  ## Files Modified This Session
  <list of file paths only -- no contents>

  ## Recovery Instructions
  1. Read docs/status/PROGRESS.md (cycle state)
  2. Read docs/status/<PHASE>-TRACK-NNN.md (find last completed step)
  3. Read docs/status/CHECKLIST-NNN-XX.md for any in-progress WUs
  4. Run: git log --oneline -5 (verify last checkpoint)
  5. Read references/constraints.md (apply prevention rules)
  6. Read MEMORY.md (failure patterns)
  7. Resume from "Next Step" above
  ```

---

## PROGRESS.md COMPACT SUMMARY

PROGRESS.md contains one compact entry per phase, plus the overall cycle state.
It is the fast-read view of "where are we?" -- not a detailed log.

  ```
  # PROGRESS -- Cycle NNN
  Last updated: YYYY-MM-DD HH:MM
  Overall status: in-progress | complete | blocked
  Current phase: research | plan | implement | final-review | reflect

  ## Phase Status
  [x] Phase 0: Session init -- YYYY-MM-DD
  [x] Phase 1: Research -- RESEARCH-NNN.md produced (Q-Agent + R-Agent complete) -- YYYY-MM-DD
  [x] Phase 2: Plan -- Design approved, Outlines approved, MASTER-PLAN-NNN.md approved -- YYYY-MM-DD
  [~] Phase 3: Implement -- GROUP-1 complete, GROUP-2 in progress -- YYYY-MM-DD
  [ ] Phase 4: Final review
  [ ] Phase 5: Reflect
  [ ] Phase 6: Improve

  ## Gap Status
  | GAP | Severity | WU | Status |
  |-----|----------|----|--------|
  | GAP-01 | critical | WU-01-01 | complete |
  | GAP-02 | high | WU-02-01 | iter-3 in progress |
  ```

---

## CYCLE ARCHIVE (docs/status/CYCLE-NNN.md)

Written at Phase 5 (Reflect). Never modified after writing.

  ```
  # CYCLE NNN SUMMARY
  Completed: YYYY-MM-DD HH:MM
  Duration: <hours>
  Modules analyzed: N
  Gaps found: N (critical: N, high: N, medium: N, low: N)
  Gaps resolved: N
  Gaps deferred: N
  WUs implemented: N
  Total iterations: N (average per WU: N)
  Tests written: N new
  Prevention rules added: N
  Avg-ctx-tokens-per-gap: N   (quality/efficiency metric -- tracked in EFFICIENCY-HISTORY.md)
  Gap-closed-rate: N/N        (gaps resolved / gaps attempted this cycle)

  ## Harness Gap Categories Observed
  <list of gap categories from runtime/observability.md>

  ## Key Failures and Memory Entries
  <list of MEMORY.md entries written this cycle>
  ```
