## Description: <br>
Linux Omniscient combines cognitive prompting, code and command execution, and Linux desktop, hardware, peripheral, network, serial, IoT, and GUI automation controls into an agent-operable workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent plan tasks, generate code or shell commands, and operate a Linux desktop and connected devices for automation and troubleshooting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a Linux desktop and connected devices with very broad authority. <br>
Mitigation: Install only when this level of control is intentional, supervise use, and require explicit confirmation before sensitive or destructive actions. <br>
Risk: Screen capture, OCR, camera, microphone, GUI clicking, and GUI typing can expose private information or act in sensitive sessions. <br>
Mitigation: Confirm each capture or input action, avoid use on machines with sensitive open sessions, and monitor the desktop while the skill is active. <br>
Risk: Process, power, network, DNS, proxy, printer, Bluetooth, serial, and Home Assistant actions can disrupt local systems or connected environments. <br>
Mitigation: Review target devices and commands before execution, prefer query-before-action workflows, and avoid passing long-lived tokens or passwords through chat or command-line arguments. <br>


## Reference(s): <br>
- [Linux Omniscient on ClawHub](https://clawhub.ai/wangjiaocheng/linux-omniscient) <br>
- [Command Reference](references/command_reference.md) <br>
- [Security Checklist](references/security_checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, code snippets, and human-readable summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local scripts that return JSON or command output for the agent to summarize.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
