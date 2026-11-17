## Description:

OpenCode CLI integration skill for agents such as OpenClaw to run multi-step coding tasks with Plan-to-Build workflow, session management, MCP integration, and background task monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tchen6500](https://clawhub.ai/user/tchen6500)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to delegate coding work to OpenCode CLI, keep planning and implementation in the same session, configure optional MCP tools, and monitor long-running background tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MCP setup can run local server packages or downloaded code with project access.

Mitigation: Verify package names and publishers, avoid unpinned global npm installs, and prefer project-local or sandboxed execution.

Risk: MCP configuration can expose API keys or service credentials if committed or shared.

Mitigation: Keep API keys out of committed configuration and use environment-specific secret handling.

Risk: Supabase MCP tools can change schema or data in connected projects.

Mitigation: Use backed-up or non-production Supabase projects unless schema or data changes are explicitly intended.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tchen6500/skills/opencode-cli)
- [MCP Configuration Guide](references/mcp-config-guide.md)
- [Built-in Tools Guide](references/built-in-tools-guide.md)
- [Skills Configuration Guide](references/skills-config-guide.md)
- [Practical Tips Guide](references/tips-guide.md)
- [OpenCode Documentation](https://opencode.ai/docs)
- [OpenCode Config Schema](https://opencode.ai/config.json)
- [AgentSkills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OpenCode CLI commands, MCP configuration examples, session-management steps, and background-task monitoring guidance.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
