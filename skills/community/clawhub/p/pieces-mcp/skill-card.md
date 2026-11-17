## Description:

Connect OpenClaw to Pieces through MCP so an agent can use PiecesOS long-term memory for retrieval, durable memory creation, configuration, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackrosspieces](https://clawhub.ai/user/jackrosspieces)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect OpenClaw to a remote PiecesOS MCP server, query long-term memory, write durable memory summaries, and troubleshoot MCP connection issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead users to expose sensitive Pieces long-term memory through a public tunnel.

Mitigation: Use a private or authenticated tunnel instead of a bare public URL, and query or write Pieces memory only when needed.

Risk: The skill asks the agent to make persistent MCPorter configuration changes.

Mitigation: Review the MCPorter configuration change before saving it and avoid unnecessary global npm installation.

Risk: Pieces long-term memory results may contain sensitive context.

Mitigation: Treat retrieved Pieces data as sensitive and limit its use to the user-requested task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackrosspieces/skills/pieces-mcp)
- [Publisher profile](https://clawhub.ai/user/jackrosspieces)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents through human confirmation prompts, MCP endpoint construction, MCPorter configuration, memory query and creation patterns, and troubleshooting.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
