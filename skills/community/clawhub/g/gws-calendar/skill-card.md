## Description:

Google Calendar: Manage calendars and events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to have an agent inspect Google Calendar CLI schemas and prepare gws calendar commands for managing calendars, events, ACLs, free/busy queries, and settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar state can be changed or data deleted through delete, clear, ACL update, move, patch, update, insert, import, and quickAdd operations.

Mitigation: Require explicit user approval and review gws schema output and parameters before running state-changing commands.

Risk: The skill depends on the external gws CLI and generated shared authentication guidance.

Mitigation: Confirm gws is installed and use the shared auth and security guidance before invoking calendar commands.

Risk: Google Calendar operations may expose or modify personal or organizational calendar data.

Mitigation: Limit requests to the user-authorized calendar scope and confirm target calendars, events, and ACLs before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-calendar)
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI and method-specific schema inspection before constructing parameters.]

## Skill Version(s):

1.0.13 (source: server release metadata; artifact metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
