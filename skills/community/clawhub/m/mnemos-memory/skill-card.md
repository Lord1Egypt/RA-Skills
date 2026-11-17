## Description:

Use when users or OpenClaw/ClawHub agents need to install, configure, self-bootstrap, troubleshoot, or operate Mnemos for persistent scoped agent memory, or when they mention Mnemos, agent memory, scoped memory, memory MCP tools, or memory automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anthony-maio](https://clawhub.ai/user/anthony-maio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent operators use this skill to install, configure, operate, and troubleshoot Mnemos as a local-first persistent memory layer for coding agents and MCP-capable hosts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to install mutable third-party software and configure persistent memory integrations.

Mitigation: Review the resolved Mnemos package or plugin source and dependency versions, prefer a pinned version in an isolated environment, and approve installation and host configuration changes yourself.

Risk: Persistent memory workflows may store prompts, tool failures, and project facts, and configured embedding providers may receive data needed for retrieval.

Mitigation: Review what will be stored or sent to the configured embedding provider, use appropriate scopes, and inspect or correct stored facts when they look wrong.

## Reference(s):

- [Host Setup](references/hosts.md)
- [Operations](references/operations.md)
- [Mnemos Memory on ClawHub](https://clawhub.ai/anthony-maio/skills/mnemos-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Host-specific setup, operating-loop, and troubleshooting guidance.]

## Skill Version(s):

0.6.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
