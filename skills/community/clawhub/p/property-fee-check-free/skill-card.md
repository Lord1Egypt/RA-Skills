## Description:

Checks Chinese property-fee tables locally for row-level fee, late-fee, payable-total, total-row, duplicate, and blank-field issues, with findings tied to source line numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External property managers and operations teams use this skill to check copied property-fee billing tables for arithmetic inconsistencies, duplicate customers, blank fields, and omitted free-tier checks. It is arithmetic and table-check assistance, not legal, contract, or accounting approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat arithmetic/table-check findings as legal, contract, or accounting approval.

Mitigation: Present results as calculation assistance and require review of contract terms, rate rules, and accounting policy before acting on billing or collection decisions.

Risk: The free version omits several range and reasonableness checks, including limits for late-fee rates, overdue days, billing months, nonpositive area, negative price, and late fees exceeding prior arrears.

Mitigation: Review the reported omitted checks and perform those controls separately when they matter to the billing decision.

Risk: Incomplete or malformed input can prevent a reliable conclusion.

Mitigation: Require the source table to include recognizable headers and all needed rows; do not interpret insufficient-input output as no issues found.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/property-fee-check-free)

## Skill Output:

**Output Type(s):** [analysis, text, json, guidance]

**Output Format:** [Human-readable text or JSON result objects with findings, summaries, executed checks, and omitted checks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers; materials remain local according to security evidence and artifact behavior.]

## Skill Version(s):

1.0.28 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
