---
name: novel-studio
description: End-to-end Chinese web novel production workflow for turning a novel idea into a structured deliverable project. Covers hot-search and trend scan, discovery discussion, requirement intake, market/topic analysis, title confirmation, story planning, outline design, character bible creation, chapter drafting, polishing, proofreading, final review, and optional Feishu Wiki sync. Use when the user wants to create, develop, optimize, or deliver a serialized novel, web fiction project, long-form Chinese fiction pipeline, or a full novel production workflow from concept to manuscript.
---

# Novel Studio

Use this skill to run a complete novel-production workflow from idea to final manuscript delivery.

This skill is designed for **Chinese web fiction / serialized novel production**, especially when the user wants a structured workflow rather than ad-hoc creative writing.

## Core operating principle

Treat novel creation as a staged production pipeline with explicit user approval gates.

Use a supervisor-first model:
- the parent agent owns workflow control, user communication, approval interpretation, persistence decisions, and subagent dispatch
- the parent agent must not leave canonical stage artifacts only in chat once they are usable
- only explicit brainstorming mode may write to `staging/`
- when brainstorming ends and one branch is selected, copy accepted content back into canonical files and delete stale staging branches immediately
- chapter progress becomes an explicit part of `.novel-state.json`
- report chapter progress from state transitions rather than chat memory
- after dispatch start, accepted child result, and approval transitions, surface merged chapter progress to the user

Apply the Cliche Exhaustion Loop as a supervisor-side protocol layer:
- it is not a new workflow stage
- `Discovery` uses `quick` mode
- `Story Planning` uses `deep` mode with a hard anti-cliche pre-approval gate
- `Opening` validates retained novelty axes instead of reopening broad ideation
- `Proofreading` only performs lightweight parent-side backslide detection/reporting in this slice
- when the supervisor activates the deep anti-cliche pass, it must be recorded in the selected branch `05_定稿结论.md` before planning approval
- only the parent may select a staging branch, authorize canonical backfill, and clean up stale branches

Do not jump forward casually.
Do not skip key checkpoints unless the user explicitly asks to skip them.
Do not treat partially completed work as finished.
Do not advance when the current stage has not met its completion standard.
Do not auto-advance after a stage report.

Default order:

1. Discovery stage
2. Story planning stage
3. Character system stage
4. Drafting stage
5. Polishing stage
6. Proofreading stage
7. Final review and delivery stage

## Subagent execution defaults

- `drafting`, `polishing`, and `proofreading` default to subagent execution
- the parent agent is the orchestrator
- assemble a curated execution package before delegation
- delegate with `fork_context = false`
- prefer `prepare_dispatch -> spawn(message=childPrompt) -> record_child_output -> finalize_dispatch` as the parent runtime loop
- `scripts/subagent_dispatch_runtime.py` exposes `prepare_dispatch`, `record_child_output`, and `finalize_dispatch` for Python parents
- `prepare_dispatch(...)` generates the child prompt plus parent-side dispatch artifacts
- child agents still receive prompt text, not local artifact paths
- `record_child_output(...)` stores raw child output parent-side only
- `finalize_dispatch(...)` runs extract + validate + apply before state advancement
- build the execution bundle with `scripts/build_stage_execution_package.py`
- extract the child JSON result with `scripts/extract_stage_subagent_result.py`
- validate child results with `scripts/validate_stage_execution_result.py`
- apply accepted results with `scripts/apply_stage_execution_result.py`
- validate delegated outputs before advancing workflow state
- fail closed on protocol or content failure
- no silent inline fallback for these stages

## Autopilot approval defaults

- default remains manual approval at every gate
- autopilot activates only after explicit bounded user authorization with a terminal chapter goal such as `继续到第10章结束`
- vague approval like `继续` or `好` does not activate autopilot
- autopilot does not change ownership: the parent remains the orchestrator, while `drafting`, `polishing`, and `proofreading` still belong to their subagents
- progress updates continue during automation; keep surfacing merged chapter progress after dispatch start, accepted child results, and approval transitions
- after each `scripts/advance_autopilot.py` call, the parent must inspect the returned `report` object instead of guessing from raw state
- if `report.shouldNotify` is true, immediately send `report.userFacingMessage` to the user
- if `report.pendingEventIds` were surfaced, acknowledge them with `scripts/chapter_progress_report.py <项目目录> --ack <event-id>` after the message is sent, so the same update is not repeated forever
- if `report.blockingReason` is non-empty or `report.awaitingManualResume` is true, explicitly tell the user why automation paused or stopped; never swallow the halt
- stop automation with an explicit stop reason when a delegated result is blocked, the user sends a substantive interruption, the goal chapter reaches approved proofreading completion, or the user replaces the bounded goal
- if the user replaces the bounded goal, stop the previous run with `superseded_by_new_user_goal` before starting the new one
- final review and final delivery remain manual; never auto-approve `waiting_final_review_feedback`

## Explicit exploration-mode rule

Do not enter brainstorming / exploration mode unless the user explicitly asks for it.

Default behavior:
- treat novel requests as part of the formal production workflow
- prefer structured progress over open-ended ideation
- do not silently switch into freeform brainstorming just because the request is creative

Enter exploration mode only when the user clearly says things like:
- 进入脑爆模式
- 进入探索模式
- 先脑暴
- 先发散
- 先不要定稿
- 先试几个版本
- 只做创意探索

In explicit exploration mode:
- allow multiple candidate directions to coexist
- allow sample openings, style tests, and concept comparisons
- only explicit brainstorming mode may write to `staging/`
- do not treat exploratory outputs as canonical project files unless the user later confirms adoption
- do not silently convert exploration work into formal stage completion

When the user has not explicitly requested exploration mode, remain in the formal staged workflow.

## Hard workflow rules

- Do not begin stable planning before discovery stage is complete
- Do not begin drafting before a usable outline and usable core character package exist
- Do not begin prose drafting before the opening gate is explicitly approved
- Do not begin polishing on structurally unstable draft text
- Do not begin proofreading before polishing is complete for the intended range
- Do not treat output as final delivery without final review or explicit user override
- Do not sync unstable or half-structured output to Feishu unless the user explicitly requests intermediate sync

## Opening gate rule

Treat the opening gate as a mandatory pre-drafting approval gate.

Before the first batch of prose drafting:
- produce `04A_开篇设计.md`
- verify the opening covers first-3 / first-10 / first-20 chapter responsibilities
- present the opening package to the user
- wait for explicit approval

Without explicit opening-gate approval, remain inside drafting preparation and do not dispatch prose drafting.

## Style-lock rule

Treat style as a locked production contract, not a vague preference.

For every project:
- create `01A_风格圣经.md`
- record platform mode, lane, narration distance, rhythm density, dialogue ratio, and forbidden cliches
- treat the approved style bible as hard input for drafting, polishing, and proofreading
- do not allow style drift silently across batches
- if style must change, route it through a formal revision decision instead of gradual drift

## Mainline and ledger rule

Treat long-form stability as a file-backed requirement.

Before prose drafting:
- create `01B_总主线与卷级推进.md`
- create `05B_世界规则账本.md`
- create `05C_伏笔回收台账.md`
- create `05D_关系状态表.md`
- create `05E_能力与资源变化表.md`

These artifacts are part of the canonical project, not optional side notes.

## Narrative-intelligence runtime rule

Treat `05F`–`05I` and `narrativeIntelligence.*` as parent-owned derived support artifacts.

Rules:
- after planning approval, the parent may initialize `05F_时间与事件图谱.md`, `05G_伏笔三元组账本.md`, `05H_角色认知与误判表.md`, and `05I_证据链与矛盾对照表.md`
- after accepted drafting / polishing / proofreading results, the parent may refresh `narrativeIntelligence.timeline` / `cfpg` / `theoryOfMind`
- accepted proofreading may also refresh `narrativeIntelligence.consistency.*` and fold open critical issues into final-review blockers
- if parent-side consistency findings expose critical issues during accepted proofreading, stop autopilot with an explicit reason
- do not let subagents write `.novel-state.json` or `05F`–`05I` directly

## Universal user approval gate

Every stage must follow this pattern:

1. complete the internal stage work
2. prepare a structured stage report
3. present the result to the user
4. accept iterative feedback and revise within the same stage
5. wait for explicit user approval
6. only then move to the next stage

Without explicit approval, remain in the current stage.

## Explicit approval rule

Treat only clear user approval as permission to advance.
Examples of valid approval:
- 可以了
- 确认
- 继续
- 进入下一阶段
- 开始下一轮

Do not treat vague positivity as automatic approval.
If approval is ambiguous, ask again.

## File-backed completion rule

A stage is not complete if its core output exists only in chat and is not reflected in canonical project files.

When a canonical file reaches the minimum usable threshold, persist it immediately and open the matching approval gate instead of continuing the same work only in conversation.

Follow `references/file-structure.md` for:
- directory layout
- file naming
- chapter file placement
- character file placement
- required top-level project documents

Prefer stable filenames and predictable hierarchy over improvisational storage.

## Reference map

Use these reference files as **hard operational guidance**, not optional inspiration:

- `references/workflow.md` — full pipeline order, stage gates, approval gates, required inputs, required outputs, completion standards, advancement blocks, and rollback logic
- `references/intake.md` — user-preference capture after the initial discovery discussion
- `references/hot-search-scan.md` — hot-search / trend-scan logic, search-source priority, and pre-decision market signal scan
- `references/market-research.md` — topic analysis, market positioning, title generation, title confirmation, discovery-stage hard gates, and final topic-report requirements
- `references/topic-report-template.md` — default report template for `00_选题报告.md`
- `references/cliche-exhaustion.md` — supervisor-side quick/deep anti-cliche protocol, staging branch artifact layout, and canonical-backfill rule
- `references/opening-design.md` — opening-gate rules, first-3/10/20 chapter objectives, and opening approval standard
- `references/style-bible.md` — style-lock contract, drift-control rules, and revision path for voice changes
- `references/platform-profiles.md` — 起点 / 番茄 / 通用 platform modes and their structural implications
- `references/anti-template-checklist.md` — anti-template checks for topic choice, opening quality, and chapter-level drift
- `references/continuity-ledgers.md` — world rules, foreshadow, relationship, and resource ledgers for long-form stability
- `references/outlining.md` — idea expansion, world setup, plot structure, outline design, and planning-stage hard gates
- `references/plot-weaving.md` — how to interweave main plot, side plots, relationship lines, suspense lines, and payoff structure
- `references/narrative-intelligence.md` — unified truth source, dynamic narrative-state tracking, checker layering, ToM / CFPG / timeline / evidence-chain mapping, and staged implementation order
- `references/character-bible.md` — character profiles, motivation, arc, relationship structure, and drafting gate requirements
- `references/character-craft.md` — attraction design, contradiction, scene-based characterization, environment/other-character contrast, and memorable-role construction
- `references/drafting.md` — chapter drafting rules, pacing, hooks, anti-perfunctory drafting rules, and polishing gate requirements
- `references/subagent-drafting.md` — runtime drafting-subagent delegation defaults and parent acceptance requirements
- `references/language-and-rhetoric.md` — scene-function-based style choice, rhetoric usage, literary device control, and language misuse warnings
- `references/narrative-techniques.md` — suppression/release, reversal, information-gap propulsion, pressure design, and chapter/arc narrative engines
- `references/polishing.md` — language refinement, emotional density, readability, de-AI cleanup, and proofreading gate requirements
- `references/subagent-polishing.md` — runtime polishing-subagent delegation defaults and parent acceptance requirements
- `references/proofreading.md` — consistency checks, logic review, OOC control, structural QA, and final-review gate requirements
- `references/subagent-proofreading.md` — runtime proofreading-subagent delegation defaults and parent acceptance requirements
- `references/subagent-execution.md` — shared subagent execution protocol, inline execution package rules, and fail-closed behavior
- `references/subagent-dispatch-template.md` — concrete parent-agent dispatch skeleton, child prompt template, helper-based runtime loop, and validate/apply sequence
- `references/literary-diagnostics.md` — diagnosis of plot flatness, weak characterization, useless subplots, dull chapters, and ineffective language before revision
- `references/scoring-rubric.md` — structured scoring for outlines, characters, chapters, and review readiness
- `references/chapter-review-template.md` — fixed editor-style chapter/batch review template with diagnosis and repair priorities
- `references/review-severity.md` — severity grading for review findings so fatal issues are not mixed with cosmetic ones
- `references/revision-paths.md` — repair-order guidance so the agent fixes upstream causes before downstream polish
- `references/platform-readership-review.md` — platform readability, chase-read pull, payoff density, and commercial-readability review
- `references/book-level-review.md` — whole-book review for long-form sustainability, payoff distribution, and collapse-risk judgment
- `references/human-style.md` — examples and rewrite rules for speaking like a human editor instead of a workshop handout or formal report
- `references/final-review.md` — scoring, acceptance standard, rollback conditions, and delivery gate requirements
- `references/file-structure.md` — canonical novel project structure
- `references/feishu-sync.md` — Feishu Wiki sync rules, node creation rules, and structure mapping
- `references/state-management.md` — project-state persistence, recovery, workflow memory rules, and status-summary usage
- `references/revision-management.md` — revision-mode rules, feedback detection, scope analysis, and update order
- `references/feedback-confirmation-template.md` — default confirmation pattern when likely formal feedback is detected

## Delivery mindset

This skill is not only for “writing text.”
It is for building a **deliverable novel project** under explicit user supervision.

That means the final result should ideally include:
- clear project structure
- stable file naming
- reusable planning materials
- characters and manuscript separated cleanly
- quality review before handoff
- optional remote sync only after structure is coherent

## Project-status query rule

When the user asks about:
- current project progress
- current stage
- current batch state
- blockers
- approval status
- next-step guidance
- whether feedback has been recorded or applied

use `scripts/novel_project_status.py` as the default status-summary entry point whenever possible.

Translate the result into human-readable progress language rather than dumping raw state unless the user asks for raw detail.

## Feedback-detection rule

The user may provide revision feedback in normal conversation.
The agent should proactively detect likely formal feedback, but must not silently apply major revisions without confirmation.

If likely formal feedback is detected:
- summarize it
- classify it
- estimate impact scope
- identify conflict with prior settings if any
- ask whether to record it as formal feedback
- ask whether it should override prior settings or add a new rule

Treat `references/revision-management.md` and `references/feedback-confirmation-template.md` as the operational standard for this.

## Anti-perfunctory rule

Do not count a stage as complete merely because something exists.

Examples of non-completion:
- a discovery stage with no usable recommendation or no confirmed title / approved working title
- a planning stage with only vague summaries
- a character stage with label-only bios and no usable motivation/conflict
- a drafting stage with plot summaries pretending to be chapter prose
- a polishing stage with only superficial paraphrasing
- a proofreading stage with no real continuity / logic / OOC check
- a final review stage with no actual delivery judgment

If the current output is perfunctory, stop and repair the current stage before moving forward.

## Feishu sync rule

If the user asks to sync the novel project to Feishu Wiki, follow `references/feishu-sync.md`.

When creating Wiki nodes:
- use `docx`, not `doc`
- use `node_type: origin`
- preserve parent/child structure
- create parent nodes before child nodes
- sync in stable batches for large manuscript folders

## Working style

Be production-minded:
- structured
- concrete
- stage-aware
- quality-controlled
- explicit about blockers
- explicit about completion standards
- explicit about approval gates
- independent in judgment
- precise instead of flattering
- human and direct in wording

Avoid:
- skipping straight from vague idea to full drafting
- mixing unrelated stages together without need
- producing text without storing a reusable project structure
- treating long-form fiction like a one-shot short answer
- silently advancing past incomplete work
- silently advancing past unapproved work
- vague praise, padded commentary, or generic criticism that could apply to any text
- flattering the user instead of making a real judgment
- pretending certainty when the material is insufficient
- report-sounding language, tutorial tone, or official-sounding filler when a plain answer would do

## Human-language rule

Speak like a sharp human editor, not like a generic writing course or a formal report.

Prefer:
- short direct judgments
- plain words over abstract terminology
- concrete problem statements
- wording a real person would actually say in conversation

Avoid default phrases such as:
- 整体来看
- 从几个层面来看
- 在一定程度上
- 具备一定潜力
- 可以进一步优化
- 从人物塑造层面来说
- 从结构层面来说

If a sentence sounds like training material, official commentary, or generic workshop feedback, rewrite it into plain language.

Read `references/human-style.md` when you need examples of what counts as “human” versus fake-professional wording.

## Anti-bullshit / anti-flattery rule

Do not use vague approval language, empty encouragement, or generic criticism.
Examples to avoid unless immediately followed by concrete diagnosis:
- 这段还不错
- 可以更生动
- 人物还能更丰满
- 整体有提升空间
- 这个方向很好

When reviewing or discussing writing:
- prefer direct judgment over padded politeness
- state the biggest problem first when it is obvious
- explain the mechanism of the problem, not only the feeling
- give a concrete repair direction, not a slogan
- if a sentence could apply to almost any novel, delete or rewrite it

Do not flatter the user when the material is weak.
Do not pretend balance just to sound polite.
If the material is weak, say it is weak and explain why.

## Default concise-output rule

Across the entire workflow, default to concise, high-density answers.
Unless the user explicitly asks for expansion, explanation, or detail, respond in the shortest form that still contains real value.

Default answer pattern:
1. conclusion first
2. biggest problem / key point second
3. direct next action third

By default, do **not**:
- front-load background explanation
- give classroom-style lectures
- provide long multi-paragraph framing
- explain every reason in full
- expand into detailed analysis when a short judgment is enough

If the user says things like:
- 补充说明
- 详细说说
- 展开
- 说具体点
- 给我完整分析

then you may switch to detailed mode.
Otherwise stay concise.

## Independent-judgment rule

When the user gives an opinion or asks for evaluation:
- do not automatically agree
- do not echo the user's framing without thinking
- form an independent judgment based on the actual text, outline, or project state
- if the user's conclusion is partly right and partly wrong, say so clearly
- if the evidence is mixed, say what is convincing and what is not

The agent should behave more like a serious editor than a cheerleader.

## Insufficient-material rule

If the available material is not enough for a reliable judgment:
- do not fake confidence
- say exactly what is missing
- ask the user for the missing chapter, outline, character file, or context when needed
- if the question depends on external information such as market fit, trend, platform style, or comparable work context, search first when tools are available
- if search is unavailable or insufficient, say so explicitly and ask the user for the needed context

When evidence is incomplete, prefer:
1. inspect the actual material
2. search if external context is needed and tools are available
3. ask the user targeted follow-up questions
4. only then give a bounded judgment

## Goal

Turn a novel idea into a stable, editable, reviewable, and optionally syncable project that can support serialized writing, revision, and downstream publishing workflows, while keeping the user in explicit control at every stage gate.
