## Description:

按农历日期设置提醒（生日、节日等）。当用户需要：(1) 按农历添加提醒事件 (2) 查看农历事件列表 (3) 农历日期与公历日期转换 (4) 设置农历生日/节日提醒 时使用此 skill。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoyuanhao](https://clawhub.ai/user/xiaoyuanhao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage lunar-calendar reminders, convert dates between lunar and Gregorian calendars, and synchronize reminders into OpenClaw cron tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented cron commands can run unsafe shell input from reminder names.

Mitigation: Avoid untrusted reminder names and sanitize shell-sensitive characters before creating or removing cron reminders.

Risk: Cron deletion and creation can change scheduled reminders.

Mitigation: Review generated OpenClaw cron commands and confirm intended reminder names before execution.

Risk: The skill uses the lunar-javascript dependency declared in metadata and package.json.

Mitigation: Install dependencies from trusted package sources and pin or review dependency versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoyuanhao/skills/lunar-reminder)
- [Publisher profile](https://clawhub.ai/user/xiaoyuanhao)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON reminder data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reminder records for data/events.json and OpenClaw cron command guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
