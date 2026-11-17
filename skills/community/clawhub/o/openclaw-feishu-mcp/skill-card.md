## Description:

OpenClaw FEISHU MCP configures OpenClaw agents to use Feishu MCP for cloud document and table operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cry779](https://clawhub.ai/user/cry779)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure Feishu MCP access so agents can read, create, replace, and append Feishu documents, and read or write document tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release publishes a concrete Feishu app secret.

Mitigation: Treat the secret as exposed, rotate it if owned, and configure a user-owned Feishu app credential before use.

Risk: Auto-authenticated Feishu actions can read from or modify cloud documents and tables.

Mitigation: Use least-privilege docx permissions and require explicit user intent before write, append, create, or table-write actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cry779/skills/openclaw-feishu-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and action examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-owned Feishu app with appropriate docx permissions and explicit authorization before write, append, create, or table-write actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
