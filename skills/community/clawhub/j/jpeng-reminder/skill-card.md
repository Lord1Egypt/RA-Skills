## Description:

Reminder and scheduling skill. Set one-time or recurring reminders, manage tasks, and send notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create one-time or recurring reminders, list reminder tasks, mark them complete, delete them, and receive scheduled notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reminder messages and schedules are documented as locally persisted data in ~/.openclaw/reminders.json.

Mitigation: Avoid storing highly sensitive reminder details on shared or backed-up machines.

Risk: The package documents commands for scripts/reminder.py, but the executable script is not included in the package.

Mitigation: Verify any separate reminder.py implementation before running the documented commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-reminder)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with bash command examples and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documents local persistence in ~/.openclaw/reminders.json; the package does not include the referenced reminder.py script.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
