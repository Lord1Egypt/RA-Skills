## Description: <br>
Polymarket Odds lets agents query Polymarket prediction-market odds, events, prices, tags, and order books through a no-API-key CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deanpress](https://clawhub.ai/user/deanpress) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to look up market-implied probabilities for sports, politics, crypto, business, technology, and other current-event questions as one signal for odds analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searches are sent to public Polymarket APIs and may contain private or sensitive user intent. <br>
Mitigation: Avoid entering private or sensitive information in market searches. <br>
Risk: Returned prices are market-implied probabilities, not guaranteed predictions, financial advice, or betting advice. <br>
Mitigation: Treat prices as one signal for analysis and verify important decisions with additional sources. <br>


## Reference(s): <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>
- [ClawHub release page](https://clawhub.ai/deanpress/polymarket-odds) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text CLI output with market titles, probabilities, volume, liquidity, and orderbook summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public Polymarket endpoints; no API key required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
