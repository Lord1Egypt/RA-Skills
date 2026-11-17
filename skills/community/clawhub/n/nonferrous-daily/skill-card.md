## Description:

Daily non-ferrous metals briefing for AI agents that collects public Cu/Zn/Ni/Co/Mg/Bi market data, news, inventory signals, futures structure, and sentiment to produce a professional daily metals research report for Telegram delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ramboxie](https://clawhub.ai/user/ramboxie)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to automate daily non-ferrous metals monitoring and produce concise market briefings with price, inventory, news, sentiment, trend, and risk context. It is intended for research-style market reporting and does not replace independent trading, compliance, or risk review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may be delivered to the wrong audience if Telegram bot credentials or chat IDs are misconfigured.

Mitigation: Use DRY_RUN first, verify the target chat, and keep unrelated secrets out of the project .env file.

Risk: Public third-party market data may be delayed, unavailable, revised, or inconsistent across sources.

Mitigation: Independently verify important price, inventory, and signal outputs before relying on them for decisions.

Risk: A plaintext HTTP fallback source can expose requests to transport-layer tampering or observation.

Mitigation: Treat data from fallback sources as lower-confidence and cross-check it against HTTPS sources before use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ramboxie/skills/nonferrous-daily)
- [Analysis Daily Template](references/ANALYSIS_DAILY_TEMPLATE.md)
- [Metal Daily Analysis Playbook](references/ANALYSIS_PLAYBOOK.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown market briefing with optional JSON data collection output and Telegram delivery]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-configured Telegram bot token and chat ID for delivery; data comes from third-party public sources and may require independent verification.]

## Skill Version(s):

1.3.7 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
