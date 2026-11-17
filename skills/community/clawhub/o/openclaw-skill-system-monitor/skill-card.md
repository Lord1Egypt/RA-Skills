## Description:

Real-time system metrics monitoring for CPU, memory, disk, network, processes, and system load on macOS and Linux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppopen](https://clawhub.ai/user/ppopen)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and support engineers use this skill to ask an agent for local system health checks, resource usage summaries, process lists, disk status, and network diagnostics. It is useful for quick triage on macOS and Linux hosts using native command-line tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local diagnostic output can expose host details such as usernames, process arguments, ports, mounted filesystems, and network connections.

Mitigation: Review command output before sharing it outside the trusted environment.

Risk: Commands rely on platform-specific tools and output formats, so a suggested check may fail or produce different fields across macOS and Linux.

Mitigation: Confirm the detected platform and installed command availability before relying on the results.

## Reference(s):

- [System Monitor on ClawHub](https://clawhub.ai/ppopen/skills/openclaw-skill-system-monitor)
- [Publisher profile: ppopen](https://clawhub.ai/user/ppopen)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell command examples and terminal output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local host details such as usernames, process arguments, ports, mounted filesystems, and network connections.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
