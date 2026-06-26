# State Management

## 1. Goal

Preserve project workflow state across interruption, restart, and long production cycles.

Novel work is long-running. The workflow must not depend only on short-term chat context.

---

## 2. State file location

Use a project-local state file:

`[project root]/.novel-state.json`

This file is the primary structured workflow memory for the current project.

---

## 3. Required state responsibilities

The state system must record at least:
- current stage
- current substage when relevant
- last completed stage
- next intended stage
- approval status for each stage
- blocking issues
- artifact existence status
- working title / final title state
- current batch state when drafting has begun
- current revision state when formal revision is active
- latest closed revision snapshot
- last update time
- opening-gate approval state
- style-lock version and platform mode
- lane / track choice
- ledger artifact existence
- parent-owned `narrativeIntelligence.*` summary, including timeline risk, open critical issues, and revision actions
- review-side brainstorming overlay status, including `review.brainstormMode`, `review.brainstormFocus`, `review.brainstormRound`, and `review.selectedBranch`
- parent-owned style-risk anti-cliche summary, including `narrativeIntelligence.styleRisk.noveltyAxes` and `narrativeIntelligence.styleRisk.lastClicheScanStage`
- autopilot goal / latest progress / stop reason state when bounded automation is active

---

## 4. Read-before-work rule

Before starting any stage:
- load `.novel-state.json` if it exists
- determine the current stage, blockers, and next valid action from the state file
- do not infer workflow position only from vague chat memory if structured state exists

When the user asks for project status, current progress, blockers, approval state, current batch state, or next-step guidance, use `scripts/novel_project_status.py` as the default status-summary tool.

---

## 5. Write-after-stage rule

After each stage-level event, update the state file.

This includes:
- stage start
- stage completion
- user approval
- user rejection / revision request
- blocking issue creation
- rollback to an earlier stage
- final delivery
- Feishu sync completion if relevant
- autopilot activation, supersede, progress update, and explicit stop events
- planning approval initialization for derived narrative-intelligence artifacts `05F`–`05I`
- accepted drafting / polishing / proofreading refreshes for `narrativeIntelligence.*`

Do not persist runtime subagent ids in `.novel-state.json`.
Do not persist session ids, raw execution packages, or raw subagent conversation history in `.novel-state.json`.
Persist only lightweight execution summaries and autopilot progress/stop fields when drafting, polishing, or proofreading ran through subagent execution.
Parent ownership is exclusive in this slice: only the parent may update `.novel-state.json`, choose a staging branch for promotion, authorize canonical backfill, or clean up stale Cliche Exhaustion branches.

---

## 6. Discovery-state tracking

By the end of Discovery stage, state should reflect whether these artifacts exist:
- `00A_热点扫描.md`
- `00B_用户偏好.md`
- `00C_底盘与切口决策.md`
- `00_选题报告.md`

It should also record whether:
- title is confirmed
- working title is approved
- discovery stage is approved for advancement

---

## 7. Batch-writing state tracking

Once drafting begins, state must also track the current batch.

At minimum it should record:
- current batch chapter range
- current batch chapter count
- chapterTasks for the approved current batch
- pendingProgressItems for unsent chapter-progress changes
- whether batch scope is confirmed
- whether chapter-plan package exists
- whether chapter-plan package is approved
- whether draft writing is complete
- whether polishing is complete
- whether proofreading / batch final pass is complete
- whether recap has been updated
- whether the workflow is currently waiting for user decision on the next batch
- current batch focus
- current batch attraction points
- current batch climax target
- whether `04A_开篇设计.md` exists
- whether the opening gate is approved
- whether the style bible exists
- whether the mainline spec exists
- whether the ledger set exists

Chapter progress is explicit state, not chat-only memory.
`chapterTasks` tracks the latest per-chapter phase/status summary.
`pendingProgressItems` tracks lightweight progress events that still need to be reported or acknowledged.

---

## 8. Revision-state tracking

Once formal revision is active, state must record at least:
- whether revision mode is active
- feedback type
- feedback summary
- affected stages
- affected files
- override mode
- scope summary
- conflict summary
- revision plan summary
- revision result summary
- current revision gate
- whether revision mode is awaiting user approval
- latest closed revision snapshot

These fields must be explicit enough for interruption recovery.

The revision entry point may also prefill scope / plan from `narrativeIntelligence.revisionActions` when open critical findings already exist.

For Cliche Exhaustion Loop continuity, keep these fields explicit under `review.*`:
- `review.brainstormMode`
- `review.brainstormFocus`
- `review.brainstormRound`
- `review.selectedBranch`

Rules:
- use `review.brainstormMode: "cliche_exhaustion"` for this loop slice
- `review.brainstormRound` is a round label string such as `mutation` or `enumeration`, not a numeric counter
- `review.selectedBranch` should use the stage-prefixed branch key form used elsewhere, for example `story-planning/版本B`
- `review.selectedBranch` should point to the branch whose `05_定稿结论.md` authorized canonical backfill
- if Story Planning activated the deep anti-cliche pass, planning approval should not be recorded until that retained conclusion exists in the selected branch

---

## 9. Autopilot-state tracking

Bounded automation lives under `autoPilot.*`.

State must record at least:
- whether autopilot is currently active
- the normalized terminal goal chapter under `goalChapter`
- the goal completion contract under `goalCondition`
- when automation started and which user message authorized it
- the latest merged progress timestamp and summary under `lastProgressAt` / `lastProgressSummary`
- the explicit stop reason under `stopReason`
- when automation stopped under `stoppedAt`
- whether manual resume is required under `awaitingManualResume`

Rules:
- default remains manual approval, so `autoPilot.active: false` is the normal baseline
- store the target goal explicitly as `goalChapter` + `goalCondition`; for current automation the goal condition remains `proofreading_completed`
- store the latest surfaced automation progress explicitly as `lastProgressSummary`, not only in chat
- stop reasons must stay explicit, for example `blocked: 人物口吻漂移`, `user_interruption`, or `goal_reached`
- if the user replaces the bounded goal, record `superseded_by_new_user_goal` for the old run before starting the new one
- final review remains manual; `review.finalDecision` and `approvals.finalApproved` are separate from `autoPilot.*`

---

## 10. Final-review state tracking

Once final review is written, state must also record at least:
- latest final-review decision
- whether the project is judged delivery-ready
- final-review blockers from the latest report
- final-review summary for interruption recovery and status output

These fields live under `review.*`.

Open critical issues from `narrativeIntelligence.consistency.openCriticalIssues` must be foldable into `review.finalBlockingIssues`.

They do not replace `approvals.finalApproved`.
`review.finalDecision` records the latest final-review judgment, while `approvals.finalApproved` remains the separate user confirmation for final delivery.

---

## 11. Narrative-intelligence tracking

`narrativeIntelligence.*` is parent-owned derived state.

State must record at least:
- whether the timeline layer is enabled
- the latest batch and chapter labels touched by parent-side refresh
- open temporal risks
- CFPG triple counts
- the latest consistency-check stage
- evidence-backed open critical issues
- revision actions derived from open critical issues when applicable
- `narrativeIntelligence.styleRisk.noveltyAxes`
- `narrativeIntelligence.styleRisk.lastClicheScanStage`

Rules:
- initialize `05F`–`05I` after planning approval
- refresh timeline / CFPG / ToM metadata after accepted drafting, polishing, and proofreading
- accepted proofreading may refresh `consistency.*` and stop autopilot with an explicit blocker reason
- accepted proofreading may refresh `narrativeIntelligence.styleRisk.*` parent-side
- default `narrativeIntelligence.styleRisk.noveltyAxes` to `[]`
- default `narrativeIntelligence.styleRisk.lastClicheScanStage` to `null`
- do not let subagents write `.novel-state.json` or `05F`–`05I` directly

---

## 12. Approval tracking

State should distinguish between:
- artifact exists
- artifact approved

These are not the same.

Examples:
- `outlineDoc: true` does not mean `outlineApproved: true`
- `topicReport: true` does not mean `discoveryApproved: true`
- `chapterPlanExists: true` does not mean `chapterPlanApproved: true`
- `openingDesign: true` does not mean `openingApproved: true`

State should also record the current review gate and the latest meaningful user feedback summary.
This makes interruption recovery much safer than relying only on boolean flags.

Supervisor persistence fields must be explicit under `review.*`:
- `pendingArtifactPaths`
- `lastPersistedStage`
- `lastPersistedAt`
- `brainstormActive`
- `activeBranches`

Required invariants:
- if `pendingArtifactPaths` is non-empty, workflow status must be `awaiting_user_approval`
- if `brainstormActive` is true, only explicit brainstorming mode may write to `staging/`
- `activeBranches` should contain only currently valid branch ids

---

## 13. Blocking issue tracking

Blocking issues must be recorded explicitly.

Examples:
- title not confirmed
- outline has unresolved objections
- protagonist definition still unstable
- proofreading found unresolved blocker
- user asked for revision before advancement
- current batch chapter-plan not yet approved
- current batch is waiting for user decision whether to continue
- revision is waiting for scope confirmation
- revision is waiting for plan approval
- revision result is waiting for approval

Do not silently ignore blockers.

---

## 14. Fallback recovery rule

If `.novel-state.json` is missing:
- recover a provisional state from file structure and existing artifacts
- clearly mark that the state is reconstructed
- write the reconstructed state back to `.novel-state.json`

Do not rely on memory-only recovery when a structured state file can be rebuilt.

---

## 15. Required state quality

A usable state file should answer:
- where is the project now
- what stage was last completed
- what has already been approved
- what is blocked
- what should happen next
- what batch is currently active
- whether the current batch is waiting for user approval or next-batch decision
- what the latest bounded autopilot goal, progress, and stop reason are
- whether formal revision is active
- what revision gate is open
- what the latest closed revision was
- what the latest final-review result was
- what the latest narrative-intelligence summary says

If the state file cannot answer those, it is incomplete.
