## Description:

Connect OpenClaw agents to Miro via the Model Context Protocol for board reading and writing, diagram generation, code generation from boards, and collaborative design workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigbubbaagent-bot](https://clawhub.ai/user/bigbubbaagent-bot)

### License/Terms of Use:


## Use Case:

Developers, designers, and product teams use this skill to configure Miro MCP clients, connect agents to team-scoped Miro boards, generate diagrams from code or requirements, and turn board content into implementation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connected agent can read and write Miro boards in the selected team.

Mitigation: Confirm the selected team before use, prefer least-privilege scopes where the client supports them, avoid sensitive production boards unless approved, and keep auto-approval disabled for write tools.

Risk: Using the optional MCP Inspector as a global npm install can broaden local debugging exposure.

Mitigation: Use the Inspector only for local debugging and pin or isolate the install when possible.

Risk: Expensive board-context reads can consume Miro AI credits or hit stricter tool-specific limits.

Mitigation: Batch operations, cache frequently accessed content, and avoid parallel context_get calls.

## Reference(s):

- [Connecting Miro MCP to AI Coding Tools](references/ai-coding-tools.md)
- [Best Practices for Miro MCP](references/best-practices.md)
- [Connecting to Miro MCP](references/mcp-connection.md)
- [Miro MCP Overview](references/mcp-overview.md)
- [Miro MCP Tools & Prompts](references/mcp-prompts.md)
- [REST API Essentials for Miro MCP](references/rest-api-essentials.md)
- [Miro MCP Server](https://mcp.miro.com/)
- [Miro MCP Server in GitHub MCP Registry](https://github.com/mcp/miroapp/mcp-server)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration, shell command examples, REST API snippets, and agent prompts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require OAuth-authenticated access to the selected Miro team; generated agent actions can read or write board content.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
