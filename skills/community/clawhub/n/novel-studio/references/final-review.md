# Final Review

## 1. Goal

Decide whether the project is ready for final delivery.

Final review is the acceptance gate.
Its job is to judge whether the current project version is deliverable.

---

## 2. Required input

You must have:
- proofread manuscript
- final project files
- review notes or explicit no-blocker judgment
- user quality priorities if they were specified
- parent-side narrative-consistency findings when present

---

## 3. Forbidden to start if

Do not start final review if:
- proofreading is incomplete
- major blocking issues are still unresolved
- the manuscript is still under major rewrite
- the project file structure is incomplete for the intended delivery scope
- `narrativeIntelligence.consistency.openCriticalIssues` still contains unresolved critical issues and the user has not accepted them as blockers

---

## 4. Required review dimensions

Evaluate at least:
- plot coherence
- readability
- style consistency
- emotional effectiveness
- pacing control
- character integrity
- de-AI quality
- delivery readiness

Optional if relevant:
- adaptation potential
- serial continuation potential
- platform fit

---

## 5. Required output

Final review must produce:
- `07_终审报告.md`
- an explicit decision: `pass` / `conditional pass` / `rework required`
- top strengths
- major weaknesses
- whether blocking issues remain
- delivery readiness judgment
- a concise summary explaining the final judgment

When parent-side narrative critical issues exist, merge them into the blocker set rather than ignoring them.

The report must include these fixed sections:
- `## 最终结论`
- `## 是否可交付`
- `## 主要优点`
- `## 主要问题`
- `## 阻塞问题`
- `## 建议动作`

Inside `## 最终结论`, the decision value must be exactly one of:
- `pass`
- `conditional pass`
- `rework required`

Inside `## 是否可交付`, use an explicit boolean:
- `true`
- `false`

---

## 6. Completion standard

Final review is complete only if:
- the decision is explicit
- blocking issues are either resolved or clearly named
- the judgment explains why the work passes or fails
- the project is assessed against the user’s actual standard, not vague perfectionism
- narrative critical issues are either resolved, merged into blockers, or explicitly accepted by user override

---

## 7. Do not advance if

Do not treat the work as final delivery if:
- final review has not happened
- the review avoids judgment
- blocking issues remain unresolved
- core files are still missing
- the current quality clearly fails the user’s stated goal

---

## 8. Hard delivery rule

Do not present the project as complete final delivery without:
- final review
- or explicit user override accepting current state as-is

If the user accepts current quality despite known flaws, record that explicitly.

---

## 9. Rework triggers

Common reasons for rework:
- major unresolved logic failure
- clear OOC drift
- broken pacing across important sections
- obvious AI texture still dominating
- emotional weak spots in critical scenes
- project structure incomplete or disorderly

---

## 10. Rollback condition

Return to the earliest stage that can actually fix the issue.
Examples:
- structural weakness -> outline
- role collapse -> character bible or drafting
- weak prose / machine texture -> polishing
- continuity failure -> proofreading or upstream stage depending on cause

Do not hide upstream failure inside a superficial final-review patch.

---

## 11. Quality bar

Good final review:
- is decisive
- is readable
- is evidence-based
- distinguishes fatal issues from polish issues
- protects delivery standards without perfection paralysis

Bad final review:
- is vague
- avoids judgment
- overreacts to minor flaws
- ignores major weaknesses
