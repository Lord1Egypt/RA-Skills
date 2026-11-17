## Description:

Checks monthly housing-fund contribution tables by recalculating employer and employee contributions, contribution totals, total-row consistency, duplicate people, missing or negative fields, and base values outside the table-provided limits, with findings tied to source line numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, payroll, treasury, and HR staff use this skill during monthly housing-fund payment preparation to check copied contribution-table text before reporting, payroll posting, or accounting handoff. It is intended for arithmetic and table-consistency review, not for legal or policy compliance decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat arithmetic checks as legal or policy compliance advice.

Mitigation: Review outputs before relying on them and verify local housing-fund rules separately; the skill explicitly does not determine current legal limits or policy compliance.

Risk: The free version omits several checks, including low-base adjustment, allowed-rate validation, employment-month matching, interruption detection, wage-basis comparison, and ranked refund or supplement actions.

Mitigation: Use the listed executed and omitted checks to decide whether additional manual review or another tool is needed before making payroll or remittance decisions.

Risk: Incomplete or malformed input can prevent reliable conclusions.

Mitigation: Provide the table header and detail rows together, including period, name, contribution base, employer and employee rates, employer and employee monthly contributions, and total contribution fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/housing-fund-check-free)
- [ClawHub publisher profile: chenqg618](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Human-readable text or JSON containing executed checks, findings, summaries, source line references, missing-input guidance, and checks not included in the free version.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally according to evidence; insufficient input returns missing-field guidance instead of a positive or negative conclusion.]

## Skill Version(s):

1.0.53 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
