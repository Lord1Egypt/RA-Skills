## Description: <br>
Detect arbitrage opportunities on Polymarket, including spread arbitrage, cross-market correlations, and news-driven opportunities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neckr0ik](https://clawhub.ai/user/Neckr0ik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to inspect Polymarket market data for potential arbitrage signals, market-pricing inconsistencies, and related trading opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Arbitrage findings may be incorrect or become stale as market prices, fees, liquidity, and execution conditions change. <br>
Mitigation: Verify market data, fee assumptions, liquidity, and resolution terms independently before making any trading decision. <br>
Risk: POLYMARKET_API_KEY may expose account access if broad credentials are configured. <br>
Mitigation: Use limited-scope credentials where available and avoid sharing or committing credential values. <br>
Risk: Some documented features, including webhook alerts and monitoring behavior, may not be present in the packaged script. <br>
Mitigation: Confirm packaged behavior in a controlled environment before relying on alerts or continuous monitoring. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Neckr0ik/neckr0ik-polymarket-trader) <br>
- [Polymarket CLOB API endpoint](https://clob.polymarket.com) <br>
- [Polymarket public API endpoint](https://polymarket.com/public-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command examples and tabular or JSON-style arbitrage findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use POLYMARKET_API_KEY for market data access; outputs are informational and do not execute trades.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
