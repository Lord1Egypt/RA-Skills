## Description:

Shopping Claw gives agents spending power, financial management, and checkout guidance for CreditClaw and OpenClaw bots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[triplehippo](https://clawhub.ai/user/triplehippo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to register and operate CreditClaw-enabled agents that can request payment approval, complete browser checkouts, manage wallet status, and sell through checkout pages or payment links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend real money through a wallet-linked API key.

Mitigation: Keep approval mode set to ask_for_everything unless the service is fully trusted, and enforce strict merchant, category, and amount limits.

Risk: Checkout flows can retrieve keys that decrypt payment-card details.

Mitigation: Do not store, log, or persist decrypted card data; use ephemeral checkout sessions and discard card data immediately after each transaction.

Risk: Remote Markdown or message content may influence checkout behavior.

Mitigation: Do not treat remote Markdown or message instructions as trusted commands without extra validation and human review.

Risk: Broad financial authority can create misuse or overspending exposure.

Mitigation: Avoid broad auto-approval rules, monitor the CreditClaw dashboard, and review activity before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/triplehippo/skills/payment)
- [CreditClaw homepage](https://creditclaw.com)
- [CreditClaw API base](https://creditclaw.com/api/v1)
- [Main skill guide](artifact/SKILL.md)
- [Checkout guide](artifact/CHECKOUT-GUIDE.md)
- [OpenClaw sub-agent checkout guide](artifact/agents/OPENCLAW.md)
- [Stripe Wallet x402 guide](artifact/STRIPE-X402-WALLET.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guides with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY; OpenClaw metadata indicates user_confirmed invocation.]

## Skill Version(s):

2.9.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
