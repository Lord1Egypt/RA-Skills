## Description:

Implement in-app purchases and subscriptions across iOS, Android, and Flutter with RevenueCat, paywalls, receipt validation, and subscription analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to implement mobile in-app purchases, subscriptions, paywalls, receipt validation, restore flows, and subscription analytics across native iOS, Android, Flutter, and managed IAP services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copied payment code or subscription examples could result in insecure entitlement handling.

Mitigation: Review and harden implementation before use; verify Apple, Google, or RevenueCat purchase state server-side before granting access.

Risk: Webhook or notification handling could incorrectly grant, extend, or revoke paid access.

Mitigation: Verify webhook authenticity, process lifecycle events idempotently, and audit entitlement changes.

Risk: Payment secrets, receipts, and subscriber data may be exposed or retained incorrectly.

Mitigation: Keep secret API keys server-side, minimize stored receipts and subscriber data, and define retention, access-control, and audit policies.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ivangdavila/skills/in-app-purchases)
- [Skill overview and quick reference](artifact/SKILL.md)
- [StoreKit 2 iOS in-app purchases](artifact/storekit.md)
- [Google Play Billing Android in-app purchases](artifact/google-play.md)
- [Flutter in-app purchases](artifact/flutter.md)
- [RevenueCat cross-platform subscriptions](artifact/revenuecat.md)
- [Server-side receipt verification](artifact/server.md)
- [Paywall design conversion patterns](artifact/paywalls.md)
- [Subscription analytics metrics and tracking](artifact/analytics.md)
- [Testing in-app purchases sandbox and debug](artifact/testing.md)
- [Platform comparison IAP services](artifact/platforms.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline code blocks and implementation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform-specific setup snippets, server-verification patterns, paywall guidance, testing scenarios, and subscription analytics guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
