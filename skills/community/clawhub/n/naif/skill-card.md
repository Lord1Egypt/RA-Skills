## Description:

Create and manage AI-powered trading bots via natural language. Paper & live trading, portfolio monitoring, backtesting, stock quotes, and options chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[naiiif83](https://clawhub.ai/user/naiiif83)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to create and manage trading bots, monitor portfolios, place orders, retrieve market data, and backtest strategies through natural-language prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading, position closures, and bot-management prompts can affect real brokerage accounts.

Mitigation: Confirm paper trading is the default, use broker-side limits or least-privilege permissions, and require explicit human confirmation before live orders, position closures, bot starts, or deletions.

Risk: The required API key grants access to VibeTrader and linked trading authority.

Mitigation: Keep VIBETRADER_API_KEY protected and install only when the user intends to link VibeTrader to brokerage trading authority.

## Reference(s):

- [VibeTrader homepage](https://vibetrader.markets)
- [VibeTrader documentation](https://vibetrader.markets/docs)

## Skill Output:

**Output Type(s):** [text, guidance, shell commands, configuration]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VIBETRADER_API_KEY for authenticated use.]

## Skill Version(s):

1.0.0 (source: openclaw.plugin.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
