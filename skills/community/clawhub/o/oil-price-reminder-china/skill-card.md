## Description: <br>
自动监控国家发改委油价公告，判断近期油价涨跌趋势，并在调价窗口前提醒用户加油或等待。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[catplus-eric](https://clawhub.ai/user/catplus-eric) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Drivers and personal agents in China use this skill to monitor public fuel-price announcements and receive timely guidance on whether to refuel before or after an expected adjustment. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Fuel-price reminders may be approximate because adjustment timing is estimated rather than guaranteed. <br>
Mitigation: Use the reminder as planning guidance and verify current official announcements or local prices before making time-sensitive refueling decisions. <br>
Risk: A recurring schedule can continue checking and sending reminders after the user no longer wants monitoring. <br>
Mitigation: Confirm the cron schedule, notification channel, disable procedure, and removal of /workspace/memory/oil_state.json during setup. <br>
Risk: Some advertised configuration behavior may require manual setup. <br>
Mitigation: Review the script and configure schedule, city expectations, state location, and messaging behavior before deployment. <br>


## Reference(s): <br>
- [National Development and Reform Commission news releases](https://www.ndrc.gov.cn/xwdt/xwfb/) <br>
- [ClawHub skill page](https://clawhub.ai/catplus-eric/oil-price-reminder-china) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text reminder messages with setup and scheduling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores a small local state file to reduce repeated reminders] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
