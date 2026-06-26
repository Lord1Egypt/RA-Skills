## Description: <br>
Query live prediction market data from the Prediction Bridge API for event odds, market prices, whale trades, trader analytics, and prediction-market news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kimCheese888](https://clawhub.ai/user/kimCheese888) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to query current prediction-market events, prices, whale trades, trader analytics, leaderboards, and related news through a bundled command-line client. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prediction-market searches, market identifiers, and wallet addresses are sent to the Prediction Bridge API. <br>
Mitigation: Avoid sensitive private queries or wallet identifiers unless that data sharing is acceptable. <br>
Risk: The API base URL can be overridden with PREDICTION_BRIDGE_URL. <br>
Mitigation: Set PREDICTION_BRIDGE_URL only to an endpoint the user trusts. <br>


## Reference(s): <br>
- [Prediction Bridge API](https://prediction-bridge.onrender.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the bundled CLI prints JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Python standard library only; PREDICTION_BRIDGE_URL can override the default API endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
