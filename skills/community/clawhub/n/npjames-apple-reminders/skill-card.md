## Description:

Manage Apple Reminders via the remindctl CLI on macOS, including listing, adding, editing, completing, deleting, filtering by list or date, and producing JSON or plain-text output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[npjameszheng1125-netizen](https://clawhub.ai/user/npjameszheng1125-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and macOS users use this skill to have an agent propose and run remindctl commands for viewing, creating, editing, completing, deleting, and exporting Apple Reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide delete and list-delete operations against Apple Reminders.

Mitigation: Show the matching reminder or list before deletion and avoid force deletion unless the target is confirmed.

Risk: The skill operates on a user's Apple Reminders data through a local CLI.

Mitigation: Install only when the user intends to grant Reminders access, and use macOS privacy settings to review or revoke permission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/npjameszheng1125-netizen/skills/npjames-apple-reminders)
- [remindctl project homepage](https://github.com/steipete/remindctl)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target macOS and require remindctl authorization to Apple Reminders.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
