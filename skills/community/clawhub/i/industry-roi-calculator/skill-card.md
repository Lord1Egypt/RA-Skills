## Description:

Generates an industry-specific ROI estimate card from customer industry, company size, scenario, and current cost, including PoC scope suggestions, risk assumptions, and de-identified case references for presales value discussions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[william202404](https://clawhub.ai/user/william202404)

### License/Terms of Use:

MIT-0

## Use Case:

Presales, product, and technical teams use this skill to turn customer cost and scenario inputs into a concise ROI estimate, PoC validation scope, risk assumptions, and next-step guidance. The output supports early value framing and internal qualification, not formal financial audit or binding pricing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ROI figures may be mistaken for audited financial results or binding commercial commitments.

Mitigation: Present outputs as rough business estimates, validate customer inputs, and review assumptions before sharing reports externally.

Risk: Incomplete or attacker-controlled free-form inputs can produce misleading or unsafe report text when rendered or published.

Mitigation: Validate inputs, review generated reports before publication, and avoid passing untrusted free-form text into externally shared reports without review.

Risk: High calculated ROI values can overstate the business case.

Mitigation: Preserve and review the skill's anomaly warning for ROI above 5x, then verify the source cost and benefit assumptions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/william202404/skills/industry-roi-calculator)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Chinese-language ROI estimates, cost and benefit breakdowns, PoC scope suggestions, risk assumptions, confidence labels, anomaly warnings, and de-identified case references.]

## Skill Version(s):

1.0.0 (source: server release evidence, frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
