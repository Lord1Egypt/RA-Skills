## Description:

Klaviyo API integration with managed OAuth for accessing and managing profiles, lists, segments, campaigns, flows, events, metrics, templates, catalogs, and webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xspeter](https://clawhub.ai/user/0xspeter)

### License/Terms of Use:

MIT

## Use Case:

Developers and marketing operations teams use this skill to let an agent operate Klaviyo resources through Maton-managed OAuth. It supports customer data, email marketing, analytics, campaign, flow, catalog, webhook, subscription, suppression, and bulk import workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read customer data and change, send, or delete important Klaviyo marketing assets.

Mitigation: Install only when the agent is intended to operate the Klaviyo account, use least-privilege OAuth scopes where possible, and protect MATON_API_KEY.

Risk: Campaign sends, deletes, webhook changes, bulk imports, subscription changes, and suppression changes can affect customers or audience membership.

Mitigation: Manually confirm these operations after checking exact target IDs and affected audience size.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xspeter/skills/klaviyo-1-0-4)
- [Publisher profile](https://clawhub.ai/user/0xspeter)
- [Klaviyo API Documentation](https://developers.klaviyo.com)
- [Klaviyo API Reference](https://developers.klaviyo.com/en/reference/api_overview)
- [Klaviyo Developer Portal](https://developers.klaviyo.com/en)
- [Maton settings](https://maton.ai/settings)
- [Maton connection control panel](https://ctrl.maton.ai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with Python, JavaScript, curl, HTTP endpoint, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, a Klaviyo OAuth connection, and Klaviyo revision headers.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata version is 1.0.4 and skill frontmatter version is 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
