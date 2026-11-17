## Description:

Productivity Tracker analyzes user-provided activity logs, time notes, goals, or schedules to produce time categories, bottlenecks, focus leaks, and next-day actions without requiring account access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers can use this skill to track activities, categorize time, analyze focus patterns, and generate daily or weekly productivity reviews from data they provide. It is suited for local personal productivity workflows where the user controls the activity records and reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Report generation can overwrite Markdown files outside the intended logs folder.

Mitigation: Constrain report dates to a strict YYYY-MM-DD format, resolve the output path before writing, and reject any path that escapes the logs directory.

Risk: Activity names, timestamps, and generated reports may reveal sensitive routines.

Mitigation: Keep activity data local, limit filesystem permissions to the skill's own data directory, and avoid entering sensitive personal or workplace details unless local storage protections are in place.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/productivity-improving)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV, Guidance]

**Output Format:** [Plain-text insights, Markdown reports, JSON activity records, and CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated from local user-provided activity data and may be written under the skill's data directory.]

## Skill Version(s):

1.1.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
