## Description:

Buy at Nvidia | Manage compatible cards, wallets & payments. Financial management for Agents and OpenClaw bots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[triplehippo](https://clawhub.ai/user/triplehippo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent register with CreditClaw, check wallet status and spending permissions, request payment approvals, make approved purchases, sign x402 payments, manage top-ups and transaction history, and create checkout or invoice links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent continuing authority to spend real money.

Mitigation: Use strict per-transaction, daily, and monthly limits, require explicit approval for every transaction, monitor activity, and keep wallet freeze or key revocation available.

Risk: The skill can fetch and act on server-provided messages or instructions.

Mitigation: Treat remote messages as operational data, verify event type and source, reject any request to leak secrets or bypass owner policy, and acknowledge messages only after safe handling.

Risk: The skill depends on a payment API key that represents spending authority.

Mitigation: Store CREDITCLAW_API_KEY in a secrets manager, send it only to creditclaw.com API endpoints, scope and revoke keys where possible, and rotate immediately after exposure.

Risk: The skill can decrypt full payment-card details for checkout.

Mitigation: Decrypt card data only for an approved checkout, keep decrypted values in memory only, never log or persist them, and discard them immediately after use.

Risk: The skill can handle customer, buyer, and shipping data.

Mitigation: Collect and transmit only the minimum needed data, confirm owner intent for purchases or sales, and avoid retaining personal data outside the required transaction flow.

Risk: The x402 and wallet flows can authorize on-chain or stablecoin payments.

Mitigation: Require approval thresholds, amount and domain allowlists, balance checks, and transaction reconciliation before and after each payment.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/triplehippo/skills/nvidia)
- [CreditClaw Main Skill Documentation](https://creditclaw.com/skill.md)
- [Encrypted Card Checkout Guide](https://creditclaw.com/encrypted-card.md)
- [Stripe Wallet x402 Guide](https://creditclaw.com/stripe-x402-wallet.md)
- [CreditClaw Wallet Management Guide](https://creditclaw.com/management.md)
- [CreditClaw Checkout Guide](https://creditclaw.com/checkout.md)
- [CreditClaw Heartbeat Guide](https://creditclaw.com/heartbeat.md)
- [CreditClaw Skill Metadata](https://creditclaw.com/skill.json)
- [Crossmint Wallet Purchase Guide](https://creditclaw.com/crossmint-wallet.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and can direct API calls to CreditClaw payment endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 2.3.4 and skill.json lists 2.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
