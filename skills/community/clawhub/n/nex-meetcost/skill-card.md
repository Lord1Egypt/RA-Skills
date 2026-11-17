## Description:

Meeting cost calculator. See what meetings actually cost in billable time. Per-attendee rates by role, recurring meeting projections (weekly/monthly/yearly), cost-per-type breakdowns. Python stdlib only, SQLite storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexaiguy](https://clawhub.ai/user/nexaiguy)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, managers, consultants, and operations teams use this skill to calculate meeting costs from attendee roles, hourly rates, duration, and recurring schedules. It can also log meetings locally, summarize cost trends, and export meeting records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores meeting details in a local SQLite database under ~/.nex-meetcost.

Mitigation: Install and run it only in environments where local storage of meeting titles, attendees, rates, notes, and costs is acceptable.

Risk: The export --output option can write outside the intended export folder and overwrite user-writable files.

Mitigation: Avoid untrusted suggested export commands and use simple filenames for exports until this behavior is fixed.

## Reference(s):

- [Nex MeetCost on ClawHub](https://clawhub.ai/nexaiguy/skills/nex-meetcost)
- [Nex AI website](https://nex-ai.be)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local SQLite data and JSON or CSV exports when the user runs the generated commands.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
