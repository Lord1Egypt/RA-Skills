## Description:

Manage quick notes and time-based reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yusaku-0426](https://clawhub.ai/user/yusaku-0426)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to add and search quick notes and to create, list, and fire time-based reminders. It supports interpreting reminder times in the Asia/Tokyo timezone and formatting them as ISO 8601 timestamps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reminder firing can prompt outbound messages to a specified channel without clear confirmation or channel controls.

Mitigation: Install only in agents that are permitted to post reminder messages, restrict allowed channels, and require review or confirmation before outbound posting.

Risk: The artifact declares required scripts for notes and reminders, but those scripts are not included in the evidence.

Mitigation: Verify or add scripts/notes.js and scripts/reminders.js before relying on note storage, reminder scheduling, or firing behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yusaku-0426/skills/notes-reminders)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and structured guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires notes.js and reminders.js scripts declared in metadata; those scripts are not included in the artifact evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
