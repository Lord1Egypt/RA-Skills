## Description:

降价监控+自动下单。用户设置目标价和截止日期后，系统定时轮询飞猪价格，达标后通知或自动下单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaorabbits](https://clawhub.ai/user/zhaorabbits)

### License/Terms of Use:

MIT-0

## Use Case:

Travel shoppers use this skill to monitor hotel, flight, or travel product prices on Fliggy against a target price and deadline. It can notify the user when the target is met and may support auto-booking when the user explicitly authorizes it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent monitoring jobs may continue after the user no longer needs them.

Mitigation: Require explicit confirmation before creating monitoring jobs and automatically remove scheduled jobs when monitoring ends or reaches its deadline.

Risk: Auto-booking can create travel purchases without enough user control.

Mitigation: Require explicit user authorization before enabling auto-booking and notify the user immediately if booking fails or prices change.

Risk: Invalid travel inputs or unsafe command construction could cause incorrect checks or execution risk.

Mitigation: Validate travel/search inputs and avoid shell-interpolated commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaorabbits/skills/price-drop-tracker)
- [Publisher profile](https://clawhub.ai/user/zhaorabbits)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown status messages with inline command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes price checks, notifications, expiry reminders, and optional booking actions when explicitly authorized.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
