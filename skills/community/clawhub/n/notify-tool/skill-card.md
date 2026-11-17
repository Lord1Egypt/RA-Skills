## Description:

Send desktop notifications from command line scripts and automated tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to send local desktop alerts for task completion, reminders, process status, and urgent operational messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Notification title or message text can execute unintended shell commands through the bundled helper.

Mitigation: Review before installing and avoid untrusted or automatically forwarded notification text unless the helper is changed to call notify-send without a shell.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Notification guidance may include title, message, and urgency options.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
