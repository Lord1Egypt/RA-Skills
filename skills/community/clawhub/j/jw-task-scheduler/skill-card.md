## Description:

Task Scheduler helps agents create and manage recurring, one-time, and reminder tasks for operations automation, scheduled reports, and notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a85012712](https://clawhub.ai/user/a85012712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent users use this skill to define scheduled tasks, reminders, recurring reports, and notification workflows for automation contexts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent scheduled jobs may keep running without clearly documented approval or deletion safeguards.

Mitigation: Require explicit user confirmation before creating jobs, expose review and deletion controls, and periodically audit active schedules.

Risk: Scheduled tasks may read local memory files and send reports to Feishu destinations without clearly defined data limits.

Mitigation: Restrict file reads to approved allowlists, redact sensitive content, and send notifications only to approved Feishu recipients or channels.

Risk: Automatic retries can repeat incorrect notifications or repeated data access when a task fails.

Mitigation: Use bounded retries, record failure logs, alert the user on repeated failures, and pause jobs that continue to fail.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/a85012712/skills/jw-task-scheduler)
- [ClawHub Publisher Profile](https://clawhub.ai/user/a85012712)

## Skill Output:

**Output Type(s):** [Text, Configuration, Guidance]

**Output Format:** [Markdown task descriptions with cron-style schedules and notification settings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task names, execution times, task content, retry expectations, and notification channels.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
