## Description:

Influencer account diagnosis tool that screens accounts against a six-dimension scorecard and a three-part anti-fraud check to produce a partner, negotiate, request-more-data, or pass recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[handsomeng](https://clawhub.ai/user/handsomeng)

### License/Terms of Use:

MIT-0

## Use Case:

Brand, ecommerce, and marketing operators use this skill to evaluate whether an influencer account is suitable for paid collaboration. It asks for account, audience, engagement, commerce, and pricing data, then returns a structured screening result and cooperation recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may show first-run promotional text and off-platform contact prompts that are unrelated to the influencer screening workflow.

Mitigation: Review the first-run content before installation and remove or decline promotional contact prompts when they are not appropriate for the deployment.

Risk: The skill may persist a local onboarding marker at ~/.ljhskill/onboarding.json.

Mitigation: Delete ~/.ljhskill/onboarding.json if local onboarding state should not be retained.

Risk: The workflow may retain business analysis artifacts involving brand, pricing, audience, or campaign data.

Mitigation: Avoid storing sensitive campaign data in shared environments, and decline or delete local archives when handling sensitive commercial information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/handsomeng/skills/ljh-daren)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown diagnosis report with tables, score counts, anti-fraud findings, and a cooperation recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request missing influencer account, audience, engagement, commerce, and pricing data before completing the diagnosis.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
