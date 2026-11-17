## Description:

Query live prediction market data from the Prediction Bridge API for event odds, market prices, whale trades, trader analytics, leaderboards, and prediction-market news across supported platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kimcheese888](https://clawhub.ai/user/kimcheese888)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to fetch live prediction-market information and analytics through a bundled command-line client. It supports semantic event search, event browsing, market history, whale-trade monitoring, trader analytics, leaderboards, and news lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, market IDs, and wallet addresses used in queries may be sent to the configured Prediction Bridge API endpoint.

Mitigation: Avoid sending sensitive query terms or wallet addresses unless that disclosure is acceptable for the use case.

Risk: Changing PREDICTION_BRIDGE_URL can route requests to a different service.

Mitigation: Only override PREDICTION_BRIDGE_URL with an endpoint that the user or deploying organization trusts.

## Reference(s):

- [Prediction Bridge API endpoint](https://prediction-bridge.onrender.com)
- [ClawHub skill page](https://clawhub.ai/kimcheese888/skills/prediction-bridge)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON returned by the bundled CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Python standard library only; live queries depend on the configured Prediction Bridge API endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
