## Description:

Checks Chinese-format intangible asset amortization ledgers locally by recalculating amortization, accumulated amortization, book value, column totals, duplicate asset IDs, missing fields, negative amounts, and non-positive amortization months with source-line citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and asset accounting teams use this skill during monthly close or annual audit preparation to check whether intangible asset ledger arithmetic ties out. Results should be treated as deterministic arithmetic checks, not legal, tax, or audit advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat arithmetic findings as legal, tax, or audit conclusions.

Mitigation: Review results as ledger arithmetic checks only and route accounting, tax, and audit judgments to qualified reviewers.

Risk: The free release intentionally omits higher-level compliance and exception checks.

Mitigation: Review the reported scope and checks_not_run fields before relying on the output for close or audit workflows.

Risk: Missing or malformed ledger headers can prevent meaningful conclusions.

Mitigation: Provide a Chinese-format ledger with the required headers and treat insufficient_input output as no conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/intangible-amortization-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Human-readable console text or structured JSON with findings, summary, scope, and missing-input guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Every finding cites the source line; insufficient materials produce missing-input guidance instead of a pass/fail conclusion.]

## Skill Version(s):

1.0.49 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
