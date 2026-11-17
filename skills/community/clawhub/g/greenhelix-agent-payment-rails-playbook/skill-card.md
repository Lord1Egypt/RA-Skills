## Description:

The Agent Payment Rails Playbook. Ship multi-protocol agentic payments (x402, ACP, AP2, UCP, MPP) with spending controls, KYA compliance, and escrow protection from first transaction to production.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this guide to plan and implement multi-rail payment flows for AI agents, including x402, ACP, AP2/TAP, UCP, MPP, spending controls, escrow, disputes, and production monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples can create or confirm real payment actions if production credentials are used.

Mitigation: Use sandbox-only credentials by default and require explicit human review before running create_payment_intent, confirm_payment, wallet, webhook, escrow, or dispute examples against production systems.

Risk: Payment tokens, signing keys, API keys, or personal data could be exposed through example metadata, logs, or webhook payloads.

Mitigation: Keep credentials in scoped environment variables, avoid placing tokens or personal emails in metadata, and redact sensitive fields from logs and examples.

Risk: Requests could target an unexpected payment gateway or facilitator host.

Mitigation: Pin approved gateway and facilitator hosts before production use and review any endpoint changes as part of deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-agent-payment-rails-playbook)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API gateway](https://api.greenhelix.net/v1)
- [x402 facilitator](https://x402.org/facilitator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guide with Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable educational guide; examples reference payment credentials and should be reviewed before use against production systems.]

## Skill Version(s):

1.3.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
