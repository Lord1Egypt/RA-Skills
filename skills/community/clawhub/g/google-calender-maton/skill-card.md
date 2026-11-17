## Description:

Create, update, list, and delete Google Calendar events with support for attendees, time zones, and Google Meet through Maton API key authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otman-ai](https://clawhub.ai/user/otman-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to manage Google Calendar events through Maton Gateway, including scheduling meetings, updating attendees, creating Meet links, and deleting events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables reading, changing, deleting, and notifying people from the user's primary Google Calendar.

Mitigation: Review the skill before installing, use only a trusted Maton API key, confirm event IDs before updates or deletion, and explicitly approve attendee email addresses and notification settings.

Risk: Sensitive personal or business scheduling information may be handled through the gateway workflow.

Mitigation: Use the skill only with calendar data and credentials appropriate for the intended environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/otman-ai/skills/google-calender-maton)
- [Maton Google Calendar Gateway endpoint](https://gateway.maton.ai/google-calendar/calendar/v3)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with curl and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted Maton API key and access to the target Google Calendar.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
