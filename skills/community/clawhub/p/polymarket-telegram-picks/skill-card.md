## Description:

Fetches same-day pre-match Polymarket NBA odds, supports AI analysis of betting picks, and sends recommendations to Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wall-nut417](https://clawhub.ai/user/wall-nut417)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch daily pre-match NBA markets from Polymarket, have an agent draft concise Chinese betting-related analysis, and send the result to a configured Telegram chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill produces betting-related recommendations that may be speculative or financially risky.

Mitigation: Treat recommendations as informational, review the reasoning before acting, and do not rely on them as financial advice.

Risk: Telegram bot credentials and outbound messages can expose private chat access or sensitive context.

Mitigation: Use environment variables or a managed secret store, do not commit config/config.json, and review message content before sending.

Risk: The workflow depends on third-party Polymarket and Telegram API availability and current market data.

Mitigation: Check fetch or send errors before trusting the daily result, and verify important market information against the source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wall-nut417/skills/polymarket-telegram-picks)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)
- [Telegram Bot API](https://api.telegram.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with inline shell commands and Telegram message content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Telegram messages longer than about 4000 characters are truncated by the send script.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
