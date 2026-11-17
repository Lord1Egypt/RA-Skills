## Description:

Meeting Prep Agent researches scheduled meeting attendees and companies, then generates concise pre-meeting briefs with talking points, icebreakers, and context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[audsmith28](https://clawhub.ai/user/audsmith28)

### License/Terms of Use:


## Use Case:

Employees, sales teams, recruiters, investors, and other meeting participants use this skill to prepare for calendar events or specific attendees by generating briefing material from calendar context and public research sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended automation may run under-scoped meeting preparation behavior before the scripts are fully reviewed.

Mitigation: Review the scripts and avoid enabling cron or automatic prep until the placeholder behavior is replaced and event filtering is verified.

Risk: Generated briefs can store meeting details and attendee research locally.

Mitigation: Use private file permissions, review storage settings, and retain briefs only as long as needed.

Risk: The brief display command can show arbitrary local files when invoked with a path.

Mitigation: Restrict brief display to the configured briefs directory before relying on the command in routine workflows.

Risk: History updates may overwrite existing prep state.

Mitigation: Preserve existing history data when updating deduplication records and test this behavior before enabling automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/audsmith28/skills/meeting-prep-agent)
- [Publisher profile](https://clawhub.ai/user/audsmith28)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text meeting briefs with setup and automation commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Briefs may be stored locally and optionally delivered through configured channels.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
