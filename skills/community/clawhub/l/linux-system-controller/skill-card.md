## Description: <br>
Linux System Controller lets an agent control Linux desktop windows, processes, hardware settings, serial devices, IoT endpoints, keyboard and mouse automation, screenshots, OCR, and visual recognition through bundled CLI scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and power users use this skill when they intentionally want an agent to automate or inspect a Linux workstation, manage local processes and system settings, interact with serial devices, or call smart-home and HTTP APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad local-control capability can affect windows, running processes, network state, power state, serial devices, screenshots, OCR, and IoT endpoints. <br>
Mitigation: Install and run the skill only on systems where this level of agent control is intended, and review exact commands and target URLs before execution. <br>
Risk: Screenshots and OCR may expose secrets or private data visible on the desktop. <br>
Mitigation: Avoid using screenshot, OCR, or visual automation features while sensitive information is displayed. <br>
Risk: IoT and HTTP actions may require tokens and can affect external devices or services. <br>
Mitigation: Use least-privilege, short-lived tokens where possible and confirm the endpoint, entity, and requested action before use. <br>
Risk: Power, process, window, and network commands can interrupt work or connectivity. <br>
Mitigation: Follow the artifact's list-or-query-first workflow and require explicit confirmation before destructive actions such as shutdown, restart, process termination, window close, or disabling network adapters. <br>


## Reference(s): <br>
- [Linux System Controller Command Reference](references/command_reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wangjiaocheng/linux-system-controller) <br>
- [Publisher Profile](https://clawhub.ai/user/wangjiaocheng) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-like command output from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger local Linux commands, desktop automation, screenshots or OCR, serial I/O, and HTTP API calls when the host agent executes the described scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
