## Description:

Helps agents view calendars, check availability, and manage Google Calendar events through a Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams use this skill to review schedules, find free time, and create or update Google Calendar events with their approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar access may expose personal scheduling details.

Mitigation: Use the narrowest Google scopes and connection needed, and share only the calendar details necessary for the task.

Risk: Calendar changes can reschedule or cancel events and notify attendees.

Mitigation: Confirm the target event, proposed change, and intended effect with the user before every write.

Risk: Functions, triggers, or destinations can keep running or forwarding data after setup.

Mitigation: Review each automation and destination carefully and obtain separate approval before enabling ongoing forwarding.

Risk: Raw HTTP access requires handling a Maton API key when the CLI is unavailable.

Mitigation: Prefer OAuth login through the CLI; never print, log, or persist an API key.

## Reference(s):

- [Google Calendar skill release](https://clawhub.ai/byungkyu/skills/google-calendar-api)
- [Google Calendar API reference](https://developers.google.com/calendar/api/v3/reference)
- [Maton documentation](https://docs.maton.ai)
- [Maton homepage](https://maton.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Conversational text or Markdown with optional command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include calendar details from the authorized connection; avoid exposing unnecessary personal data.]

## Skill Version(s):

1.2.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
