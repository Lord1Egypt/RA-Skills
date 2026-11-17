## Description:

Manage Apple Reminders via remindctl CLI (list, add, edit, complete, delete). Supports lists, date filters, and JSON/plain output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohdalhashemi98-hue](https://clawhub.ai/user/mohdalhashemi98-hue)

### License/Terms of Use:


## Use Case:

External users and agents use this skill on macOS to list, create, edit, complete, and delete Apple Reminders through the remindctl command-line tool. It is intended for personal reminder and list workflows that should sync through Apple Reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read, write, complete, and delete Apple Reminders through a third-party CLI after Reminders permission is granted.

Mitigation: Install only when comfortable granting that access, and review the target list or reminder before write, complete, or delete actions.

Risk: Delete operations can permanently remove the wrong reminder or list, especially when forced by ID.

Mitigation: Ask the agent to show the target reminder or list first and confirm the exact item before using delete or --force.

## Reference(s):

- [remindctl project](https://github.com/steipete/remindctl)
- [ClawHub skill page](https://clawhub.ai/mohdalhashemi98-hue/skills/mh-apple-reminders)
- [Publisher profile](https://clawhub.ai/user/mohdalhashemi98-hue)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance]

**Output Format:** [Markdown with inline bash commands and optional JSON or plain-text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS and the remindctl binary; Apple Reminders permission is requested by the CLI.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
