## Description:

Integrate payments with provider selection, checkout flows, subscription billing, and security best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and product engineers use this skill to compare payment providers and plan checkout, webhook, subscription, fraud, PCI, refund, and chargeback handling for commercial payment integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw payment-provider webhook payload logging can expose sensitive payment or customer data in production logs.

Mitigation: Log sanitized event IDs, event types, correlation IDs, and processing outcomes instead of full provider payloads.

## Reference(s):

- [Payment Integration Patterns](artifact/integration.md)
- [Payment Providers Comparison](artifact/providers.md)
- [Payment Security](artifact/security.md)
- [Subscription Billing](artifact/subscriptions.md)
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/payments)
- [ClawHub Publisher Profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown guidance with tables, checklists, and short plaintext examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no credential environment variables, MCP references, or external tools were detected.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
