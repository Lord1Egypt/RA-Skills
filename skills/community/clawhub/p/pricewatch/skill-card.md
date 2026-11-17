## Description:

Monitors competitor prices across Amazon, Walmart, Shopify, and Etsy with AI-driven normalization, alerts, and historical trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juntinglu-229](https://clawhub.ai/user/juntinglu-229)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce operators, pricing teams, and developers use this skill to monitor competitor product URLs, record price history, and receive alerts or reports when pricing changes may require action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured product URLs may cause the skill to send requests to unintended internal systems.

Mitigation: Only add trusted public product URLs and run the skill in an environment that cannot reach internal admin panels or cloud metadata services.

Risk: User-configured notification endpoints can expose alert data or route messages to untrusted services.

Mitigation: Use trusted Slack, Telegram, email, or webhook endpoints and review destination credentials before enabling notifications.

Risk: Live latest-resolution install commands can change behavior between runs.

Mitigation: Prefer pinned install and run commands for repeatable deployments.

## Reference(s):

- [ClawHub PriceWatch Listing](https://clawhub.ai/juntinglu-229/skills/pricewatch)

## Skill Output:

**Output Type(s):** [text, JSON, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON CLI output with configuration examples and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create local SQLite price history and send user-configured Slack or Telegram notifications.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
