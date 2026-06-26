## Description: <br>
Provides agents with CreditClaw payment, wallet, checkout, and accounting workflows for Nvidia shopping and broader financial management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TripleHippo](https://clawhub.ai/user/TripleHippo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to connect CreditClaw payment authority, check balances and spending rules, request card or x402 purchases, and create checkout links or storefronts under owner controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Nvidia-facing identity may obscure that the skill grants broad CreditClaw payment and selling authority. <br>
Mitigation: Install only when broad payment and selling workflows are intended, and verify CreditClaw account ownership, payment rails, and spending limits before use. <br>
Risk: Leaked API keys or webhook secrets could expose payment authority. <br>
Mitigation: Store CREDITCLAW_API_KEY and webhook secrets in a secrets manager and send the API key only to creditclaw.com endpoints. <br>
Risk: Customer emails, shipping addresses, public shop data, or payment-related information may be processed or exposed through CreditClaw workflows. <br>
Mitigation: Avoid sending real customer, shipping, or shop data unless the operator has reviewed where it will be processed and exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TripleHippo/nvidia) <br>
- [TripleHippo Publisher Profile](https://clawhub.ai/user/TripleHippo) <br>
- [CreditClaw Skill Guide](https://creditclaw.com/skill.md) <br>
- [CreditClaw Encrypted Card Guide](https://creditclaw.com/encrypted-card.md) <br>
- [CreditClaw Stripe x402 Wallet Guide](https://creditclaw.com/stripe-x402-wallet.md) <br>
- [CreditClaw Management Guide](https://creditclaw.com/management.md) <br>
- [CreditClaw Checkout Guide](https://creditclaw.com/checkout.md) <br>
- [CreditClaw Heartbeat Guide](https://creditclaw.com/heartbeat.md) <br>
- [CreditClaw Skill Metadata](https://creditclaw.com/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown guidance with JSON examples and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated CreditClaw API use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
