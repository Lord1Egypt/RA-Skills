## Description: <br>
Linux operations quick reference for process management, log analysis, network diagnostics, performance monitoring, and user management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afine907](https://clawhub.ai/user/afine907) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, system administrators, and agents use this skill as a concise Linux operations cheat sheet when choosing commands for process control, log inspection, network checks, resource monitoring, file discovery, and user or permission management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reference includes powerful administrative commands for service control, process termination, firewall changes, user deletion, and sudo configuration. <br>
Mitigation: Review each command before use and require explicit approval before running commands that change system state, accounts, permissions, services, or firewall rules. <br>
Risk: The packet capture examples can collect sensitive network traffic when run on broad interfaces or without filters. <br>
Mitigation: Limit captures to approved interfaces, hosts, ports, and time windows, and handle any capture files as potentially sensitive data. <br>
Risk: The passwordless sudo example can weaken host controls if copied without an operational need. <br>
Mitigation: Avoid blanket NOPASSWD sudo rules unless they are explicitly approved and narrowly scoped for a controlled environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/afine907/linux-ops) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Process Management Reference](artifact/references/process.md) <br>
- [System Resources Reference](artifact/references/system.md) <br>
- [Network Diagnostics Reference](artifact/references/network.md) <br>
- [Log Analysis Reference](artifact/references/logs.md) <br>
- [User Permissions Reference](artifact/references/users.md) <br>
- [Linux Command Line Cheat Sheet](https://cheatography.com/davechild/cheat-sheets/linux-command-line/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline Linux shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides reference commands only; it does not execute commands automatically or install code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
