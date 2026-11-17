## Description:

Monitors GitHub trending repositories by language and time range and sends daily alerts through Telegram, Discord, or email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhdryanchang](https://clawhub.ai/user/zhdryanchang)

### License/Terms of Use:

MIT

## Use Case:

Developers, open source contributors, and technical teams use this skill to track trending GitHub repositories, filter results by language and time range, and receive scheduled or on-demand notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A live-looking SkillPay API key is included in release materials.

Mitigation: Replace and rotate the key before use, remove committed secrets, and load payment credentials from a protected runtime secret store.

Risk: Subscription and payment-related routes can expose or modify user payment and notification data when deployed with unsafe defaults.

Mitigation: Add authentication, object-level authorization, and rate limits to subscription, unsubscribe, subscription status, notification, and payment routes before production use.

Risk: Payment callbacks may be accepted without provider verification.

Mitigation: Verify callback signatures or provider-issued tokens and reject callbacks that cannot be cryptographically tied to SkillPay.

Risk: Notification delivery shares user-supplied channel details and repository content with third-party services.

Mitigation: Disclose third-party data sharing and sanitize or escape email and notification content before sending.

Risk: Dependency resolution may drift without a reviewed lockfile.

Mitigation: Commit and review a package lockfile and rescan dependencies before publishing or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhdryanchang/skills/github-trending-monitor)
- [README](README.md)
- [Skill documentation](SKILL.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell and JSON examples; runtime responses are JSON and notification messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports language and time-range filters, scheduled reports, and Telegram, Discord, or email notification channels.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
