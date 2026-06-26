## Description: <br>
Keeps the OpenClaw gateway running persistently on Windows, Linux, and macOS with service registration, restart, health-check, and power-management guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgy2020](https://clawhub.ai/user/lgy2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who run OpenClaw Gateway on a laptop or workstation use this skill to keep the gateway available across reboots, crashes, sleep events, and network interruptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional sleep-prevention and startup-service commands can change whole-machine power and boot behavior. <br>
Mitigation: Prefer `openclaw gateway install` first, run elevated power or scheduler commands only on a trusted always-on machine, and confirm undo steps before applying them. <br>
Risk: A persistent gateway can continue running after the terminal closes or the user session changes. <br>
Mitigation: Use `openclaw gateway status`, `openclaw logs --follow`, and the stop or uninstall commands to monitor and disable continuous operation when it is no longer needed. <br>


## Reference(s): <br>
- [Openclaw Keepalive on ClawHub](https://clawhub.ai/lgy2020/keepalive) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; the skill provides commands and configuration guidance for the user or agent to review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
