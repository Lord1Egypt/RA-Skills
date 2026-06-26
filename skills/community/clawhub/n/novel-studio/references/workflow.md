# Workflow

## 1. Workflow overview

Use this workflow to turn a novel idea into a structured, reviewable, and deliverable fiction project.

Exploration / brainstorming mode is **not** the default workflow.
Only use explicit exploration behavior when the user clearly asks for it with requests such as:
- 进入脑爆模式
- 进入探索模式
- 先脑暴
- 先发散
- 先不要定稿
- 先试几个版本
- 只做创意探索

When the user has not explicitly requested exploration mode:
- remain in the formal staged workflow
- prefer structured progress over open-ended ideation
- do not silently switch into freeform brainstorming

Default stage order:

1. Discovery stage
2. Story planning stage
3. Character system stage
4. Drafting stage
5. Polishing stage
6. Proofreading stage
7. Final review and delivery stage

Do not casually skip stages.
If the user explicitly asks to skip a stage, continue only after stating the risk and recording the assumption.

---

## 2. Global hard rules

### 2.1 Stage discipline
- Do not start stable planning before discovery stage is complete
- Do not start drafting before planning and character system stages are complete
- Do not start the first prose batch before the opening gate is approved
- Do not polish text that is still structurally unstable
- Do not proofread text that is still under major rewrite
- Do not treat unreviewed output as final delivery

### 2.2 Universal user approval discipline
Every stage must end with:
1. structured stage report
2. iterative user feedback handling
3. explicit user approval before advancement

Without explicit user approval, remain in the current stage.
Only explicit brainstorming mode may write to `staging/`.

### 2.3 File discipline
All major stage outputs must be reflected in canonical project files, not only in chat.

The workflow status model must stay explicit:
- `collecting_inputs`
- `producing_artifact`
- `awaiting_user_approval`
- `brainstorming`
- `blocked`

Hard rule: the moment a canonical file is written or refreshed, the workflow enters a stage-specific approval gate.
Persisted stage output should move the workflow to `awaiting_user_approval`, not stay in freeform discussion.

### 2.4 Advancement discipline
Do not advance to the next stage unless:
- required inputs are present
- required outputs are produced
- completion standard is met
- no listed blocker remains unresolved
- the user explicitly approves advancement

### 2.5 Autopilot overlay
- manual approval remains the default; without explicit autopilot authorization, every gate stays manual
- autopilot activates only after explicit bounded user authorization with a terminal chapter goal such as `继续到第10章结束`
- vague approval like `继续` or `好` does not activate autopilot
- autopilot does not change ownership: the parent remains the orchestrator, while `drafting`, `polishing`, and `proofreading` still run through their subagents
- progress updates still continue during automation; keep surfacing merged chapter progress after dispatch start, accepted child results, and approval transitions
- `scripts/advance_autopilot.py` advances at most one safe step per call
- each `scripts/advance_autopilot.py` result also includes a `report` object; parent orchestration should use it as the single source for notify / pause / stop decisions instead of inferring from raw state
- if `report.shouldNotify` is true, send `report.userFacingMessage` immediately and ack any surfaced `report.pendingEventIds` after the message is delivered
- if `report.blockingReason` is present or `report.awaitingManualResume` is true, surface that halt to the user explicitly instead of silently polling again
- one-step advancement is limited to confirming `batch.scopeConfirmed`, safely approving `batch.chapterPlanApproved` from a parseable `05_本轮章节规划.md`, or approving an eligible open review gate
- eligible auto-approvable review gates are only `waiting_draft_feedback`, `waiting_polishing_feedback`, and `waiting_proofreading_feedback`
- blocked delegated results must halt autopilot with an explicit stop reason such as `blocked: 人物口吻漂移`
- substantive user interruptions must halt autopilot with stop reason `user_interruption`
- when the goal chapter reaches approved proofreading completion, halt autopilot with stop reason `goal_reached`
- if the user replaces the bounded goal, stop the old run with `superseded_by_new_user_goal` before starting the new one
- never auto-approve `waiting_final_review_feedback`; `advance_autopilot.py` returns `final_review_manual` and final review stays manual

### 2.6 Cliche Exhaustion Loop overlay
- treat the Cliche Exhaustion Loop as a supervisor-side protocol layer, not a new workflow stage
- `Discovery` uses `quick` mode to expose the intuitive cliché version before topic approval
- `Story Planning` uses `deep` mode to enumerate cliché samples, retained novelty axes, and fallback risks for the chosen direction
- planning approval should not occur until the retained direction has completed the deep anti-cliche pass and a supervisor-side conclusion records what novelty axes survived
- when the supervisor activates the deep anti-cliche pass for Story Planning, that conclusion must be persisted in `05_定稿结论.md` before planning approval
- `Opening` validates retained novelty axes instead of reopening broad ideation
- `Proofreading` only reports lightweight parent-side backslide detection in this slice
- the parent remains the sole owner of `.novel-state.json`, staging branch selection, canonical backfill, and stale-branch cleanup

---

## 3. Stage 1: Discovery stage

### Goal
Use hot-search/trend scan first, then discuss direction with the user, then capture the user’s preferences, then produce a formal topic decision and title decision.

### Internal sub-steps
1. hot-search / trend scan
2. initial recommendation summary
3. user discussion and preference capture
4. topic comparison
5. top recommendation
6. title candidate generation
7. structured stage report
8. iterative revision with user
9. explicit approval gate

### Required input
At least enough information to identify a rough creative area, or explicit permission to begin with broad market scanning before narrowing.

### Forbidden to start if
- the request is too vague even for broad market scanning
- user constraints directly conflict and remain unresolved at the most basic level

### Required output
This stage must produce:
- hot-search / trend-scan summary
- user preference summary
- topic comparison
- top recommendation
- title candidates
- confirmed final title or explicitly approved working title
- usable `00_选题报告.md`

### Completion standard
This stage is complete only if:
- current market signal scan exists
- user preference capture exists
- topic comparison is explicit
- one top recommendation exists
- title candidates exist
- the user explicitly confirms a final title or explicitly approves a working title
- the user explicitly approves advancing to the next stage

### Do not advance if
- hot-search / trend-scan is missing
- recommendation is generic
- title is still undecided
- user preferences are still unresolved enough to distort planning
- the user still has unresolved objections
- user approval to advance is missing

### Rollback condition
Return to discovery if later planning reveals that the chosen topic or title is no longer viable.

---

## 4. Stage 2: Story planning stage

### Goal
Turn the decided topic/title into a strong story concept and usable structural outline.

### Internal sub-steps
1. idea expansion
2. story promise definition
3. structure selection
4. outline creation
5. early chapter direction
6. structured stage report
7. iterative revision with user
8. explicit approval gate

### Required input
- confirmed final title or explicitly approved working title
- usable discovery-stage output

### Forbidden to start if
- discovery stage is incomplete
- title confirmation is incomplete

### Required output
This stage must produce:
- `01_想法.md`
- `02_大纲.md`
- optionally `04_章节骨架.md`
- a planning-stage report for user review

### Completion standard
This stage is complete only if:
- hook, protagonist setup, conflict, and story promise are explicit
- outline contains at least three major turning points
- early chapter direction exists
- escalation path is visible
- the retained direction has passed the deep anti-cliche pre-approval gate
- the deep anti-cliche pass is recorded in `05_定稿结论.md` when that overlay path was activated
- the user explicitly approves the planning result

After planning approval, the parent may initialize derived narrative-intelligence artifacts `05F`–`05I`.

### Do not advance if
- the outline is still summary-only
- major conflict progression is missing
- early chapter direction is absent
- the retained direction has not completed deep anti-cliche review
- the deep anti-cliche pass was activated but no `05_定稿结论.md` records the retained conclusion
- the user has unresolved objections
- user approval to advance is missing

### Rollback condition
Return to planning if character or drafting stages reveal structural weakness.

---

## 5. Stage 3: Character system stage

### Goal
Build a drafting-ready character package.

### Internal sub-steps
1. protagonist definition
2. core cast definition
3. relationship structure
4. motivation/conflict/arc notes
5. file output
6. structured stage report
7. iterative revision with user
8. explicit approval gate

### Required input
- usable outline
- usable story planning output

### Forbidden to start if
- planning stage is incomplete
- protagonist role is still undefined

### Required output
This stage must produce:
- `03_人物小传.md`
- `characters/*.md` for core roles or equivalent usable character package
- a character-stage report for user review

### Completion standard
This stage is complete only if:
- protagonist definition is usable
- major supporting cast is usable
- relationship logic is understandable
- core motivations and conflicts are stated
- the user explicitly approves the character package

### Do not advance if
- protagonist identity is unstable
- supporting cast has no clear function
- relationship logic is too vague for drafting
- the user has unresolved objections
- user approval to advance is missing

### Rollback condition
Return to character system if drafting reveals role collapse or OOC caused by weak foundations.

---

## 6. Stage 4: Drafting stage

### Goal
Produce real draft chapters under explicit user supervision.

Execution mechanism default: parent-orchestrated drafting subagent execution. Stage semantics do not change.
The parent agent validates prerequisites, delegates drafting work to the drafting subagent, then accepts or rejects the returned batch before reporting to the user.
Default parent runtime loop: `prepare_dispatch -> spawn(message=childPrompt) -> record_child_output -> finalize_dispatch`.
The parent still sends only `childPrompt` to the child subagent and keeps dispatch artifacts parent-side.
The drafting subagent must not be dispatched until the chapter-plan package for the target batch exists and is explicitly approved.
Before the first batch of prose drafting, the project must pass the opening gate with an approved `04A_开篇设计.md`.

### Internal sub-steps
1. complete / confirm `01A_风格圣经.md`, `01B_总主线与卷级推进.md`, and the ledger files
2. if this is the first prose batch, complete the opening gate
3. generate or confirm chapter-plan package for the target batch
4. revise the chapter-plan package until explicitly approved
5. draft target chapter batch
6. self-check draft batch
7. structured stage report / batch report
8. iterative revision with user
9. explicit approval gate for next batch or next stage

### Required input
- usable outline
- usable character package
- approved opening gate for the first prose batch
- approved style bible / platform mode / lane decision
- usable mainline spec and ledger files
- drafting scope or target chapter range

### Forbidden to start if
- planning stage is incomplete
- character stage is incomplete
- the first prose batch has not yet passed the opening gate
- the style bible or mainline spec is missing
- the ledger files are missing
- the target batch cannot yet be turned into a usable chapter-plan package
- chapter intent is structurally ambiguous

### Required output
This stage must produce:
- for the first prose batch, an approved `04A_开篇设计.md`
- an approved chapter-plan package for the target batch
- manuscript files for the target chapter range
- prose chapters, not only summaries
- stage report or batch report for user review

### Completion standard
This stage is complete only if:
- the first prose batch passed the opening gate before prose drafting began
- an approved chapter-plan package exists for the intended chapter range
- manuscript files exist for the intended chapter range
- chapters materially move story, tension, or character
- the text is prose, not outline fragments
- the user explicitly approves either the batch continuation or stage completion

### Do not advance if
- the opening gate has not been approved for the first prose batch
- manuscript files are missing
- intended chapter range is incomplete
- output is perfunctory or summary-like
- the user has unresolved objections
- user approval to advance is missing

### Rollback condition
Return to planning or character system if drafting repeatedly breaks due to upstream weakness.

---

## 7. Stage 5: Polishing stage

### Goal
Refine the draft range into a more readable, more human, more emotionally effective version.

Execution mechanism default: parent-orchestrated polishing subagent execution. Stage semantics do not change.
The parent agent validates prerequisites, delegates polishing work to the polishing subagent, then accepts or rejects the returned batch before reporting to the user.
Default parent runtime loop: `prepare_dispatch -> spawn(message=childPrompt) -> record_child_output -> finalize_dispatch`.

### Internal sub-steps
1. polish target range
2. reduce AI texture
3. improve rhythm, clarity, emotional texture, and dialogue quality
4. structured stage report
5. iterative revision with user
6. explicit approval gate

### Required input
- approved draft batch for the target range
- corresponding chapter-plan package for the target range
- usable outline
- usable character package
- style baseline or tone target

### Forbidden to start if
- draft stage approval is missing
- chapter-plan package is missing
- manuscript is still under major structural rewrite
- target range is incomplete

### Required output
This stage must produce:
- polished target range
- a substantive editorial review
- explicit optimization suggestions
- a polishing-stage report for user review

### Completion standard
This stage is complete only if:
- the intended target range is fully polished
- obvious machine texture is materially reduced
- readability is materially improved
- a substantive editorial review exists
- explicit optimization suggestions exist
- the user explicitly approves the polished result

### Do not advance if
- polishing covers only part of the intended range
- the review is vague or empty
- obvious AI texture still dominates
- scene-tone mismatch remains unresolved
- obvious outline/style mismatch remains unresolved
- the user has unresolved objections
- user approval to advance is missing

### Rollback condition
Return to drafting if the text is too structurally weak to rescue via polishing.

---

## 8. Stage 6: Proofreading stage

### Goal
Run consistency, logic, continuity, and OOC checks before final review.

Execution mechanism default: parent-orchestrated proofreading subagent execution. Stage semantics do not change.
The parent agent validates prerequisites, delegates proofreading work to the proofreading subagent, then accepts or rejects the returned report before reporting to the user.
Default parent runtime loop: `prepare_dispatch -> spawn(message=childPrompt) -> record_child_output -> finalize_dispatch`.

### Internal sub-steps
1. continuity check
2. logic check
3. character consistency / OOC check
4. issue summary and fix direction
5. structured stage report
6. iterative revision with user
7. explicit approval gate

### Required input
- polished current batch
- approved chapter-plan package for the current batch
- usable outline
- usable character package
- recap context when relevant

### Forbidden to start if
- no polished manuscript exists for the target range
- major rewrite is still ongoing
- chapter-plan package is missing

### Required output
This stage must produce:
- continuity check result
- logic check result
- OOC / character consistency check result
- issue list or explicit no-blocker statement
- fix direction when issues exist
- a proofreading-stage report for user review

Accepted proofreading also refreshes parent-owned narrative-consistency output before final review:
- refresh `05I_证据链与矛盾对照表.md`
- update `narrativeIntelligence.consistency.*`
- if evidence-backed critical issues remain, stop autopilot with an explicit blocker reason

### Completion standard
This stage is complete only if:
- continuity has been checked
- logic has been checked
- character consistency / OOC has been checked
- blocking issues are either resolved or explicitly recorded
- the report clearly states whether the batch is acceptable, conditionally acceptable, or needs revision
- the user explicitly approves advancement

### Do not advance if
- checks were not actually performed
- blocking contradictions remain unresolved
- severe OOC remains unresolved
- the batch no longer matches the approved chapter plan
- the batch drifts from the outline or intended style in a major way
- the user has unresolved objections
- user approval to advance is missing

### Rollback condition
Return to the earliest upstream stage that can really fix the issue.

---

## 9. Stage 7: Final review and delivery stage

### Goal
Decide whether the project is ready for delivery, then deliver or sync if approved.

Autopilot must not approve this gate. Final review and final delivery remain manual.

### Internal sub-steps
1. final review judgment
2. strengths / weaknesses / blocker assessment
3. delivery readiness decision
4. structured stage report
5. iterative revision with user if needed
6. explicit approval gate
7. local delivery and optional Feishu sync

### Required input
- proofread manuscript
- final project files
- review notes or explicit no-blocker judgment
- parent-side narrative-consistency findings when present

### Forbidden to start if
- proofreading is incomplete
- major blocking issues remain unresolved
- `narrativeIntelligence.consistency.openCriticalIssues` still contains unresolved critical issues unless the user explicitly accepts them as blockers

### Required output
This stage must produce:
- explicit final review decision
- delivery summary
- optional Feishu sync result if requested
- blocker folding from parent-side narrative critical issues when present

### Completion standard
This stage is complete only if:
- final review decision is explicit
- blocking issues are either resolved or explicitly accepted by user override
- the user explicitly approves final delivery
- requested sync is completed if requested

### Do not advance if
- final review avoids judgment
- blocking issues remain unresolved without user override
- the user has not explicitly approved final delivery
- requested sync is incomplete

### Rollback condition
Return to the earliest failing upstream stage indicated by final review.

---

## 10. Workflow mindset

This workflow is designed for **project delivery under explicit user supervision**, not casual one-shot text generation.

Always optimize for:
- clarity
- structure
- continuity
- reusability
- long-form stability
- editable output
- explicit completion gates
- explicit user approval gates
- concise reporting by default

Default communication style during the workflow:
- lead with the conclusion
- keep stage reports compact unless the user asks for detail
- avoid padded explanation, repeated framing, and lecture-style expansion
- expand only when the user explicitly asks for more detail
