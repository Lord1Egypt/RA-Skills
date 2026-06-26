# Drafting

## 1. Goal

Use a reciprocal batch-writing workflow instead of one-pass full-manuscript generation.

Exploration-style draft experiments are not the default behavior.
Only switch to exploratory drafting when the user explicitly asks for brainstorming / exploration behavior such as:
- 进入脑爆模式
- 进入探索模式
- 先脑暴
- 先发散
- 先不要定稿
- 先试几个版本
- 只做创意探索

Without that explicit request:
- treat drafting as formal production work
- require confirmed batch scope and approved chapter-plan package
- do not silently convert drafting into freeform experimentation

Do not start batch drafting until the opening gate has been explicitly approved.

Drafting should proceed in controlled loops:
1. if this is the first prose batch, complete and approve the opening gate
2. confirm batch scope with the user
3. produce a chapter-plan package
4. revise that package with the user until explicitly approved
5. write the draft chapters
6. hand the batch to polishing and review
7. complete consistency review and batch final pass
8. update recap memory
9. ask whether to continue

Default execution mechanism: drafting uses a drafting subagent. The parent agent remains the orchestrator.
The parent agent must verify preconditions before delegation, dispatch with `fork_context = false`, and accept or reject the returned drafting package before reporting stage progress.
Preferred parent runtime loop: `prepare_dispatch -> spawn(message=childPrompt) -> record_child_output -> finalize_dispatch`.
Use `scripts/subagent_dispatch_runtime.py` when the parent is coordinating drafting in Python.
Execution mechanism changes do not change drafting-stage semantics.

Do not default to writing the whole manuscript in one pass.

---

## 2. Supporting craft references

When drafting, also use these references as needed:
- read `language-and-rhetoric.md` when adjusting language intensity, scene texture, rhetorical density, and genre-appropriate prose style
- read `narrative-techniques.md` when a scene or chapter needs stronger payoff shape, suppression/release, reversal, information-gap propulsion, or ending pull
- read `character-craft.md` when a scene feels technically correct but the characters still feel generic, flat, or interchangeable
- read `chapter-review-template.md` when reviewing a chapter or batch before handoff and you need a fixed diagnosis structure instead of vague impressions

## 3. Required input

You must have:
- usable outline
- usable character bible
- approved `01A_风格圣经.md`
- approved `01B_总主线与卷级推进.md`
- approved `04A_开篇设计.md` before the first prose batch
- approved lane / platform decision
- usable ledger files for world rules, foreshadow, relationships, and resources
- current recap context if previous batches already exist

---

## 4. Forbidden to start if

Do not start drafting if:
- outline stage is incomplete
- character stage is incomplete
- the opening gate is not yet approved for the first prose batch
- the style bible is missing
- the mainline spec is missing
- the ledger files are missing
- chapter intent is structurally ambiguous
- the current batch scope is not explicitly confirmed by the user

The parent agent must not delegate drafting until all start conditions are satisfied.

---

## 5. Reciprocal batch-writing workflow

### Step 4.1 Batch scope confirmation
Before writing anything, confirm with the user:
- how many chapters this batch should include
- what chapter range this batch covers

Do not proceed without explicit user confirmation of batch scope.

### Step 4.2 Chapter-plan package generation
After batch scope is confirmed, generate a chapter-plan package based on:
- outline
- recap / previous-story context
- theme
- style
- character files

For each chapter in the batch, explicitly define:
- what content this chapter must complete
- which characters appear
- where the climax or local high point is
- what the attractive point / hook is

This chapter-plan package is required before draft writing.

### Step 4.3 Chapter-plan review loop
Present the chapter-plan package to the user.
Revise it through multiple rounds until the user explicitly approves it.

Do not begin draft prose until the chapter-plan package is explicitly approved.

### Step 4.4 Draft writing
Only after chapter-plan approval:
- write the actual draft prose for each chapter in the batch
- save it into canonical manuscript files
- overwrite an existing target manuscript file only when the parent has explicitly granted overwrite permission for that dispatch
- otherwise fail closed instead of rewriting an existing manuscript file or creating ad-hoc duplicate variants

### Step 4.5 Batch handoff
After draft writing, the batch must move into polishing and substantive review before it can be considered complete.

### Step 4.6 End-of-batch decision
After the batch is fully processed and approved, ask the user whether to continue the next batch.

Do not silently continue into the next batch.

---

## 6. Required output

This stage must produce:
- for the first prose batch, an approved `04A_开篇设计.md`
- a chapter-plan package for the current batch
- manuscript files for the approved chapter range
- a batch report for user review

Recommended explicit artifact for planning the batch:
- `05_本轮章节规划.md` or equivalent batch-planning record

Main manuscript artifact:
- `manuscript/*.md`

The drafting subagent should modify only the target manuscript files for the approved chapter range.
Do not modify planning, recap, review, or state artifacts during drafting execution.

---

## 7. Completion standard

A drafting batch is complete only if:
- the first prose batch passed the opening gate before prose writing
- the user explicitly confirmed the batch chapter count / range
- the chapter-plan package exists
- the chapter-plan package was explicitly approved by the user
- manuscript files exist for the approved chapter range
- the text is prose, not outline fragments or summaries
- each chapter materially advances story, character, or tension
- the batch has been handed forward for polishing/review

---

## 8. Do not advance if

Do not advance into polishing or the next batch if:
- the batch scope was never explicitly confirmed
- the chapter-plan package does not exist
- the chapter-plan package has not been explicitly approved
- manuscript files are missing
- intended chapter range is incomplete
- output is perfunctory or summary-like
- the user has unresolved objections
- user approval for the current batch is missing

---

## 9. Hard anti-perfunctory rule

The following do **not** count as completed drafting:
- bullet summaries pretending to be chapter text
- scene placeholders without real scene writing
- vague narrative bridges replacing actual events
- repetitive filler chapters with no meaningful progression
- prose that merely restates the outline at slightly greater length
- chapter-plan notes presented as if they were the actual draft
- chapters where things happen but nothing meaningfully changes in pressure, relationship, knowledge, or emotional state
- chapters that only transport the cast from one later event to another without scene-level dramatic value

---

## 10. Hook and chapter-plan requirements

For each chapter in the batch, the planning package must state:
- chapter objective
- appearing characters
- local climax or tension peak
- attractive point / reader hook

Do not allow vague chapter planning such as:
- “推动剧情发展”
- “角色互动一下”
- “埋点伏笔”

These are insufficient on their own.

---

## 11. Rollback condition

Return to chapter-plan generation or chapter-plan review if:
- the user says the planned chapter direction is wrong
- the batch does not match desired tone, rhythm, or attraction points
- the draft repeatedly breaks because the chapter plan is too vague

Return to planning or character system if:
- batch-level writing exposes upstream structural weakness
- scene writing repeatedly breaks due to missing plot logic or role logic

---

## 12. End-of-batch recap rule

After a batch fully completes downstream review, update the project recap document so later batches can restore continuity quickly.

Do not rely only on short-term chat context for ongoing long-form drafting.

---

## 13. Quality bar

A valid drafting batch is:
- batch-scoped
- pre-planned
- explicitly approved before prose writing
- written as real prose
- structured enough for polishing and review

Invalid drafting includes:
- one-pass uncontrolled long generation
- no chapter-plan package
- no user approval before writing
- plot summaries pretending to be scenes
- filler masked as atmosphere
- silent batch continuation without user approval
