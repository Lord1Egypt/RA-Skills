## Description:

Guides agents in accessing and managing Klaviyo marketing data and workflows through a user-authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and developers use this skill to retrieve customer and campaign data, manage Klaviyo resources, and set up approved marketing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access to customer marketing data can expose personal information or exceed the intended task.

Mitigation: Choose the narrowest available OAuth scopes, start with read-only operations, and share only the data needed.

Risk: Campaign sends and bulk consent changes can affect many customers and may be difficult to reverse.

Mitigation: Review recipients, scope, and intended effects with the user before approving each action.

Risk: Webhooks, hosted functions, and triggers can create ongoing flows of customer data.

Mitigation: Confirm destinations, data shared, and automation scope with the user before enabling them.

## Reference(s):

- [ClawHub Klaviyo skill](https://clawhub.ai/byungkyu/skills/klaviyo)
- [Maton homepage](https://maton.ai)
- [Klaviyo API reference](https://developers.klaviyo.com/en/reference/api_overview)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown guidance with command, code, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Maton account, network access, and an authorized Klaviyo connection.]

## Skill Version(s):

1.2.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
