## Description:

Add paywall to OpenClaw Telegram bots with Stripe external links, Telegram Stars, and TON Wallet Pay, including webhook server, credits system, and AGENTS.md behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add paid credit top-ups and soft paywall behavior to OpenClaw Telegram bots. It provides implementation guidance for Stripe payment links, Telegram Stars invoices, TON Wallet Pay options, webhook handling, and bot payment prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sample webhook behavior can grant paid credits from unauthenticated Telegram payment requests or untrusted payment data.

Mitigation: Authenticate Telegram webhooks with a secret token and validate pre-checkout and successful-payment data against server-side orders before crediting users.

Risk: Billing state may be written for untrusted user identifiers or unsafe workspace paths.

Mitigation: Strictly validate user IDs and path containment before writing usage or credit files.

Risk: Payment callbacks may be replayed or processed more than once.

Mitigation: Use idempotency keys or equivalent transaction records before applying credits.

Risk: The sample payment server exposes webhook endpoints on port 8001.

Mitigation: Avoid direct public exposure of port 8001; deploy behind authenticated, monitored, and properly routed infrastructure.

Risk: Payment wording and flow may be unclear to users in some locales.

Mitigation: Review payment wording for transparency, local compliance, and locale-appropriate user expectations before release.

## Reference(s):

- [Canlah AI homepage](https://canlah.ai)
- [Phy Telegram Bot Payments on ClawHub](https://clawhub.ai/phy041/skills/phy-telegram-bot-payments)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with Python, shell, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes webhook server examples, payment option scripts, setup checklist, pricing guidance, and AGENTS.md behavior text.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
