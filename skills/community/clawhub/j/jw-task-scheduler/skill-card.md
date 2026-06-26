## Description: <br>
智能任务调度技能 - 定时任务、周期任务、一次性提醒的创建与管理。适用于自动化运维、定时报告、提醒通知。觸發詞：定時、排程、排程任務、自動化、提醒、周期任务。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a85012712](https://clawhub.ai/user/a85012712) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to create and manage scheduled tasks, recurring jobs, one-time reminders, notifications, retries, and execution logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent tasks that read local files, write logs, retry automatically, and send reports to Feishu. <br>
Mitigation: Require explicit confirmation before create, modify, delete, and external-send actions; define task names, schedules, end dates, allowed files, Feishu recipients, and log retention. <br>


## Reference(s): <br>
- [Task Scheduler release page](https://clawhub.ai/a85012712/jw-task-scheduler) <br>
- [Publisher profile: a85012712](https://clawhub.ai/user/a85012712) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, Markdown] <br>
**Output Format:** [Markdown with task names, schedules, execution instructions, notification settings, and log guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe persistent schedules, retries, file reads, log writes, and Feishu notification behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
