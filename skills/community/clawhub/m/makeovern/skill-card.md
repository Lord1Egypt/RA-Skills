## Description:

Use this skill when a user wants to run timed focus sessions (Pomodoro technique) from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeljseba](https://clawhub.ai/user/abeljseba)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to run Pomodoro-style focus timers from the terminal, optionally customize session length, trigger local notifications, and review a local session log.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local notifications rely on macOS osascript and may not work in non-macOS terminal environments.

Mitigation: Review or adapt the notification command for the target operating system before relying on timer alerts.

Risk: The optional logging command stores focus-session timestamps in ~/pomodoro.log.

Mitigation: Avoid the logging command, or manage the log file, when users do not want a local activity trail.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abeljseba/skills/makeovern)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may run timers, trigger macOS notifications, and optionally append session timestamps to a local log file.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
