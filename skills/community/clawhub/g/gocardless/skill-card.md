## Description:

GoCardless-compatible payments and wallet guidance that gives agents controlled spending, card checkout, x402 wallet, and seller checkout workflows through CreditClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jononovo](https://clawhub.ai/user/jononovo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent register with CreditClaw, monitor wallet status, request owner-approved purchases, sign x402 payments, and create checkout or invoice flows for receiving payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants an agent real payment authority.

Mitigation: Install only when that authority is intended, keep approval mode at ask_for_everything, and set low spending limits and allowlists.

Risk: The raw-card rail can expose sensitive card-handling and PCI implications.

Mitigation: Avoid the raw-card rail unless card handling has been reviewed; never store or log decrypted card details.

Risk: Remote skill files may change after review.

Mitigation: Use pinned and reviewed copies of remote documentation before relying on them for payment operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jononovo/skills/gocardless)
- [CreditClaw Main Skill Guide](https://creditclaw.com/skill.md)
- [CreditClaw Encrypted Card Guide](https://creditclaw.com/encrypted-card.md)
- [CreditClaw Stripe x402 Wallet Guide](https://creditclaw.com/stripe-x402-wallet.md)
- [CreditClaw Management Guide](https://creditclaw.com/management.md)
- [CreditClaw Checkout Guide](https://creditclaw.com/checkout.md)
- [CreditClaw Heartbeat Guide](https://creditclaw.com/heartbeat.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with API examples, curl commands, JSON payload examples, and operational checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and produces payment-operation guidance that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
