## Description:

Send email and SMS and manage a Pingram account via hosted MCP in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[millerm30](https://clawhub.ai/user/millerm30)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to connect Pingram's hosted MCP server, send email or SMS notifications, inspect delivery logs, and manage related Pingram account resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Message bodies, recipient addresses, phone numbers, delivery logs, domains, and account actions are handled by Pingram's hosted service.

Mitigation: Install only when Pingram should process that data, and avoid sending sensitive content unless the user accepts Pingram handling it.

Risk: The skill can guide an agent toward email/SMS sends and account-management actions that may have external effects.

Mitigation: Confirm high-impact sends and account changes with the user before asking the agent to perform them.

Risk: MCP authentication can expire or attach to the wrong Pingram account if an existing browser session is reused.

Mitigation: Reconnect or re-run OAuth when auth errors occur, and use logout plus a private browser session when switching Pingram accounts.

## Reference(s):

- [Pingram OpenClaw integration docs](https://www.pingram.io/docs/integrations/openclaw)
- [Pingram MCP server](https://mcp.pingram.io)
- [Pingram Canada MCP server](https://mcp.ca.pingram.io)
- [Pingram EU MCP server](https://mcp.eu.pingram.io)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an OpenClaw MCP connection and Pingram OAuth session before hosted tools can be used.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
