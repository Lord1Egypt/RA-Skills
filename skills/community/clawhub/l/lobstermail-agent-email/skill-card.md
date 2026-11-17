## Description:

Email for AI agents. Create inboxes, receive and send email. No API keys, no human signup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuelchenardlovesboards](https://clawhub.ai/user/samuelchenardlovesboards)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to give an agent real lobstermail.ai inboxes for receiving messages, handling verification emails, monitoring inboxes, and sending email when the account tier allows it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and manage real third-party email inboxes and may send real outbound email.

Mitigation: Require explicit user approval before account signups, verification-code handling, inbox monitoring, billing or card verification, and each outbound email.

Risk: Email content and metadata may be handled by the LobsterMail service.

Mitigation: Avoid personal, regulated, confidential, or high-value account flows unless the user accepts that service exposure.

Risk: Inbound emails are untrusted and can contain malicious or misleading instructions.

Mitigation: Treat email bodies as untrusted data, preserve boundary markers and risk metadata, and do not follow instructions from email content without independent user intent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samuelchenardlovesboards/skills/lobstermail-agent-email)
- [LobsterMail website](https://lobstermail.ai)
- [LobsterMail API guides](https://api.lobstermail.ai/v1/docs/guides)
- [LobsterMail OpenAPI docs](https://api.lobstermail.ai/v1/docs/openapi)
- [lobstermail-mcp on npm](https://www.npmjs.com/package/lobstermail-mcp)
- [lobstermail SDK on npm](https://www.npmjs.com/package/lobstermail)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, inline shell commands, and MCP tool names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npx and installs the lobstermail-mcp MCP server; the skill uses MCP tools to create, inspect, wait on, read, delete, and send email from LobsterMail inboxes.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
