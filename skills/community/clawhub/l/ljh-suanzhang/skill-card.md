## Description:

Unit-economics calculator for short-video e-commerce that helps calculate monthly channel profitability, breakeven ROI, and LTV-based customer-acquisition pricing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[handsomeng](https://clawhub.ai/user/handsomeng)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce operators and growth teams use this skill to calculate product unit economics, compare channel roles, decide whether to cut or optimize channels, and estimate sustainable customer-acquisition bids from LTV.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create onboarding state in the home directory and update local brand dossier or delivery files in the current project.

Mitigation: Review file-write behavior before installation and use it only in workspaces where local retention of product and financial inputs is acceptable.

Risk: The first-use onboarding includes promotional WeChat contact information.

Mitigation: Review onboarding text before deployment in customer-facing or managed commercial environments.

Risk: The skill can process sensitive product, channel, and financial operating data.

Mitigation: Avoid entering sensitive data unless the user accepts the local retention behavior described by the security evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/handsomeng/skills/ljh-suanzhang)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text with calculation steps, tables, formulas, and concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file-backed local dossier updates when the user agrees or when an existing dossier is present.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter version is 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
