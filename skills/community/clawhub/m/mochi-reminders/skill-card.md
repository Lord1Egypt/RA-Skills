## Description:

Audit scheduler jobs, record real delivery receipts and export calendar events. Use for Reminders and Scheduled Tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users use this skill to schedule and audit OpenClaw reminders, record verified delivery outcomes, and export supported reminders to calendar files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A reminder can be scheduled for the wrong recipient, account, timezone, or recurrence.

Mitigation: Confirm the route and schedule before creation, read the saved job back, and inspect existing jobs before retrying an uncertain creation.

Risk: Reminder records and calendar exports stay in the workspace, while native jobs continue until managed through the scheduler.

Mitigation: Use the intended active workspace and account, review workspace access, and manage or pause jobs through the native scheduler.

Risk: Live scheduler behavior and external installation services were not tested.

Mitigation: Prefer a trusted, fixed installer version where available and verify the scheduler’s read-back and actual outputs.

## Reference(s):

- [Input contract](references/input.md)
- [Native scheduling integration](references/scheduling.md)
- [OpenClaw cron documentation](https://docs.openclaw.ai/cli/cron)
- [OpenClaw job management documentation](https://docs.openclaw.ai/automation/cron-jobs/managing-jobs)
- [ClawHub skill release](https://clawhub.ai/hznetnewpower/skills/mochi-reminders)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Files, Shell commands]

**Output Format:** [JSON plans and audit results, Markdown receipts, ICS calendar files, and native scheduler commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calendar exports are workspace files and support one-time reminders and daily, weekly, or monthly fixed-time cron schedules.]

## Skill Version(s):

1.1.1 (source: frontmatter; server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
