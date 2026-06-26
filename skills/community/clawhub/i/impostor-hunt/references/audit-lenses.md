# Audit Lenses

Lenses are split into **main-line** (must run, feed the verdict) and **side-line** (run if budget allows, feed the side section only).

Each lens has three questions. The questions are deliberately not exhaustive; they are anchors.

---

## Main-line lenses (must run)

### L1 — Purpose Alignment

Is the artifact serving the user's real purpose, or only completing the literal task?

- What is the user-side outcome that *would* fail if this artifact is wrong?
- Does the artifact's output mechanism actually drive that outcome?
- If the artifact stayed exactly as is and the user used it for a year, would the purpose be served?

### L2 — Causal Authenticity

Is the result produced by the logic that the purpose requires, or by a cheaper substitute?

- What causal chain does the surface output suggest?
- What causal chain is actually in the code/data/process?
- If the two differ, which patterns from `causal-impersonation-patterns.md` apply?

### L3 — Validation Integrity

Could the validation in place actually reject a wrong implementation?

- If the implementation silently returned a plausible wrong answer, would any test/check fail?
- Are the validation inputs independent of the implementation?
- Are negative cases covered?

### L4 — Complexity Preservation

Was a hard problem quietly replaced with an easier one?

- Which dimensions of the user's problem (scale, dynamics, adversariality, distribution shift) are absent in the artifact?
- Was the simplification documented and accepted, or invisible?
- Does the artifact still claim to solve the original problem after the simplification?

---

## Side-line lenses (run if budget allows; feed side section only)

### L5 — Entity Reality

Are the fields, endpoints, files, configs, roles, metrics, rules referenced actually real?

### L6 — Semantic Consistency

For identically named things across modules, is the meaning the same?

### L7 — Constraint Closure

Do user/business/technical constraints propagate from requirements through implementation, validation, and runtime?

### L8 — Path Completeness

Beyond happy path: failures, boundaries, exceptions, long-term use.

### L9 — User Consequence

If the user believes the completion claim and acts on it, where is harm most likely?

### L10 — Claim Truth

Are the literal claims true on their own terms? (Note: this is shallower than L2 — L2 asks whether the *mechanism* is the right one even when the claim is literally true.)

---

## Allocation rule

If audit budget is **shallow**: run L1–L4 only. Side section may be empty.
If **standard**: L1–L4 plus 2–3 side lenses chosen by relevance.
If **deep**: all ten lenses.

Findings always route by lens:
- L1–L4 → main audit, eligible for verdict.
- L5–L10 → side section, never affect verdict.
