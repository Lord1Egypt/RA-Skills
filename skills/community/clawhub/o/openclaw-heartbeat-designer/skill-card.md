## Description:

A Chinese-language agent skill that recommends recurring heartbeat check scenarios and generates ready-to-use HEARTBEAT.md checklist snippets with cron schedule suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jack-long-2022](https://clawhub.ai/user/jack-long-2022)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and productivity-focused users use this skill to design recurring checks for email, calendars, code quality, backups, market information, and similar workflows. It helps choose suitable heartbeat scenarios, limit overload, and produce cron timing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cron schedules or timezone conversions may trigger checks at the wrong time if copied without review.

Mitigation: Review generated cron expressions, confirm the intended timezone, and test the schedule before enabling recurring checks.

Risk: Heartbeat integrations can touch sensitive services such as email, calendars, billing, passwords, backups, or social accounts.

Mitigation: Grant only the minimum required access and review any integration permissions before connecting the resulting configuration.

Risk: Too many active heartbeat checks can create noisy or ignored alerts.

Mitigation: Keep active heartbeat items to five or fewer and reduce, merge, or remove low-priority checks when schedules become dense.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jack-long-2022/skills/openclaw-heartbeat-designer)
- [SKILL.md](artifact/SKILL.md)
- [SCENARIOS.md](artifact/SCENARIOS.md)
- [CRON.md](artifact/CRON.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with cron expressions and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory schedule and checklist content for user review before activation.]

## Skill Version(s):

1.1.0 (source: release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
