## Description:

Detect arbitrage opportunities on Polymarket, including spread arbitrage, cross-market correlations, and news-driven opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neckr0ik](https://clawhub.ai/user/neckr0ik)

### License/Terms of Use:

MIT

## Use Case:

External developers and prediction-market operators use this skill to scan Polymarket market data for possible arbitrage, correlation, news-related, and near-resolution trading signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may contact Polymarket services and use POLYMARKET_API_KEY when present.

Mitigation: Run it only in an environment where outbound Polymarket access and that credential use are approved.

Risk: Some documented commands and webhook behavior are not implemented in the artifact.

Mitigation: Validate the available CLI commands before relying on operational workflows or alerts.

Risk: Outputs are trading signals and may be incomplete, stale, or based on fallback sample data.

Mitigation: Confirm market data, fees, liquidity, and execution assumptions independently before making trades.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neckr0ik/skills/neckr0ik-polymarket-trader)
- [ClawHub publisher profile](https://clawhub.ai/user/neckr0ik)
- [Polymarket CLOB API endpoint](https://clob.polymarket.com)
- [Polymarket public API endpoint](https://polymarket.com/public-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text with CLI commands and arbitrage signal summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include market IDs, prices, spreads, confidence estimates, volumes, expiration dates, and trading-signal notes.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact files report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
