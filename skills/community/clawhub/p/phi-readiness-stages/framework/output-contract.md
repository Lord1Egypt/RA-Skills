# Output Contract

Every PRS assessment must return the following sections in order.

## 1. Scoped summary

- workload or system name
- environment
- deployment boundary
- framework version used
- assessed date
- reviewer

## 2. Applicability and role

- whether PHI or ePHI is in scope now, planned later, or explicitly out of scope
- likely role: covered entity, business associate, subcontractor, outside HIPAA scope, or unclear
- rationale and caveats

## 3. Evidence reviewed

- evidence grouped by level from `framework/evidence-levels.md`
- evidence freshness from `framework/evidence-freshness.md`
- evidence gaps
- explicit note if review is repo-only
- assessment evidence handling note from `framework/assessment-evidence-handling.md`

## 4. Official sources verified

For each source used:

- title
- URL
- source type: law, official guidance, implementation guidance
- access date

## 5. Crosswalk and policy basis

- crosswalk rows relied on from `mappings/hipaa-security-rule-crosswalk.md` when rule-level traceability matters
- required versus addressable context when material to the decision
- explicit note for any `PRS policy` call that is stricter than the HIPAA baseline

## 6. Current stage assignment

- exact PRS stage code and frozen public label
- confidence: high, medium, or low
- concise explanation of why the stage is not lower
- concise explanation of why the stage is not higher

## 7. Domain findings

For each required domain relevant to the next candidate stage:

- status: met, partial, missing, or unclear
- observed evidence
- blockers

## 8. Recommended actions

Ordered by priority:

- action
- why it matters
- evidence artifact expected after completion
- stage impact

## 9. Caveats

- no legal determination
- no certification claim
- any scope or evidence limitations

## 10. Regulatory boundary note

- whether adjacent Privacy Rule, Breach Notification Rule, state law, FTC, or other review is still needed
- whether the assessment is limited to Security Rule-oriented readiness

## 11. Safe public wording

Provide one short public-safe statement using the exact frozen public label.

## 12. Optional calibration note

When an example materially informed the judgment:

- nearest example used
- short note on the key differences from that example
