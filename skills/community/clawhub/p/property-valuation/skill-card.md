## Description:

Estimate property values using comps, income approach, and market analysis with adjustment calculations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users can use this skill to help an agent structure property value estimates for buying, selling, refinancing, or investment analysis. It guides comparable-sales, income, and market-condition reasoning while making valuation method, adjustments, and confidence explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Property details and valuation history may be stored locally in plaintext under ~/property-valuation/.

Mitigation: Avoid saving exact addresses or sensitive transaction details unless needed, and periodically review or delete the local memory and valuation files.

Risk: Valuations may be incomplete or stale when users do not provide recent comparable sales, market conditions, or investment income data.

Mitigation: Use recent user-provided comps and market context, state confidence clearly, and present estimates as decision support rather than a certified appraisal.

## Reference(s):

- [Property Valuation on ClawHub](https://clawhub.ai/ivangdavila/skills/property-valuation)
- [Property Valuation homepage](https://clawic.com/skills/property-valuation)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown guidance with valuation calculations and local memory instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local plaintext memory and valuation notes under ~/property-valuation/ when the user opts in.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
