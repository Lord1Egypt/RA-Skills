## Description:

Use when the user asks for Pionex market data, including price, ticker, order book depth, recent trades, symbol info, and OHLCV klines, through read-only commands that do not require API credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pibrandon](https://clawhub.ai/user/pibrandon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve public Pionex market data such as depth, tickers, recent trades, symbol metadata, and klines before analysis or order preparation. The skill is not intended for account balances, credentialed account access, or placing and cancelling orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends a global npm install without pinning an exact package version.

Mitigation: Install only from a trusted Pionex npm package source, avoid sudo, and pin or review the exact package version before global installation.

Risk: Market-data output may be used as a precursor to trading decisions.

Mitigation: Use the skill only for public market-data lookup, verify price and symbol rules before trading, and route balance or order actions to the appropriate separate skill.

## Reference(s):

- [Pionex API Docs](https://pionex-doc.gitbook.io/apidocs/)
- [Pionex Homepage](https://www.pionex.com)
- [ClawHub Skill Page](https://clawhub.ai/pibrandon/skills/pionex-market)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and concise command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only market-data workflow; no API credentials required by the skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
