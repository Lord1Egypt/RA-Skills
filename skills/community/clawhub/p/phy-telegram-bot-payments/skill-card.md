## Description: <br>
Adds paid-credit paywalls to OpenClaw Telegram bots using Stripe payment links, Telegram Stars invoices, or TON Wallet Pay, with webhook and agent-behavior guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building OpenClaw Telegram bots use this skill to add paid top-ups, payment options, credit tracking, and quota paywall behavior around generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sample payment webhooks can modify local credit files with insufficient scoping or Telegram user ID validation. <br>
Mitigation: Validate Telegram user IDs as numeric IDs and constrain credit-file writes to a dedicated application data directory. <br>
Risk: Payment callbacks may be accepted without strong origin checks if webhook secrets are empty or Telegram webhook requests are not authenticated. <br>
Mitigation: Require a non-empty Stripe webhook signing secret and use Telegram webhook secret tokens or an equivalent origin check. <br>
Risk: Client-provided payment metadata can lead to incorrect credit grants if credits are trusted directly from payment payloads. <br>
Mitigation: Map Stripe price IDs to credit amounts server-side and reject unknown or inconsistent payment records. <br>
Risk: Calling setWebhook during startup can unintentionally change a bot's Telegram delivery mode. <br>
Mitigation: Only call setWebhook during intentional deployment changes and document how it interacts with the bot's polling or webhook configuration. <br>


## Reference(s): <br>
- [Canlah AI homepage](https://canlah.ai) <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-telegram-bot-payments) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code and shell-command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes agent-facing implementation examples that require environment-specific secrets, URLs, price IDs, and webhook settings.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
