## Description:

Cross-rail spend tracking for AI agents across Visa IC, Mastercard Agent Pay, Stripe ACP, x402, and ACH in one dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to let AI agents report financial transactions, register with PayRail402, and check agent status for budget enforcement, anomaly detection, and cross-rail reconciliation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends agent transaction metadata, owner contact details, callback URLs, and PayRail402 credentials to a network service.

Mitigation: Install only when PayRail402 is trusted for this data, use dedicated credentials, and limit submitted transaction details to what is necessary.

Risk: The API base URL is configurable, so a changed endpoint could receive financial metadata or credentials.

Mitigation: Keep the default endpoint unless the replacement is controlled and trusted; review configuration before deployment.

Risk: Webhook-token authentication places the token in the URL path.

Mitigation: Prefer API-key header authentication where possible, avoid logging full request URLs, and rotate webhook tokens if exposure is suspected.

## Reference(s):

- [PayRail402 Homepage](https://payrail402.com)
- [PayRail402 API Documentation](https://payrail402.com/llms-full.txt)
- [PayRail402 Agent Discovery Card](https://payrail402.com/.well-known/agent-card.json)
- [ClawHub Skill Listing](https://clawhub.ai/rsquaredsolutions2026/skills/payrail402)

## Skill Output:

**Output Type(s):** [API Calls, Text, Configuration, Guidance]

**Output Format:** [JSON responses and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns transaction tracking, registration, and status results from the configured PayRail402 endpoint.]

## Skill Version(s):

1.0.2 (source: server release metadata and changelog; artifact frontmatter shows 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
