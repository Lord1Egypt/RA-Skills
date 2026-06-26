## Description: <br>
Query Polymarket prediction market odds and events via CLI, including market search, current prices, event listings by category, and orderbook depth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ceeyang](https://clawhub.ai/user/ceeyang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agents use this skill to look up public Polymarket market-implied odds, active events, prices, and orderbook data for probability-oriented questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Polymarket APIs and may include sensitive personal information if entered by the user. <br>
Mitigation: Avoid submitting sensitive personal information in market searches or token lookups. <br>
Risk: Prediction market odds are public market data and may be mistaken for financial, legal, medical, or political advice. <br>
Mitigation: Treat returned odds as informational market-implied probabilities and review them before relying on them for decisions. <br>


## Reference(s): <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>
- [ClawHub skill page](https://clawhub.ai/ceeyang/polymarket-odds-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [CLI text output and Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public Polymarket endpoints and requires no API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
