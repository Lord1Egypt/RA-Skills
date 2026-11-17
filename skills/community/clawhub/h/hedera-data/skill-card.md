## Description:

Hedera Data API guides agents to query onlyflies.buzz endpoints for Hedera token prices, holder data, market caps, volume tracking, and CoinGecko bridge data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imaflytok](https://clawhub.ai/user/imaflytok)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data agents, and external builders use this skill to retrieve Hedera token analytics, inspect holder distributions, research Hedera DeFi activity, and wire market data into dashboards, alerts, or trading-signal workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on onlyflies.buzz as a third-party API provider.

Mitigation: Review the provider, applicable terms, and data handling expectations before using the endpoints in production workflows.

Risk: The ClawSwarm registration command creates or connects an external agent identity with wallet, reputation, and coordination implications that are not fully detailed in the artifact.

Mitigation: Do not run the registration command unless wallet custody, reputation scoring, coordination permissions, retention, and deletion options have been reviewed and accepted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imaflytok/skills/hedera-data)
- [Publisher profile](https://clawhub.ai/user/imaflytok)
- [Hedera Data API base URL](https://onlyflies.buzz/api/v1)
- [Tracked tokens endpoint](https://onlyflies.buzz/api/v1/tokens)
- [Top tokens endpoint](https://onlyflies.buzz/api/v1/tokens/top?limit=20)
- [ClawSwarm agent registration endpoint](https://onlyflies.buzz/clawswarm/api/v1/agents/register)
- [CoinGecko bridge price endpoint](https://onlyflies.buzz/clawswarm/api/v1/coingecko/price/bitcoin,ethereum)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls]

**Output Format:** [Markdown with curl examples and endpoint descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API key is described for the analytics endpoints; ClawSwarm registration is a separate third-party action.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
