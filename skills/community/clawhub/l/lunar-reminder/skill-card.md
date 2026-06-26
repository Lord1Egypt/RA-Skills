## Description: <br>
Helps an agent create, view, delete, convert, and sync reminders based on Chinese lunar-calendar dates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoyuanhao](https://clawhub.ai/user/xiaoyuanhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to manage local reminders for lunar birthdays, festivals, and date conversions, then optionally sync reminder notifications to OpenClaw cron jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reminder details are stored locally in the skill directory and may include personal dates or notes. <br>
Mitigation: Use simple reminder names, avoid sensitive notes, and review or delete local event data when it is no longer needed. <br>
Risk: Synced cron reminders can continue firing until removed. <br>
Mitigation: Periodically review OpenClaw cron jobs and remove stale lunar_<event name> jobs. <br>
Risk: Scheduled notifications use the Asia/Shanghai timezone. <br>
Mitigation: Confirm Asia/Shanghai is the intended timezone before relying on reminder timing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaoyuanhao/lunar-reminder) <br>
- [Publisher profile](https://clawhub.ai/user/xiaoyuanhao) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown responses with shell command snippets and local JSON event data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Asia/Shanghai for scheduled reminder notifications.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; package.json lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
