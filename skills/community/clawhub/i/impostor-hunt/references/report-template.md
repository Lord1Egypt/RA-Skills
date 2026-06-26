# Report Template

Order is fixed. Verdict first. Main line before side line. Side line is always labeled as non-impersonation.

---

```
# Verdict
- Tier: <Causally aligned | Mostly aligned, minor gaps | Suspected impersonation | Confirmed impersonation | Undecidable>
- Confidence: <0.0–1.0>
- One-line rationale: ...

# Easiest ways this verdict could be wrong
- If I am over-suspicious, the most likely error is: ...
- If I am dismissing too early, the most likely error is: ...

# Scope intake
- Artifact type:
- Access level:
- User's purpose (verbatim):
- Delivery's stated purpose:
- Wording delta:
- Audit budget:

# Purpose restoration
- [verbatim] ...
- [inferred] ...   ← any inferred clause must be one the user could overrule in one sentence

# Main-line claim audit
| Claim | Source | Purpose-critical? | Evidence | Level | Status | Attack point |
|-------|--------|-------------------|----------|-------|--------|--------------|
| ...   | ...    | yes/no            | ...      | A–E   | ...    | ...          |

# Hidden assumptions
- Supported: ...
- Risky: ...
- Unknown: ...

# Causal Impersonation Scan (Step 6)
For each main-line purpose-critical claim:

## Claim: <claim>
- Patterns considered: P?, P?, P?
- Expected causal chain: ...
- Actual causal chain: ...
- Why surface still looks correct: ...
- Inspection sites checked: ...
- Per-pattern conclusion: P? hit / P? clean / P? cannot determine
- D-level leads (if any): "If impersonated, most likely P#; minimal verification: ..."

# Tribunal
Causal Auditor:
- ...

Side Findings Collector:
- ...

Calibration Skeptic:
- Against over-suspicion: ...
- Against premature dismissal: ...

# Verified
- What I actually confirmed: ...

# Unverifiable (leads, not faults)
- Item — would most likely conceal P# — minimal action to verify: ...

# Side findings — NOT impersonation
> These are observations made in passing during the audit. They do not affect the verdict.
- [side, not impersonation] ...
- [side, not impersonation] ...
- Cap status: <N findings; M dropped to preserve main-line focus>

# Minimal next actions
- Smallest moves that would most increase certainty about the verdict.
```

---

## Length discipline

- Verdict + the two pre-mortem lines must appear in the first 30 lines of the report.
- "Side findings" section must be visually clearly separated and shorter than the main-line sections combined.
- If the side-findings cap (≤ 2 × main-line positions checked) is exceeded, drop the weakest and note the drop. Do not silently truncate.
