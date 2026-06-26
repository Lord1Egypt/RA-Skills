## Description: <br>
Let your agent shop online with guardrailed wallets, multiple payment methods, and owner approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TripleHippo](https://clawhub.ai/user/TripleHippo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent make online purchases through CreditClaw wallets, owner approval flows, spending limits, and payment rails for Amazon, Shopify, SaaS, online merchants, and x402-enabled services. <br>

### Deployment Geography for Use: <br>
Global, subject to payment rail and merchant restrictions such as US-only Amazon shipping in the bundled Amazon guide. <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables real-money spending across multiple payment rails, including purchases, top-ups, payment links, and x402 payments. <br>
Mitigation: Treat installation as a live financial integration; start with ask-for-everything approval and low per-transaction, daily, and monthly limits. <br>
Risk: The public display name references Microsoft while the artifact behavior is CreditClaw payment and shopping functionality. <br>
Mitigation: Verify the Microsoft/CreditClaw naming mismatch before deployment and ensure users understand the actual payment provider and behavior. <br>
Risk: CREDITCLAW_API_KEY can authorize wallet and payment actions if exposed. <br>
Mitigation: Store CREDITCLAW_API_KEY in a secret manager and send it only to CreditClaw API endpoints. <br>
Risk: Auto-approval, payment links, top-ups, x402, and agent-to-agent payments can broaden the spending surface. <br>
Mitigation: Enable these capabilities only after explicit owner review and keep account, merchant, category, and rail guardrails active. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TripleHippo/microsoft) <br>
- [Publisher Profile](https://clawhub.ai/user/TripleHippo) <br>
- [CreditClaw Homepage](https://creditclaw.com) <br>
- [CreditClaw Skill Guide](https://creditclaw.com/creditcard/skill.md) <br>
- [Shopping Guide](https://creditclaw.com/creditcard/shopping.md) <br>
- [Amazon Purchase Guide](https://creditclaw.com/creditcard/amazon.md) <br>
- [Pre-paid Wallet Guide](https://creditclaw.com/creditcard/prepaid-wallet.md) <br>
- [Self-Hosted Card Guide](https://creditclaw.com/creditcard/self-hosted-card.md) <br>
- [Stripe x402 Wallet Guide](https://creditclaw.com/creditcard/stripe-x402-wallet.md) <br>
- [Heartbeat Guide](https://creditclaw.com/creditcard/heartbeat.md) <br>
- [Machine-readable Skill Metadata](https://creditclaw.com/creditcard/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents through payment setup, wallet checks, spending approvals, purchases, top-up requests, payment links, and transaction status checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata; artifact frontmatter reports 2.3.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
