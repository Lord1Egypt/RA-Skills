## Description:

Connect OpenClaw to LeadShark Apex, the remote MCP server for LinkedIn posts, comment to DM automations, prospecting and sending limits on your LeadShark account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rzere](https://clawhub.ai/user/rzere)

### License/Terms of Use:

MIT-0

## Use Case:

LeadShark users and developers use this skill to connect OpenClaw to their account and automate LinkedIn prospecting, posts, comments-to-DM workflows, and sending within account-plan limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connection can access LinkedIn account data and act as the user, so unreviewed automations could publish, comment, or message unexpectedly.

Mitigation: Prefer OAuth, review available tools and permissions, and require approval before publishing, messaging, or activating automations; protect any fallback API key.

## Reference(s):

- [LeadShark LinkedIn MCP Server](https://leadshark.io/linkedin-mcp-server)
- [LeadShark MCP Documentation](https://apex.leadshark.io/docs/mcp)
- [LeadShark API Documentation](https://apex.leadshark.io/docs/api)
- [ClawHub Release Page](https://clawhub.ai/rzere/skills/leadshark)

## Skill Output:

**Output Type(s):** [Text, API calls, Guidance]

**Output Format:** [LinkedIn content and account actions, with setup and automation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Account-bound LinkedIn actions are subject to LeadShark plan limits.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
