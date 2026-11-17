## Description:

Linsoai Track helps agents create, schedule, monitor, and manage cron, interval, and one-time tasks from natural language, with automated execution and notification routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylvia](https://clawhub.ai/user/kylvia)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn natural-language scheduling requests into OpenClaw tasks, then inspect, pause, resume, edit, delete, or manually run those tasks. It is suited for recurring monitoring, reminders, reports, migration from Linso Track task descriptions, and notification workflows across IM, email, or webhook channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or change persistent automated jobs that continue running after setup.

Mitigation: Review each generated schedule, time zone, task message, and notification condition before enabling the task.

Risk: Scheduled task output may be sent to external notification channels such as IM, email, or webhooks.

Mitigation: Confirm notification targets explicitly and avoid placing secrets or sensitive output in task messages or notifications.

Risk: Bulk-imported natural-language task descriptions may create unintended jobs or unsafe actions.

Mitigation: Avoid bulk-importing untrusted task descriptions and inspect imported jobs before allowing them to run.

Risk: Management actions such as delete, edit, manual run, webhook, email, and backup cleanup can have destructive or externally visible effects.

Mitigation: Require explicit confirmation before executing those actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kylvia/skills/linsoai-track)
- [Notification Channel Configuration Guide](artifact/references/NOTIFICATIONS.md)
- [Scheduling Frequency Quick Reference](artifact/references/SCHEDULING.md)
- [Task Template Library](artifact/references/TEMPLATES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with cron expressions, task management tables, notification instructions, and inline shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scheduled task names, frequencies, time zones, task messages, notification targets, and management actions.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
