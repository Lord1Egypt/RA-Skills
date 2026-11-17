## Description:

Runtime security for OpenClaw that protects MCP servers and CLI tools from prompt injection, data exfiltration, and privilege escalation at runtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivanpantheon](https://clawhub.ai/user/ivanpantheon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install Navil, wrap MCP servers with runtime monitoring, scan configurations, review findings, and manage rollback or telemetry settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs unpinned external software.

Mitigation: Install in an isolated environment such as pipx or a virtual environment, and verify the package provenance and version before use.

Risk: The skill can rewrite MCP tool routes by wrapping all MCP servers.

Mitigation: Review the dry-run configuration diff before applying changes and confirm rollback with navil wrap <path-to-config> --undo.

Risk: The skill sends anonymous telemetry by default.

Mitigation: Set NAVIL_DISABLE_CLOUD_SYNC=true to opt out when telemetry is not desired.

## Reference(s):

- [Navil GitHub Repository](https://github.com/navilai/navil)
- [Navil Documentation](https://navil.ai/docs)
- [Community Threat Radar](https://navil.ai/radar)
- [Navil Issues](https://github.com/navilai/navil/issues)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Markdown]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include security scores, severity-grouped findings, pass/fail audit tables, configuration diffs, and rollback guidance.]

## Skill Version(s):

1.0.2 (source: frontmatter, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
