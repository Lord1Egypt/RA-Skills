## Description: <br>
Let your agent shop online with guardrailed wallets, multiple payment methods, and owner approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TripleHippo](https://clawhub.ai/user/TripleHippo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent make online purchases, manage guarded payment rails, request owner approvals, and create checkout or storefront payment flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent high-impact spending authority. <br>
Mitigation: Keep owner approval enabled, enforce strict spending controls, and confirm buyer, invoice, and shipping details before sending payments. <br>
Risk: The encrypted-card rail asks agents to run remotely delivered decryption code for card data. <br>
Mitigation: Use the encrypted-card rail only when sub-agent isolation and log redaction are available, and review any delivered decrypt script before execution. <br>
Risk: Leaked credentials could allow unauthorized use of CreditClaw payment APIs. <br>
Mitigation: Restrict access to CREDITCLAW_API_KEY and send it only to CreditClaw API endpoints. <br>
Risk: Card files or decrypted card data could be exposed through logs, repositories, backups, or persistent context. <br>
Mitigation: Store card files outside repositories and backups with restrictive permissions, avoid logging card data, and delete ephemeral checkout contexts after use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TripleHippo/mastercard) <br>
- [CreditClaw Main Skill Guide](https://creditclaw.com/creditcard/skill.md) <br>
- [CreditClaw Checkout Guide](https://creditclaw.com/creditcard/checkout.md) <br>
- [CreditClaw Encrypted Card Guide](https://creditclaw.com/creditcard/encrypted-card.md) <br>
- [CreditClaw Spending Permissions Guide](https://creditclaw.com/creditcard/spending.md) <br>
- [CreditClaw Stripe x402 Wallet Guide](https://creditclaw.com/creditcard/stripe-x402-wallet.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands, API endpoint descriptions, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated CreditClaw API requests.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
