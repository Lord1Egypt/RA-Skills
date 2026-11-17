## Description:

Atomic node skill to exclusively update the start and end time of a Google Calendar event.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent needs to reschedule an existing Google Calendar event by changing only its start and end times.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill updates Google Calendar events through an authenticated CLI, so incorrect calendar IDs, event IDs, or timestamps could change the wrong event or time.

Mitigation: Validate calendar IDs, event IDs, and RFC3339 timestamps before execution, pass CLI arguments as a structured argument list, and confirm the returned JSON start and end times match the request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zvirb/skills/google-calendar-update-time)
- [Publisher profile](https://clawhub.ai/user/zvirb)

## Skill Output:

**Output Type(s):** [shell commands, JSON, guidance]

**Output Format:** [JSON response from the gog CLI after executing the calendar update command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the authenticated gog CLI and validates that returned start and end times match the requested values.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
