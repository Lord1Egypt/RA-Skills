## Description:

Linux System Controller helps an agent propose and run Linux desktop, process, hardware, serial, IoT, mouse, keyboard, screenshot, OCR, and visual-recognition control commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and desktop automation users can use this skill to control Linux windows, processes, hardware settings, serial devices, IoT endpoints, and GUI workflows from an agent session. It is best suited to contained Linux environments where system-control actions can be reviewed before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports verified command-injection flaws and broad local system control.

Mitigation: Review and harden command construction before installing; use the skill only in a contained environment and avoid running it as root.

Risk: The security evidence reports runtime package installation.

Mitigation: Preinstall and pin dependencies through the deployment environment instead of allowing runtime pip installation.

Risk: The skill can control local desktop state, power, network adapters, serial devices, and HTTP endpoints.

Mitigation: Require explicit user confirmation for destructive actions, restrict HTTP destinations, and validate target windows, processes, devices, and ports before acting.

Risk: Home Assistant and generic HTTP commands may expose tokens when passed on the command line.

Mitigation: Avoid real long-lived tokens on command lines; prefer short-lived credentials or environment-level secret handling.

## Reference(s):

- [Command Reference](references/command_reference.md)
- [ClawHub Skill Page](https://clawhub.ai/wangjiaocheng/skills/linux-system-controller)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown guidance with inline shell commands; script executions return JSON or plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Linux system access, compatible desktop tooling, and explicit review before destructive or sensitive operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
