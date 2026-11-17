## Description:

Trades Polymarket crypto prediction markets for Solana, Bitcoin, and Ethereum using CoinGecko momentum signals, Simmer context checks, and configurable dry-run or live execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chokle](https://clawhub.ai/user/chokle)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to run a configurable momentum strategy that scans crypto prediction markets, estimates divergence from CoinGecko price trends, and simulates or places trades through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated trading can run every 15 minutes and place live prediction-market trades through the Simmer credential.

Mitigation: Keep TRADING_VENUE on sim until tested, cap trade size and trade count, and enforce strict Simmer account limits before enabling live venues.

Risk: Context-check failures may allow trading to proceed without flip-flop, slippage, or HOLD safeguards.

Mitigation: Review or change the context-check path to fail closed before allowing real-money trading.

Risk: A broad or exposed Simmer credential could allow unintended trading activity.

Mitigation: Use a limited-purpose SIMMER_API_KEY and rotate it if it is exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chokle/skills/polymarket-sol-momentum)
- [Simmer docs](https://docs.simmer.markets)
- [Simmer skill building guide](https://docs.simmer.markets/skills/building)
- [CoinGecko free API](https://www.coingecko.com/en/api/documentation)
- [Polymarket](https://polymarket.com)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with Python strategy code and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and supports scheduled runs, dry-run testing, and live trading configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
