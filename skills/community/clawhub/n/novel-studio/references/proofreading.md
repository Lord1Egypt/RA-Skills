# Proofreading

## 1. Goal

Run consistency, logic, continuity, and OOC checks on the current approved batch before batch-level final pass.

Proofreading in this workflow is batch-scoped and should help determine whether the current batch is ready to be accepted, revised again, or rolled back.
Within the Cliche Exhaustion Loop, lightweight backslide detection is parent-side only in this slice.

Default execution mechanism: proofreading uses a bounded proofreading subagent. The parent agent remains the orchestrator.
The parent agent must verify preconditions before delegation, dispatch with `fork_context = false`, and accept or reject the returned proofreading report before reporting stage progress.
Preferred parent runtime loop: `prepare_dispatch -> spawn(message=childPrompt) -> record_child_output -> finalize_dispatch`.
The child still receives prompt text only; proofreading dispatch artifacts stay parent-side.
The only canonical file proofreading may write is `05A_本轮校对报告.md`.
Execution mechanism changes do not change proofreading-stage semantics.
The child proofreading bundle/result contract does not change because of this slice.

Accepted proofreading has a parent-side post-processing hook:
- refresh `narrativeIntelligence.timeline` / `cfpg` / `theoryOfMind`
- refresh `05I_证据链与矛盾对照表.md` plus `narrativeIntelligence.consistency.*`
- accepted proofreading may trigger a parent-side style-risk refresh
- this slice only does deterministic duplicate checks for `05_本轮章节规划.md` attraction points and climax targets, storing them in `narrativeIntelligence.styleRisk.clichePatterns`
- always record `narrativeIntelligence.styleRisk.lastClicheScanStage = "proofreading"` during that parent-side refresh, even when no duplicates are found
- cliche findings alone do not stop autopilot, add a new approval gate, change the child proofreading contract, or become final-review blockers in this slice
- if evidence-backed critical issues remain, stop autopilot with an explicit blocker reason
- do not silently rewrite the child report; checker output is parent-owned derived state

---

## 2. Supporting diagnostic references

When proofreading, also use these references as needed:
- read `literary-diagnostics.md` when a batch feels flat, scattered, emotionally weak, rhetorically off, or structurally dull but the exact cause is unclear
- read `plot-weaving.md` when reviewing whether side plots actually feed back into consequence
- read `character-craft.md` when checking whether core roles are attractive, differentiated, and scene-effective rather than label-based
- read `scoring-rubric.md` when the user wants a quality score, pass/fail judgment, readiness judgment, or a more structured evaluation basis
- read `chapter-review-template.md` when you need to present chapter-level or batch-level review comments in a fixed editorial format
- read `review-severity.md` when you need to classify which issues are fatal, major, secondary, or cosmetic
- read `revision-paths.md` when the review must also tell the user what to fix first and what not to waste time fixing yet
- read `platform-readership-review.md` when the user wants evaluation of opening capture, chase-read pull, payoff density, commercial readability, or platform fit
- read `book-level-review.md` when the user asks for long-form health, whole-book risk, collapse-point judgment, or serialization sustainability review

## 3. Required input

You must have:
- a polished current batch
- the approved chapter-plan package for that batch
- usable outline
- usable character package
- recap context from earlier batches if relevant

---

## 4. Forbidden to start if

Do not start proofreading if:
- polishing is incomplete
- the current batch is still under major rewrite
- the chapter-plan package is missing
- the current batch range is incomplete

---

## 5. Required output

Proofreading must produce:
- continuity check result
- logic check result
- OOC / character consistency check result
- issue list or explicit no-blocker statement
- fix direction when issues exist
- `05A_本轮校对报告.md`
- a proofreading-stage report for user review

The parent may additionally refresh `05I_证据链与矛盾对照表.md` after accepted proofreading. That checker artifact does not replace `05A_本轮校对报告.md`; it supplements it.

Default proofreading output should stay compact unless the user asks for detail:
- conclusion first
- top issues second
- fix order third

Proofreading is diagnostic. Do not do silent fixing during proofreading.

---

## 6. Required check dimensions

At minimum, check:
- continuity within the current batch
- continuity against prior recap context where relevant
- plot logic
- character consistency / OOC risk
- alignment with approved chapter plan
- alignment with outline
- alignment with style tone where relevant
- whether important side plots or relationship lines produce actual consequence rather than decorative presence
- whether core characters remain attractive, differentiated, and scene-effective rather than collapsing into interchangeable delivery tools
- whether each chapter has visible dramatic movement rather than only transport or exposition
- whether the batch has slid back toward previously enumerated cliché samples or dropped retained novelty axes

---

## 7. Completion standard

Proofreading is complete only if:
- the current batch has been checked across all required dimensions
- blocking issues are either resolved or explicitly recorded
- the report clearly states whether the batch is acceptable, conditionally acceptable, or needs revision
- the user has reviewed the proofreading result
- the user explicitly approves advancement or requests another revision cycle

---

## 8. Do not advance if

Do not advance to batch final pass or next-batch decision if:
- continuity checks were not actually performed
- blocking contradictions remain unresolved
- severe OOC remains unresolved
- the batch no longer matches the approved chapter plan
- the batch drifts from the outline or intended style in a major way
- the user has unresolved objections
- user approval to advance is missing

---

## 9. Hard anti-perfunctory rule

The following do **not** count as completed proofreading:
- “整体没问题” with no actual checks recorded
- surface wording comments only
- vague statements that avoid naming inconsistencies
- checking only one dimension while ignoring logic, continuity, or OOC risk
- saying the batch is fine without comparing it against the approved chapter plan
- agreeing with the user's complaint or self-assessment without independently checking the material
- using empty praise or empty criticism instead of concrete diagnosis

---

## 10. Multi-round revision rule

Treat proofreading as another user-reviewed loop.

If issues remain:
- send the batch back to the appropriate stage
- revise
- re-check
- present updated results
- wait for explicit user approval

Do not auto-advance after one proofreading pass.

---

## 11. Batch final-pass role

When proofreading is accepted, this stage serves as the batch-level consistency and quality gate before:
- updating `05_前情回顾.md`
- asking whether to continue the next batch

This means proofreading is not only error checking. It is the final gate for the current batch before continuation.

The batch is not fully closed until the recap document has been updated.

---

## 12. Rollback condition

Return to polishing if:
- prose quality or tone alignment is still the main problem

Return to drafting if:
- chapter-plan execution is wrong
- continuity breaks are caused by incorrect or missing scene content
- the batch fails because core draft content is off-target

Return to planning or character system if:
- the batch exposes deeper structural or role-definition problems

---

## 13. Quality bar

A valid proofreading result is:
- specific
- batch-aware
- continuity-aware
- aligned with approved chapter intent
- explicit about whether the batch can pass
- if the judgment is acceptable, the report uses an explicit no-blocker conclusion instead of a hidden issue list
- if the judgment is conditionally acceptable, the report records caveats through risks and fix direction rather than blocker entries
- phrased in plain human language rather than generic workshop jargon

Invalid proofreading includes:
- only checking surface wording
- ignoring structural contradictions
- declaring success without actual consistency review
- moving forward without explicit user approval
- hiding the real point behind padded professional-sounding language
