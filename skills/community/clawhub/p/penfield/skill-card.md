## Description:

Persistent memory for OpenClaw agents. Store decisions, preferences, and context that survive across sessions. Build knowledge graphs that compound over time. Hybrid search (BM25 + vector + graph) recalls what matters when you need it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dial481](https://clawhub.ai/user/dial481)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Penfield to persist decisions, preferences, session checkpoints, artifacts, and connected memory across OpenClaw sessions and other MCP-compatible tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist and sync agent context, memories, and files with an external service.

Mitigation: Use it only for data appropriate for external retention and avoid storing secrets, raw private data, regulated data, or company-sensitive information.

Risk: The documented install path uses npm package installation and MCP proxy commands that may resolve mutable package versions.

Mitigation: Prefer pinned package versions and install in a controlled environment before enabling the plugin for production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dial481/skills/penfield)
- [Publisher profile](https://clawhub.ai/user/dial481)
- [openclaw-penfield npm package](https://www.npmjs.com/package/openclaw-penfield)
- [Penfield website](https://penfield.app)
- [Penfield MCP server](https://mcp.penfield.app)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with tool names, JSON examples, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides an agent in storing, recalling, connecting, updating, and syncing memory and artifact records.]

## Skill Version(s):

2.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
