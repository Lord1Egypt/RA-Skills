## Description:

Let your agent shop online with guardrailed wallets, multiple payment methods, and owner approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[triplehippo](https://clawhub.ai/user/triplehippo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent make online purchases, manage wallet status, request top-ups, generate payment links, and use supported payment rails under owner-controlled spending rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent spending and payment-link capabilities that can move money or initiate purchases.

Mitigation: Keep approval mode set to ask-for-everything unless autonomous spending is intentional, and configure low per-transaction and daily limits.

Risk: A leaked CreditClaw API key could allow unauthorized use of the wallet.

Mitigation: Store CREDITCLAW_API_KEY only in a trusted secrets manager or environment variable, and send it only to creditclaw.com API endpoints.

Risk: Purchasing workflows can expose addresses, emails, merchant details, wallet status, and transaction information to CreditClaw and sometimes merchants or payment processors.

Mitigation: Review what data is required before each purchase and restrict merchants, categories, and domains to intended use cases.

Risk: The artifacts document curl-based installation commands for remote files.

Mitigation: Prefer a signed or checksum-verified package before installation, or verify downloaded files against trusted hashes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/triplehippo/skills/microsoft)
- [CreditClaw Homepage](https://creditclaw.com)
- [CreditClaw Skill Guide](https://creditclaw.com/creditcard/skill.md)
- [Shopping Guide](https://creditclaw.com/creditcard/shopping.md)
- [Amazon Shopping Guide](https://creditclaw.com/creditcard/amazon.md)
- [Pre-paid Wallet Guide](https://creditclaw.com/creditcard/prepaid-wallet.md)
- [Self-Hosted Card Guide](https://creditclaw.com/creditcard/self-hosted-card.md)
- [Stripe x402 Wallet Guide](https://creditclaw.com/creditcard/stripe-x402-wallet.md)
- [Heartbeat Guide](https://creditclaw.com/creditcard/heartbeat.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with inline bash commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated CreditClaw API requests.]

## Skill Version(s):

1.0.0 (source: release evidence; artifact frontmatter reports 2.3.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
