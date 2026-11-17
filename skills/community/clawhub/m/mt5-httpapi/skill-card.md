## Description:

HTTP client for a user-deployed mt5-httpapi MetaTrader 5 bridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query a configured MetaTrader 5 bridge for account, market, history, and backtest information. It can also manage orders, positions, terminals, and chart deployments when the user has explicitly configured the bridge and confirms each consequential action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bridge can expose brokerage account data and accept live trading or account-management actions.

Mitigation: Use a trusted, self-hosted endpoint with authentication enabled, and require action-specific confirmation before each trade, terminal operation, or live chart deployment change.

Risk: The scanner reports capabilities and setup steps beyond the stated HTTP client purpose, and its evidence is incomplete because local references remain unresolved.

Mitigation: Review the skill's file, remote management, tunnel, and privileged installation guidance and resolve the referenced material before enabling those capabilities.

## Reference(s):

- [Setup guide](artifact/references/setup.md)
- [mt5-httpapi project](https://github.com/psyb0t/mt5-httpapi)
- [ClawHub skill page](https://clawhub.ai/psyb0t/skills/mt5-httpapi)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON API responses and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mutating trade, terminal, and chart deployment actions require explicit confirmation.]

## Skill Version(s):

4.33.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
