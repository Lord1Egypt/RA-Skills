## Description:

NEPSE Analyst helps agents answer Nepal stock market questions with price checks, technical analysis, fundamentals, watchlists, and market alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uddin-rajaul](https://clawhub.ai/user/uddin-rajaul)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to inspect NEPSE stock prices, fundamentals, technical indicators, watchlists, and price alerts. It supports market-analysis responses while requiring clear risk notes for volatile Nepal equity trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram credentials may be displayed by the installer or stored in shell configuration.

Mitigation: Avoid entering Telegram secrets into the installer; store a narrowly scoped bot token and chat ID in a dedicated secret mechanism.

Risk: Watchlist symbols, prices, and alert thresholds may be sent to Telegram when alerts are enabled.

Mitigation: Enable Telegram only for information you are comfortable sharing with that bot and chat, and disclose this behavior to users.

Risk: The setup flow installs Python packages with a broad pip command.

Mitigation: Install dependencies in a virtual environment with pinned versions and do not run setup with elevated privileges.

Risk: Market analysis depends on scraped third-party data that may be stale, unavailable, or incomplete.

Mitigation: Tell users when data is unavailable or limited and keep the skill's analysis-only risk note in user-facing responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uddin-rajaul/skills/nepse-skill)
- [Publisher profile](https://clawhub.ai/user/uddin-rajaul)
- [Merolagani data source](https://merolagani.com)
- [Sharesansar fallback data source](https://www.sharesansar.com)
- [Telegram Bot API integration endpoint](https://api.telegram.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis and concise confirmations based on JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local watchlist, alert, and RSI history JSON files and may send Telegram notifications when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
