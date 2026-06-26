## Description: <br>
Shopping Claw gives agents and OpenClaw bots controlled spending, checkout, wallet, storefront, and payment-management workflows through CreditClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[triplehippo](https://clawhub.ai/user/triplehippo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to let an agent request owner-approved purchases, complete merchant checkouts, monitor spending status, manage wallet activity, and create payment links or storefront pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authorize agents to spend money and complete purchases. <br>
Mitigation: Use ask-for-everything approval, strict per-transaction limits, daily or monthly caps, and domain allowlists before enabling purchases. <br>
Risk: The CREDITCLAW_API_KEY can grant access to payment and wallet workflows if exposed. <br>
Mitigation: Store CREDITCLAW_API_KEY in a secrets manager and use it only for CreditClaw API requests. <br>
Risk: Merchant checkouts, invoices, public shop changes, and final order details can cause unintended financial activity. <br>
Mitigation: Avoid unknown merchant checkouts and have the owner verify invoices, storefront changes, and final order details before proceeding. <br>
Risk: Checkout flows may involve decrypted card data during a transaction. <br>
Mitigation: Keep decrypted card data in memory only for the active checkout, never log or persist it, and discard it immediately after confirmation or failure. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/triplehippo/payment) <br>
- [CreditClaw Homepage](https://creditclaw.com) <br>
- [CreditClaw API Base](https://creditclaw.com/api/v1) <br>
- [Main Skill Guide](artifact/SKILL.md) <br>
- [Checkout Guide](artifact/CHECKOUT-GUIDE.md) <br>
- [Shopping Guide](artifact/SHOPPING-GUIDE.md) <br>
- [Stripe x402 Wallet Guide](artifact/STRIPE-X402-WALLET.md) <br>
- [OpenClaw Checkout Guide](artifact/agents/OPENCLAW.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown instructions with curl examples, JSON request and response examples, and browser checkout guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and user-confirmed invocation.] <br>

## Skill Version(s): <br>
2.9.0 (source: server evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
