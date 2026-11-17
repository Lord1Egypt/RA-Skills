## Description:

Monitor Polymarket prediction markets for potential arbitrage signals, with scanner outputs for math arbitrage and guidance for cross-market and orderbook risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johny0920](https://clawhub.ai/user/johny0920)

### License/Terms of Use:


## Use Case:

Developers and market-monitoring users can use this skill to scan Polymarket market data, review potential arbitrage opportunities, and generate JSON records for paper-trading analysis before any manual trading decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags the skill as suspicious because it overstates trading capabilities and contains unsafe command execution and credential-handling patterns.

Mitigation: Review before installing, run in a virtual environment, pin dependencies, avoid untrusted --data-dir values, and do not pass real webhook tokens on the command line.

Risk: Scanner output may reflect stale homepage prices, midpoint prices, or markets without enough liquidity to execute at the displayed price.

Mitigation: Treat results as paper-trading signals, manually verify current prices and liquidity on Polymarket, and apply conservative edge, volume, and position-size limits.

Risk: Automated trading or wallet integration could lose funds quickly if detection, execution, or credential handling is flawed.

Mitigation: Use the skill as a read-only scanner unless a separate reviewed execution system, private-key management plan, and trading risk controls are in place.

## Reference(s):

- [Arbitrage Types](references/arbitrage_types.md)
- [Getting Started](references/getting_started.md)
- [Polymarket](https://polymarket.com)
- [Polymarket Documentation](https://docs.polymarket.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local market and arbitrage JSON files under the configured data directory.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
