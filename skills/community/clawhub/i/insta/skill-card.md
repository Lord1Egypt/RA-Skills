## Description: <br>
Lets an AI agent shop online with funded CreditClaw wallets, Stripe-powered payment rails, spending guardrails, owner approval flows, and order tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codejika](https://clawhub.ai/user/codejika) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent register a CreditClaw wallet, check spending permissions, request purchases, route payments through supported rails, and report approval or order status. It is intended for real commerce workflows where the owner funds the wallet and controls limits, approvals, categories, and freezes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make or request real financial transactions. <br>
Mitigation: Use it only for intended CreditClaw purchasing workflows, verify the publisher and skill identity, start with ask-for-everything approval, and set low per-transaction, daily, monthly, and category limits. <br>
Risk: A leaked CREDITCLAW_API_KEY could allow unauthorized wallet activity. <br>
Mitigation: Store the key in a secrets manager and send it only to creditclaw.com API endpoints. <br>
Risk: Purchase, shipping, webhook, and payment-signing data may leave the agent environment. <br>
Mitigation: Confirm that users understand data may be sent to CreditClaw and downstream merchants or payment services before enabling real purchases. <br>
Risk: The release metadata and artifact content use different branding and version signals. <br>
Mitigation: Review the exact enabled payment rail and current release identity before allowing automated or semi-automated spending. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/codejika/insta) <br>
- [CreditClaw homepage](https://creditclaw.com) <br>
- [CreditClaw API base](https://creditclaw.com/api/v1) <br>
- [CreditClaw Stripe skill](https://creditclaw.com/stripe/skill.md) <br>
- [Shopping guide](https://creditclaw.com/stripe/shopping.md) <br>
- [Amazon purchase guide](https://creditclaw.com/stripe/amazon.md) <br>
- [Pre-paid Wallet guide](https://creditclaw.com/stripe/prepaid-wallet.md) <br>
- [Self-Hosted Card guide](https://creditclaw.com/stripe/self-hosted-card.md) <br>
- [Stripe x402 Wallet guide](https://creditclaw.com/stripe/stripe-x402-wallet.md) <br>
- [Heartbeat guide](https://creditclaw.com/stripe/heartbeat.md) <br>
- [Skill metadata](https://creditclaw.com/stripe/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown documentation with JSON examples and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated CreditClaw API calls; outputs can include purchase, approval, balance, transaction, webhook, and payment-link details.] <br>

## Skill Version(s): <br>
1.2.1 (source: ClawHub release evidence; artifact frontmatter reports 2.3.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
