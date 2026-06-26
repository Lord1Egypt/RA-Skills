## Description: <br>
MasterCard AgentPay helps agents and OpenClaw bots use CreditClaw payment rails for guarded card purchases, wallet payments, checkout pages, and spending management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codejika](https://clawhub.ai/user/codejika) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to register bots with CreditClaw, manage owner-approved spending, execute card or x402 wallet payments, and create checkout or invoice flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend money and handle customer or shipping data. <br>
Mitigation: Start in ask-for-everything approval mode, set low per-transaction, daily, and monthly limits, and require explicit confirmation before purchases, invoices, emails, or public shop publishing. <br>
Risk: A leaked CreditClaw API key could allow unauthorized use of the owner's payment account. <br>
Mitigation: Store CREDITCLAW_API_KEY in a secure secret store and never send it to any domain outside creditclaw.com. <br>
Risk: Card checkout flows may expose sensitive card data during a transaction. <br>
Mitigation: Use the one-time checkout key only for the approved transaction, keep decrypted card details in memory, and discard them immediately after checkout. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/codejika/mastercard-agentpay) <br>
- [CreditClaw skill documentation](https://creditclaw.com/skill.md) <br>
- [Encrypted card rail guide](https://creditclaw.com/encrypted-card.md) <br>
- [Stripe x402 wallet guide](https://creditclaw.com/stripe-x402-wallet.md) <br>
- [Checkout guide](https://creditclaw.com/checkout.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with curl examples and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and sends requests to https://creditclaw.com/api/v1.] <br>

## Skill Version(s): <br>
2.3.4 (source: release evidence and skill.md frontmatter, released 2026-03-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
