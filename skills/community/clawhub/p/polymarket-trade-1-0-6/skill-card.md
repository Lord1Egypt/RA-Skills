## Description:

Query Polymarket prediction markets, check odds, find trending markets, search events, and track price movements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xvolica](https://clawhub.ai/user/xvolica)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect public Polymarket market data, monitor price movement, configure local watchlist alerts, and simulate paper trades without connecting a wallet or executing real trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches public Polymarket data and can create local watchlist and paper-trading records under ~/.polymarket.

Mitigation: Review the commands before running them, keep cron alerts limited to intended markets, and inspect or remove the local JSON files when no longer needed.

Risk: Users may confuse paper-trading output or market odds with real trading capability or financial advice.

Mitigation: Treat results as informational market data and local simulation only; the skill does not connect wallets, use credentials, or execute real-money trades.

## Reference(s):

- [Polymarket](https://polymarket.com)
- [Polymarket Docs](https://docs.polymarket.com)
- [Public Gamma API](https://gamma-api.polymarket.com)
- [ClawHub Skill Page](https://clawhub.ai/xvolica/skills/polymarket-trade-1-0-6)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples and terminal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local watchlist and paper-trading JSON files under ~/.polymarket when the user runs those commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
