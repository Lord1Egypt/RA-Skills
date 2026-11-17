## Description:

Runs a local Chinese-language check of hospital drug and supply inventory and department requisition tables, including row arithmetic, totals, duplicate rows, blanks, and cited findings for the free-tier checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashier, pharmacy, and supply staff use this skill during monthly closing, reconciliation, or inventory review to check hospital drug and supply tables for arithmetic and completeness issues. It is limited to the declared free checks and does not replace policy, pricing, procurement, or physical inventory review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill only checks declared table arithmetic, totals, duplicates, blanks, and negative values; it omits several paid-tier and business-policy checks.

Mitigation: Use the findings as reconciliation support only, and separately review omitted checks, pricing rules, approval workflow, procurement terms, and physical inventory.

Risk: A clean result for the free checks can still miss issues outside the artifact's declared scope.

Mitigation: Review the generated findings and source-line citations before relying on the result, especially for month-end closing or audit workflows.

Risk: The input may contain sensitive hospital inventory or department usage data.

Mitigation: Run the bundled local command in an approved environment and avoid sending source tables to external systems unless separately authorized.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/hospital-supply-consumption-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Console text or JSON containing executed checks, omitted checks, findings, source line references, and insufficient-input guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; no API key, registration, or network use is described in the artifact.]

## Skill Version(s):

1.0.49 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
