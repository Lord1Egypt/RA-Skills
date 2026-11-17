## Description:

MidOS provides MCP tools for AI-agent knowledge management, hybrid search, persistent memory, planning, orchestration, and EUREKA synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msruruguay](https://clawhub.ai/user/msruruguay)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to connect AI agents to the MidOS MCP service for search, persistent memory, planning, knowledge quality checks, health checks, and notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent remote memory may retain sensitive personal, business, or credential data.

Mitigation: Avoid saving sensitive data unless retention and deletion controls are understood and approved.

Risk: Broad shell, file-write, HTTP fetch, and webhook tools can affect private files, repositories, production systems, or external recipients.

Mitigation: Use an explicit MCP tool allowlist, disable shell/file-write/webhook tools unless needed, and require approval for writes and outbound sends.

Risk: The scan verdict is suspicious because tool scope and user-control guidance are insufficient.

Mitigation: Review the skill before installing it in any agent with access to private files, credentials, repositories, or production systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/msruruguay/skills/midos-mcp)
- [MidOS homepage](https://midos.dev)
- [MidOS MCP API base](https://midos.dev/mcp)
- [MidOS documentation](https://midos.dev/docs)
- [MidOS core repository](https://github.com/MidOSresearch/midos-core)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-RPC examples, shell commands, and MCP tool outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve remote persistent memory, search, planning, file, shell, HTTP fetch, and webhook actions depending on the enabled MCP tool allowlist.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
