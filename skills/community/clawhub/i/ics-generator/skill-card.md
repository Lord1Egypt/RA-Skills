## Description:

Generates Google Calendar-compatible .ics files from structured event data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengqunkoo](https://clawhub.ai/user/zhengqunkoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn schedules, study plans, or task lists into importable iCalendar content for Google Calendar and compatible calendar clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsanitized event text may produce malformed calendar content because iCalendar escaping and validation are not documented as implemented.

Mitigation: Use trusted or sanitized event data and review generated .ics content before importing or distributing it.

Risk: The documented lastDate date-shifting behavior may not work as written.

Mitigation: Confirm event dates in the generated calendar output when using chunked or sequential schedules.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [iCalendar (.ics) string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normalizes event times to UTC and generates unique event identifiers.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
