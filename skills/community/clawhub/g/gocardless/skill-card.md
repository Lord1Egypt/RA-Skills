## Description: <br>
GoCardless compatible Payments & Wallet gives an agent CreditClaw-powered spending, wallet, checkout, and payment-management workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jononovo](https://clawhub.ai/user/jononovo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to connect agents to CreditClaw payment rails, request owner-approved purchases, track balances and spending rules, create payment links, issue invoices, publish checkout pages, and receive payment webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate real spending, payment collection, invoices, checkout pages, and card-decryption checkout flows. <br>
Mitigation: Use a dedicated low-limit account or payment method, keep ask-for-everything approval enabled, and require explicit human confirmation before purchases, invoice emails, public shop publishing, Crossmint orders, or card-decryption checkout flows. <br>
Risk: CreditClaw API keys, webhook secrets, Authorization headers, and decrypted card data are sensitive payment-control materials. <br>
Mitigation: Store CREDITCLAW_API_KEY and webhook secrets only in a secrets manager, send the API key only to creditclaw.com API endpoints, avoid logging Authorization headers or card data, and discard decrypted card details immediately after checkout. <br>
Risk: The release is labeled GoCardless while the security evidence identifies the payment-control provider as CreditClaw, which can confuse trust decisions. <br>
Mitigation: Install only after intentionally trusting CreditClaw to handle payment credentials and agent spending, not solely because of the GoCardless label. <br>
Risk: Some rails have availability limits, including a private beta Stripe x402 wallet rail and a not-yet-general Crossmint wallet flow. <br>
Mitigation: Check rail status before use, handle unavailable endpoints as non-fatal, and fall back to the active owner-approved payment rail. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jononovo/gocardless) <br>
- [CreditClaw main skill documentation](https://creditclaw.com/skill.md) <br>
- [Encrypted Card checkout guide](https://creditclaw.com/encrypted-card.md) <br>
- [Stripe x402 wallet guide](https://creditclaw.com/stripe-x402-wallet.md) <br>
- [CreditClaw wallet management guide](https://creditclaw.com/management.md) <br>
- [CreditClaw checkout guide](https://creditclaw.com/checkout.md) <br>
- [CreditClaw heartbeat guide](https://creditclaw.com/heartbeat.md) <br>
- [CreditClaw skill metadata](https://creditclaw.com/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API request examples, JSON response examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CREDITCLAW_API_KEY for authenticated CreditClaw API calls; purchase and checkout flows may require owner approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
