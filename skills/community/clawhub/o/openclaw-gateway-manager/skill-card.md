## Description: <br>
Manage OpenClaw gateways by querying status, modifying ports, restarting and verifying configurations, creating instances, deleting instances with backups, and scanning ports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seastaradmin](https://clawhub.ai/user/seastaradmin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage local OpenClaw gateway instances across macOS, Linux, and Windows. It helps discover OpenClaw configuration paths, inspect gateway status, change ports, restart gateways, verify configurations, create instances, and delete instances with backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify OpenClaw configuration files, restart or kill gateway processes, and create user-level background services. <br>
Mitigation: Install only when local OpenClaw system management is intended; review generated service files before enabling them and use simple instance names and numeric ports. <br>
Risk: Instance deletion can remove local configuration, session, and memory directories even when backups are created. <br>
Mitigation: Keep independent backups before using create, set-port, restart, or delete operations, and rely on the documented multi-confirmation deletion flow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/seastaradmin/openclaw-gateway-manager) <br>
- [Common Ports Reference](references/common-ports.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or terminal-oriented text with bash commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct local script execution for OpenClaw gateway status, port changes, service management, and instance lifecycle tasks.] <br>

## Skill Version(s): <br>
1.0.3 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
