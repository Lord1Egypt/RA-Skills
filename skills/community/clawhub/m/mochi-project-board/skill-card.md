## Description:

Manage project tasks, dependencies, owners, deadlines and effort, then export board reports, overdue tasks and calendar dates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT-0

## Use Case:

Project managers and teams can organize projects, tasks, dependencies, owners, due dates, and effort, then review overdue or blocked work and export reports or calendar dates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local project state and exported reports may contain sensitive project details.

Mitigation: Limit access to the workspace database and exported reports.

Risk: Task updates or removal can change persisted project data.

Mitigation: Keep a backup before changes that may need to be reversed.

Risk: An exported calendar file does not create reminders by itself.

Mitigation: Import the .ics file into a calendar and configure reminders there if needed.

## Reference(s):

- [Action contract](references/input.md)
- [MochiLab homepage](https://mochilab.bz)
- [ClawHub release page](https://clawhub.ai/hznetnewpower/skills/mochi-project-board)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [Local JSON, HTML, and CSV reports, an iCalendar (.ics) deadline file, and task summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports and persistent project state are workspace-local. Calendar exports contain all-day dates and do not configure reminders.]

## Skill Version(s):

1.0.1 (source: evidence.json release.version and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
