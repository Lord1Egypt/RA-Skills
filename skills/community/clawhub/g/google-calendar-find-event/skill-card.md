## Description:

Atomic node skill to search for events in Google Calendar using the gog CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to query Google Calendar events for a specified time range or subject through the configured gog CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can query Google Calendar through the configured gog CLI, which may expose calendar event details to the agent.

Mitigation: Install and use it only where that calendar access is acceptable for the configured account.

Risk: Vague schedule requests could access broader calendar data than the user intended.

Mitigation: Ask for a date range or subject before accessing calendar events when the request is unclear.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zvirb/skills/google-calendar-find-event)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [JSON array of calendar event objects, with Markdown guidance for command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the local gog CLI and a configured Google Calendar account.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
