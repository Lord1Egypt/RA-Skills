## Description:

Mirrors configured high-performing Polymarket wallet trades through Simmer with trade-size filters, dry-run support, and safeguards for flip-flopping, slippage, duplicate positions, and resolved markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chokle](https://clawhub.ai/user/chokle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor selected Polymarket wallets and copy qualifying trades through Simmer. It is intended for configurable copytrading workflows that start in dry-run mode and move to live recurring execution only after account limits, wallet lists, and API access are reviewed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The managed automaton is configured for recurring live trading and could place unintended orders.

Mitigation: Use dry-run mode first, disable the managed --live schedule unless recurring execution is intended, and confirm account trading limits before enabling live runs.

Risk: A Simmer API key can grant access to accounts with real funds.

Mitigation: Grant credentials only after reviewing wallet selection, market handling, and account limits; keep the API key scoped and stored as an environment secret.

Risk: Dependency or SDK behavior changes could affect trade execution.

Mitigation: Pin the simmer-sdk dependency version and test behavior in dry-run mode before upgrading or running with live trading enabled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chokle/skills/polymarket-whale-copytrade)
- [Publisher profile](https://clawhub.ai/user/chokle)
- [Simmer docs](https://docs.simmer.markets)
- [Simmer skill building guide](https://docs.simmer.markets/skills/building)
- [Polymarket](https://polymarket.com)
- [Polymarket leaderboard](https://polymarket.com/leaderboard)
- [Polymarket CLOB API documentation](https://docs.polymarket.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, CLI commands, configuration values, and terminal status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; dry run is the default manual mode, while the managed automaton is configured for recurring live execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
