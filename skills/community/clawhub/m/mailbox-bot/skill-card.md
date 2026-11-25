## Description:

Postal mail API and MCP server for AI agents: send letters, certified mail and postcards, and give an agent its own street address + PMB with webhooks, OCR search and human-approved scan, forward or discard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arbengine](https://clawhub.ai/user/arbengine)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this agent skill to send outbound physical mail, manage inbound mail proposals with human approval, and connect mailbox workflows through REST or MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer is unpinned, and the partial scan could not resolve some referenced content.

Mitigation: Review the install source and unresolved references before connecting, and proceed only if you trust the mailbox service and its instructions.

## Reference(s):

- [API Documentation](https://mailbox.bot/api-docs)
- [MCP Install Guide](https://mailbox.bot/mcp-install)
- [Public MCP Tool Catalog](https://mailbox.bot/api/mcp/tools-public)
- [OpenAPI Specification](https://mailbox.bot/openapi.json)
- [Sandbox and Test Keys](https://mailbox.bot/api-docs#sandbox)
- [Pricing](https://mailbox.bot/pricing)

## Skill Output:

**Output Type(s):** [API Calls, Configuration instructions, Shell commands, Guidance]

**Output Format:** [REST or MCP requests and responses, JSON configuration, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Human approval is required for inbound mail actions and can be required for outbound mail.]

## Skill Version(s):

5.3.4 (source: frontmatter, CHANGELOG released 2026-11-20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
