## Description:

24/7 autonomous monitoring for crypto portfolios, whales, and market conditions. Multi-condition alerts via OpenClaw heartbeat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flotapponnier](https://clawhub.ai/user/flotapponnier)

### License/Terms of Use:

MIT-0

## Use Case:

External users, portfolio managers, and traders use this skill to configure ongoing crypto portfolio, wallet, token discovery, price movement, and market-brief monitoring through an OpenClaw agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may store monitoring rules, wallet or watchlist identifiers, previous values, schedules, and alert destinations for ongoing checks.

Mitigation: Use dedicated or pseudonymous wallet addresses and notification channels when privacy matters, and confirm monitored items and alert destinations before enabling heartbeat monitoring.

Risk: The skill requires a Mobula API key for authenticated data access.

Mitigation: Use an API key with appropriate limits, rotate it if exposed, and avoid sharing it in prompts, logs, or public configuration.

Risk: Alerts sent through Telegram, WhatsApp, Discord, or similar services may disclose trading interests or wallet activity to third-party services.

Mitigation: Choose alert destinations deliberately and limit message content to the level of portfolio or wallet detail acceptable for that channel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flotapponnier/skills/mobula-alerts)
- [Mobula homepage](https://mobula.io)
- [Mobula API documentation](https://docs.mobula.io)
- [Repository listed in skill documentation](https://github.com/Flotapponnier/Crypto-date-openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and monitoring examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Mobula API key and may rely on related Mobula price and wallet skills for full monitoring workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
