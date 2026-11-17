## Description:

Build a cross-exchange, cross-strategy real-time portfolio risk monitoring system with webhooks, an event bus, SLA compliance monitoring, drawdown alerts, correlation monitoring, liquidation proximity checks, and circuit breakers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading operations teams use this guide to design portfolio-level risk monitoring across multiple exchanges and strategies. It helps agents produce implementation guidance, code examples, shell commands, and configuration patterns for alerts, circuit breakers, and operational monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples involving live exchange credentials or order cancellation could affect real trading accounts if copied into production.

Mitigation: Use sandbox credentials first, avoid write-capable exchange API keys unless automated cancellation is intended, and add explicit confirmations or dry-run controls.

Risk: Signing keys and API credentials could be exposed through terminal output, logs, or copied examples.

Mitigation: Store signing keys and API credentials in a secret manager and avoid printing them in logs or shell history.

Risk: The guide is non-executing but security evidence marks it review-required due to under-disclosed trading-account impact.

Mitigation: Review the generated implementation plan and operational permissions before deployment, especially any circuit-breaker or exchange-order behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-trading-bot-risk-service)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API endpoint](https://api.greenhelix.net/v1)
- [Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executing guide content that may reference AGENT_SIGNING_KEY and trading API credentials.]

## Skill Version(s):

1.3.1 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
