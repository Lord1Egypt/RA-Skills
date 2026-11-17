## Description:

Product Launch Radar monitors product launch activity across multiple sources, filters high-value updates, and prioritizes briefings for decision makers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, investors, technical leads, and market analysts use this skill to aggregate product launch signals, reduce noise, generate daily or weekly briefs, and route important updates to configured team channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Competitive-intelligence briefs may be shared with unintended recipients if notification or report settings are misconfigured.

Mitigation: Confirm the Feishu webhook, email recipients, and report path before installation, and share generated briefs only with the configured recipients.

Risk: Scheduled or webhook-triggered runs may execute at an unexpected time or with overbroad access.

Mitigation: Confirm the cron schedule and timezone, and use scoped tokens for the API trigger.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/skills/product-launch-radar)
- [Workflow definition](artifact/workflow.json)
- [Configuration reference](artifact/config.yaml)
- [Usage examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown briefs, JSON API responses, shell commands, and configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save reports to ./reports/daily-brief-{date}.md and route notifications through configured Feishu or email channels.]

## Skill Version(s):

1.0.0 (source: release evidence and workflow.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
