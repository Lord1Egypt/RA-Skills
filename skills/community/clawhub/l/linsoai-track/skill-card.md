## Description: <br>
Linsoai Track helps agents create, schedule, monitor, and manage recurring or one-time tasks from natural language, with optional notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kylvia](https://clawhub.ai/user/kylvia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn natural-language scheduling requests into managed OpenClaw tasks, including cron schedules, interval jobs, one-time reminders, task management actions, and notification routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent scheduled jobs may continue running after they are no longer needed. <br>
Mitigation: Regularly list, pause, or delete tasks that are stale, incorrect, or no longer useful. <br>
Risk: Task notifications may send information to external channels, webhook URLs, or email systems. <br>
Mitigation: Review notification destinations, webhook URLs, and task message content before enabling or importing tasks. <br>
Risk: Secrets can be exposed if users place credentials in task descriptions or notification bodies. <br>
Mitigation: Keep secrets out of task text and protect bot tokens, SMTP credentials, and webhook authentication values through the host platform's credential controls. <br>


## Reference(s): <br>
- [Scheduling frequency guide](references/SCHEDULING.md) <br>
- [Notification channel guide](references/NOTIFICATIONS.md) <br>
- [Task template library](references/TEMPLATES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and natural-language task instructions with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cron expressions, interval schedules, one-time timestamps, time zones, notification routing, and task management actions.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
