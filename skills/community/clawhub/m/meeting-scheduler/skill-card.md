## Description:

Schedule meetings between your owner and another person by coordinating with their PA, finding available slots in both calendars, and sending a calendar invite.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and assistants use this skill to coordinate meetings, find available calendar slots, contact another participant or PA, create calendar invites, and confirm scheduling changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar details may be exposed while checking availability.

Mitigation: Prefer free/busy or redacted busy blocks and require a dry-run summary before displaying or sharing calendar details.

Risk: The skill can contact people, create invites, and delete or change calendar events.

Mitigation: Require explicit user approval before contacting anyone or creating, deleting, or changing calendar events.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/netanel-abergel/skills/meeting-scheduler)
- [Skill definition](artifact/SKILL.md)
- [Deprecation notice](artifact/DEPRECATED.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, Shell commands, Code, Configuration]

**Output Format:** [Markdown with message templates and inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires calendar access and user-specific account, attendee, timing, and meeting details before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
