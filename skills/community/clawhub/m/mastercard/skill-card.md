## Description:

Let your agent shop online with guardrailed wallets, multiple payment methods, and owner approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[triplehippo](https://clawhub.ai/user/triplehippo)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to register and operate a CreditClaw wallet for guarded online purchases, payment requests, balance checks, and owner-mediated spending approvals. It is intended for workflows where an agent may spend or receive funds under explicit human-configured limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can grant an agent real financial authority and access to sensitive payment data.

Mitigation: Use ask-for-everything approval, keep spending limits low, restrict the checkout environment, and review each purchase before execution.

Risk: Server-delivered checkout steps or scripts could be unsafe if executed without local verification.

Mitigation: Avoid running server-delivered scripts or free-form instructions unless files are verified by version and hash and execution is limited to expected CreditClaw workflows.

Risk: A leaked CREDITCLAW_API_KEY could allow unauthorized wallet actions.

Mitigation: Store CREDITCLAW_API_KEY in a secure secret store and send it only to creditclaw.com API endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/triplehippo/skills/mastercard)
- [CreditClaw homepage](https://creditclaw.com)
- [CreditClaw main skill guide](https://creditclaw.com/creditcard/skill.md)
- [Checkout guide](https://creditclaw.com/creditcard/checkout.md)
- [Encrypted Card guide](https://creditclaw.com/creditcard/encrypted-card.md)
- [Spending permissions guide](https://creditclaw.com/creditcard/spending.md)
- [Stripe x402 wallet guide](https://creditclaw.com/creditcard/stripe-x402-wallet.md)
- [Skill metadata](https://creditclaw.com/creditcard/skill.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API examples, curl commands, configuration values, and JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses CREDITCLAW_API_KEY and CreditClaw HTTPS API endpoints; may guide agents through approval, wallet, checkout, and webhook workflows.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
