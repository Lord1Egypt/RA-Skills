## Description:

Official Kakiyo skill from Kakiyo.com for managing LinkedIn automation campaigns, prospects, and AI agents via Kakiyo MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberboyayush](https://clawhub.ai/user/cyberboyayush)

### License/Terms of Use:


## Use Case:

Developers, operators, and sales teams use this skill to let an agent configure Kakiyo access, manage LinkedIn outreach campaigns and prospects, monitor analytics, manage AI agents, administer client workspaces, configure webhooks, and manage do-not-contact entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad authority to change outreach campaigns, clients, webhooks, and workspaces without clear confirmation safeguards.

Mitigation: Require user confirmation before create, update, delete, invite, webhook, batch prospect, and campaign or agent pause/resume actions.

Risk: Actions may target the wrong workspace, campaign, recipient, or webhook URL.

Mitigation: Verify workspace IDs, campaign IDs, recipients, and webhook URLs before execution.

Risk: The integration can access LinkedIn outreach and account data through Kakiyo.

Mitigation: Install only when the user trusts Kakiyo with their LinkedIn outreach and account data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyberboyayush/skills/kakiyo)
- [Kakiyo homepage](https://kakiyo.com)
- [Kakiyo documentation](https://docs.kakiyo.com)
- [Kakiyo MCP server documentation](https://docs.kakiyo.com/mcp-server)
- [Kakiyo API reference](https://docs.kakiyo.com/api-reference)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-formatted MCP responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mcporter and KAKIYO_API_KEY; interacts with the Kakiyo MCP server.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
