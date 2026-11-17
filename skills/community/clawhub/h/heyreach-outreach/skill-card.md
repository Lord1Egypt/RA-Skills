## Description:

Manage LinkedIn outreach campaigns, leads, lists, inbox conversations, and analytics via HeyReach through the superagnt unified API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superagnt](https://clawhub.ai/user/superagnt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to manage HeyReach campaigns, leads, inbox conversations, connected sender accounts, and outreach analytics through an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a superagnt API key and uses the connected HeyReach account, so calls may expose account data or have vendor-side effects.

Mitigation: Use a key intended for this integration and keep it private; confirm before sending messages, deleting or changing records, or performing account administration.

Risk: Campaign, sender-account, and organization operations can change outreach activity or workspace access.

Mitigation: Limit calls to the user's request and get explicit confirmation before outbound, destructive, or administrative actions.

## Reference(s):

- [HeyReach Integration documentation](https://superagnt.com/r/ch-heyreach-outreach-docs)
- [superagnt MCP server](https://mcp.superagnt.com/mcp)
- [superagnt connections page](https://app.superagnt.com/dashboard/connections)

## Skill Output:

**Output Type(s):** [API Calls, JSON data, Shell commands, Guidance]

**Output Format:** [Markdown instructions with curl examples; API responses in JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions and returned data depend on the connected HeyReach account and the requested operation.]

## Skill Version(s):

2.0.14 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
