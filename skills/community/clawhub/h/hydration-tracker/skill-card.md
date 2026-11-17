## Description:

Track daily water intake, set hydration goals, and get drink reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to log water intake, set daily hydration goals, check progress, and review recent hydration trends from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates persistent local hydration history and goal files under ~/.water_reminder.

Mitigation: Review the stored local JSON files before sharing the machine or backing up the home directory.

Risk: The reminder command provides a manually invoked tip and does not schedule automatic reminders.

Mitigation: Use an external scheduler or reminder application if automatic notifications are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain1/skills/hydration-tracker)
- [BytesAgain homepage](https://bytesagain.com)
- [Hydration Tracker documentation](https://bytesagain.com/skills/hydration-tracker)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text command output with local JSON data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local files under ~/.water_reminder for hydration history and daily goal configuration.]

## Skill Version(s):

2.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
