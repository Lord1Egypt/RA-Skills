## Description:

Compare matching sports odds across bookmakers using odds-api.net, including moneylines, spreads, totals, and player props.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odds-api](https://clawhub.ai/user/odds-api)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and sports odds users with an odds-api.net account can discover events and compare bookmaker prices for the same selection, with event and market details kept distinct.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The odds provider receives the configured API key and requested sports filters; requests also consume account quota.

Mitigation: Configure ODDS_API_KEY through the agent runtime instead of chat or command arguments. Keep the default endpoint for normal use and use dummy credentials with local mocks.

## Reference(s):

- [odds-api.net API reference](https://odds-api.net/docs)
- [Supported betting markets](https://odds-api.net/betting-markets)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [JSON by default, or a Markdown comparison table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Groups prices by event and selection details; reports bookmaker freshness and timestamps when available, plus exclusions and pagination details.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
