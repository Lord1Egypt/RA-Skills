# Evidence Model

Used for main-line claims only. Side findings do not require this grading.

---

## Levels

**A — Direct evidence**
Source code, real runtime output, real data, authoritative documentation, or a reproducible command directly supports or refutes the claim.

**B — Strong indirect evidence**
Multiple independent indirect signals converge on the same conclusion, though no single signal closes the loop.

**C — Weak evidence**
Naming looks right, demo runs, screenshot looks fine, a single example passes, tests exist but cannot meaningfully fail. Surface signals only.

**D — Unverifiable**
Current materials do not allow a judgment. Not error, not pass.

**E — Contradicted**
Evidence directly refutes the claim.

---

## Hard rules

- A purpose-critical claim resting only on C-level evidence cannot be judged "completed".
- D-level claims cannot be called fraud. They are **leads**: record what type of impersonation each unverified item would most likely conceal if it were impersonation.
- E-level evidence is required (or two purpose-critical C-level claims plus a concrete failure scenario) to issue **Confirmed impersonation**.
- The skill does not execute code to elevate D → A by default. Running code can manufacture new surface-correct outputs that mask the original impersonation. Execution requires explicit user request.

---

## D-level treatment

For each D-level claim, record one line:

> If this item is impersonated, the most likely pattern would be P# — and the minimal action to verify would be: ...

This converts D from a dead end into a tracked lead.
