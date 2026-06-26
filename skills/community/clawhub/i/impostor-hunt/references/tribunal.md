# Tribunal

Three roles. No role-play prose. Each role outputs 1–3 strongest points only.

---

## Role 1 — Causal Auditor (main line)

Argues directly about impersonation.

- States the strongest specific evidence that a causal chain is impersonated, citing inspection sites and the matched pattern from `causal-impersonation-patterns.md`.
- Or states the strongest specific evidence that the chain is authentic, citing checked sites.
- Must reference at least one Step 6 trio (expected chain / actual chain / why invisible).

Output format:

```
Causal Auditor:
- Claim under scrutiny: ...
- Pattern matched (or ruled out): P? — ...
- Inspection site(s): ...
- Conclusion: hit / clean / cannot determine
```

---

## Role 2 — Side Findings Collector (side line)

Sweeps non-impersonation observations out of the main reasoning so they do not contaminate the verdict.

- Lists side findings briefly with one-line evidence.
- Explicitly marks each as **not impersonation**.
- Enforces the side-findings cap (≤ 2 × main-line positions checked). If over, drops weakest with a note.

Output format:

```
Side Findings Collector:
- [side, not impersonation] ...
- [side, not impersonation] ...
- Cap status: N findings, M dropped to preserve focus
```

---

## Role 3 — Calibration Skeptic (bidirectional)

Defends against both errors.

- Against over-suspicion: which Causal Auditor points are weaker than they look? Which are pattern-matches without real evidence?
- Against premature dismissal: which "clean" calls were made on insufficient inspection? Which patterns were skipped that should not have been?

Both directions must appear, even when one is short.

Output format:

```
Calibration Skeptic:
- Against over-suspicion: ...
- Against premature dismissal: ...
```

---

## Tribunal hard rules

- A "Confirmed impersonation" verdict requires Causal Auditor to cite at least one pattern hit with E-level evidence, or two with C-level evidence plus a concrete failure scenario.
- A "Causally aligned" verdict requires Causal Auditor to cite at least 3 patterns marked **clean** with named inspection sites, *and* Calibration Skeptic's "premature dismissal" branch to be non-empty (forces the auditor to consider what they might have missed).
- Side Findings Collector's output never enters the verdict logic. If a finding seems to bear on impersonation, it must be reclassified to the main line and re-evaluated by Causal Auditor.
