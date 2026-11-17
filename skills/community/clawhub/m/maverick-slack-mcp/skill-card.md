## Description:

Search, read, and update Slack messages, channel history, canvases, and users through Slack’s hosted MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick](https://clawhub.ai/user/maverick)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to search Slack conversations and users, read channel history, and make explicitly requested message or canvas updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connected Slack account can read authorized workspace content and make requested changes.

Mitigation: Review the Slack app’s permissions and grant only the access needed.

Risk: Access tokens can expose the connected Slack account if mishandled.

Mitigation: Protect the access token and revoke Slack access when it is no longer needed.

Risk: Messages or canvas changes may reach an unintended destination or contain unintended content.

Mitigation: Check the destination and preview the proposed content before sending or applying changes.

## Reference(s):

- [Slack MCP server documentation](https://docs.slack.dev/ai/slack-mcp-server/)
- [mcporter configuration reference](https://github.com/openclaw/mcporter/blob/v0.11.1/docs/config.md)

## Skill Output:

**Output Type(s):** [Text, Slack messages, Workspace content updates]

**Output Format:** [Text and Slack workspace content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include externally visible message or canvas changes when explicitly requested.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
