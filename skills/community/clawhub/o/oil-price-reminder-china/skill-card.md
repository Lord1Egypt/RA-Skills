## Description:

油价智能提醒技能自动监控国家发改委油价公告，判断近期油价涨跌趋势，并在调价窗口前提醒用户加油或等待调价。

This skill is ready for commercial/non-commercial use.

## Publisher:

[catplus-eric](https://clawhub.ai/user/catplus-eric)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to monitor China NDRC fuel-price announcements and receive timely guidance on whether to refuel before or after an expected price adjustment. The skill is intended for scheduled reminder workflows that can run periodically and write local reminder state.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Enabling the skill can create a recurring cron job that keeps running and contacts the NDRC website.

Mitigation: Review the exact schedule before enabling it, keep the check frequency modest, and require clear disable or removal steps for the cron job.

Risk: Several advertised safety and configuration controls are not implemented in the artifact.

Mitigation: Ask the publisher to add explicit confirmation, duplicate-job protection, configurable city and frequency handling, and duplicate-reminder controls before relying on it.

Risk: The reminder depends on external NDRC web content and an estimated adjustment window.

Mitigation: Treat reminders as advisory and confirm important refueling decisions against official announcements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/catplus-eric/skills/oil-price-reminder-china)
- [National Development and Reform Commission news releases](https://www.ndrc.gov.cn/xwdt/xwfb/)
- [National Development and Reform Commission](https://www.ndrc.gov.cn)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text reminders and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local JSON state for reminder tracking.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
