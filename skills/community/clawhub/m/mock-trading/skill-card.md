## Description:

Simulates cryptocurrency paper trading with algorithmic strategies such as SMA crossover and mean reversion without risking real capital.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yadavabhijeet4](https://clawhub.ai/user/yadavabhijeet4)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, trading hobbyists, and evaluators use this skill to run paper-trading simulations, test simple cryptocurrency strategies, and monitor a local mock portfolio without connecting to an exchange.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts CoinGecko for public cryptocurrency prices.

Mitigation: Use it only in environments where outbound access to CoinGecko is acceptable.

Risk: The skill modifies a local portfolio JSON file during each simulated trading tick.

Mitigation: Run it against a dedicated mock portfolio file and keep backups if the portfolio state matters.

Risk: Repeated HEARTBEAT.md or cron execution can continually update the mock portfolio.

Mitigation: Enable automation only when repeated paper-trading ticks are intentional, and review the schedule before deployment.

Risk: Paper-trading output could be mistaken for financial advice or real exchange activity.

Mitigation: Present results as simulation data only and do not use the skill to place real trades.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yadavabhijeet4/skills/mock-trading)
- [CoinGecko Simple Price API Endpoint](https://api.coingecko.com/api/v3/simple/price?ids={asset_id}&vs_currencies=usd)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown or text guidance with shell commands and JSON portfolio updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Updates a local mock portfolio file; evidence indicates paper trading only, with no real trades or credential use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
