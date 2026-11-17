## Description:

Milktea Dashboard helps milk tea shop operators generate daily and weekly operating reports, inventory alerts, sales trend analysis, and automated reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shylamb-token](https://clawhub.ai/user/shylamb-token)

### License/Terms of Use:

MIT-0

## Use Case:

Shop operators and developers use this skill to connect POS/ERP or local sales and inventory data, schedule daily and weekly Markdown reports, and receive restocking or anomaly alerts through configured messaging channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated reports and alerts may share business-sensitive sales, cost, inventory, shop, and recommendation data through external messaging channels.

Mitigation: Review and explicitly configure every message channel and recipient before enabling scheduled reports or alerts.

Risk: Scheduled cron jobs can continue sending reports or inventory alerts after operational needs change.

Mitigation: Confirm how to disable or remove the cron jobs during installation and offboarding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shylamb-token/skills/milktea-dashboard)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and plain-text alerts, with shell commands for cron setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include revenue, cost, inventory, shop names, and operational recommendations; configure recipients before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
