## Description:

协助团队成员整理每日工作内容并生成日报、周报、月报，同时在第二天提醒未完成的任务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[beargzhaike](https://clawhub.ai/user/beargzhaike)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and team members use this skill to summarize daily, weekly, and monthly work in Chinese, using screenshot-derived logs, manual descriptions, and memory files when available. It can also identify unfinished items and prepare next-day reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Silent screenshot-based tracking may capture private messages, credentials, customer data, or unrelated sensitive work.

Mitigation: Use only where screenshot tracking is intentional, capture scope is controlled, and sensitive applications or accounts are excluded.

Risk: Automatically generated reports may expose sensitive screen-derived activity to unintended recipients.

Mitigation: Review report recipients, retention, and automation settings before enabling automatic daily report delivery.

Risk: Logs stored under .workbuddy may retain sensitive work activity summaries.

Mitigation: Define retention and access controls for screenshot logs and memory files before regular use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beargzhaike/skills/haike-work-reporter)
- [ClawHub publisher profile](https://clawhub.ai/user/beargzhaike)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration]

**Output Format:** [Markdown reports and reminder guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default language is Chinese; reports may summarize screenshot-derived activity logs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
