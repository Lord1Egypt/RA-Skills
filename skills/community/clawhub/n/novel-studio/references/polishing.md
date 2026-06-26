# Polishing

## 1. Goal

Refine the approved draft batch into cleaner, stronger, more emotionally effective prose, then produce a substantive editorial review.

Polishing in this workflow is not only line cleanup.
It must include:
- language refinement
- AI-texture reduction
- substantive evaluation
- concrete optimization advice
- user review loop

Default execution mechanism: polishing uses a polishing subagent. The parent agent remains the orchestrator.
The parent agent must verify preconditions before delegation, dispatch with `fork_context = false`, require an explicit `polishingFocus`, and accept or reject the returned polishing package before reporting stage progress.
Preferred parent runtime loop: `prepare_dispatch -> spawn(message=childPrompt) -> record_child_output -> finalize_dispatch`.
Use `scripts/subagent_dispatch_runtime.py` when the parent is coordinating polishing in Python.
Execution mechanism changes do not change polishing-stage semantics.

---

## 2. Required input

You must have:
- an approved draft batch
- the corresponding chapter-plan package
- usable outline
- usable character package
- style baseline or tone target

---

## 3. Forbidden to start if

Do not start polishing if:
- the current batch was not explicitly approved at draft stage
- the chapter-plan package is missing
- the draft is still structurally unstable
- the intended chapter range is incomplete

---

## 4. Required output

This stage must produce:
- a polished version of the current batch
- a substantive editorial review
- explicit optimization suggestions
- a polishing-stage report for user review

---

## 5. What polishing must do

At minimum, polishing must:
- check and correct obvious typos when present
- improve awkward sentences
- reduce visible AI-style tone where possible
- improve readability and rhythm
- preserve intended tone and character voice
- preserve compliance with the approved chapter plan

---

## 6. Mandatory substantive review

After polishing, provide a substantive editorial review.

This review must explicitly evaluate:
- whether scenes match the intended tone
- whether the story remains coherent
- whether the chapter batch still matches the outline
- whether the writing still matches the intended style baseline
- whether the attractive points / hooks are actually landing

This review must also provide concrete optimization suggestions.

---

## 7. Hard anti-empty-review rule

The following do **not** count as a valid review:
- “整体不错”
- “情节还可以”
- “文风统一”
- vague praise without evidence
- generic AI-style filler commentary

The review must be substantive, specific, and useful.

---

## 8. Completion standard

This stage is complete only if:
- the full target batch has been polished
- a substantive editorial review exists
- optimization suggestions exist
- the user has reviewed the polishing result
- the user explicitly approves advancement or requests further revision

---

## 9. Do not advance if

Do not advance if:
- only partial polishing has been done
- the review is vague or empty
- AI texture still strongly dominates and has not been acknowledged
- scene-tone mismatch remains unresolved
- obvious outline/style mismatch remains unresolved
- the user has unresolved objections
- user approval to advance is missing

---

## 10. Multi-round revision rule

Treat polishing as a user-reviewed revision loop.

If the user gives feedback:
- stay in polishing
- revise the current batch again
- present the updated result
- wait for explicit approval

Do not move into proofreading merely because one polishing pass has been completed.

---

## 11. Rollback condition

Return to drafting if:
- the chapter-plan execution itself is wrong
- the scene structure is too weak to be fixed at polish level
- the polished batch still fails because the underlying draft content is off-target

---

## 12. Quality bar

A valid polishing result is:
- cleaner
- more human
- more readable
- still aligned with outline, tone, and approved plan
- accompanied by a substantive review

Invalid polishing includes:
- surface-level paraphrasing only
- no real editorial judgment
- no optimization guidance
- empty praise
- moving forward without explicit user approval
