# Report Templates — prompt-eval

Complete markdown table templates for Final Report Sections 1-6.
Load this file when generating the Final Report after Step 5 and after Step 6.

---

## Section 1 — Test Overview & TP Scorecard

The single most important table in the report. Shows test coverage and per-TP health at a glance.

### 1.1 Test Count Summary

| Dimension | Cases | % of total |
|-----------|-------|------------|
| happy_path | N | X% |
| rule_check | N | X% |
| boundary | N | X% |
| error_case | N | X% |
| safety | N | X% |
| qualitative | N | X% |
| i18n | N | X% |
| **Total** | **N** | **100%** |

### 1.2 Per-TP Scorecard

| TP | Name | Type | Cases | Avg (/3.0) | Score=1 | Score=2 | Score=3 | Status |
|----|------|------|-------|------------|---------|---------|---------|--------|
| TP1 | [Name] | quant | N | X.XX | N (X%) | N (X%) | N (X%) | ✅ / ⚠️ / ❌ |
| TP2 | [Name] | quant | N | X.XX | N (X%) | N (X%) | N (X%) | |
| … | | | | | | | | |
| TP_safety | Safety Compliance | safety | N | X.XX | **N ❌** | N | N | |
| TP_qual_X | [Name] | qual | N | X.XX | N | N | N | |

Status legend: ✅ avg ≥ 2.5 | ⚠️ avg 2.0–2.4 | ❌ avg < 2.0 or any score=1 exists

### 1.3 Overall Health

| Metric | Value |
|--------|-------|
| Total cases scored | N |
| Overall pass rate (case avg ≥ 2.5/3.0) | X% |
| Overall average TP score | X.XX / 3.00 |
| Overall normalized score | X% |
| Bad cases (score ≤ 50% or any TP=1) | N |
| Weakest TP | TP_X "[Name]" — avg X.XX/3.0 |
| Strongest TP | TP_X "[Name]" — avg X.XX/3.0 |

If `TP_safety` is present and has any score=1 cases, flag them:
> ⚠️ Safety failures: N cases — see Section 2 (Bad Case Patterns) for details.

---

## Section 2 — Recurring Bad Case Patterns

**Definition of bad case:** total_score ≤ 50% of max, OR any single TP = 1.

Do not list every bad case individually. **Group them by root cause pattern.**
For each pattern:

```
#### Pattern [N]: [Short name for the failure pattern]

Frequency: X bad cases share this root cause
Affected TP: TP_X "[Name]" — avg X.XX among affected cases
Representative cases: TC00X, TC00Y, TC00Z

**What these inputs have in common:**
[1–2 sentences describing the shared input characteristic that triggers the failure]

**What prompt_a does wrong:**
[Concrete description of the failure — quote from a representative output]

**Why this happens:**
[The specific gap in prompt_a: missing rule, ambiguous instruction, uncovered branch,
conflicting directives, absent guardrail. Cite the section of prompt_a.]
```

Group ALL bad cases into patterns. If a case doesn't fit any pattern, it belongs
to "Pattern N: Isolated failures" — list test_ids only.

---

## Section 3 — Main Optimization Directions

Synthesize findings from Sections 1 and 2 into a ranked list of directions.
One direction = one root cause → one fix target.

```
| Priority | Direction | Evidence | Expected TP impact |
|----------|-----------|----------|-------------------|
| P0 | [Fix rule gap X] | [N cases, Pattern 1] | TP_X: X.XX → ~X.XX |
| P1 | [Clarify ambiguous rule Y] | [N cases, Pattern 2] | TP_X: X.XX → ~X.XX |
| P2 | [Improve qualitative anchor Z] | [avg X.XX on qual cases] | TP_qual_X: X.XX → ~X.XX |
```

P0 = must fix (score=1 on core TP, or a pattern affecting core functionality)
P1 = should fix (score=2 pattern affecting main functionality)
P2 = nice to fix (edge cases, style, minor quality gaps)

For each P0 direction, add a paragraph:
> **Root cause:** [Why prompt_a behaves this way]
> **Fix:** [Exact instruction to add, change, or remove — be specific about placement]
> **Expected outcome:** [Which test categories should improve, by roughly how much]

---

## Section 4 — Suggested Candidate Prompt (`prompt_a_candidate`)

Write the **complete revised candidate version** of `prompt_a` with all P0 and P1 fixes applied.

Requirements:
- Include the full prompt text, not just the changed sections
- Mark every changed line or block with an inline comment `# CHANGED: [reason]`
  or `# ADDED: [reason]` so the user can see what was modified and why
- Do not add changes that aren't supported by test evidence
- P2 fixes are optional — note them as `# OPTIONAL: [reason]` if included

Format:

```
### prompt_a_candidate (for validation)

---
[Full revised prompt text]

Changes summary:
| # | Change | Section modified | Fixes |
|---|--------|-----------------|-------|
| 1 | [Description of change] | [Section/line] | Pattern X, TC00Y |
| 2 | … | … | … |
---
```

If `prompt_a` is very long (>500 words), show only the changed sections with
clear markers (`... [unchanged] ...`) and include the full changes summary table.

---

## Section 5 — Iteration Validation (Baseline vs Candidate)

After running Step 6, report whether the candidate prompt passes validation gates.

Required table:

| Metric | Baseline (`prompt_a`) | Candidate (`prompt_a_candidate`) | Delta | Gate |
|--------|------------------------|----------------------------------|-------|------|
| Overall pass rate (case avg ≥ 2.5/3.0) | X% | Y% | +Z pp | pass/fail |
| Core TP avg (mean of core TPs, /3.0) | X.XX | Y.YY | +Z.ZZ | pass/fail |
| P0-related score=1 count | X | Y | -Z | pass/fail |
| TP_safety avg (if present) | X.XX | Y.YY | +/-Z.ZZ | pass/fail |

Gate rules:
- `P0-related score=1 count` must be zero
- `Core TP avg` must improve by >= 0.40
- `Overall pass rate` must improve by >= 10 percentage points
- `TP_safety avg` must not decrease (if safety TP exists)

If all gates pass: promote candidate to `prompt_a_final`.
If any gate fails: run one additional iteration (generate `prompt_a_v3_candidate`,
retest on the same validation subset), then re-evaluate gates.

Include a short conclusion:
- `Iteration status`: passed in 1 round / passed in 2 rounds / not passed
- `Remaining risk`: highest unresolved TP or pattern (if any)

---

## Section 6 — Final Deliverable Prompt (`prompt_a_final`)

Deliver exactly one final copy-paste prompt:

```
### prompt_a_final (copy-paste ready)

---
[Full final prompt text]
---
```

Add a traceability table:

| change_id | Change summary | Evidence (pattern / TP) | Validation result |
|-----------|----------------|--------------------------|-------------------|
| C01 | ... | Pattern 1, TP2 | improved / unchanged |
| C02 | ... | Pattern 2, TP_qual_X | improved / unchanged |

Do not include speculative edits that were not tied to scored evidence.
