## Description: <br>
Navil Shield helps protect OpenClaw MCP servers and CLI tools at runtime from prompt injection, data exfiltration, and privilege escalation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivanpantheon](https://clawhub.ai/user/ivanpantheon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install and operate Navil as a runtime security layer for OpenClaw MCP servers, including scanning configurations, wrapping servers with monitoring, reviewing security status, and undoing wrapping when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install an external package and persistently wrap MCP server configuration. <br>
Mitigation: Use a virtual environment or pipx, verify the Navil package source, inspect the wrap dry-run, require explicit confirmation before wrapping, and keep the documented undo command available. <br>
Risk: Navil shares telemetry by default unless disabled. <br>
Mitigation: Set NAVIL_DISABLE_CLOUD_SYNC=true before first use when outbound telemetry is not acceptable, and review the cloud status before relying on the threat network. <br>
Risk: The skill auto-runs on broad security-related triggers and can change runtime routing for MCP tools. <br>
Mitigation: Activate it only when runtime proxying is intended, review the target OpenClaw configuration path, and re-check security findings after any new skill or MCP server is added. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivanpantheon/navil-shield) <br>
- [Publisher Profile](https://clawhub.ai/user/ivanpantheon) <br>
- [Navil Homepage](https://github.com/navilai/navil) <br>
- [Navil Documentation](https://navil.ai/docs) <br>
- [Navil Community Threat Radar](https://navil.ai/radar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes scan summaries, security findings, configuration wrapping guidance, and undo commands.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
