## Description: <br>
Short alias skill for listing files, directories, processes, or system information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlang-cn](https://clawhub.ai/user/openlang-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill as a quick reference for listing files, directories, running processes, network listeners, routes, environment variables, and related system state across Linux, macOS, Windows, and PowerShell. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The one-letter trigger may be invoked unintentionally in contexts where broader system-listing guidance is not desired. <br>
Mitigation: Confirm the user intends to use the listing-command reference before applying sensitive examples. <br>
Risk: Process, network, route, firewall, and environment-variable listing commands can expose sensitive local details. <br>
Mitigation: Filter or redact sensitive values before sharing command output, especially in shared or sensitive workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openlang-cn/l) <br>
- [Publisher profile](https://clawhub.ai/user/openlang-cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides command variants and cross-platform notes; does not generate or execute commands by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
