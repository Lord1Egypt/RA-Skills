## Description:

Analyzes Hong Kong leveraged ETFs by evaluating holdings, price deviation, liquidity risk, rebalancing windows, arbitrage opportunities, and position-adjustment signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuzimaki](https://clawhub.ai/user/wuzimaki)

### License/Terms of Use:


## Use Case:

External users and trading analysts use this skill to analyze Hong Kong leveraged ETF holdings, market deviations, liquidity conditions, rebalancing timing, arbitrage opportunities, and related risk alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require market-data access for ETF holdings, component prices, NAV data, and fund-flow inputs.

Mitigation: Grant only the market-data access needed for the intended analysis and avoid embedding trading account credentials in the agent environment.

Risk: The skill may read local project notes or analysis logs if those paths exist, which could contain private trading records.

Mitigation: Keep sensitive account details and private trading records out of referenced log locations unless they are intentionally in scope for the agent.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text analysis with recommendations and risk alerts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on market-data access and ETF holdings or NAV data supplied by the agent environment.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version note)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
