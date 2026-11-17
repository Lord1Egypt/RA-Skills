## Description:

Enable OpenClaw to control and use the computer like a human for desktop automation, screenshots, screen recording, file management, application control, mouse and keyboard control, scheduled tasks, and system monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhmza](https://clawhub.ai/user/zhmza)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to let an agent operate a desktop session through command-line and Python interfaces for GUI automation, screenshots, screen recording, application control, file operations, and system monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can capture screens, record activity, type into applications, launch commands, delete files, and kill processes in the user's desktop session.

Mitigation: Use it only in a constrained test account or virtual machine, avoid elevated privileges, and review each proposed desktop or file operation before execution.

Risk: Documented confirmation and sandbox controls are not authoritative because the security evidence says they are not actually enforced.

Mitigation: Do not rely on those documented controls unless the implementation is changed to enforce them; apply external OS, account, and filesystem restrictions instead.

Risk: Relaxing display access controls can broaden desktop access.

Mitigation: Avoid using xhost +local: and prefer least-privilege desktop access settings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhmza/skills/openclaw-computer-use-v2-0-0-tar)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute desktop-control operations that affect the user's active session and files.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
