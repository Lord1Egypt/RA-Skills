## Description:

Market Morning Brief produces daily morning and evening intelligence digests for prediction market traders, combining Kalshi portfolio P&L, Polymarket activity, crypto prices, optional edge and social-signal sections, and an AI-filtered evening news mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingmadellc](https://clawhub.ai/user/kingmadellc)

### License/Terms of Use:

MIT-0

## Use Case:

Prediction market traders and their agents use this skill to produce concise morning and evening briefs covering portfolio P&L, market activity, optional edge and divergence signals, crypto prices, and AI-filtered news.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive portfolio briefs, including P&L and trading signals, can be sent to a configured webhook even when dry-run says no delivery will occur.

Mitigation: Configure OPENCLAW_SLACK_WEBHOOK or slack_webhook_url only when external delivery is intended, use a private destination, and do not rely on dry-run to prevent webhook delivery or history writes in this version.

Risk: Real trading credentials and portfolio data may be used when live Kalshi or Coinbase sections are enabled.

Mitigation: Use least-privilege API keys where possible, store private keys securely, and review configuration before enabling live account sections.

Risk: Installing the broader OpenClaw stack may add additional trading tools beyond briefing.

Mitigation: Install only the companion skills needed for brief sections you intend to use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kingmadellc/skills/market-morning-brief)
- [Market Morning Brief section documentation](references/sections.md)
- [Market Morning Brief integration guide](references/integration.md)
- [Evening briefing AI-filtered news pipeline](references/evening-pipeline.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text market briefs with optional Markdown command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Brief output is designed for short, scannable chat delivery; unavailable data sources degrade to explicit unavailable sections.]

## Skill Version(s):

1.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
