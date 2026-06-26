## Description: <br>
Let your agent shop online with guardrailed wallets, multiple payment methods, and owner approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codejika](https://clawhub.ai/user/codejika) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent register for CreditClaw, monitor spending permissions, request top-ups, make approved purchases through wallet or encrypted-card rails, and create checkout pages, invoices, payment links, or storefronts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is listed as insurance-like but the security summary identifies a broad CreditClaw payment skill with card, shopping, invoice, and storefront authority. <br>
Mitigation: Install only when real payment-wallet authority is intended, and review the skill against that payment use case before enabling it. <br>
Risk: The CREDITCLAW_API_KEY and webhook secret authorize sensitive wallet operations. <br>
Mitigation: Store secrets in a secret manager, never send the API key outside creditclaw.com API requests, and rotate credentials if exposure is suspected. <br>
Risk: Encrypted-card flows can expose decrypted card details if handled by the main agent or stored in logs, backups, or shared workspaces. <br>
Mitigation: Use the documented ephemeral sub-agent checkout flow, avoid main-agent card decryption, and never store, log, or persist decrypted card data. <br>
Risk: Purchases, invoice emails, payment links, and shop publishing can move money or create public payment surfaces. <br>
Mitigation: Use the strictest human-approval mode and require explicit owner approval before purchases, invoice sends, payment-link sharing, or shop publication. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/codejika/insure) <br>
- [CreditClaw main skill guide](https://creditclaw.com/creditcard/skill.md) <br>
- [CreditClaw checkout guide](https://creditclaw.com/creditcard/checkout.md) <br>
- [CreditClaw encrypted card guide](https://creditclaw.com/creditcard/encrypted-card.md) <br>
- [CreditClaw spending guide](https://creditclaw.com/creditcard/spending.md) <br>
- [CreditClaw management guide](https://creditclaw.com/creditcard/management.md) <br>
- [CreditClaw heartbeat guide](https://creditclaw.com/creditcard/heartbeat.md) <br>
- [CreditClaw Crossmint wallet guide](https://creditclaw.com/creditcard/crossmint-wallet.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated CreditClaw API use.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata; artifact frontmatter reports 2.3.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
