## Description: <br>
Query Polymarket prediction markets for market prices, event probabilities, betting odds, and related market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dannyshmueli](https://clawhub.ai/user/dannyshmueli) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to look up public Polymarket market odds, top markets, event groups, and specific markets by slug. Returned probabilities should be treated as market data, not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes public, unauthenticated requests to Polymarket when asked for market odds. <br>
Mitigation: Install and use it only when outbound requests to Polymarket's public API are acceptable. <br>
Risk: Returned prices and probabilities may be mistaken for financial advice. <br>
Mitigation: Treat outputs as market data and apply independent judgment before making decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dannyshmueli/pm-odds) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text market summaries or raw JSON from the Polymarket public API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public, unauthenticated API requests and does not request credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
