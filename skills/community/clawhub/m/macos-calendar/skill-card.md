## Description:

Create, list, and manage macOS Calendar events via AppleScript for reminders, meetings, deadlines, recurring events, and other Apple Calendar tasks on macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucaperret](https://clawhub.ai/user/lucaperret)

### License/Terms of Use:

MIT

## Use Case:

Employees, external users, and developers can use this skill to let an agent list writable macOS calendars and create Apple Calendar events from structured scheduling details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create real Apple Calendar events and alerts on the user's Mac.

Mitigation: Review ambiguous scheduling requests and confirm the calendar, date, time, recurrence, and alarm details before running event creation.

Risk: Event titles and calendar names are written to a local action log, and Calendar.app may open when the helper runs.

Mitigation: Avoid putting highly sensitive details in event titles when local logging is a concern, and make users aware that Calendar.app may launch.

## Reference(s):

- [iCal Recurrence Rules](references/recurrence.md)
- [Project homepage](https://github.com/lucaperret/agent-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces commands and structured event fields for local macOS Calendar automation.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
